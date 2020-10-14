#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from google.colab import drive
drive.mount('/content/drive')


# In[ ]:


import os
os.chdir("/content/drive/My Drive/repos/MusicalPy") 


# In[ ]:


from midimusic.helpers.fileHelper import *
from midimusic.helpers.timer import *
from midimusic.api_interaction.musenetSettings import *

import copy
import time
import IPython
import pretty_midi
import numpy as np
from time import gmtime, strftime
import os


# In[ ]:


class pictureManipulation:
  def plot_piano_roll(pm, start_pitch, end_pitch, fs=100):
      librosa.display.specshow(pm.get_piano_roll(fs)[start_pitch:end_pitch],
                              hop_length=1, sr=fs, x_axis=None, y_axis=None,
                              fmin=pretty_midi.note_number_to_hz(start_pitch))
      
  def png_location(midi_location):
    return "{}.png".format(".".join(midi_location.split(".")[:-1]))

  def save_piano_roll_image_from_midi_location(midi_location, start_pitch, end_pitch, fs=100, width=8, height=8):
    pm = pretty_midi.PrettyMIDI(midi_location)
    png_out = png_location(midi_location)
    if(path.exists(png_out)):
      c.png_location = png_out
      print("image exists: {}".format(png_out))
      return True
    plt.figure(figsize=(width, height))
    pictureManipulation.plot_piano_roll(pm.to_midi(), start_pitch, end_pitch)
    fileHandler.touch_directory(png_out)
    plt.savefig(png_out,bbox_inches='tight')
    return png_out


# In[ ]:


class audioManipulation:
  def __init__(self, tracks):
    self.tracks = tracks

  def instrument_name_to_program(self, string):
    lookup = {
      "piano": "Acoustic Grand Piano",
      "bass": "Acoustic Bass",
      "winds": "Recorder",
      "drums": "Synth Drum",
      "harp": "Orchestral Harp",
      "guitar": "Acoustic Guitar (nylon)",
      "strings": "Violin"
    }
    try:
      return pretty_midi.instrument_name_to_program(lookup[string].title())
    except:
      return pretty_midi.instrument_name_to_program(string.title())
        
  def append_notes_to_inst(self, inst, notes, velocity=100):
    for note in notes:
        inst.notes.append(pretty_midi.Note(velocity, note["pitch"], note["time_on"], note["time_on"] + note["duration"]))
    return inst

  def to_midi(self):
    pm = pretty_midi.PrettyMIDI(initial_tempo=120)
    if self.tracks is not None:
      for track in self.tracks:
        inst = pretty_midi.Instrument(program=self.instrument_name_to_program(track['instrument']), is_drum=False)
        inst = self.append_notes_to_inst(inst, track['notes'])
        pm.instruments.append(inst)
    return pm

  def play(self, play_each = True, sleep=False):
    IPython.display.display(IPython.display.Audio(self.to_midi().synthesize(fs=16000), rate=16000, autoplay=play_each))
    if sleep:
        time.sleep(self.totalTime + .25)

  def play_gens(self, **kwargs):
    for c in self.children:
      c.play(**kwargs)

  def save_midi(self, filename = None):
    if filename is None:
      filename = "{}/{}.mid".format(self.project_root, self.default_filename())
    fileHelper.touch_directory(filename)
    self.to_midi().write(filename)
    self.midi_location = filename
    return filename


# In[ ]:


from midimusic.helpers.fileHelper import *

class completion(fileHelper, audioManipulation, pictureManipulation):
  def __init__(self, project_root = None, file_extension = "completion", **kwargs):
    self.settings = musenetSettings(**kwargs)
    self.children = []
    self.totalTime = 0
    self.tracks = None
    self.midi_location = None
    self.png_location = None
    self.file_extension = file_extension
    self.loop_count = None
    self.fetch_count = None
    if project_root is not None:
      self.project_root = project_root
    #else all is blank

  def add_children(self, processed_musenet):
    for item in processed_musenet:
      tmp = completion()
      tmp.settings = copy.copy(self.settings)
      tmp.settings.enc = ("{} {}".format(self.settings.enc.strip(), item['encoding'].strip())).strip()
      tmp.totalTime = item["totalTime"]
      tmp.tracks = item["tracks"]
      tmp.project_root = self.project_root
      self.children.append(tmp)

  def has_children(self):
    return len(self.children) > 0
  
  def default_filename(self):
    instr = self.settings.instrumentation
    return "{}/{}/{}/{}".format(self.settings.genre, 
                                self.settings.temp, "_".join([x for x in instr.keys() if instr[x] is True]), 
                                timer.filetime())

  def load_objects(filename):
    json = completion.load_json(filename)
    return completion.objectize(json)

  def objectize(json):
    if json is None:
      return None
    partial = fileHelper.convert(json, completion())
    partial.settings = fileHelper.convert(partial.settings, musenetSettings())
    if not partial.has_children():
      return partial
    else:
      for i in range(len(partial.children)):
        partial.children[i] = completion.objectize(partial.children[i])
      return partial


# In[ ]:


c = completion()
b = completion("testing/save-load")


# In[ ]:


c.settings


# In[ ]:


b.children.append(c)
b.children.append(c)


# In[ ]:


d = completion()
c.children.append(d)


# In[ ]:


out = b.save()


# In[ ]:


d = completion.load_objects(out)


# In[ ]:


assert isinstance(d.children[0].children[0].settings, musenetSettings)


# In[ ]:




