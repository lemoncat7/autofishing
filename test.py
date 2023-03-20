'''
Description: 
version: 
Author: 莫邪
Date: 2023-03-19 17:25:14
LastEditors: 莫邪
LastEditTime: 2023-03-19 18:34:14
'''
from pynput import keyboard, mouse
byte = '16'
b = bytes.fromhex(byte)
print(b)
c = chr(b[0])
print(c)
kb = keyboard.Controller()
kb.press('\x16')
