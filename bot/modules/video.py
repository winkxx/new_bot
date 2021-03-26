
import threading
import youtube_dl
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
import sys
import requests
import os

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
        text=f"视频名称：{video_name}\n" \
             f"作者:{video_uploader}\n" \
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
                text="Resume",
                callback_data=f"Resume "
            ),
            InlineKeyboardButton(
                text=f"Pause",
                callback_data=f"Pause "
            ),
            InlineKeyboardButton(
                text=f"Remove",
                callback_data=f"Remove "
            )
        ]
    ]
    img = requests.get(url=video_img)
    img_name=f"{message.chat.id}{message.message_id}temp"
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
