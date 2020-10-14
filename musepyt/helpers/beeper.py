#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import IPython, pretty_midi

def beep_beep(action):
  sound = pretty_midi.Instrument(program=42)
  if action == "complete":
    for note_name in ['C5', 'E5', 'G5']:
      note_number = pretty_midi.note_name_to_number(note_name)
      note1 = pretty_midi.Note(velocity=100, pitch=note_number, start=0, end=.5)
      note2 = pretty_midi.Note(velocity=100, pitch=note_number, start=.25, end=.75)
      sound.notes.append(note1)
      sound.notes.append(note2)
  if action == "error":
    for note_name in ['C3', 'E3', 'G3']:
      note_number = pretty_midi.note_name_to_number(note_name)
      note1 = pretty_midi.Note(velocity=100, pitch=note_number, start=0, end=.25)
      note2 = pretty_midi.Note(velocity=100, pitch=note_number, start=.75, end=1)
      sound.notes.append(note1)
      sound.notes.append(note2)
  IPython.display.display(IPython.display.Audio(sound.synthesize(fs=16000), rate=16000, autoplay=True))


# In[ ]:





# In[ ]:




