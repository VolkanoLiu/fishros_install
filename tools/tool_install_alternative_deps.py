# -*- coding: utf-8 -*-
from .base import BaseTool
from .base import PrintUtils,CmdTask,FileUtils,AptUtils,ChooseTask
from .base import osversion,osarch
from .base import run_tool_file
import os

class Tool(BaseTool):
    def __init__(self):
        self.name = "一键安装机器人额外依赖"
        self.type = BaseTool.TYPE_INSTALL
        self.author = 'VolkanoLiu'

    def install_alternative_deps(self):
        PrintUtils.print_info("开始安装机器人额外依赖...")
        CmdTask("sudo apt update",os_command=True).run()

        PrintUtils.print_info("开始安装package.xml依赖...")
        CmdTask("rosdepc install --from-paths deps --ignore-src -r -y",os_command=True).run()

        PrintUtils.print_info("开始安装gstreamer...")
        CmdTask("sudo apt install libgstreamer-plugins-base1.0-dev libgstreamer-plugins-good1.0-dev libgstreamer-plugins-bad1.0-dev",os_command=True).run()

        PrintUtils.print_info("开始安装mosquitto...")
        CmdTask("sudo apt install mosquitto mosquitto-clients -y",os_command=True).run()
        mosquitto_conf_path = "/etc/mosquitto/conf.d/"
        mosquitto_conf_name = "default.conf"
        mosquitto_conf_path_full = os.path.join(mosquitto_conf_path, mosquitto_conf_name)
        conf = """# 监听本地地址和端口
listener 1883 0.0.0.0

# 密码验证
allow_anonymous true

# 密码文件路径
# password_file /etc/mosquitto/passwd

# 日志配置（可选）
# log_dest file /var/log/mosquitto/mosquitto.log
# log_type all
"""
        if FileUtils.exists(mosquitto_conf_path_full):
            user_input = input("检测到已存在的mosquitto配置文件，是否替换该文件[y/N]？")
            if user_input.lower() in ['y', 'yes']:
                FileUtils.delete(mosquitto_conf_path_full)
                FileUtils.new(path=mosquitto_conf_path, name=mosquitto_conf_name, data=conf)
        CmdTask("sudo systemctl restart mosquitto.service").run()

        PrintUtils.print_info("开始安装mediamtx...")
        if osarch == "amd64":
            CmdTask('wget https://github.com/bluenviron/mediamtx/releases/download/v1.15.5/mediamtx_v1.15.5_linux_amd64.tar.gz -O /tmp/mediamtx.tar.gz',os_command=True).run()
        elif osarch == "arm64":
            CmdTask('wget https://github.com/bluenviron/mediamtx/releases/download/v1.15.5/mediamtx_v1.15.5_linux_arm64.tar.gz -O /tmp/mediamtx.tar.gz',os_command=True).run()
        user_homes = FileUtils.getusershome()
        user = FileUtils.getusers()[0]
        user_home = user_homes[0]
        CmdTask("mkdir -p {}mediamtx".format(user_home)).run()
        CmdTask("tar -xzvf /tmp/mediamtx.tar.gz -C {}mediamtx".format(user_home)).run()
        
        service_path = "/etc/systemd/system/"
        mediamtx_service_name = "mediamtx.service"
        mediamtx_service_path_full = os.path.join(service_path, mediamtx_service_name)
        service = f"""[Unit]
Description=MediaMTX RTSP/RTMP/HLS/WebRTC Server
Documentation=https://github.com/bluenviron/mediamtx
After=network.target

[Service]
Type=simple
ExecStart={user_home}mediamtx/mediamtx {user_home}mediamtx/mediamtx.yml
WorkingDirectory={user_home}mediamtx

# 运行用户（替换为实际用户名）
User={user}
Group={user}

# 重启策略
Restart=on-failure
RestartSec=5

# 环境变量（可选）
Environment="MEDIAMTX_CONFIG={user_home}mediamtx/mediamtx.yml"

# 日志
StandardOutput=journal
StandardError=journal
SyslogIdentifier=mediamtx

# 安全设置（可选，增强安全性）
# NoNewPrivileges=true
# PrivateTmp=true

[Install]
WantedBy=multi-user.target
"""
        if FileUtils.exists(mediamtx_service_path_full):
            FileUtils.delete(mediamtx_service_path_full)
        FileUtils.new(path=service_path, name=mediamtx_service_name, data=service)
        CmdTask("sudo systemctl enable mediamtx.service").run()
        CmdTask("sudo systemctl restart mediamtx.service").run()

    def run(self):
        self.install_alternative_deps()
