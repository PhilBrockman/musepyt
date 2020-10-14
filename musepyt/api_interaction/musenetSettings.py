#!/usr/bin/env python
# coding: utf-8

# In[1]:


class musenetSettings:
  def __init__(self, enc="", audioFormat = "mp3", genre="thebeatles", truncation = 27, temp=.8, length=225, instrumentation = ["piano"]):
    self.project_root = "musenet_settings"
    self.enc = enc
    self.genre = genre
    self.temp = temp
    self.legal_instruments = "piano strings winds drums harp guitar bass".split(" ")
    self.turn_on(instrumentation)
    self.length = length
    self.truncation = truncation
    self.audioFormat = audioFormat
   
  def legal_composers():
    return ['chopin',
            'mozart',
            'rachmaninoff',
            'country',
            'bach',
            'beethoven',
            'thebeatles',
            'franksinatra',
            'tchaikovsky'] 

  def turn_on(self, instruments):
    self.toggle_instruments(instruments, True)

  def turn_off(self, instruments):
    self.toggle_instruments(instruments, False)

  def toggle_instruments(self, instruments, state):
    instr_dict = {}
    lower_instruments = [x.lower() for x in instruments]
    for item in self.legal_instruments:
      if item in lower_instruments:
        instr_dict[item] = state
      else:
        instr_dict[item] = not state
    self.instrumentation = instr_dict

  def instrumentation_settings(self, piano=False, strings=False,winds=False,drums=False,harp=False,guitar=False,bass=False):
    instr = {"piano":piano,"strings":strings,"winds":winds,
             "drums":drums,"harp":harp,"guitar":guitar,"bass":bass}
    return instr

  def __str__(self):
    s = """genre: {}\ntemp: {}\ninstrumentation: {}\ntokens: {}\ntruncation: {}\naudio format: {}\nenc: <{}>"""
    return s.format(self.genre, self.temp, self.instrumentation, self.length, self.truncation, self.audioFormat, self.enc)


# In[2]:


assert musenetSettings(instrumentation = ["piano", "winds"]).instrumentation == {'bass': False,
 'drums': False,
 'guitar': False,
 'harp': False,
 'piano': True,
 'strings': False,
 'winds': True}


# In[3]:


assert musenetSettings.legal_composers()[0] == "chopin"


# In[ ]:




