'''
Description: 
version: 
Author: 莫邪
Date: 2022-11-30 13:46:36
LastEditors: 莫邪
LastEditTime: 2022-12-07 09:24:43
'''
# -*- coding: utf-8 -*-

import pynput.mouse as mouse
import pynput.keyboard as keyboard
import sys,os, time

class EventNode():
  next_ = None
  func_ = None

  def __init__(self, func, next = None) -> None:
    self.func_ = func
    self.next_ = next
    pass

  def exec(self,*args):
    if self.func_:
      self.func_(*args)
      self._next(*args)

  def _next(self, *args):
    if self.next_:
      self.next_.exec(*args)
      
class EventList():
  funcs_ = None
  def push_back(self,func):
    if not self.funcs_:
      self.funcs_ = EventNode(func)
      return
    funcs = self.funcs_
    while funcs.next_:
      funcs = funcs.next_
    funcs.next_ = EventNode(func)
  
  def exec(self, *args):
    if self.funcs_:
      self.funcs_.exec(*args)

def MousePosition(x, y):
  ctr = mouse.Controller()
  ctr.position = (int(x), int(y))
  return ctr

def MouseMove(x, y):
  ctr = mouse.Controller()
  ctr.move(int(x), int(y))
  return ctr

def MouseScroll(x, y, dx, dy):
  ctr = MousePosition(x, y)
  ctr.scroll(int(dx), int(dy))

def MouseClick(x, y, mouse_type, times = 1):
  # print(func, x, y)
  ctr = MousePosition(x, y)
  ctr.click(mouse_type, times)

def MousePress(x, y, mouse_type):
  # print(func, x, y)
  ctr = MousePosition(x, y)
  ctr.press(mouse_type)

def MouseRelease(x, y, mouse_type):
  # print(func, x, y)
  ctr = MousePosition(x, y)
  ctr.release(mouse_type)

def KeyPress(key):
  ctr = keyboard.Controller()
  ctr.press(key)

def KeyRelease(key):
  ctr = keyboard.Controller()
  ctr.release(key)

class GlobalListener():
  key_press = EventList()
  key_release = EventList()
  mouse_click = EventList()
  mouse_move = EventList()
  mouse_scroll = EventList()
  def _KeyboardPress(self, key):
    try:
      # print(key)
      self.key_press.exec(key)
    except Exception as e:
      print(e)
    pass

  def _KeyboardRelease(self, key):
    try:
      self.key_release.exec(key)
    except Exception as e:
      print(e)
    pass

  def _MouseClick(self, x, y , button, pressed):
    try:
      # print(x, y, button, pressed)
      self.mouse_click.exec(*[x, y, button, pressed])
    except Exception as e:
      print(e)
    pass

  def _MouseMove(self, x, y):
    try:
      # print(x, y)
      self.mouse_move.exec(x, y)
    except Exception as e:
      print(e)
    pass

  def _MouseScroll(self, x, y ,dx, dy):
    try:
      # print(x, y, dx, dy)
      self.mouse_scroll.exec(x, y, dx, dy)
    except Exception as e:
      print(e)
    pass

  def Listen(self):
    try:
      with mouse.Listener(on_click=self._MouseClick, on_move=self._MouseMove, on_scroll=self._MouseScroll) as m_listener,\
          keyboard.Listener(on_press=self._KeyboardPress, on_release=self._KeyboardRelease) as k_listener:
        m_listener.join()
        k_listener.join()
    except Exception as e:
      print(e)
