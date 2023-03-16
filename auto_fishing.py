'''
Description: 
version: 
Author: 莫邪
Date: 2023-03-16 10:58:33
LastEditors: 莫邪
LastEditTime: 2023-03-16 18:43:38
'''
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore
from datetime import datetime
from win_api import *
import keyhot

class MainWindow(QtWidgets.QWidget):
  __log = 5
  __log_type = {5:'debug', '4':'info', 3:'warning', 2:'error', 1:'fatal'}
  step_list = StepNodeList
  def __init__(self, parent = None):
    super(MainWindow, self).__init__(parent)
    self.__ui__()
    self.__conn__()
  def __get_time(self):
    now = datetime.now()
    return now.strftime("%m/%d %I:%M:%S")

  def __ui__(self):
    self.resize(300,450)
    self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
    layout = QtWidgets.QVBoxLayout()
    content_layout = QtWidgets.QSplitter(QtCore.Qt.Vertical)
    up_wid = QtWidgets.QWidget()
    up_wid.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    up_layout = QtWidgets.QVBoxLayout()
    up_label = QtWidgets.QLabel('日志:')
    log_text = QtWidgets.QTextEdit('----log level: %s----'%(self.__log_type[self.__log]), self)
    log_text.setReadOnly(True)
    log_text.setObjectName('log')
    up_layout.addWidget(up_label)
    up_layout.addWidget(log_text)
    up_wid.setLayout(up_layout)
    down_wid = QtWidgets.QWidget()
    down_layout = QtWidgets.QVBoxLayout()
    down_label = QtWidgets.QLabel('模拟路径列表:')
    self.list_view = QtWidgets.QListView(self)
    model = QtGui.QStandardItemModel()
    model.setHorizontalHeaderLabels(['Column 1'])
    self.list_view.setModel(model)
    self.list_view.setSelectionMode(QtWidgets.QListView.MultiSelection)
    down_layout.addWidget(down_label)
    down_layout.addWidget(self.list_view)
    down_wid.setLayout(down_layout)
    content_layout.addWidget(up_wid)
    content_layout.addWidget(down_wid)
    b_layout = QtWidgets.QHBoxLayout()
    quit = QtWidgets.QPushButton('exit', self)
    quit.setObjectName('exit')
    quit.hide()
    simulation = QtWidgets.QPushButton('模拟', self)
    simulation.setObjectName('simulation')
    run = QtWidgets.QPushButton('运行', self)
    run.setObjectName('run')
    b_layout.addWidget(quit)
    b_layout.addStretch(1)
    b_layout.addWidget(simulation)
    b_layout.addWidget(run)
    layout.addWidget(content_layout)
    layout.addLayout(b_layout)
    self.setLayout(layout)

  def __debug(self, log_level, text=''):
    if log_level >= 5:
      self.findChild(QtWidgets.QTextEdit, 'log').append('%s <font color="orange">DEBUG</font> %s'%(self.__get_time(),text))
  
  def __info(self, log_level, text=''):
    if log_level >= 4:
      self.findChild(QtWidgets.QTextEdit, 'log').append('%s <font color="blue">INFO</font> %s'%(self.__get_time(),text))
  
  def __warning(self, log_level, text=''):
    if log_level >= 3:# 创建文本格式对象
      self.findChild(QtWidgets.QTextEdit, 'log').append('%s <font color="yellow">WARNING</font> <b>%s</b>'%(self.__get_time(),text))
  
  def __error(self, log_level, text=''):
    if log_level >= 2:
      self.findChild(QtWidgets.QTextEdit, 'log').append('%s <font color="red">ERROR</font> <b>%s</b>'%(self.__get_time(),text))
  
  def __fatal(self, log_level, text=''):
    if log_level >= 1:
      self.findChild(QtWidgets.QTextEdit, 'log').append('%s FATAL %s'%(self.__get_time(),text))

  def Log(self, type, text):
    if type == 5:
      self.__debug(self.__log, text)
    elif type == 4:
      self.__info(self.__log, text)
    elif type == 3:
      self.__warning(self.__log, text)
    elif type == 2:
      self.__error(self.__log, text)
    elif type == 1:
      self.__fatal(self.__log, text)
    
  def __add_item__(self, text):
    # 添加列表项
    item = QtGui.QStandardItem(text)
    item.setCheckable(True)
    # 设置数据模型
    self.list_view.model().appendRow([item])
    self.Log(4, 'have added simulation path: %s'%text)

  def __conn__(self):
    self.findChild(QtWidgets.QPushButton, 'simulation').clicked.connect(self.add_simulation_path)
    self.findChild(QtWidgets.QPushButton, 'exit').clicked.connect(exit)
  
  def mouse_move_handler(self, x, y):
    self.Log(5, "Mouse move event: %d %d"%(x, y))
    self.step_list.push_back('mouse move', keyhot.MousePosition, x, y)

  def keyboard_event_handler(self, event):
      self.Log(5, "event: %s"%event)

  def add_simulation_path(self):
    self.Log(4, 'start to simulation path')
    hwnd = GetSorftHindle('记事本', self.Log)
    if not hwnd:
      self.Log(2, 'sorftware handle get error')
    self.__add_item__('path')


if __name__ == "__main__":
  app = QtWidgets.QApplication([])
  window = MainWindow()
  window.show()
  app.exec_()