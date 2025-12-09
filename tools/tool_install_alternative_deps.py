# -*- coding: utf-8 -*-
from .base import BaseTool
from .base import PrintUtils,CmdTask,FileUtils,AptUtils,ChooseTask
from .base import osversion,osarch
from .base import run_tool_file

class Tool(BaseTool):
    def __init__(self):
        self.name = "一键安装机器人额外依赖"
        self.type = BaseTool.TYPE_INSTALL
        self.author = 'VolkanoLiu'

    def install_alternative_deps(self):
        PrintUtils.print_info("开始安装机器人额外依赖...")
        PrintUtils.print_info("开始安装package.xml依赖...")
        PrintUtils.print_info("开始安装gstreamer...")
        PrintUtils.print_info("开始安装mosquitto...")
        PrintUtils.print_info("开始安装mediamtx...")

    def run(self):
        self.install_alternative_deps()
