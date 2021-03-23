
import asyncio
import subprocess
import os
import sys
import nest_asyncio
import threading
import time
import re
from config import aria2, BOT_name
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
nest_asyncio.apply()
os.system("df -lh")

def run_rclone(dir,title,info,file_num,client, message):

    Rclone_remote=os.environ.get('Remote')
    Upload=os.environ.get('Upload')

    name=f"{str(info.message_id)}_{str(info.chat.id)}"
    if int(file_num)==1:
        shell=f"rclone copy \"{dir}\" \"{Rclone_remote}:{Upload}\"  -v --stats-one-line --stats=1s --log-file=\"{name}.log\" "
    else:
        shell=f"rclone copy \"{dir}\" \"{Rclone_remote}:{Upload}/{title}\"  -v --stats-one-line --stats=1s --log-file=\"{name}.log\" "
    print(shell)
    cmd = subprocess.Popen(shell, stdin=subprocess.PIPE, stderr=sys.stderr, close_fds=True,
                           stdout=subprocess.PIPE, universal_newlines=True, shell=True, bufsize=1)
    # 实时输出
    temp_text=None
    while True:
        time.sleep(1)
        fname = f'{name}.log'
        with open(fname, 'r') as f:  #打开文件
            try:
                lines = f.readlines() #读取所有行

                for a in range(-1,-10,-1):
                    last_line = lines[a] #取最后一行
                    if last_line !="\n":
                        break

                print (f"上传中\n{last_line}")
                if temp_text != last_line and "ETA" in last_line:
                    log_time,file_part,upload_Progress,upload_speed,part_time=re.findall("(.*?)INFO.*?(\d.*?),.*?(\d+%),.*?(\d.*?s).*?ETA.*?(\d.*?)",last_line , re.S)[0]
                    text=f"{title}\n" \
                         f"更新时间：`{log_time}`\n" \
                         f"上传部分：`{file_part}`\n" \
                         f"上传进度：`{upload_Progress}`\n" \
                         f"上传速度：`{upload_speed}`\n" \
                         f"剩余时间:`{part_time}`"
                    client.edit_message_text(text=text,chat_id=info.chat.id,message_id=info.message_id,parse_mode='markdown')
                    temp_text = last_line
                f.close()

            except Exception as e:
                print(e)
                f.close()
                continue

        if subprocess.Popen.poll(cmd) == 0:  # 判断子进程是否结束
            print("上传结束")
            client.send_message(text=f"{title}\n上传结束",chat_id=info.chat.id)
            os.remove(f"{name}.log")
            return

    return

async def start_down_telegram_file(client, message):
    try:
        answer = await client.ask(chat_id=message.chat.id, text='请发送TG文件,或输入 /cancel 取消')

        info=answer
        print(info)
        sys.stdout.flush()
        if info.text == "/cancel":
            await client.send_message(text="取消发送", chat_id=message.chat.id, parse_mode='markdown')
            return "False"
        elif info.document == None:
            await client.send_message(text="发送的不是文件", chat_id=message.chat.id, parse_mode='markdown')
            return "False"

        else:
            try:
                return info

            except Exception as e:
                print(f"标记1 {e}")
                sys.stdout.flush()
                await client.send_message(text="下载文件失败", chat_id=message.chat.id, parse_mode='markdown')
                return "False"
    except Exception as e:
        print(f"start_down_telegram_file {e}")
        sys.stdout.flush()

def progress(current, total,client,message,name):

    print(f"{current * 100 / total:.1f}%")
    pro=f"{current * 100 / total:.1f}%"
    client.edit_message_text(chat_id=message.chat.id,message_id=message.message_id,text=f"{name}\n下载中:{pro}")




def tgfile_download(client, message, new_message):
    file_name=new_message.document.file_name
    info=client.send_message(text="开始下载", chat_id=message.chat.id, parse_mode='markdown')
    file = client.download_media(message=new_message, progress=progress, progress_args=(client,info,file_name,))
    try:
        print("开始上传")
        file_dir =file
        files_num =1
        run_rclone(file_dir, file_name, info=info, file_num=files_num, client=client, message=message)
        os.remove(path=file)
        return

    except Exception as e:
        print(e)
        print("Upload Issue!")
        return


def get_msg(client, message):
    return asyncio.run(start_down_telegram_file(client, message))

# now in your sync code you should be able to use:

#commands=['downtgfile']
def get_telegram_file(client, message):
    '''loop = asyncio.get_event_loop()
    temp = loop.run_until_complete(start_down_telegram_file(client, message))'''
    temp=get_msg(client, message)
    sys.stdout.flush()
    if temp =="False":
        return
    else:

        t1 = threading.Thread(target=tgfile_download, args=(client, message, temp))
        t1.start()
        return

