import telebot
from telebot import types
import configparser
import scraper
from keep_alive import keep_alive
import os

#
keep_alive()
bot = telebot.TeleBot('5759486107:AAEn3ZxHZPrFCs1wsfLasDEdFK9YrThimBs')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    bot.reply_to(message, "¡Bienvenido! Este bot te permite añadir usuarios a tu grupo de Telegram.", reply_markup=markup)

@bot.message_handler(commands=['cat'])
def cat_config(message):
    with open('config.data', 'r') as file:
        config_data = file.read()
    bot.reply_to(message, f"Contenido de config.data:\n\n{config_data}")
    
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

bot.infinity_polling()
