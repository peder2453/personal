import time
import random
import logging
from datetime import datetime, date
from telethon.sync import TelegramClient
from telethon.errors import FloodWaitError

api_id = 34660237
api_hash = "8bbdf8056ddbdec6fec77920e56ec7c0"

group_id = -1003832509384


# 日志配置
logging.basicConfig(
    filename="tg_scheduler.log",
    level=logging.INFO,
    format="%(asctime)s %(message)s"
)


def log(msg):
    print(msg)
    logging.info(msg)


def is_small_week():
    week_number = datetime.now().isocalendar().week
    return week_number % 2 == 1


def week_type():
    return "小周" if is_small_week() else "大周"


def weekday_name(day):
    names = ["周一","周二","周三","周四","周五","周六","周日"]
    return names[day]


def is_workday(today):
    weekday = today.weekday()

    if is_small_week():
        return weekday <= 5
    else:
        return weekday <= 4


def in_morning_window(now):
    return now.hour == 8 and 35 <= now.minute <= 40


def in_evening_window(now):
    return now.hour == 18 and 3 <= now.minute <= 5


def send_message_safe(client, text):

    while True:
        try:
            client.send_message(group_id, text)
            log("发送成功: " + text)
            return

        except FloodWaitError as e:
            log(f"FloodWait {e.seconds}s")
            time.sleep(e.seconds)

        except Exception as e:
            log("发送失败: " + str(e))
            time.sleep(30)


today = date.today()
weekday = today.weekday()
week_number = datetime.now().isocalendar().week

log("==============")
log("脚本启动")
log(f"当前周数: {week_number}")
log(f"周类型: {week_type()}")
log(f"今天: {weekday_name(weekday)}")

if is_workday(today):
    log("今天需要打卡")
else:
    log("今天不用打卡")


while True:

    try:

        with TelegramClient("session", api_id, api_hash) as client:

            log("telegram connected")

            last_morning = None
            last_evening = None

            while True:

                now = datetime.now()
                today = date.today()

                if is_workday(today):

                    if in_morning_window(now) and last_morning != today:

                        delay = random.randint(10,120)
                        log(f"早上打卡延迟 {delay}s")
                        time.sleep(delay)

                        send_message_safe(client,"/上班打卡")

                        last_morning = today


                    if in_evening_window(now) and last_evening != today:

                        delay = random.randint(10,120)
                        log(f"晚上打卡延迟 {delay}s")
                        time.sleep(delay)

                        send_message_safe(client,"/下班打卡")

                        last_evening = today


                time.sleep(30)

    except Exception as e:

        log("连接异常: " + str(e))
        log("30秒后重连")

        time.sleep(30)