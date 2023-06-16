import telebot
from telebot import types
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import os, sys
import configparser
import csv
import time
import configparser

bot = telebot.TeleBot('5681732028:AAErgYe8EPUMFz9kg4whvaHgefroADzr1fE')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    bot.reply_to(message, "¡Bienvenido! Este bot te permite añadir usuarios a tu grupo de Telegram.", reply_markup=markup)

@bot.message_handler(commands=['setup'])
def setup(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    msg = bot.reply_to(message, "Ingrese su API ID:", reply_markup=markup)
    bot.register_next_step_handler(msg, process_api_id)

def process_api_id(message):
    api_id = message.text
    msg = bot.reply_to(message, "Ingrese su Hash ID:")
    bot.register_next_step_handler(msg, process_hash_id, api_id)

def process_hash_id(message, api_id):
    hash_id = message.text
    msg = bot.reply_to(message, "Ingrese su número de teléfono:")
    bot.register_next_step_handler(msg, process_phone_number, api_id, hash_id)

def process_phone_number(message, api_id, hash_id):
    phone_number = message.text

    cpass = configparser.RawConfigParser()
    cpass.add_section('cred')
    cpass.set('cred', 'id', api_id)
    cpass.set('cred', 'hash', hash_id)
    cpass.set('cred', 'phone', phone_number)

    with open('config.data', 'w') as setup:
        cpass.write(setup)

    bot.reply_to(message, "Configuración guardada exitosamente.")

@bot.message_handler(commands=['scraper'])
def scraper(message):
    cpass = configparser.RawConfigParser()
    cpass.read('config.data')

    try:
        api_id = cpass['cred']['id']
        api_hash = cpass['cred']['hash']
        phone = cpass['cred']['phone']
        client = TelegramClient(phone, api_id, api_hash)
    except KeyError:
        bot.reply_to(message, "Primero ejecuta /setup")
        return

    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        bot.reply_to(message, "Ingresa el código:")
        return

    chats = []
    last_date = None
    chunk_size = 200
    groups = []

    result = client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash=0
    ))
    chats.extend(result.chats)

    for chat in chats:
        try:
            if chat.megagroup == True:
                groups.append(chat)
        except:
            continue

    bot.reply_to(message, "Elige un grupo para obtener los miembros:")
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for i, g in enumerate(groups):
        keyboard.add(types.KeyboardButton(f'[{i}] - {g.title}'))

    msg = bot.send_message(message.chat.id, "Elige un grupo:", reply_markup=keyboard)
    bot.register_next_step_handler(msg, process_group_selection, client)


def process_group_selection(message, client):
    try:
        group_index = int(message.text[1:-1])  # Obtener el índice del grupo seleccionado
        target_group = groups[group_index]  # Obtener el grupo seleccionado

        bot.reply_to(message, "Obteniendo miembros...")
        time.sleep(1)
        all_participants = []
        all_participants = client.get_participants(target_group, aggressive=True)
        
        bot.reply_to(message, "Guardando en el archivo...")
        time.sleep(1)
        with open("members.csv", "w", encoding='UTF-8') as f:
            writer = csv.writer(f, delimiter=",", lineterminator="\n")
            writer.writerow(['username', 'user id', 'access hash', 'name', 'group', 'group id'])
            for user in all_participants:
                if user.username:
                    username = user.username
                else:
                    username = ""
                if user.first_name:
                    first_name = user.first_name
                else:
               first_name = ""
                if user.last_name:
                    last_name = user.last_name
                else:
                    last_name = ""
                name = (first_name + ' ' + last_name).strip()
                writer.writerow([username, user.id, user.access_hash, name, target_group.title, target_group.id])

        bot.reply_to(message, "Miembros extraídos exitosamente.")
#    except Exception as e:
#        bot.reply_to(message, f"Ocurrió un error: {str(e)}")
        
bot.polling()     
