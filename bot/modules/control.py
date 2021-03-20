# -*- coding: utf-8 -*-

from config import aria2, BOT_name
from pyrogram.handlers import MessageHandler
import sys
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
import os
import time
import threading

'''

def run_rclone(dir,title,info,file_num):

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
                    bot.edit_message_text(text=text,chat_id=info.chat.id,message_id=info.message_id,parse_mode='Markdown')
                    temp_text = last_line
                f.close()

            except Exception as e:
                print(e)
                f.close()
                continue

        if subprocess.Popen.poll(cmd) == 0:  # 判断子进程是否结束
            print("上传结束")
            bot.send_message(text=f"{title}\n上传结束",chat_id=info.chat.id)
            os.remove(f"{name}.log")
            return

    return







@bot.message_handler(commands=['magnet'],func=lambda message:str(message.chat.id) == str(Telegram_user_id))
def start_download(message):
    try:
        keywords = str(message.text)
        if str(BOT_name) in keywords:
            keywords = keywords.replace(f"/magnet@{BOT_name} ", "")
            print(keywords)
            t1 = threading.Thread(target=the_download, args=(keywords,message))
            t1.start()
        else:
            keywords = keywords.replace(f"/magnet ", "")
            print(keywords)
            t1 = threading.Thread(target=the_download, args=(keywords,message))
            t1.start()

    except Exception as e:
        print(f"magnet :{e}")

@bot.message_handler(commands=['mirror'],func=lambda message:str(message.chat.id) == str(Telegram_user_id))
def start_http_download(message):
    try:
        keywords = str(message.text)
        if str(BOT_name) in keywords:
            keywords = keywords.replace(f"/mirror@{BOT_name} ", "")
            print(keywords)
            t1 = threading.Thread(target=http_download, args=(keywords,message))
            t1.start()
        else:
            keywords = keywords.replace(f"/mirror ", "")
            print(keywords)
            t1 = threading.Thread(target=http_download, args=(keywords,message))
            t1.start()

    except Exception as e:
        print(f"start_http_download :{e}")'''

async def file_download(client, message,file_dir):
    #os.system("df -lh")
    try:
        print("开始下载")
        sys.stdout.flush()
        currdownload = aria2.add_torrent(torrent_file_path=file_dir)
        info=await client.send_message(chat_id=message.chat.id, text="开始下载", parse_mode='markdown')
        print("发送信息")
        sys.stdout.flush()
    except Exception as e:
        print(e)
        if (str(e).endswith("No URI to download.")):
            print("No link provided!")
            client.send_message(chat_id=message.chat.id,text="No link provided!",parse_mode='markdown')

        return
    new_inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Resume",
                callback_data=f"Resume {currdownload.gid}"
            ),
        InlineKeyboardButton(
            text=f"Pause",
            callback_data=f"Pause {currdownload.gid}"
        ),
        InlineKeyboardButton(
            text=f"Remove",
            callback_data=f"Remove {currdownload.gid}"
        )
        ]
    ]

    new_reply_markup = InlineKeyboardMarkup(inline_keyboard=new_inline_keyboard)
    client.edit_message_text(text="Download complete",chat_id=info.chat.id,message_id=info.message_id,parse_mode='markdown' ,reply_markup=new_reply_markup)
    prevmessage = None

    while currdownload.is_active or not currdownload.is_complete:
        time.sleep(3)
        try:
            currdownload.update()
        except Exception as e:
            if (str(e).endswith("is not found")):
                print("Magnet Deleted")
                print("Magnet download was removed")
                client.edit_message_text(text="Magnet download was removed",chat_id=info.chat.id,message_id=info.message_id,parse_mode='markdown' ,reply_markup=new_reply_markup)
                break
            print(e)
            print("Issue in downloading!")

        if currdownload.status == 'removed':
            print("Magnet was cancelled")
            print("Magnet download was cancelled")
            client.edit_message_text(text="Magnet download was cancelled",chat_id=info.chat.id,message_id=info.message_id,parse_mode='markdown' ,reply_markup=new_reply_markup)
            break

        if currdownload.status == 'error':
            print("Mirror had an error")
            currdownload.remove(force=True, files=True)
            print("Magnet failed to resume/download!\nRun /cancel once and try again.")
            client.edit_message_text(text="Magnet failed to resume/download!\nRun /cancel once and try again.",chat_id=info.chat.id,message_id=info.message_id,parse_mode='markdown' ,reply_markup=new_reply_markup)
            break

        print(f"Magnet Status? {currdownload.status}")

        if currdownload.status == "active":
            try:
                currdownload.update()
                barop = progessbar(currdownload.completed_length,currdownload.total_length)

                updateText = f"{currdownload.status} \n" \
                             f"'{currdownload.name}'\n" \
                             f"Progress : {hum_convert(currdownload.completed_length)}/{hum_convert(currdownload.total_length)} \n" \
                             f"Peers:{currdownload.connections}\n" \
                             f"Speed {hum_convert(currdownload.download_speed)}/s\n" \
                             f"{barop}\n" \
                             f"Free:{get_free_space_mb()}GB"

                if prevmessage != updateText:
                    print(f"更新状态\n{updateText}")
                    client.edit_message_text(text=updateText,chat_id=info.chat.id,message_id=info.message_id,parse_mode='markdown' ,reply_markup=new_reply_markup)
                    prevmessage = updateText
                time.sleep(2)
            except Exception as e:
                if (str(e).endswith("is not found")):
                    break
                print(e)
                print("Issue in downloading!")
                time.sleep(2)
        elif currdownload.status == "paused":
            try:
                currdownload.update()
                barop = progessbar(currdownload.completed_length,currdownload.total_length)

                updateText = f"{currdownload.status} \n" \
                             f"'{currdownload.name}'\n" \
                             f"Progress : {hum_convert(currdownload.completed_length)}/{hum_convert(currdownload.total_length)} \n" \
                             f"Peers:{currdownload.connections}\n" \
                             f"Speed {hum_convert(currdownload.download_speed)}/s\n" \
                             f"{barop}\n" \
                             f"Free:{get_free_space_mb()}GB"

                if prevmessage != updateText:
                    print(f"更新状态\n{updateText}")
                    client.edit_message_text(text=updateText,chat_id=info.chat.id,message_id=info.message_id,parse_mode='markdown', reply_markup=new_reply_markup)
                    prevmessage = updateText
                time.sleep(2)
            except Exception as e:
                print(e)
                print("Download Paused Flood")
                time.sleep(2)




    if currdownload.is_complete:
        print(currdownload.name)
        try:
            print("开始上传")
            file_dir=f"{currdownload.dir}/{currdownload.name}"
            files_num=int(len(currdownload.files))
            #run_rclone(file_dir,currdownload.name,info=info,file_num=files_num)
            #currdownload.remove(force=True,files=True)
            return

        except Exception as e:
            print(e)
            print("Upload Issue!")
            return
    return None

def http_download(client, message,url,):
    try:
        currdownload = aria2.add_uris([url])
        info = client.send_message(chat_id=message.chat.id, text="开始下载", parse_mode='markdown')
    except Exception as e:
        print(e)
        if (str(e).endswith("No URI to download.")):
            print("No link provided!")
            client.send_message(chat_id=message.chat.id,text="No link provided!",parse_mode='markdown')
            return None
    new_inline_keyboard = [
        [
            InlineKeyboardButton(
                text="Resume",
                callback_data=f"Resume {currdownload.gid}"
            ),
            InlineKeyboardButton(
                text=f"Pause",
                callback_data=f"Pause {currdownload.gid}"
            ),
            InlineKeyboardButton(
                text=f"Remove",
                callback_data=f"Remove {currdownload.gid}"
            )
        ]
    ]

    new_reply_markup = InlineKeyboardMarkup(inline_keyboard=new_inline_keyboard)
    client.edit_message_text(text="Downloading", chat_id=info.chat.id, message_id=info.message_id,
                             parse_mode='markdown', reply_markup=new_reply_markup)


    prevmessage=None
    while currdownload.is_active or not currdownload.is_complete:

        try:
            currdownload.update()
        except Exception as e:
            if (str(e).endswith("is not found")):
                print("url Deleted")
                print("url download was removed")
                client.edit_message_text(text="url download was removed",chat_id=info.chat.id,message_id=info.message_id,parse_mode='markdown')
                break
            print(e)
            print("url in downloading!")

        if currdownload.status == 'removed':
            print("url was cancelled")
            print("url download was cancelled")
            client.edit_message_text(text="Magnet download was cancelled",chat_id=info.chat.id,message_id=info.message_id,parse_mode='markdown')
            break

        if currdownload.status == 'error':
            print("url had an error")
            currdownload.remove(force=True, files=True)
            print("url failed to resume/download!.")
            client.edit_message_text(text="Magnet failed to resume/download!\nRun /cancel once and try again.",chat_id=info.chat.id,message_id=info.message_id,parse_mode='markdown')
            break

        print(f"url Status? {currdownload.status}")

        if currdownload.status == "active":
            try:
                currdownload.update()
                barop = progessbar(currdownload.completed_length,currdownload.total_length)

                updateText = f"{currdownload.status} \n" \
                             f"'{currdownload.name}'\n" \
                             f"Progress : {hum_convert(currdownload.completed_length)}/{hum_convert(currdownload.total_length)} \n" \
                             f"Speed {hum_convert(currdownload.download_speed)}/s\n" \
                             f"{barop}\n" \
                             f"Free:{get_free_space_mb()}GB"

                if prevmessage != updateText:
                    print(f"更新状态\n{updateText}")
                    client.edit_message_text(text=updateText,chat_id=info.chat.id,message_id=info.message_id,parse_mode='markdown', reply_markup=new_reply_markup)
                    prevmessage = updateText
                time.sleep(2)
            except Exception as e:
                if (str(e).endswith("is not found")):
                    break
                print(e)
                print("Issue in downloading!")
                time.sleep(2)
        elif currdownload.status == "paused":
            try:
                currdownload.update()
                barop = progessbar(currdownload.completed_length,currdownload.total_length)

                updateText = f"{currdownload.status} \n" \
                             f"'{currdownload.name}'\n" \
                             f"Progress : {hum_convert(currdownload.completed_length)}/{hum_convert(currdownload.total_length)} \n" \
                             f"Speed {hum_convert(currdownload.download_speed)}/s\n" \
                             f"{barop}\n" \
                             f"Free:{get_free_space_mb()}GB"

                if prevmessage != updateText:
                    print(f"更新状态\n{updateText}")
                    client.edit_message_text(text=updateText,chat_id=info.chat.id,message_id=info.message_id,parse_mode='markdown', reply_markup=new_reply_markup)
                    prevmessage = updateText
                time.sleep(2)
            except Exception as e:
                print(e)
                print("Download Paused Flood")
                time.sleep(2)
        time.sleep(2)

        time.sleep(1)
    if currdownload.is_complete:
        print(currdownload.name)
        try:
            print("开始上传")
            file_dir=f"{currdownload.dir}/{currdownload.name}"
            #run_rclone(file_dir,currdownload.name,info=info,file_num=1)
            #currdownload.remove(force=True,files=True)

        except Exception as e:
            print(e)
            print("Upload Issue!")
    return None


def progessbar(new, tot):
    """Builds progressbar
    Args:
        new: current progress
        tot: total length of the download
    Returns:
        progressbar as a string of length 20
    """
    length = 20
    progress = int(round(length * new / float(tot)))
    percent = round(new/float(tot) * 100.0, 1)
    bar = '=' * progress + '-' * (length - progress)
    return '[%s] %s %s\r' % (bar, percent, '%')


def hum_convert(value):
    value=float(value)
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = 1024.0
    for i in range(len(units)):
        if (value / size) < 1:
            return "%.2f%s" % (value, units[i])
        value = value / size

def get_free_space_mb():
    result=os.statvfs('/root/')
    block_size=result.f_frsize
    total_blocks=result.f_blocks
    free_blocks=result.f_bfree
    # giga=1024*1024*1024
    giga=1000*1000*1000
    total_size=total_blocks*block_size/giga
    free_size=free_blocks*block_size/giga
    print('total_size = %s' % int(total_size))
    print('free_size = %s' % free_size)
    return int(free_size)

def progress(current, total):

    print(f"{current * 100 / total:.1f}%")


def file_del(gid):
    print("开始删除")
    try:
        dele = aria2.get_download(gid=str(gid))
        torrent_name=dele.name
        del_result=dele.remove(force=True, files=True)
        if del_result==True:
            print(f"{torrent_name}\n删除成功")
            return f"删除成功"
        else:
            print(f"{torrent_name}\n删除失败")
            return f"删除失败"
    except Exception as e:
        print (e)
        return f"\n删除失败：{e}"

def file_resume(gid):
    print("开始任务")
    try:
        the_resume = aria2.get_download(gid=str(gid))
        torrent_name=the_resume.name
        resume_result=the_resume.resume()
        if resume_result==True:
            print(f"{torrent_name}\n开始成功")
            return f"开始成功"
        else:
            print(f"{torrent_name}\n开始失败")
            return f"开始失败"
    except Exception as e:
        print (e)
        return f"\n开始失败：{e}"

def file_pause(gid):
    print("暂停任务")
    try:
        the_pause = aria2.get_download(gid=str(gid))
        torrent_name=the_pause.name
        resume_result=the_pause.pause()
        if resume_result==True:
            print(f"{torrent_name}\n暂停成功")
            return f"暂停成功"
        else:
            print(f"{torrent_name}\n暂停失败")
            return f"暂停失败"
    except Exception as e:
        print (e)
        return f"\n暂停失败：{e}"

def all_callback(client, message):
    try:

        if "Remove" in message.data:
            the_gid=str(message.data).replace("Remove ","")
            info_text = file_del(gid=the_gid)
            client.answer_callback_query(callback_query_id=message.id,text=info_text,cache_time=3)
        elif "Resume" in message.data:
            the_gid=str(message.data).replace("Resume ","")
            info_text = file_resume(gid=the_gid)
            client.answer_callback_query(callback_query_id=message.id,text=info_text,cache_time=3)
        elif "Pause" in message.data:
            the_gid=str(message.data).replace("Pause ","")
            info_text = file_pause(gid=the_gid)
            client.answer_callback_query(callback_query_id=message.id,text=info_text,cache_time=3)

    except Exception as e:
        print(f"all_callback :{e}")


#commands=['magfile']
async def send_telegram_file(client, message):

    answer = await client.ask(chat_id=message.chat.id, text='请发送种子文件,或输入 /cancel 取消')
    print(answer)
    print(answer.document)
    if answer.document==None:
        await client.send_message(text="发送的不是文件", chat_id=message.chat.id, parse_mode='markdown')
        return
    elif answer.text=="/cancel":
        await client.send_message(text="取消发送", chat_id=message.chat.id, parse_mode='markdown')
        return
    else:
        try:

            file_dir = await client.download_media(message=answer, progress=progress)
            t1 = threading.Thread(target=file_download, args=(client, message,file_dir))
            t1.start()
            return
        except Exception as e:
            print(f"{e}")
            await client.send_message(text="下载文件失败", chat_id=message.chat.id, parse_mode='markdown')
            return
    #await client.send_message(chat_id=message.chat.id, text=f'Your name is: {answer.text}')
    #client.send_message(text="请发送文件,或输入 /cancel 取消", chat_id=message.chat.id, parse_mode='markdown')







