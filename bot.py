import os
import configparser
import telebot

# Inicializar el bot con el token proporcionado por BotFather
bot = telebot.TeleBot('TOKEN_DEL_BOT')

# Función para mostrar el banner inicial
def banner():
    os.system('clear')
    banner_text = """
╔═╗┌─┐┌┬┐┬ ┬┌─┐
╚═╗├┤  │ │ │├─┘
╚═╝└─┘ ┴ └─┘┴

Version : 1.01
Subscribe Termux Professor on Youtube
www.youtube.com/c/TermuxProfessorYT
    """
    bot.send_message(chat_id, banner_text)

# Handler para el comando /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    banner()
    bot.send_message(chat_id, "[+] Installing requirements ...")
    os.system('python3 -m pip install telethon')
    os.system('pip3 install telethon')
    banner()
    bot.send_message(chat_id, "Enter API ID:")
    bot.register_next_step_handler(message, get_api_id)

# Función para obtener el ID de la API
def get_api_id(message):
    chat_id = message.chat.id
    api_id = message.text
    bot.send_message(chat_id, "Enter Hash ID:")
    bot.register_next_step_handler(message, get_hash_id, api_id)

# Función para obtener el Hash ID
def get_hash_id(message, api_id):
    chat_id = message.chat.id
    hash_id = message.text
    bot.send_message(chat_id, "Enter Phone Number:")
    bot.register_next_step_handler(message, save_credentials, api_id, hash_id)

# Función para guardar las credenciales en el archivo de configuración
def save_credentials(message, api_id, hash_id):
    chat_id = message.chat.id
    phone_number = message.text
    
    # Crear y guardar las credenciales en el archivo de configuración
    cpass = configparser.RawConfigParser()
    cpass.add_section('cred')
    cpass.set('cred', 'id', api_id)
    cpass.set('cred', 'hash', hash_id)
    cpass.set('cred', 'phone', phone_number)
    with open('config.data', 'w') as setup:
        cpass.write(setup)
    
    bot.send_message(chat_id, "[+] Setup complete!")
    bot.send_message(chat_id, "[+] Now you can run any tool!")
    bot.send_message(chat_id, "[+] Make sure to read the docs for installation and API setup")
    bot.send_message(chat_id, "[+] https://github.com/termuxprofessor/TeleGram-Scraper-Adder/blob/master/README.md")

# Iniciar el bot
bot.infinity_polling()
