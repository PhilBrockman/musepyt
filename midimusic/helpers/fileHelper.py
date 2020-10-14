
import json
import os
class fileHelper():
  def __init__(self):
    self.file_extension = "file_handler"
    self.project_root = "file_handler"
    self.last_save_location

  def cls(self):
    b = self.__init__()
    b.file_extension = "NONE"
    return b

  def default_filename(self):
    return "file_handler"

  def touch_directory(filename):
    if(len(filename.split("/")) > 0):
      path = "{}".format("/".join(filename.split("/")[:-1]))
      os.makedirs(path,exist_ok=True)

  def save(self, filename = None):
    if filename is None:
      filename = self.default_filename()
    filename = "{}/{}.{}".format(self.project_root, filename, self.file_extension)
    fileHelper.touch_directory(filename)

    with open(filename, 'w') as outfile:
      json.dump(self.toJson(), outfile)

    self.last_save_location = filename
    return filename


  def toJson(self):
    return json.dumps(self, default=lambda o: o.__dict__)

  def load_json(filename):
    with open( filename, "rb" ) as infile:
      return json.loads(json.load(infile))

  def load(filename, fresh_class):
    json = fileHelper.load_json(filename)
    return fileHelper.convert(json, fresh_class)

  def convert(json, dclass):
    for x in json:
      dclass.__dict__[x] = json[x]
    return dclass


# In[ ]:


class tester(fileHelper):
  def __init__(self):
    self.file_extension = "filehelpertester"
    self.project_root = "testing"
    self.data = "fuubar"


# In[ ]:


class adder(fileHelper):
  def __init__(self, *args):
    self.file_extension = "assert_test"
    self.project_root = "assert"
    self.obs = args

  def add(self):
    total = 0
    for o in self.obs:
      total += o
    return total
