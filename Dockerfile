FROM ubuntu

RUN apt-get update
RUN apt-get install sudo
RUN sudo apt-get update
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN echo 'Asia/Shanghai' >/etc/timezone
RUN apt-get install wget -y
RUN apt-get install git -y
RUN apt-get install curl -y
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN sudo apt-get install python3-distutils -y
RUN python3 get-pip.py

RUN apt install tzdata -y
RUN apt-get install aria2 -y



RUN mkdir /root/.aria2
COPY config /root/.aria2/

COPY root /

RUN pip3 install -r requirements.txt

#COPY bot /bot

RUN sudo chmod 777 /root/.aria2/
RUN sudo chmod 777 /rclone
RUN mv /rclone /usr/bin/

CMD wget https://raw.githubusercontent.com/winkxx/new_bot/main/start.sh  && chmod 0777 start.sh && bash start.sh
