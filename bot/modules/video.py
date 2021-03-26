
import threading
import youtube_dl
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton

def get_video_info(client, message, url):
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
    result = ydl.extract_info(
        url=url,
        download=False,

    )
    print(result)
    video_name=result['title']
    video_description=result['description']
    video_img=result['thumbnails'][len(result['thumbnails'])-1]["url"]
    video_uploader=result['uploader']
    text=f"视频名称：{video_name}\n" \
         f"作者:{video_uploader}\n" \
         f"简介：{video_description}\n"
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

    new_reply_markup = InlineKeyboardMarkup(inline_keyboard=new_inline_keyboard)
    client.send_photo(caption=text, photo=video_img,chat_id=message.chat.id, message_id=message.message_id,
                             parse_mode='markdown', reply_markup=new_reply_markup)




def start_get_video_info(client, message):
    keywords = message.text.split()[1]
    print(keywords)

    t1 = threading.Thread(target=get_video_info, args=(client, message, keywords))
    t1.start()