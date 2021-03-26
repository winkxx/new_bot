
import threading

import youtube_dl
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
import sys
import requests
import os
import time


temp_time= time.time()




def download_video(client, message):
    def download_video_status(d):
        global temp_time

        time_end = time.time()
        if time_end - temp_time < 2:
            return
        else:
            temp_time = time.time()
            if d['status'] == 'downloading':
                # print(d)
                text="下载中 " + d['_percent_str'] + " " + d['_speed_str']
                client.send_message(chat_id=message.chat.id, text=text, parse_mode='markdown')
                return
            if d['status'] == 'finished':
                filename = d['filename']
                print(filename)
                client.send_message(chat_id=message.chat.id, text=filename, parse_mode='markdown')

    import re
    
    caption = str(message.message.caption)
    
    web_url = re.findall("web_url:(.*?)\n", caption, re.S)[0]
    ydl_opts = {
        'format': 'bestvideo[width>=1080]+bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'progress_hooks': [download_video_status]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([web_url])
        return 

    


def get_video_info(client, message, url):
    try:
        print(url)
        sys.stdout.flush()
        ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
        result = ydl.extract_info(
            url=url,
            download=False,

        )
        #print(result)
        video_name=result['title']
        video_description=result['description']
        video_img=result['thumbnails'][len(result['thumbnails'])-1]["url"]
        video_uploader=result['uploader']
        web_url=result['webpage_url']
        text=f"视频名称：{video_name}\n" \
             f"作者:{video_uploader}\n" \
             f"web_url:{web_url}\n" \
             f"简介：{video_description}\n"
        print(text)
        print(video_img)
        sys.stdout.flush()
    except Exception as e:
        client.send_message(chat_id=message.chat.id, text=f"无法获取视频信息:\n{e}", parse_mode='markdown')
        return

    new_inline_keyboard = [
        [
            InlineKeyboardButton(
                text="上传网盘",
                callback_data=f"videorclone"
            ),
            InlineKeyboardButton(
                text=f"发送给我",
                callback_data=f"videotg"
            )
        ]
    ]
    img = requests.get(url=video_img)
    img_name=f"{message.chat.id}{message.message_id}.png"
    with open(img_name, 'wb') as f:
        f.write(img.content)
        f.close()
    new_reply_markup = InlineKeyboardMarkup(inline_keyboard=new_inline_keyboard)
    client.send_photo(caption=text[0:1024], photo=img_name,chat_id=message.chat.id,
                             parse_mode='markdown', reply_markup=new_reply_markup)
    os.remove(img_name)




def start_get_video_info(client, message):
    keywords = message.text.split()[1]
    print(keywords)

    t1 = threading.Thread(target=get_video_info, args=(client, message, keywords))
    t1.start()
