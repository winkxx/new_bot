# -*- coding: utf-8 -*-
from apscheduler.schedulers.background import BackgroundScheduler
import sys
from modules.check import new_clock, second_clock
from config import client, Telegram_user_id
from pyrogram.handlers import MessageHandler,CallbackQueryHandler
from pyrogram import filters
from modules.pixiv import start_download_pixiv,start_download_id,start_download_pixivtg
from modules.control import send_telegram_file,start_http_download,start_download,start_http_downloadtg
from modules.call import all_callback
from modules.moretg import get_telegram_file,get_file_id,sendfile_by_id
from modules.picacg import seach_main
from modules.rclone import start_rclonecopy,start_rclonelsd,start_rclonels,start_rclonecopyurl

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

    http_download_message_handler = MessageHandler(
        start_http_download,
        filters=filters.command("mirror")
    )
    magnet_download_message_handler = MessageHandler(
        start_download,
        filters=filters.command("magnet")
    )

    telegram_file_message_handler = MessageHandler(
        get_telegram_file,
        filters=filters.command("downtgfile")
    )
    seach_main_file_message_handler = MessageHandler(
        seach_main,
        filters=filters.command("search")
    )

    start_download_idtg_message_handler = MessageHandler(
        start_download_pixivtg,
        filters=filters.command("pixivusertg")
    )

    start_http_downloadtg_message_handler = MessageHandler(
        start_http_downloadtg,
        filters=filters.command("mirrortg")
    )
    start_rclonecopy_message_handler = MessageHandler(
        start_rclonecopy,
        filters=filters.command("rclonecopy")
    )

    start_rclonelsd_message_handler = MessageHandler(
        start_rclonelsd,
        filters=filters.command("rclonelsd")
    )

    start_rclone_message_handler = MessageHandler(
        start_rclonels,
        filters=filters.command("rclone")
    )

    start_rclonecopyurl_message_handler = MessageHandler(
        start_rclonecopyurl,
        filters=filters.command("rclonecopyurl")
    )

    get_file_id_message_handler = MessageHandler(
        get_file_id,
        filters=filters.command("getfileid")
    )
    sendfile_by_id_message_handler = MessageHandler(
        sendfile_by_id,
        filters=filters.command("getfile")
    )

    client.add_handler(start_message_handler,group=1)
    client.add_handler(pixivuser_message_handler,group=1)
    client.add_handler(pixivid_message_handler,group=1)
    client.add_handler(magfile_message_handler,group=3)
    client.add_handler(all_callback_handler,group=0)
    client.add_handler(http_download_message_handler,group=1)
    client.add_handler(magnet_download_message_handler, group=1)
    client.add_handler(telegram_file_message_handler, group=1)
    client.add_handler(seach_main_file_message_handler, group=1)
    client.add_handler(start_download_idtg_message_handler, group=1)
    client.add_handler(start_http_downloadtg_message_handler, group=1)
    client.add_handler(start_rclonecopy_message_handler , group=1)
    client.add_handler(start_rclonelsd_message_handler, group=1)
    client.add_handler(start_rclone_message_handler, group=1)
    client.add_handler(start_rclonecopyurl_message_handler, group=1)
    client.add_handler(get_file_id_message_handler, group=1)
    client.add_handler(sendfile_by_id_message_handler, group=1)
    client.run()

if __name__ == '__main__':

    start_bot()

