#!/usr/bin/env python
# coding: utf-8

# In[ ]:


try:
  import pretty_midi
except:
  get_ipython().system(u'pip install pretty_midi')

import analyzers, api_interaction, helpers
