from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

TOKEN = "8774258964:AAHv3YuSwidetuqeZqXRLmqspFXPogfP2rc"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id
    text = update.message.text

    # 打印群ID
    print("群ID:", chat_id)
    print("收到消息:", text)

    # 当前时间
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 上班打卡
    if text.strip() == "/上班打卡":
        reply = f"打卡时间 {now}"
        await update.message.reply_text(reply)

    # 下班打卡
    elif text.strip() == "/下班打卡":
        reply = f"打卡时间 {now}"
        await update.message.reply_text(reply)

    # 获取群id
    elif text.strip() == "id":
        await update.message.reply_text(chat_id)


def main():

    app = ApplicationBuilder().token(TOKEN).build()

    # 监听所有文本消息
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    print("机器人已启动...")

    app.run_polling()


if __name__ == "__main__":
    main()