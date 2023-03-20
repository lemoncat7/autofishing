# -*- coding: utf-8 -*-

import tkinter as tk
from admin import *
from enum import Enum
from datetime import datetime
import configparser
import threading
import win32


class Control(Enum):
  LOG_LABEL, LOG, LIST_LABEL, LIST, SIMU_RUN=range(5)

class LogLevel(Enum):
  NONE,NOWRITE, FATAL, ERROR, WARNING, INFO, DEBUG=range(7)

class MyApp:
  log_map = {'NOWRITE':LogLevel.NOWRITE,
             'NONE':LogLevel.NONE, 
             'FALTAL':LogLevel.FATAL, 
             'ERROR':LogLevel.ERROR, 
             'WARING':LogLevel.WARNING, 
             'INFO':LogLevel.INFO, 
             'DEBUG':LogLevel.DEBUG}
  log_level = LogLevel.DEBUG
  path_map = {}
  handle = None
  model = None
  def __init__(self):
    self.root = tk.Tk()
    # 设置退出事件的回调函数
    self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    self.__resize()
    self.__layout()
    self.__configure()
    self.__flush()
    # self.root.mainloop()

  def __layout(self):
    '''布局'''
    l1 = tk.Label(self.root, text='日志')
    l1.grid(row=0, column=0, sticky='w')
    self.title = tk.Label(self.root, text='窗口 ', width=10)
    self.title.grid(row=0, column=1, sticky='e')
    self.xy = tk.Label(self.root, text='(x, y)', width=10)
    self.xy.grid(row=0, column=2, sticky='e')
    self.log = tk.Text(self.root)
    self.log.grid(row=1, column=0, columnspan=3)
    # self.log.config(state='readonly')
    self.log.tag_config("red", foreground="red")
    self.log.tag_config("blue", foreground="blue")
    self.log.tag_config("orange", foreground="orange")
    self.log.tag_config("yellow", foreground="yellow")
    self.log.tag_config("gray", foreground="gray")
    l2 = tk.Label(self.root, text='模拟路径')
    l2.grid(row=2, column=0, sticky='w')
    # 创建一个 Listbox 控件
    self.listbox = tk.Listbox(self.root,selectmode=tk.MULTIPLE, height=3)
    # 设置 Listbox 的边框宽度
    self.listbox.config(highlightthickness=0)
    self.listbox.grid(row=3, column=0, columnspan=3, sticky="nswe")
    self.listbox.bind('<Button-3>', self.__listbox_edit)
    self.listbox.bind('<<ListboxSelect>>', self.__save_path_map)
    self.doubel_l = tk.Label(self.root, text='S/F')
    self.doubel_l.bind("<Button-1>", self.__setting)
    self.doubel_l.bind("<Button-3>", self.__flush)
    self.doubel_l.grid(row=4,column=0)
    # 创建 button 控件
    self.simu = tk.Button(self.root, text="脚本", command=self.simu_click)
    self.simu.grid(row=4, column=1, sticky="we")
    self.run = tk.Button(self.root, text="运行", command=self.run)
    self.run.grid(row=4, column=2, sticky="we")

  def __resize(self):
    # 计算窗口位置
    screen_width = self.root.winfo_screenwidth()
    screen_height = self.root.winfo_screenheight()
    x = int((screen_width - 200) / 2)
    y = int((screen_height - 350) / 2)

    # 设置窗口大小和位置
    # self.root.geometry("200x350+{}+{}".format(x, y))
    self.root.maxsize(width=300, height=450)

  def __init(self):
    # self.Log("LOG< %s >"%self.log_level.name)
    # self.__init_listbox()
    self.flush_listBox()
    pass

  def flush_listBox(self):
    self.__save_path_map()
    pass 
  
  def __init_listbox(self):
    try:
      path = self.get_file('list_list')
      if not os.path.exists(path):
        self.Log('list_list file does not exist',3)
        with open(path, 'w+', encoding='utf-8'):
          pass
      self.path_map.clear()
      self.listbox.delete(0, 'end')
      with open(path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
          if line.find(',') == -1:
            continue
          self.Log('init list box get line %s' % (line.strip('\n')), 6)
          key, enable, value = line.strip('\n').split(',')
          self.path_map[key] = value
          self.listbox.insert('end', key)
          if enable == 'True':
            self.listbox.select_set('end',self.listbox.size() - 1)
      self.remove_script()
    except Exception as e:
      self.Log('init listbox %s'%e, 3)

  def remove_script(self):
    pass

  def __get_time(self):
    now = datetime.now()
    return now.strftime("%m/%d %I:%M:%S ")
#===================================================日志功能================================================================
  def __write_log(self, text):
    self.log.insert(tk.END, text)
    self.log.insert(tk.END, '\n')
    self.log.see('end')

  def __debug(self, text):
    self.log.insert(tk.END, self.__get_time() )
    self.log.insert(tk.END, "DEBUG ", "orange")
    self.__write_log(text)

  def __info(self, text):
    self.log.insert(tk.END, self.__get_time())
    self.log.insert(tk.END, "INFO ", "blue")
    self.__write_log(text)

  def __warning(self, text):
    self.log.insert(tk.END, self.__get_time())
    self.log.insert(tk.END, "WARNING ", "yellow")
    self.__write_log(text)

  def __error(self, text):
    self.log.insert(tk.END, self.__get_time())
    self.log.insert(tk.END, "ERROR ", "red")
    self.__write_log(text)

  def __fatal(self, text):
    self.log.insert(tk.END, self.__get_time())
    self.log.insert(tk.END, "FATAL ", "gray")
    self.__write_log(text)

  def Log(self, text, level=LogLevel.NOWRITE):
    '''日志写入 level >> 0 NONE 1 NOWRITE 2 FATAL 3 ERROR 4 WARNING 5 INFO 6 DEBUG'''
    if (LogLevel.NOWRITE == self.log_level):
      pass
    if (level == LogLevel.FATAL.value):
      if(level <= self.log_level.value):
        self.__fatal(text)
    elif (level == LogLevel.ERROR.value):
      if (level <= self.log_level.value):
        self.__error(text)
    elif (level == LogLevel.WARNING.value): 
      if(level <= self.log_level.value):
        self.__warning(text)
    elif (level == LogLevel.INFO.value):
      if (level <= self.log_level.value):
        self.__info(text)
    elif (level == LogLevel.DEBUG.value):
      if (level <= self.log_level.value):
        self.__debug(text)
    else:
      self.__write_log(text)  

  def __configure(self):
    '''让行和列自适应窗口大小'''
    self.root.rowconfigure(Control.LOG_LABEL.value, minsize=5)
    self.root.rowconfigure(Control.LOG.value, minsize=50, weight=1)
    self.root.rowconfigure(Control.LIST_LABEL.value, minsize=5)
    self.root.rowconfigure(Control.LIST.value, minsize=150, weight=1)
    self.root.rowconfigure(Control.SIMU_RUN.value, minsize=50, weight=1)
    self.root.columnconfigure(0)
    self.root.columnconfigure(1, weight=1)
    self.root.columnconfigure(2, weight=1)

  def get_file(self, path = None):
    '''获取文件路径'''
    try:
      tmp_path = os.environ.get('TEMP')
      dir = os.path.join(tmp_path,'auto')
      if not os.path.exists(dir):
        os.mkdir(dir)
      if path:
        return os.path.join(dir, path)
      return dir
    except Exception as e:
      self.Log('get file %s'%e, 3)

  def __setting(self,event):
    '''设置功能（打开配置文件）'''
    conf_path = self.get_file('config.ini')
    self.Log('保存文件后，请右击左下角 S/F 以刷新配置')
    os.system("start notepad.exe {}".format(conf_path))

  def __flush(self, event = None):
    '''刷新配置'''
    try:
      self.Log('start to read config.ini', 5)
      conf_path = self.get_file('config.ini')
      if not os.path.exists(conf_path):
        with open(conf_path, 'w+', encoding='utf8') as f:
          f.write('''[settings]\nlog=INFO\nprocess=\nmodel=''')
      # 创建 ConfigParser 对象
      config = configparser.ConfigParser()
      # 读取配置文件
      config.read(conf_path, encoding='utf8')
      self.log_level = self.log_map[config.get('settings','log')]
      self.Log("read config log level: %s"%self.log_level.name, 5)
      self.process = config.get('settings','process')
      self.model = config.get('settings','model')
      self.Log("read config process: %s" % self.process, 5)
      # self.__save_path_map()
      self.__init()
    except Exception as e:
      self.Log("flush %s"%e, 3)
    pass

  def __save_path_map(self, event = None):
    '''保存路径文件'''
    if not len(self.path_map):
      return
    path = self.get_file('list_list')
    with open(path, 'w+', encoding='utf-8') as f:
      for index in range(self.listbox.size()):
        f.write('%s,%s,%s\n'%(self.listbox.get(index), \
                            self.listbox.select_includes(index), \
                              self.path_map[self.listbox.get(index)]))

  def simu_click(self):
    '''路径模拟 生成路径配置文件'''
    # thread = threading.Thread(target=self.__simulate)
    # thread.start()
    pass

  def Lisenter(self, path = None):
    pass

  def __simulate(self):
    try:
      win32.set_sorftware_foreground(self.process)
      self.Log('start to record', 5)
      option = '路径%d'%(len(self.path_map) + 1)
      path = 'path%d'%(len(self.path_map) + 1)
      self.Lisenter(path)
      self.path_map[option] = path
      self.Log('have restored the new path',5)
      self.listbox.insert(tk.END, option)
      self.listbox.select_set(self.listbox.size() - 1)
      self.__save_path_map()
    except Exception as e:
      self.Log('simulate %s'%e, 3)

  def __listbox_edit(self, event):
    path = self.get_file('list_list')
    self.Log('保存文件后，请右击左下角 S/F 以刷新配置')
    os.system("start notepad.exe {}".format(path))
    pass
  
  def on_closing(self):
    self.root.destroy()

  def run(self, even=None):
    self.Log('end to run the simulation path',6)
    pass

if __name__ == "__main__":
  app = MyApp()