# -*- coding: utf-8 -*-
from apscheduler.schedulers.background import BackgroundScheduler
import sys
from modules.check import new_clock, second_clock
from config import client, Telegram_user_id
from pyrogram.handlers import MessageHandler,CallbackQueryHandler
from pyrogram import filters
from modules.pixiv import start_download_pixiv,start_download_id
from modules.control import send_telegram_file,all_callback

def test(client, message):
    print(client)
    print(message)
    message.reply_text(message.text)
    client.send_message(chat_id=int(Telegram_user_id), text="test")

def start_bot():
    #scheduler = BlockingScheduler()
    scheduler = BackgroundScheduler()

    scheduler.add_job(new_clock, "interval", seconds=60)
    scheduler.add_job(second_clock, "interval", seconds=60)
    print("开启监控")

    sys.stdout.flush()
    print("开始bot")
    print(Telegram_user_id)
    sys.stdout.flush()


    start_message_handler = MessageHandler(
        test,
        filters=filters.command("start")
    )


    pixivuser_message_handler = MessageHandler(
        start_download_pixiv,
        filters=filters.command("pixivuser")
    )


    pixivid_message_handler = MessageHandler(
        start_download_id,
        filters=filters.command("pixivpid")
    )

    magfile_message_handler = MessageHandler(
        send_telegram_file,
        filters=filters.command("magfile")
    )


    all_callback_handler = CallbackQueryHandler(
        callback=all_callback,


        )
    client.add_handler(start_message_handler,group=1)
    client.add_handler(pixivuser_message_handler,group=1)
    client.add_handler(pixivid_message_handler,group=1)
    client.add_handler(magfile_message_handler,group=3)
    client.add_handler(all_callback_handler,group=0)

    client.run()

start_bot()

