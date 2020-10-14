#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time
import datetime
from time import strftime,localtime

class timer:
  def __init__(self):
    self.recordings = []
    self.mark = None

  def hms(self):
    return self.now().strftime('%H:%M:%S')

  def now(self):
    return datetime.datetime.now()

  def delta_t(self, time):
    return (self.now() - time).total_seconds()

  def start(self):
    print("Starting: {}".format(self.hms()))
    self.mark = self.now()

  def stop(self):
    print("Stopping: {}".format(self.hms()))
    self.recordings.append(self.delta_t(self.mark))
    self.mark = None

  def filetime():
    return strftime("%Y_%m_%d_%H_%M_%S", localtime())


#
