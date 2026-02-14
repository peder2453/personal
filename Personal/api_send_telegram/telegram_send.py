from telethon import TelegramClient

api_id = 14941572     # 你的api_id
api_hash = '0546df1bca1f112b909c6ef8ec47fdb7'
phone = '+639626137179'  # 你的手机号

# 这里的 'my_account' 就是 session 文件名
client = TelegramClient('my_account', api_id, api_hash)

async def main():
    # 先登录并保存 session
    await client.start(phone=phone)
    await client.send_message('lIlllII0', 'Hello from my saved session!')

with client:
    client.loop.run_until_complete(main())
