from telethon import TelegramClient

api_id = 34660237
api_hash = "8bbdf8056ddbdec6fec77920e56ec7c0"

with TelegramClient("session", api_id, api_hash) as client:
    print("login success")