# 自定义 alias 配置
alias myvps="ssh -p 3952 -i ~/.ssh/id_vps_ed25519 root@141.98.199.137"
alias ll="ls -lh"
alias tailf="tail -f"
alias conwifi="source ~/venv/bin/activate && python3 ~/.login_script/playwright_login.py"
alias offwifi="source ~/venv/bin/activate && python3 ~/.login_script/playwright_login.py logoff"
alias conopenvpn="~/.login_script/openvpn/vpn-auto.exp"
alias aa="conopenvpn&conwifi"
# 结束 alias 配置