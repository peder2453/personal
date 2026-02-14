
从本地同步文件到远程
-a 保留文件信息
-v 显示

rsync -avz -e "ssh -p 3952 -i ~/.ssh/id_vps_ed25519" /Volumes/SN5000/sandrea照片完整备份 root@141.98.199.137:/data/nextcloud-docker/nextcloud/data/thomas/files/AlanSeagate