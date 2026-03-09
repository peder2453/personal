
1. 回复机器人的守护进程

```shell
vim /etc/systemd/system/replybot.service
```


```
[Unit]
Description=Telegram Reply Bot
After=network.target

[Service]
Type=simple
WorkingDirectory=/data/scripts/regulary_send_message
ExecStart=/usr/bin/python /data/scripts/regulary_send_message/reply_bot.py
Restart=always
RestartSec=5

# 防止日志丢失
StandardOutput=append:/var/log/replybot.log
StandardError=append:/var/log/replybot.log

[Install]
WantedBy=multi-user.target
```


systemctl daemon-reload

systemctl start replybot

systemctl status replybot

1. 回复机器人守护进程

cat > /etc/supervisord.d/replybot.ini <<EOF
[program:replybot]
command=/usr/bin/python /data/scripts/regulary_send_message/reply_bot.py
directory=/data/scripts/regulary_send_message
autostart=true
autorestart=true
startsecs=5

stderr_logfile=/var/log/replybot.err.log
stdout_logfile=/var/log/replybot.out.log

user=root
EOF


cat > /etc/supervisord.d/tg_scheduler.py.ini <<EOF
[program:tg_scheduler]
command=/usr/bin/python /data/scripts/regulary_send_message/tg_scheduler.py
directory=/data/scripts/regulary_send_message
autostart=true
autorestart=true
startsecs=5

stderr_logfile=/var/log/tg_scheduler.err.log
stdout_logfile=/var/log/tg_scheduler.out.log

user=root
EOF