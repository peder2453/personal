import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
import time
from google import genai

# 配置 Telegram Bot Token
TELEGRAM_TOKEN = '7755878042:AAGKlaPmZCJchqgdLqvMu90TqxI_jKyP430'

GENAI_API_KEY = "AIzaSyAkoAB33JrU8ztDqnUXsCw5atQZwaZDKo4"

client = genai.Client(api_key=GENAI_API_KEY)

# 防刷间隔（秒），默认5秒
MIN_INTERVAL = 5

# 日志配置到文件和控制台
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("telegram_ai_bot.log"),
        logging.StreamHandler()
    ]
)
logging.getLogger("httpx").disabled = True
logger = logging.getLogger(__name__)

# 记录用户上次发消息时间
user_last_message_time = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("你好，我是群聊 AI 机器人。@我提问即可，我会用 AI 回答你！")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("直接 @我 提问吧。管理员可用 /config 设置防刷间隔秒数。")

async def config_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    
    # 检查是否是群聊管理员
    if chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("这个命令只能在群聊中用。")
        return

    member = await chat.get_member(user.id)
    if not (member.status in ["creator", "administrator"]):
        await update.message.reply_text("只有管理员才能用 /config 修改配置。")
        return

    # 修改防刷间隔
    try:
        seconds = int(context.args[0])
        global MIN_INTERVAL
        MIN_INTERVAL = max(1, seconds)
        await update.message.reply_text(f"防刷间隔已更新为 {MIN_INTERVAL} 秒。")
        logger.info(f"管理员 {user.id} 设置防刷间隔为 {MIN_INTERVAL} 秒")
    except (IndexError, ValueError):
        await update.message.reply_text("用法: /config 秒数 (例如: /config 10)")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message is None:
        logger.info("收到非普通消息类型的 update，忽略。")
        return
    chat_type = message.chat.type
    user_name = f"{message.from_user.first_name} {message.from_user.last_name}({message.from_user.username})"
    print(user_name)

    logger.info(f"处理消息来自 {chat_type}，用户：{message.from_user.id}, 用户名：{user_name}")

    # 群聊中必须 @bot 才处理
    if chat_type in ["group", "supergroup"]:
        bot_username = (await context.bot.get_me()).username
        if f"@{bot_username}" not in message.text:
            return

    user_id = message.from_user.id
    now = time.time()

    # 防滥用检查
    last_time = user_last_message_time.get(user_id, 0)
    if now - last_time < MIN_INTERVAL:
        await message.reply_text("请不要太频繁发消息哦！稍等几秒再试。")
        logger.info(f"User {user_id} hit rate limit.")
        return

    user_last_message_time[user_id] = now
    user_message = message.text.replace(f"@{(await context.bot.get_me()).username}", "").strip()

    logger.info(f"收到消息：{user_message} 来自用户：{user_id}, 用户名：{user_name}")

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_message
        )
        ai_reply = response.text

        await message.reply_text(ai_reply)
        logger.info(f"回复用户：{user_id}, 用户名：{user_name}")
    except Exception as e:
        logger.error(f"调用 OpenAI 出错: {e}")
        await message.reply_text("抱歉，AI 服务暂时不可用，请稍后再试。")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(msg="发生未处理异常：", exc_info=context.error)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("config", config_command))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    app.add_error_handler(error_handler)

    logger.info("AI Telegram 群聊机器人已启动")
    app.run_polling()

if __name__ == '__main__':
    main()

