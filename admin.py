'''
Description: 
version: 
Author: 莫邪
Date: 2023-03-19 15:57:16
LastEditors: 莫邪
LastEditTime: 2023-03-19 22:03:40
'''
# -*- coding: utf-8 -*-
import os
import platform
import sys
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def start_sorftware():    
#   if not is_admin():
#       # 如果当前不是管理员权限，提示用户以管理员身份运行
#       ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
#       # sys.exit()
#       print("is ready start with admin")
    # if platform.system() == 'Windows':
    #     os.system('runas /user:Administrator cmd')
    pass