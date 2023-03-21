'''
Description: 
version: 
Author: 莫邪
Date: 2023-03-21 14:35:10
LastEditors: 莫邪
LastEditTime: 2023-03-21 14:35:32
'''
# hooks/hook-pydirectinput.py

from PyInstaller.utils.hooks import collect_submodules

hiddenimports = collect_submodules('pydirectinput')
