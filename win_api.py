'''
Description: 
version: 
Author: 莫邪
Date: 2023-03-16 15:45:41
LastEditors: 莫邪
LastEditTime: 2023-03-16 17:56:03
'''
# -*- coding: utf-8 -*-
import win32api
import win32con
import win32gui
import time

def GetSorftHindle(title, func = None):
  handle = win32gui.FindWindow(None, title)
  if func:
    if handle:
      func(5, 'get sorftware handle: %d'%(handle))
    else:
      func(3, 'get sorftware handle: %d'%(handle))
  return handle


class StepNode():
  key_word = None
  func = None
  next = None
  timec = None
  def __init__(self, key, timec, func, *argv):
    if key.startswith('\''):
      self.key_word = key.replace('\'','')
    elif key.startswith('Button'):
      self.key_word = key.replace('Button.','鼠标')
    else:
      self.key_word = key[key.find('.') + 1:]
    self.timec = timec
    self.func = func
    self.argv = argv

  def exec(self):
    time.sleep(self.timec)
    self.func(*self.argv)
    if self.next:
      self.next.exec()
  
  def show(self):
    s = self.key_word
    if self.next:
      if len(s):
        s += ' -> '
      s += self.next.show()
    return s

class StepNodeList():
  step = None
  start = False
  current_time = None
  def push_back(self, key, func, *args):
    now = time.time()
    if not self.step:
      self.step = StepNode(key, now - self.current_time, func, *args)
      return
    step = self.step
    while step.next:
      step = step.next
    step.next = StepNode(key, now - self.current_time,func, *args)
    self.current_time = now
  
  def exec(self):
    if self.step:
      self.step.exec()
  
  def show(self):
    if self.step:
      return self.step.show()
  
  def clear(self):
    if self.step:
      self.step = None
  
  def record(self) :
    self.current_time = time.time()
