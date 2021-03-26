
import threading

import youtube_dl
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
import sys
import requests
import os
import time


temp_time= time.time()

def progress(current, total,client,message,name):

    print(f"{current * 100 / total:.1f}%")
    pro=f"{current * 100 / total:.1f}%"
    try:
        client.edit_message_text(chat_id=message.chat.id,message_id=message.message_id,text=f"{name}\n上传中:{pro}")
    except Exception as e:
        print("e")


class Download_video():


    def download_video_status(self,d):
        global temp_time


        if d['status'] == 'downloading':
            time_end = time.time()
            if time_end - temp_time < 2:
                None
            else:
                temp_time = time.time()
                # print(d)
                text="下载中 " + d['_percent_str'] + " " + d['_speed_str']
                try:
                    self.client.edit_message_text(text=text, chat_id=self.info.chat.id, message_id=self.info.message_id,
                                         parse_mode='markdown')
                except:
                    None

        if d['status'] == 'finished':
            filename = d['filename']
            print(f"标记 8 {filename}")
            if ".mp4" in filename:
                self.file=filename
            try:
                self.client.edit_message_text(text=f"{filename}\n下载完成，开始上传", chat_id=self.info.chat.id, message_id=self.info.message_id,
                                          parse_mode='markdown')
            except:
                None

    def __init__(self,client, call):
        #调用父类的构函
        self.client=client
        self.call=call
        self.file=""

    def download_video(self):
        try:
            import re
            print("开始下载视频")
            sys.stdout.flush()
            message_chat_id = self.call.message.chat.id
            self.info = self.client.send_message(chat_id=message_chat_id, text="开始下载", parse_mode='markdown')
            caption = str(self.call.message.caption)

            web_url = re.findall("web_url:(.*?)\n", caption, re.S)[0]
            print(web_url)
            sys.stdout.flush()
            ydl_opts = {
                'format': "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio",
                'quiet': True,
                'no_warnings': True,
                'progress_hooks': [self.download_video_status]
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([web_url])

        except Exception as e:
            print(f"下载视频失败 :{e}")
            sys.stdout.flush()
            return

        if self.call.data =="videorclone":
            print(f"{self.file}上传到网盘")

            sys.stdout.flush()
        else:
            print(f"{self.file}发送到TG")

            sys.stdout.flush()
            os.system("ls")
            self.client.send_video(chat_id=self.call.message.chat.id,video=self.file,caption=caption ,progress=progress,
                                           progress_args=(self.client, self.info, self.file,))






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
