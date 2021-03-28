# -*- coding: utf-8 -*-
import os
import sys
import requests
import zipfile
import threading
import sys
import io
import os
from PIL import Image
from PIL import ImageFile
from pyrogram.types import InputMediaPhoto
import telegraph
from telegraph import Telegraph
from modules.control import run_await_rclone

session = requests.Session()
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 5.8; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
    'Referer': 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
}

def compress_image(outfile, mb, quality=85, k=0.9):
    """不改变图片尺寸压缩到指定大小
    :param outfile: 压缩文件保存地址
    :param mb: 压缩目标，KB
    :param step: 每次调整的压缩比率
    :param quality: 初始压缩比率
    :return: 压缩文件地址，压缩文件大小
    """

    o_size = os.path.getsize(outfile) // 1024
    print(o_size, mb)
    if o_size <= mb:
        return outfile

    ImageFile.LOAD_TRUNCATED_IMAGES = True
    while o_size > mb:
        im = Image.open(outfile)
        x, y = im.size
        out = im.resize((int(x * k), int(y * k)), Image.ANTIALIAS)
        try:
            dir, suffix = os.path.splitext(outfile)
            os.remove(outfile)
            #print(outfile)
            outfile = '{}{}'.format(dir, suffix)
            out.save(outfile, quality=quality)
        except Exception as e:
            print(e)
            break
        o_size = os.path.getsize(outfile) // 1024
    return outfile



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

# 下载模块
def download(url, title,author, id):
    global session,header
    path = author
    if not os.path.exists(path):
        os.mkdir(path)
    title = str(title)
    id = str(id)
    title = eval(repr(title).replace('\\', ''))
    title = eval(repr(title).replace('/', ''))
    title = eval(repr(title).replace('?', ''))
    title = eval(repr(title).replace('*', ''))
    title = eval(repr(title).replace('・', ''))
    title = eval(repr(title).replace('！', ''))
    title = eval(repr(title).replace('|', ''))
    title = eval(repr(title).replace(' ', ''))
    r = session.get(url, headers=header)

    try:
        if "jpg" in url:
            with open(f'{author}/{title}.jpg', 'wb') as f:
                f.write(r.content)
            print("下载成功:" + title )

            return True
        elif "png" in url:
            with open(f'{author}/{title}.png', 'wb') as f:
                f.write(r.content)
            print( "下载成功:" + title )
            return True

    except Exception as e:
        print("下载失败:" + title )
        print(e)
        return False

def zip_ya(start_dir):
    start_dir = start_dir  # 要压缩的文件夹路径
    file_news = start_dir + '.zip'  # 压缩后文件夹的名字
    z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)
    for dir_path, dir_names, file_names in os.walk(start_dir):
        f_path = dir_path.replace(start_dir, '')  # 这一句很重要，不replace的话，就从根目录开始复制
        f_path = f_path and f_path + os.sep or ''  # 实现当前文件夹以及包含的所有文件的压缩
        for filename in file_names:
            z.write(os.path.join(dir_path, filename), f_path + filename)
    z.close()
    return file_news

def del_path(path):
    if not os.path.exists(path):
        return
    if os.path.isfile(path):
        os.remove(path)
        # print( 'delete file %s' % path)
    else:
        items = os.listdir(path)
        for f in items:
            c_path = os.path.join(path, f)
            if os.path.isdir(c_path):
                del_path(c_path)
            else:
                os.remove(c_path)
                # print('delete file %s' % c_path)
        os.rmdir(path)
        # print( 'delete dir %s' % path)




async def start_download_pixiv(client, message):

        print(message)
        keywords = str(message.text)
        keywords = keywords.replace("/pixivuser ", "")
        print(keywords)
        artistid=keywords
        idurl = f"https://www.pixiv.net/ajax/user/{artistid}/profile/all"
        print(idurl)
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 5.8; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
        }
        html2 = requests.get(url=idurl, headers=header)
        print(html2)

        print(message.chat.id)
        illusts=html2.json()['body']['illusts']

        info = await client.send_message(chat_id=message.chat.id, text="开始下载", parse_mode='markdown')
        print(info)
        print(info.chat)
        img_num=len(illusts)
        img_su_num=0
        img_er_num=0
        for id in illusts:
            print(id)
            info_url = f"https://www.pixiv.net/touch/ajax/illust/details?illust_id={id}"
            ht = requests.get(url=info_url, headers=header)
            info_json=ht.json()
            img_url=info_json['body']['illust_details']['url_big']
            title=info_json['body']['illust_details']['meta']['title']+f"id-{id}"

            #.author_details.profile_img.main
            author=f"{info_json['body']['author_details']['user_name']}"

            title=str(title).replace("#","").replace(author,"").replace(":","").replace("@","").replace("/","")
            author=str(author).replace(":","").replace("@","").replace("/","")
            print(img_url)

            download_result=download(url=img_url,title=title,author=keywords,id=id)
            if download_result==True:
                img_su_num=img_su_num+1
            else:
                img_er_num=img_er_num+1

            text=f"Author:{author}\n" \
                 f"Number of pictures:{img_num}\n" \
                 f"Number of successes:{img_su_num}\n" \
                 f"Number of errors:{img_er_num}\n" \
                 f"Progessbar:\n{progessbar(img_su_num,img_num)}"

            await client.edit_message_text(chat_id=info.chat.id, message_id=info.message_id, text=text, parse_mode="markdown")
        print("开始压缩")
        sys.stdout.flush()
        name = zip_ya(keywords)
        print(name)
        print("压缩完成，开始上传")
        sys.stdout.flush()
        del_path(keywords)
        try:
            await run_await_rclone(client=client,dir=name,title=name,info=info,file_num=1,message=info)
            print("uploading")
        except Exception as e:
            print(f"{e}")
            sys.stdout.flush()
            await client.send_message(chat_id=message.chat.id, text="文件上传失败")

        await client.delete_messages(chat_id=message.chat.id, message_ids=message.message_id)
        os.system("rm '" + name + "'")


async def start_download_id(client, message):
    # print(message)
    keywords = str(message.text)
    keywords = keywords.replace("/pixivpid ", "")
    print(keywords)
    info_url = f"https://www.pixiv.net/touch/ajax/illust/details?illust_id={keywords}"
    ht = requests.get(url=info_url, headers=header)
    info_json = ht.json()
    imgurl = info_json['body']['illust_details']['url_big']
    r = session.get(url=imgurl, headers=header)
    title = info_json['body']['illust_details']['meta']['title']

    # .author_details.profile_img.main
    author = f"{info_json['body']['author_details']['user_name']}"
    if "jpg" in imgurl:
        with open(f'{keywords}.jpg', 'wb') as f:
            f.write(r.content)
            imgname=f"{keywords}.jpg"
    elif "png" in imgurl:
        with open(f'{keywords}.png', 'wb') as f:
            f.write(r.content)
            imgname = f"{keywords}.png"
    send_text=f"{title}\nAuthor:{author}\nPid:{keywords}"
    await client.send_photo(chat_id=message.chat.id,photo=imgname , caption=send_text)
    os.system("rm '" + imgname + "'")

def progress(current, total,client,message,name):

    print(f"{current * 100 / total:.1f}%")
    pro=f"{current * 100 / total:.1f}%"
    try:
        client.edit_message_text(chat_id=message.chat.id,message_id=message.message_id,text=f"{name}\n上传中:{pro}")
    except Exception as e:
        print("e")

async def start_download_pixivtg(client, message):
    # print(message)
    keywords = str(message.text)
    keywords = keywords.replace("/pixivusertg ", "")
    print(keywords)
    artistid = keywords
    idurl = f"https://www.pixiv.net/ajax/user/{artistid}/profile/all"
    print(idurl)
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 5.8; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
    }
    html2 = requests.get(url=idurl, headers=header)
    print(html2)

    illusts = html2.json()['body']['illusts']
    info = await client.send_message(chat_id=message.chat.id, text="开始下载")
    img_num = len(illusts)
    img_su_num = 0
    img_er_num = 0
    for id in illusts:
        print(id)
        info_url = f"https://www.pixiv.net/touch/ajax/illust/details?illust_id={id}"
        ht = requests.get(url=info_url, headers=header)
        info_json = ht.json()
        img_url = info_json['body']['illust_details']['url_big']
        title = info_json['body']['illust_details']['meta']['title'] + f"id-{id}"

        # .author_details.profile_img.main
        author = f"{info_json['body']['author_details']['user_name']}"

        title = str(title).replace("#", "").replace(author, "").replace(":", "").replace("@", "").replace("/", "")
        author = str(author).replace(":", "").replace("@", "").replace("/", "")
        print(img_url)

        download_result = download(url=img_url, title=title, author=keywords, id=id)
        if download_result == True:
            img_su_num = img_su_num + 1
        else:
            img_er_num = img_er_num + 1

        text = f"Author:{author}\n" \
               f"Number of pictures:{img_num}\n" \
               f"Number of successes:{img_su_num}\n" \
               f"Number of errors:{img_er_num}\n" \
               f"Progessbar:\n{progessbar(img_su_num, img_num)}"

        await client.edit_message_text(chat_id=info.chat.id, message_id=info.message_id, text=text, parse_mode="markdown")
    print("开始压缩")
    sys.stdout.flush()
    name = zip_ya(keywords)
    print(name)
    print("压缩完成，开始上传")
    del_path(keywords)
    try:
        #run_upload_rclone(client=client, dir=name, title=name, info=info, file_num=1)
        await client.send_document(chat_id=info.chat.id, document=name, caption=name, progress=progress, progress_args=(client,info,name,))
        print("uploading")

    except Exception as e:
        print(f"{e}")
        sys.stdout.flush()
        await client.send_message(chat_id=message.chat.id, text="文件上传失败")
        return

    await client.delete_messages(chat_id=message.chat.id, message_ids=message.message_id)
    os.system("rm '" + name + "'")
    return


async def start_download_pixivphoto(client, message):
    # print(message)
    keywords = str(message.text)
    keywords = keywords.replace("/pixivuserphoto ", "")
    print(keywords)
    artistid = keywords
    idurl = f"https://www.pixiv.net/ajax/user/{artistid}/profile/all"
    print(idurl)
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 5.8; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
    }
    html2 = requests.get(url=idurl, headers=header)
    print(html2)

    illusts = html2.json()['body']['illusts']
    info = await client.send_message(chat_id=message.chat.id, text="开始下载")
    img_num = len(illusts)
    img_su_num = 0
    img_er_num = 0
    for id in illusts:
        print(id)
        info_url = f"https://www.pixiv.net/touch/ajax/illust/details?illust_id={id}"
        ht = requests.get(url=info_url, headers=header)
        info_json = ht.json()
        img_url = info_json['body']['illust_details']['url_big']
        title = info_json['body']['illust_details']['meta']['title'] + f"id-{id}"

        # .author_details.profile_img.main
        author = f"{info_json['body']['author_details']['user_name']}"

        title = str(title).replace("#", "").replace(author, "").replace(":", "").replace("@", "").replace("/", "")
        author = str(author).replace(":", "").replace("@", "").replace("/", "")
        print(img_url)

        download_result = download(url=img_url, title=title, author=keywords, id=id)
        if download_result == True:
            img_su_num = img_su_num + 1
        else:
            img_er_num = img_er_num + 1

        text = f"Author:{author}\n" \
               f"Number of pictures:{img_num}\n" \
               f"Number of successes:{img_su_num}\n" \
               f"Number of errors:{img_er_num}\n" \
               f"Progessbar:\n{progessbar(img_su_num, img_num)}"

        await client.edit_message_text(chat_id=info.chat.id, message_id=info.message_id, text=text, parse_mode="markdown")


    try:
        img_list=[]
        for root, dirs, files in os.walk(keywords):
            for file in files:
                try:
                    file_dir = os.path.join(root, file)
                    print(file_dir, file)

                    if os.path.getsize(file_dir) < 1024*1024* 10:
                        img_list.append(InputMediaPhoto(media=file_dir, caption=file))
                    else:
                        file_dir=compress_image(outfile=file_dir,mb=10000)
                        img_list.append(InputMediaPhoto(media=file_dir, caption=file))

                    if len(img_list)==10:
                        await client.send_chat_action(chat_id=message.chat.id,action="upload_photo")
                        print("开始上传")
                        sys.stdout.flush()
                        await client.send_media_group(chat_id=message.chat.id,media=img_list)
                        img_list = []
                except Exception as e:
                    print(f"标记3 {e}")
                    sys.stdout.flush()

        if len(img_list) != 0:
            await client.send_chat_action(chat_id=message.chat.id, action="upload_photo")
            print("开始上传")
            sys.stdout.flush()
            await client.send_media_group(chat_id=message.chat.id, media=img_list)


    except Exception as e:
        print(f"{e}")
        sys.stdout.flush()
        await client.send_message(chat_id=message.chat.id, text="图片上传失败")
        return

    await client.delete_messages(chat_id=message.chat.id, message_ids=message.message_id)
    del_path(keywords)
    return

def put_telegraph(title,md_text):
  tele = Telegraph()

  tele.create_account(short_name='Bot')
  response = tele.create_page(
      title=title,
      html_content=md_text
  )

  text_url='https://telegra.ph/{}'.format(response['path'])
  return text_url


async def start_download_pixivtele(client, message):

    keywords = message.text.split()[1]
    print(keywords)
    artistid = keywords
    idurl = f"https://www.pixiv.net/ajax/user/{artistid}/profile/all"
    print(idurl)
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 5.8; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
    }
    html2 = requests.get(url=idurl, headers=header)
    print(html2)

    illusts = html2.json()['body']['illusts']
    info = await client.send_message(chat_id=message.chat.id, text="开始下载")
    img_num = len(illusts)
    img_su_num = 0
    img_er_num = 0
    for id in illusts:
        print(id)
        info_url = f"https://www.pixiv.net/touch/ajax/illust/details?illust_id={id}"
        ht = requests.get(url=info_url, headers=header)
        info_json = ht.json()
        img_url = info_json['body']['illust_details']['url_big']
        title = info_json['body']['illust_details']['meta']['title'] + f"id-{id}"

        # .author_details.profile_img.main
        author = f"{info_json['body']['author_details']['user_name']}"

        title = str(title).replace("#", "").replace(author, "").replace(":", "").replace("@", "").replace("/", "")
        author = str(author).replace(":", "").replace("@", "").replace("/", "")
        print(img_url)

        download_result = download(url=img_url, title=title, author=keywords, id=id)
        if download_result == True:
            img_su_num = img_su_num + 1
        else:
            img_er_num = img_er_num + 1

        text = f"Author:{author}\n" \
               f"Number of pictures:{img_num}\n" \
               f"Number of successes:{img_su_num}\n" \
               f"Number of errors:{img_er_num}\n" \
               f"Progessbar:\n{progessbar(img_su_num, img_num)}"

        await client.edit_message_text(chat_id=info.chat.id, message_id=info.message_id, text=text, parse_mode="markdown")



    img_list=[]
    name_list = []

    for root, dirs, files in os.walk(keywords):
        for file in files:
            try:
                file_dir = os.path.join(root, file)
                print(file_dir, file)

                if os.path.getsize(file_dir) < 1024*512* 10:
                    print(file_dir, file)

                    info = telegraph.upload.upload_file(file_dir)
                    url = "https://telegra.ph" + info[0]

                    name_list.append(file)
                    img_list.append(url)
                else:
                    file_dir=compress_image(outfile=file_dir,mb=5000)
                    print(file_dir, file)
                    info = telegraph.upload.upload_file(file_dir)
                    url = "https://telegra.ph" + info[0]

                    name_list.append(file)
                    img_list.append(url)



            except Exception as e:
                print(f"标记4 {e}")

                sys.stdout.flush()
                continue
    try:
        put_text = "<p>Tips:5M以上的图片会被压缩</p><br>"
        for a, b in zip(name_list, img_list):
            put_text = put_text + f"<strong>{a}</strong><br /><img src=\"{b}\" /><br>\n\n"
        print(put_text)

        put_url=put_telegraph(title=f"{keywords} 作品集", md_text=put_text)
        await client.send_message(chat_id=message.chat.id, text=put_url)



    except Exception as e:
        print(f"标记8 {e}")
        sys.stdout.flush()
        await client.send_message(chat_id=message.chat.id, text="发布失败")
        del_path(keywords)
        return

    del_path(keywords)
    return


