#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from google.colab import drive
drive.mount('/content/drive')


# In[ ]:


import os
os.chdir("/content/drive/My Drive/repos/MusicalPy") 


# In[ ]:


get_ipython().system(u'pip install mir_eval')
get_ipython().system(u'pip install librosa')
get_ipython().system(u'pip install pretty_midi')


# In[ ]:


from midimusic.analyzers.attributeAnalyzer import *
from midimusic.api_interaction.musenetSettings import *
from midimusic.api_interaction.spider import spider
from midimusic.helpers.timer import *
from midimusic.helpers.fileHelper import *


# In[ ]:


import mir_eval.display
import librosa.display
import matplotlib.pyplot as plt
import pretty_midi
from os import path
import pandas as pd
import IPython
import copy

class midiAnalyzer(attributeAnalyzer):
  def __init__(self, spi=None):
    if(spi is not None):
      self.df = self.initialize_from_spider(spi)
      
  def png_loc_from_midi_loc(midi_location):
    return "{}.png".format(".".join(midi_location.split(".")[:-1]))

  def plot_piano_roll(pm, start_pitch, end_pitch, fs=100):
      librosa.display.specshow(pm.get_piano_roll(fs)[start_pitch:end_pitch],
                              hop_length=1, sr=fs, x_axis=None, y_axis=None,
                              fmin=pretty_midi.note_number_to_hz(start_pitch))
      
  def save_piano_roll_image(midi_location, start_pitch, end_pitch, fs, width, height, overwrite):
    if midi_location is None or len(midi_location) < 3:
      return ""
    png_out = midiAnalyzer.png_loc_from_midi_loc(midi_location)
    if not overwrite and path.exists(png_out):
      return png_out
    
    print(f"loading {midi_location}")
    plt.figure(figsize=(width, height))
    pm = pretty_midi.PrettyMIDI(midi_location)
    midiAnalyzer.plot_piano_roll(pm, start_pitch, end_pitch)
    fileHelper.touch_directory(png_out)
    plt.savefig(png_out,bbox_inches='tight')
    return png_out

  def generate_images_from_loaded(self, start_pitch = 20, end_pitch = 90, overwrite = False, fs=100, width=8, height=8):
    self.df["png_location"] = [midiAnalyzer.save_piano_roll_image(x, start_pitch, end_pitch, fs, width, height, overwrite) for x in self.df["midi_location"]]
      
  def ask(self, id, question, overwrite=False):
    if not pd.isnull(self.df["png_location"].values[id]) and len(self.df["png_location"].values[id]) > 5:
      IPython.display.clear_output(wait=True)
      IPython.display.display(IPython.display.Audio(pretty_midi.PrettyMIDI(self.df["midi_location"].values[id]).synthesize(fs=16000), rate=16000, autoplay=True))
      IPython.display.display(IPython.display.Image(self.df["png_location"].values[id]))
      print(question)
      self.df[question].values[id] = input()

  def new_question(self, text):
    try:
      self.df[text]
      return False
    except:
      self.df[text] = np.NaN
      return True

  def ask_unanswered(self, question, save_every=10):
    for i in range(len(self.df)):
      if pd.isnull(self.df[question].values[i]):
        self.ask(i, question)
        if i%save_every == 0:
          self.save()
      else:
        print(f"Already answered index {i}")

  def save(self, filename = None):
    if filename is None:
      filename = f"analysis/{timer.filetime()}"
    outfile = f"{self.project_root}/{filename}"
    fileHelper.touch_directory(outfile)
    data = {}
    for key in self.__dict__.keys():
      if isinstance( self.__dict__[key], pd.DataFrame):
        data[key] = self.__dict__[key].to_json()
      else:
        data[key] = self.__dict__[key]

    with open(outfile, 'w') as out:
      json.dump((data), out)
    return outfile

  def load_from_save(infile):
    with open(infile, 'r') as json_file:
      data = json.load(json_file)
    m = midiAnalyzer()
    m.df = pd.DataFrame(json.loads(data["df"]))
    m.project_root = data["project_root"]
    return m

  def initialize_from_spider(self, s):
    self.project_root = s.project_root
    out = []
    for item in s.logger.data:
      tmp = {
            "composer":        item.settings.genre,
            "temp":            item.settings.temp,
            "instrumentation": "_".join([x for x in item.settings.instrumentation if item.settings.instrumentation[x]]),
            "max_fetches":     s.max_fetches,
            "loops":           s.loops, 
            "count":           item.loop_count,
            "midi_location":   item.midi_location,
            "analysis":        ""
            }
      if item.midi_location:
        png = midiAnalyzer.png_loc_from_midi_loc(item.midi_location)

        if path.exists(png):
          tmp["png_location"] = png
        else:
          tmp["png_location"] = ""
      out.append(tmp)

    return pd.DataFrame(out)

