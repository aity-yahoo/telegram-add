from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import configparser
import csv
import time

def scraper():
    cpass = configparser.RawConfigParser()
    cpass.read('config.data')

    try:
        api_id = cpass['cred']['id']
        api_hash = cpass['cred']['hash']
        phone = cpass['cred']['phone']
        client = TelegramClient(phone, api_id, api_hash)
    except KeyError:
        print("Primero ejecuta /setup")
        return

    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        print("Ingresa el código:")
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

    print("Elige un grupo para obtener los miembros:")
    for i, g in enumerate(groups):
        print(f'[{i}] - {g.title}')

    group_index = int(input("Elige un grupo:"))
    target_group = groups[group_index]

    print("Obteniendo miembros...")
    time.sleep(1)
    all_participants = []
    all_participants = client.get_participants(target_group, aggressive=True)
    
    print("Guardando en el archivo...")
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

    print("Miembros extraídos exitosamente.")

if __name__ == "__main__":
    scraper()
