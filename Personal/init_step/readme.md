## 登陆Wi-Fi的自动化脚步和登陆openvpn脚本，安装依赖并初始化
1. 准备环境
    brew install openvpn expect oath-toolkit
    python3 -m venv ~/venv
    source ~/venv/bin/activate
    pip install -r ~/Documents/Code/DBA/Personal/init_step/requirements.txt
    playwright install
    cp -r ~/Documents/Code/DBA/Personal/init_step/.login_script ~/
2. 设置每天早上5点定时执行
    crontab -e
0 5 * * * source ~/venv/bin/activate && python3 ~/.login_script/playwright_login.py
0 5 * * * ~/.login_script/openvpn/vpn-auto.exp  >> /tmp/exec_openvpn.log 2>&1
45 19  * * * source ~/venv/bin/activate && python3 ~/.login_script/playwright_login.py

## 上面两个的脚步的运行命令加入到别名中
1.  ~/.zshrc 一些命令的别名
    cp ~/Documents/Code/DBA/Personal/init_step/.zshrc ~/
    source ~/.zshrc
2. ~/.ssh/id_vps_ed25519 个人vps的密钥
    cp ~/Documents/Code/DBA/Personal/init_step/id_vps_ed25519 ~/.ssh/
    chmod 600 ~/.ssh/id_vps_ed25519

## 设置全局的git用户名和邮箱
git config --global user.name "peder"
git config --global user.email "peder"

## macbook 合盖不休眠命令
sudo pmset -a disablesleep 1

## 添加hosts
cat <<EOF | sudo tee -a /etc/hosts > /dev/null
103.84.45.133 navi.sihai.com
18.167.141.17 gitlab.sihai.com
47.52.105.89 dba.grafana.idc.com grafana.idc.com
16.162.233.179 jp-uat-grafana1.obgops.com dbauat.grafana.idc.com
EOF

