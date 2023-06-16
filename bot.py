import configparser
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Función para manejar el comando /start
def start(update, context):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text="¡Hola! Por favor, ingresa los siguientes datos:")

# Función para manejar el mensaje de texto
def handle_text(update, context):
    chat_id = update.message.chat_id
    text = update.message.text

    # Almacenar los datos ingresados en el archivo de configuración
    cpass = configparser.RawConfigParser()
    cpass.add_section('cred')
    cpass.set('cred', 'id', text)
    context.bot.send_message(chat_id=chat_id, text="ID de API guardado. Por favor, ingresa el ID de hash:")
    context.user_data['cpass'] = cpass

# Función para manejar el mensaje de texto
def handle_hash(update, context):
    chat_id = update.message.chat_id
    text = update.message.text

    # Almacenar los datos ingresados en el archivo de configuración
    cpass = context.user_data['cpass']
    cpass.set('cred', 'hash', text)
    context.bot.send_message(chat_id=chat_id, text="ID de hash guardado. Por favor, ingresa el número de teléfono:")

# Función para manejar el mensaje de texto
def handle_phone(update, context):
    chat_id = update.message.chat_id
    text = update.message.text

    # Almacenar los datos ingresados en el archivo de configuración
    cpass = context.user_data['cpass']
    cpass.set('cred', 'phone', text)

    # Guardar la configuración en el archivo
    with open('config.data', 'w') as setup:
        cpass.write(setup)

    context.bot.send_message(chat_id=chat_id, text="Número de teléfono guardado. Configuración completada.")

def main():
    # Inicializar el bot de Telegram
    updater = Updater("5681732028:AAErgYe8EPUMFz9kg4whvaHgefroADzr1fE")  # Reemplaza "TOKEN" con tu token de bot real

    # Obtener el despachador para registrar los controladores
    dp = updater.dispatcher

    # Agregar los controladores de comandos y mensajes de texto
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_hash))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_phone))

    # Iniciar el bot
    updater.start_polling()

    # Mantener al bot en ejecución hasta que se presione Ctrl+C
    # updater.idle()

if name == 'main':
    main()
