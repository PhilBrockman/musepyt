#!/usr/bin/env python
# coding: utf-8

# In[8]:


import ipywidgets as widgets
import IPython
import copy

class question:
  def __init__(self, string, style, options, answer =None):
    self.text = string
    self.style = style
    self.options = options
    self.answer = answer


# In[9]:


class attributeAnalyzer:
  def __init__(self, questions=[]):
    self.obj = None
    q_holder = []
    for q in questions:
      q_holder.append(copy.copy(q))
    self.questions = q_holder

  def new_question(self, *args, **kwargs):
    self.questions.append(question(*args, **kwargs))

  def has_blank_answers(self):
    for q in self.questions:
      if q.answer is None:
        return True
    return False

  def collect_input(self):
    for q in self.questions:
      q.selector = getattr(self, q.style)(q)

  def keyboardinput(self, q):
    q.answer = input(q.text)

  def __str__(self):
    out = ""
    for q in self.questions:
      out += ("{}: {}\n".format(q.text,q.answer))
    return out


# In[10]:


aa = attributeAnalyzer()
aa.new_question("how are you?", style="keyboardinput", options = {"this good": 1, "this bad": -1})
aa.new_question("What is 1+1", style="keyboardinput", options={"first":-4, "second":3, "third": 2})
assert aa.has_blank_answers()


# In[11]:


for q in aa.questions:
  q.answer = "something"

assert aa.has_blank_answers() is False


# In[13]:


b = attributeAnalyzer(aa.questions)

assert b.has_blank_answers() == False
assert len(b.questions) == 2


# In[ ]:




