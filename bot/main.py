# -*- coding: utf-8 -*-
from apscheduler.schedulers.background import BackgroundScheduler
import sys
from modules.check import new_clock, second_clock
from config import client, Telegram_user_id,aria2
from pyrogram.handlers import MessageHandler,CallbackQueryHandler
from pyrogram import filters
from modules.pixiv import start_download_pixiv,start_download_id,start_download_pixivtg,start_download_pixivphoto,start_download_pixivtele
from modules.control import send_telegram_file,start_http_download,start_download,start_http_downloadtg,check_upload
from modules.call import start_pause,start_remove,start_Resume,start_benzi_down,start_download_video
from modules.moretg import get_telegram_file,get_file_id,sendfile_by_id
from modules.picacg import seach_main
from modules.rclone import start_rclonecopy,start_rclonelsd,start_rclonels,start_rclonecopyurl
from modules.video import start_get_video_info

async def chexk_group(_, client, query):
    #print(query)
    try:
        info=await client.get_chat_member(chat_id=int(Telegram_user_id),user_id=query.from_user.id)
        print(info)
        sys.stdout.flush()
        return True
    except:
        text = "要使用bot,请先加入群组\nhttps://t.me/OneDrive_1oveClub"
        await client.send_message(chat_id=int(query.chat.id), text=text)
        return False




async def help(client, message):
    print(client)
    print(message)
    text='''********** pixiv相关 **********
/pixivuser - 打包下载P站画师的全部作品上传至云盘
/pixivusertg - 压缩打包下载P站画师的全部作品发送到TG
/pixivuserphoto - 下载P站画师的全部作品图片方式发送
pixivusertele - 下载P站画师的全部作品网页方式发送
在命令后加入作品ID，使用示例
/pixivuser 9675329

/pixivpid - 发送pixiv该id的图片
在命令后加入作品ID，使用示例
/pixivpid 88339301

********** aria2相关 **********
/magfile - 推送种子文件至aria2下载
/mirror - 推送直链至aria2下载上传至网盘
/mirrortg - 推送直链至aria2下载发送到TG
/magnet - 推送磁力链接至aria2下载
以上在命令后加入链接

********** 其它相关 **********
/downtgfile - 发送TG文件并上传至网盘
发送 /downtgfile 后按提示发送文件即可

/search - 在哔咔搜索本子
示例 /search 本子名

/rclonecopyurl - 用rclonecopyurl的方式直接上传直链文件
示例 /rclonecopyurl 文件直链

/getfileid - 发送文件获取fileid
发送 /getfileid  后按提示发送文件即可

/getfile - 发送fileid来获取文件
示例 /getfile  文件直链

/video - 使用youtube-dl下载视频
示例 /getfile  视频链接
目前测试youtube和哔哩哔哩(不包括番剧)完美适配

Bot相关联系：https://t.me/Ben_chao'''
    try:
        await client.send_message(chat_id=int(message.chat.id), text=text)
    except Exception as e:
        print(f"help :{e}")


def start_bot():
    #scheduler = BlockingScheduler()
    scheduler = BackgroundScheduler()

    scheduler.add_job(new_clock, "interval", seconds=60)
    scheduler.add_job(second_clock, "interval", seconds=60)
    scheduler.start()
    print("开启监控")

    sys.stdout.flush()
    print("开始bot")
    print(Telegram_user_id)
    sys.stdout.flush()
    aria2.listen_to_notifications(on_download_complete=check_upload, threaded=True)



    start_message_handler = MessageHandler(
        help,
        #filters=filters.command("start") & filters.user(int(Telegram_user_id))
        filters=filters.command(["start","help"]) & filters.private
    )

    pixivuser_message_handler = MessageHandler(
        start_download_pixiv,
        filters=filters.command("pixivuser") & filters.create(chexk_group) & filters.private 
    )


    pixivid_message_handler = MessageHandler(
        start_download_id,
        filters=filters.command("pixivpid") & filters.create(chexk_group) & filters.private
    )

    magfile_message_handler = MessageHandler(
        send_telegram_file,
        filters=filters.command("magfile") & filters.create(chexk_group) & filters.private
    )



    http_download_message_handler = MessageHandler(
        start_http_download,
        filters=filters.command("mirror") & filters.create(chexk_group) & filters.private
    )
    magnet_download_message_handler = MessageHandler(
        start_download,
        filters=filters.command("magnet") & filters.create(chexk_group) & filters.private
    )

    telegram_file_message_handler = MessageHandler(
        get_telegram_file,
        filters=filters.command("downtgfile") & filters.create(chexk_group) & filters.private
    )
    seach_main_file_message_handler = MessageHandler(
        seach_main,
        filters=filters.command("search") & filters.create(chexk_group) & filters.private
    )

    start_download_idtg_message_handler = MessageHandler(
        start_download_pixivtg,
        filters=filters.command("pixivusertg") & filters.create(chexk_group) & filters.private
    )

    start_http_downloadtg_message_handler = MessageHandler(
        start_http_downloadtg,
        filters=filters.command("mirrortg") & filters.create(chexk_group) & filters.private
    )
    start_rclonecopy_message_handler = MessageHandler(
        start_rclonecopy,
        filters=filters.command("rclonecopy") & filters.create(chexk_group) & filters.private
    )

    start_rclonelsd_message_handler = MessageHandler(
        start_rclonelsd,
        filters=filters.command("rclonelsd") & filters.create(chexk_group) & filters.private
    )

    start_rclone_message_handler = MessageHandler(
        start_rclonels,
        filters=filters.command("rclone") & filters.create(chexk_group) & filters.private
    )

    start_rclonecopyurl_message_handler = MessageHandler(
        start_rclonecopyurl,
        filters=filters.command("rclonecopyurl") & filters.create(chexk_group) & filters.private
    )

    get_file_id_message_handler = MessageHandler(
        get_file_id,
        filters=filters.command("getfileid") & filters.create(chexk_group) & filters.private
    )
    sendfile_by_id_message_handler = MessageHandler(
        sendfile_by_id,
        filters=filters.command("getfile") & filters.create(chexk_group) & filters.private
    )

    start_download_pixivphoto_message_handler = MessageHandler(
        start_download_pixivphoto,
        filters=filters.command("pixivuserphoto") & filters.create(chexk_group) & filters.private
    )

    start_download_pixivtele_message_handler = MessageHandler(
        start_download_pixivtele,
        filters=filters.command("pixivusertele") & filters.create(chexk_group) & filters.private
    )

    start_get_video_info_message_handler = MessageHandler(
        start_get_video_info,
        filters=filters.command("video") & filters.create(chexk_group) & filters.private
    )

    start_Resume_handler = CallbackQueryHandler(
        callback=start_Resume,
        filters=filters.create(lambda _, __, query: "Resume" in query.data )
        )

    start_pause_handler = CallbackQueryHandler(
        callback=start_pause,
        filters=filters.create(lambda _, __, query: "Pause" in query.data )
        )
    start_remove_handler = CallbackQueryHandler(
        callback=start_remove,
        filters=filters.create(lambda _, __, query: "Remove" in query.data )
        )

    start_benzi_down_handler = CallbackQueryHandler(
        callback=start_benzi_down,
        filters=filters.create(lambda _, __, query: "down" in query.data )
        )
    start_download_video_handler = CallbackQueryHandler(
        callback=start_download_video,
        filters=filters.create(lambda _, __, query: "video" in query.data )
        )

    client.add_handler(start_download_video_handler, group=0)
    client.add_handler(start_Resume_handler, group=0)
    client.add_handler(start_pause_handler, group=0)
    client.add_handler(start_remove_handler, group=0)
    client.add_handler(start_benzi_down_handler, group=0)

    client.add_handler(start_message_handler,group=1)
    client.add_handler(pixivuser_message_handler,group=1)
    client.add_handler(pixivid_message_handler,group=1)
    client.add_handler(magfile_message_handler,group=3)

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
    client.add_handler(start_download_pixivphoto_message_handler, group=1)
    client.add_handler(start_download_pixivtele_message_handler, group=1)
    client.add_handler(start_get_video_info_message_handler, group=1)
    client.run()

if __name__ == '__main__':

    start_bot()

