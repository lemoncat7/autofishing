'''
Description: 
version: 
Author: 莫邪
Date: 2023-03-19 15:57:17
LastEditors: 莫邪
LastEditTime: 2023-03-20 23:41:13
'''
# -*- coding: utf8 -*-

import win32gui
import win32api
import win32con
from pynput import keyboard 

CodeKey = {
  '\\x01': chr(1),
  '\\x03': chr(3),
  '\\x16': chr(22)
}

def find_sorftware_handle(class_name = None, title = None):
  handle = None
  if class_name:
    handle = win32gui.FindWindow(class_name, None)
  elif title:
    handle = win32gui.FindWindow(None, title)
  return handle

def set_sorftware_foreground(title = None):
  if not title:
    return False, None
  handle = find_sorftware_handle(title=title)
  if not handle:
    return False, None
  win32gui.SetForegroundWindow(handle)
  return True, handle

def get_current_title():
  # 获取活动窗口句柄
  handle = win32gui.GetForegroundWindow()
  if handle:
    # 获取窗口标题
    return win32gui.GetWindowText(handle)
  return '为获取到当前窗口名'

  
