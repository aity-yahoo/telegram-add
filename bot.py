import telebot
from telebot import types
import configparser
import csv
import time

cpass = configparser.RawConfigParser()
cpass.read('config.data')

bot = telebot.TeleBot('5681732028:AAErgYe8EPUMFz9kg4whvaHgefroADzr1fE')

@bot.message_handler(commands=['start'])
def start(message):
    try:
        api_id = cpass['cred']['id']
        api_hash = cpass['cred']['hash']
        phone = cpass['cred']['phone']
        client = TelegramClient(phone, api_id, api_hash)
    except KeyError:
        bot.reply_to(message, "[!] Ejecute /setup primero.")
        return
    
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        msg = bot.reply_to(message, "Ingrese el código de verificación:")
        bot.register_next_step_handler(msg, process_verification_code, client)
    else:
        scrape_members(message, client)

def process_verification_code(message, client):
    code = message.text
    client.sign_in(phone, code)
    scrape_members(message, client)

def scrape_members(message, client):
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

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for i, g in enumerate(groups):
        markup.add(types.KeyboardButton(f"[{i}] - {g.title}"))
    msg = bot.reply_to(message, "Seleccione un grupo para extraer miembros:", reply_markup=markup)
    bot.register_next_step_handler(msg, process_group_selection, groups)

def process_group_selection(message, groups):
    try:
        group_index = int(message.text[1:-1])
        target_group = groups[group_index]
    except (ValueError, IndexError):
        bot.reply_to(message, "Selección de grupo no válida.")
        return

    bot.reply_to(message, "Obteniendo miembros...")
    time.sleep(1)
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

bot.polling()
