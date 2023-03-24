'''
Description: 
version: 
Author: 莫邪
Date: 2023-03-19 01:05:36
LastEditors: 莫邪
LastEditTime: 2023-03-24 17:14:41
'''
# -*- coding: utf-8 -*-
from auto_app import MyApp
from pynput import keyboard, mouse
import time, os
import admin
import queue
import traceback
import win32
import threading
import pydirectinput
import re
import ctypes
PROCESS_PER_MONITOR_DPI_AWARE = 2
ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)


class AutoFish(MyApp):
  lisenter_status = False
  run_status = False
  # 创建pynput.keyboard.Controller和pynput.mouse.Controller对象 虚拟控制对象
  kb = keyboard.Controller()
  mc = mouse.Controller()
  dir = None
  script_path = None
  script_queue = queue.Queue()
  ctime = 0
  def __init__(self, perant = None):  
    self.dir = self.get_file('script')
    super(AutoFish, self).__init__()
    thread = threading.Thread(target=self.Lisenter)
    thread.start()
    self.root.attributes("-topmost", True)
    self.root.mainloop()

  def on_closing(self):
    self.lisenter_status = False
    self.run_status = False
    return super().on_closing()
  
  def __interval_time(self):
    t = int(time.time() * 1000)
    itime = t - self.ctime
    self.ctime = t
    return itime

  def simu_click(self):
    self.Log('''参数格式: 
keyboard, 300, w, 10
类型, 时间间隔, 输入参数, 次数

类型
  keyboard       键盘
  move           鼠标移动
  rotation       旋转视角
  click          鼠标
时间间隔 ms
输入参数
  [a-zA-Z0-9]    字母
  left/right     鼠标左键/右键
  x, y           坐标 x, y
次数''')
    os.startfile(self.dir)
    return super().simu_click()
    
  def flush_listBox(self):
    self.path_map.clear()
    self.listbox.delete(0, 'end')
    # 遍历目录树，获取所有文件路径
    for root, dirs, files in os.walk(self.dir):
        for file in files:
            file_path = os.path.join(root, file)
            self.path_map[file] = file_path
            # self.listbox.insert('end', file)
    path = self.get_file('list_list')
    tmp_map = {}
    with open(path, 'r', encoding='utf-8') as f:
      for line in f.readlines():
          if line.find(',') == -1:
            continue
          self.Log('init list box get line %s' % (line.strip('\n')), 6)
          key, enable, value = line.strip('\n').split(',')
          if key not in self.path_map.keys():
            continue
          tmp_map[key] = value
          self.listbox.insert('end', key)
          if enable == 'True':
            self.listbox.select_set('end',self.listbox.size() - 1)
    for key, value in self.path_map.items():
      if key not in tmp_map.keys():
        self.listbox.insert('end', key)
    return super().flush_listBox()
  
  def generate_script(self, event = None):
    self.script_flag = not self.script_flag
    if self.script_flag:
      while not self.script_queue.empty():
        self.script_queue.get()
    else: 
      key_map = {}
      script_file = os.path.join(self.dir, 'script%d'%(self.listbox.size() + 1))
      with open(script_file, 'w+', encoding='utf8') as f:
        while not self.script_queue.empty():
          list = self.script_queue.get()
          # 按键按下 如果是长按需要记录连续次数
          if list[0] == 'press':
            if not list[2] in key_map:
              key_map[list[2]] = (list[1], 1)
            else:
              key_map[list[2]] = (list[1], key_map[list[2]][1] + 1)
          elif list[0] == 'release':
            f.write('keyboard, %d, %s, %d\n'%(key_map[list[2]][0], list[2].strip('\''), key_map[list[2]][1]))

          # elif list[0] == 'down':
          # elif list[0] == 'up':

    return super().generate_script(event)

  # 定义键盘事件回调函数
  def __on_press(self, key):
    # print('按下按键: {0}'.format(key.vk))
    # key_value = 0
    # if hasattr(key, 'vk'):  # 普通按键
    #     key_value = key.vk
    # else:
    #     # 如果按键不是单个字符，则将Key对象转换为对应的键码
    #     key_value = keyboard.Key[key.name]
    # if (key == keyboard.Key.esc):
    #   self.lisenter_status = False
    # else:
    if self.script_flag:
      self.script_queue.put(['press', self.__interval_time(), str(key)])
    pass

  def __on_release(self, key):
    # print('松开按键: {0}'.format(key))
    # key_value = 0
    # if hasattr(key, 'vk'):  # 普通按键
    #     key_value = key.vk
    # else:
    #     # 如果按键不是单个字符，则将Key对象转换为对应的键码
    #     key_value = keyboard.Key[key.name]
    if (key == keyboard.Key.esc and self.run_status):
      self.Log('等待线程停止...',4)
      self.run_status = False
    # else:
    if self.script_flag:
      self.script_queue.put(['release', self.__interval_time(), str(key)])
    pass

  def __mouse_in_win(self,x, y):
    self.root.update()
    cx = self.root.winfo_x()
    cy = self.root.winfo_y()
    width = self.root.winfo_width()
    height = self.root.winfo_height()
    print(x, y)
    print(cx, cy, width, height, x > cx and x < cx + width and y > cy and y < cy + 70)
    return x > cx and x < cx + width and y > cy and y < cy + 70

  # 定义鼠标事件回调函数
  def __on_move(self, x, y):
    # print('鼠标移动到 ({0}, {1})'.format(x, y))
    # self.script_queue.put(['move', self.__interval_time(), *self.mc.position])
    # cx = self.root.winfo_x()
    # cy = self.root.winfo_y()
    # width = self.root.winfo_width()
    # height = self.root.winfo_height()
    # print(x, y)
    # print(cx, cy, width, height)
    # if (y > cy + height or y < cy) and (x < cx or x > cx + width):
    
    if self.xy_status:
      self.xy.config(text='(%d, %d)'%(x, y))
      # self.title.config(text='窗口 %s'%(win32.get_current_title()))
      # self.Log('获取当前窗口 %s'%(win32.get_current_title()))
    pass

  def __on_click(self, x, y, button, pressed):
    if pressed :
      self.xy_status = False
    elif not pressed:
      self.xy_status = True
      if self.title_flag:
        self.Log('获取当前窗口 %s'%(win32.get_current_title()))
    if self.script_flag:
      if pressed:
       # print('鼠标 {0} 按下在 ({1}, {2})'.format(button, x, y))
        self.script_queue.put(['down', self.__interval_time(), button, x, y])
      else:
      #   # print('鼠标 {0} 松开在 ({1}, {2})'.format(button, x, y))
        self.script_queue.put(['up', self.__interval_time(), button, x, y])
    pass
          
  # 开始监听鼠标和键盘事件
  def Lisenter(self, path = None):
    # while not self.script_queue.empty():
    #   self.script_queue.get()
    # import time
    # times = 5
    # while times > 0:
    #   self.Log('倒计时: %d'%times)
    #   time.sleep(1)
    #   times -= 1
    # self.Log('按下 ESC 停止录制脚本路线')
    # self.script_path = os.path.join(self.dir, path)
    self.lisenter_status = True
    # self.ctime = int(time.time() * 1000)
    k_listener = keyboard.Listener(on_press=self.__on_press, on_release=self.__on_release)
    m_listener = mouse.Listener(on_move=self.__on_move, on_click=self.__on_click)
    k_listener.start()
    m_listener.start()
    while self.lisenter_status:
      time.sleep(0.5)
    k_listener.stop()
    m_listener.stop()
    # self.write_script(self.script_path)
    return super().Lisenter()
  
  def write_script(self, filename):
    try:
      if not os.path.exists(self.dir):
        os.mkdir(self.dir)
      with open(filename, 'w+', encoding='utf8') as f:
        while not self.script_queue.empty():
          list = self.script_queue.get()
          for word in list:
            f.write(str(word).strip('\'') + ',')
          f.write('\n')
    except Exception as e:
      self.Log('write script %s'%e, 3)
  
  def Exec(self, args):
    ''':param: press, time, word, times
       :param: release,time, word, times
       :param: move,time, x, y, times
       :param: rotation,time, x, y, times
       :param: up, time, Button.left/Button.right, times
       :param: down, time, Button.left/Button.right, times'''
       
    try:
      times = -1 
      list = args.strip('\n')
      list = list.split(',')
      for l in list:
        if l == '':
          list.remove(l)
      while((times > 0 or times == -1) and self.run_status):
        # 移动
        if (list[0] == 'move'):
          if times == -1:
            if len(list) >= 5:
              times = int(list[4])
            else:
                times = 1
          self.mc.position = (list[2],list[3])
          # self.mc.move(int(list[2]),int(list[3]))
        # 旋转
        elif (list[0] == 'rotation'):
          if times == -1:
            if len(list) >= 5:
              times = int(list[4])
            else:
                times = 1
          pydirectinput.moveRel(xOffset=int(list[2]),yOffset=int(list[3]),duration=0.4,relative=True)
          # self.game_cxy = (list[2],list[3])
        # 按键
        elif (list[0] == 'press' or list[0] == 'keyboard'):
          if times == -1:
            if len(list) >= 4:
              times = int(list[3])
            else:
              times = 1
          # 检查字符串是否以 'Key.' 开头
          print(list)
          self.Log('exec press key %s'%list[2],6)
          if re.search('Key.', list[2] ) or not re.search('[0-9]', list[2]):
            # 获取键的值
            print(list[2])
            if not re.search('Key.', list[2]):
              key = getattr(keyboard.Key, list[2].strip())
              print(1, key)
            else:
              key = getattr(keyboard.Key, list[2].split('.')[-1])
              print(2, key)
            print(3, key)
          elif list[2].strip().startswith('\\x'):
            # key = bytes.fromhex(list[2][2:])
            key = win32.CodeKey[list[2].strip()]
          else:
            # 否则，将字符串作为键名直接传递
            key = list[2].strip()
          print(key)
          self.kb.press(key)
          if list[0] == 'keyboard' and times == 1:
            self.kb.release(key)
        # 释放按键
        elif (list[0] == 'release'):
          if times == -1:
            if len(list) >= 4:
              times = int(list[3])
            else:
                times = 1

          # 检查字符串是否以 'Key.' 开头
          self.Log('exec release key %s'%list[2],6)
          if list[2].startswith('Key.'):
            # 获取键的值
            key = getattr(keyboard.Key, list[2].split('.')[-1])
          elif not re.search('[0-9]', list[2]):
            key = getattr(keyboard.Key, list[2].strip())
          elif list[2].startswith('\\x'):
            # key = bytes.fromhex(list[2][2:])
            key = win32.CodeKey[list[2].strip()]
          else:
            # 否则，将字符串作为键名直接传递
            key = list[2].strip()
          self.kb.release(key)
        # 按下鼠标
        elif (list[0] == 'up'):
          if times == -1:
            if len(list) >= 4:
              times = int(list[3])
            else:
                times = 1
          if 'left' in list[2]:
            self.mc.release(mouse.Button.left)
          elif 'right' in list[2]:
            self.mc.release(mouse.Button.right)
        # 抬起鼠标
        elif (list[0] == 'down' or list[0] == 'click'):
          if times == -1:
            if len(list) >= 4:
              times = int(list[3])
            else:
                times = 1
          if 'left' in list[2]:
            self.mc.press(mouse.Button.left)
            if list[0] == 'click' and times == 1:
              self.mc.release(mouse.Button.left)
            # pydirectinput.click()
          elif 'right' in list[2]:
            self.mc.press(mouse.Button.right)
            if list[0] == 'click' and times == 1:
              self.mc.release(mouse.Button.right)
        time.sleep(float(list[1]) * 0.001)
        self.Log('times %d , type %s'%(times, list[0]), 6)
        times = times - 1 if times > 0 else times
    except Exception as e:
      self.Log('exec error %s' % e, 3)
      traceback.print_exc()

  def __run_threading(self, selections):
    try:
      time.sleep(0.5)
      self.run_status = True
      self.Log('按 ESC 键可退出运行脚本')
      ok, h = win32.set_sorftware_foreground(self.process)
      for i in range(0, int(self.loop)):
        self.Log('第 %d 次循环'%(i + 1))
        for selection in selections:
          path = self.path_map[self.listbox.get(selection)]
          self.Log('正在运行当前script :%s'%self.listbox.get(selection),5)
          self.Log('run item %s, path %s' %(self.listbox.get(selection), path), 6)
          lines = open(os.path.join(self.dir, path), 'r', encoding='utf8').readlines()
          for line in lines:
            if not self.run_status:
              break
            self.Exec(line)
          if not self.run_status:
            break
        if not self.run_status:
          self.Log('已终止运行脚本',5)
          break
      self.Log('script 运行结束',5)
    except Exception as e:
      self.Log('run threading %s'%e, 3)


  def run(self, even=None):
    try:
      ok, h = win32.set_sorftware_foreground(self.process)
      if ok:
        self.Log('run get handle %s'%h,5)
      else:
        self.Log('run cannot get handle %s start global linstener',4)
      selections = self.listbox.curselection()
      self.Log('start to run the scripts', 5)
      self.Log('在显示结束前请勿触碰其他按键', 4)
      threading.Thread(target=self.__run_threading, args=(selections,)).start()
    except Exception as e:
      self.Log('run %s'%e, 3)
    return super().run(even)

  def remove_script(self):
    try:
      if not os.path.exists(self.dir):
          os.mkdir(self.dir)
      file_list = []
    # 遍历文件夹中的所有文件
      for filename in os.listdir(self.dir):
        # 获取文件名
        file_list.append(filename)
      print(file_list)
      for key, value in self.path_map.items():
        file_list.remove(value)
      for file in file_list:
        self.Log('remove script %s has removed'%file, 5)
        os.remove(os.path.join(self.dir, file))
      return super().remove_script()
    except Exception as e: 
      self.Log('remove script %s'%e, 3)

if __name__ == "__main__":
  admin.start_sorftware()
  app = AutoFish()
  