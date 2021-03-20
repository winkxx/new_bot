#!/bin/bash


touch /root/.aria2/aria2.session
chmod 0777 /root/.aria2/ -R

mkdir /.config/
mkdir /.config/rclone
touch /.config/rclone/rclone.conf
echo "$Rclone" >>/.config/rclone/rclone.conf
wget git.io/tracker.sh
chmod 0777 /tracker.sh
/bin/bash tracker.sh "/root/.aria2/aria2.conf"

git clone https://github.com/666wcy/new_bot
mkdir /bot/
mv /new_bot/bot/* /bot/
chmod 0777 /bot/ -R
rm -rf /new_bot

nohup aria2c --conf-path=/root/.aria2/aria2.conf --rpc-listen-port=8080 --rpc-secret=$Aria2_secret &
nohup python3 /bot/web.py &

python3 /bot/main.py