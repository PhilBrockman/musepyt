#!/usr/bin/env python
# coding: utf-8

# In[1]:


from google.colab import drive
drive.mount('/content/drive')


# In[2]:


import os
os.chdir("/content/drive/My Drive/repos/MusicalPy") 
from midimusic.api_interaction.completion import *
from midimusic.api_interaction.fetcher import *
from midimusic.helpers.beeper import *


# In[3]:


import json
from time import localtime, strftime

class generator(fileHelper):
  def __init__(self, seed = None, verbose = True, play_tones = True):
    self.payload = seed
    self.result = None
    self.verbose = verbose
    self.play_tones = play_tones
    self.file_extension = "generator"
    if seed is not None:
      self.project_root = seed.project_root
    else:
      self.project_root = None

  def fetch(self):
    return self.fetch_until_response(max_fetches = 1)

  def fetch_until_response(self, max_fetches = 5):
    if self.payload is None:
      raise Exception("Payload is None")
    if self.project_root is None:
      raise Exception("no project root")
    count = 0
    while(not self.payload.has_children() and count < max_fetches):
      count += 1
      self.payload.fetch_count = count
      self.log("On fetch {}/{}".format(count, max_fetches))
      fetcher.fetch(self.payload)

    if(self.payload.has_children()):
      if self.play_tones:
        beep_beep("complete") # beep beep i'm a jeep
      self.log("successful fetching".format(count, max_fetches))
      self.result = self.payload
      self.payload = None
    else:
      self.log("failed")
      if self.play_tones:
        beep_beep("error")
      self.result = None

  def keep_fetching(self, max_fetches=3, loops=5):
    count = 0
    while(count < loops):
      self.log("On loop {}/{}".format(count+1, loops))
      self.fetch_until_response(max_fetches)
      if(self.payload is None): #successful fetching
        count += 1
        self.select_next_payload()
      else:
        break #failed a fetch
    return count


  def select_next_payload(self):
    #probably best to overwrite this method with something smarter choosing the children
    self.payload = self.result.children[-1]

  def default_filename(self):
    if self.payload is not None:
      return self.payload.default_filename()
    if self.result is not None:
      return self.result.default_filename()
    return f"generators/failed/#{timer.filetime()}"

  def log(self, msg):
    if self.verbose:
      print(msg)

  def load_objects(filename):
    json = generator.load_json(filename)
    return generator.objectize(json)

  def objectize(json):
    if json is None:
      return json
    else:
      partial = fileHelper.convert(json, generator(None, True, True))
      partial.payload = completion.objectize(partial.payload)
      partial.result  = completion.objectize(partial.result)
      return partial



# In[7]:


load = generator.load_objects("testing/gen save load/thebeatles/0.8/piano/2020_08_08_21_54_50.generator")


# In[8]:


assert isinstance(load.result, completion)


# In[8]:




