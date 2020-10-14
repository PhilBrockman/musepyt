#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
import copy

class fetcher:
  def fetch(c):
    response = fetcher.fetch_from_musenet(c)
    if fetcher.erred(response):
      return fetcher.problems(response)

    c.add_children(fetcher.process_raw_musenet(response))
    return c

  def fetch_from_musenet(c):
    settings = c.settings
    p = {"genre":settings.genre,
       "instrument":settings.instrumentation,
       "encoding":settings.enc,
       "temperature":settings.temp,
       "truncation":settings.truncation,
       "generationLength": settings.length,
       "audioFormat":settings.audioFormat}

    h = {
      "Content-Type": "application/json",
      "path": "/sample"
    }

    r = requests.post("https://musenet.openai.com/sample",
        data = json.dumps(p),
        headers = h
    )
    return r.content.decode()

  def process_raw_musenet(response):
    return json.loads(response)["completions"]

  def problems(response):
    try:
      out = fetcher.process_raw_musenet(response)
      return None
    except Exception as e:
      return e

  def erred(response):
    return isinstance(fetcher.problems(response), Exception)


# In[ ]:




