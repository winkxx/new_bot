
from config import aria2
from modules.picacg import add_download
import sys


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
        print(message)
        sys.stdout.flush()
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
        elif "down" in message.data:


            client.answer_callback_query(callback_query_id=message.id,text="开始下载",cache_time=3)

            #add_download(call=call)
    except Exception as e:
        print(f"all_callback :{e}")