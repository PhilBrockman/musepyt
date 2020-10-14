
from midimusic.helpers.fileHelper import *
from midimusic.api_interaction.musenetSettings import *
from midimusic.api_interaction.completion import *
from midimusic.api_interaction.generator import *



class spider(fileHelper):
  def __init__(self):
    self.file_extension = "spider"
    self.temps = [.7, .9]
    self.composers = musenetSettings.legal_composers()
    self.instrs = [["piano"], ["guitar"], ["piano", "strings"]]
    self.max_fetches = 2
    self.loops = 2
    self.seeds = 3
    self.project_root = None
    self.trial_complete_tones = False
    self.play_final_song = True
    self.verbose = True
    self.logger = logger()

  def default_filename(self):
    return f"spiders/{timer.filetime()}"

  def pre_check(self):
    print(f"Temps: {self.temps}")
    print(f"Commposers: {self.composers}")
    print(f"instruments: {self.instrs}")
    print(f"Max Fetches: {self.max_fetches}")
    print(f"Loops: {self.loops}")
    print(f"Project: {self.project_root}")
    print(f"Number of seeds: {self.seeds}")
    print(f"Data: {len(self.logger.data)}, Queried: {len(self.logger.queried)}")
    print(f"Trial tones: {self.trial_complete_tones} Play Songs: {self.play_final_song}")

  def set_project(self):
    self.project_root = f"loops {self.loops}/max fetches {self.max_fetches}/"

  def info_arr(self, c, t, i):
    return [c, t, i]

  def fetch_from_musenet(self):
    if self.project_root is None:
      raise Exception("Need to set a project_root")
    self.logger.project_root = self.project_root

    count = 1
    total_ittrs = len(self.composers)*len(self.temps)*len(self.instrs)*self.seeds
    for c in self.composers:
      for t in self.temps:
        for i in self.instrs:
          info = {"composer": c,
                  "instrumentation":i,
                  "temp":t}
          self.logger.log("[{}/{}] fetching seed: {}".format(count, total_ittrs, info), self.verbose)
          c_t_i = self.info_arr(c = c, t = t, i = i)
          if(c_t_i in self.logger.queried):
            count += self.seeds
            print("previously queried")
            continue
          info["children"] = {}
          for s in range(self.seeds):
            count += 1
            a = completion(genre = c, instrumentation=i, temp=t, project_root = self.project_root)
            g = generator(a)
            assert g.project_root == self.project_root
            g.play_tones = self.trial_complete_tones
            self.logger.log("child {}/{}".format(s+1, self.seeds), self.verbose)
            child_info = {}
            loops = g.keep_fetching(max_fetches=self.max_fetches, loops = self.loops)
            if loops == 0:
              final_result = a
              self.logger.log("Loops = 0", self.verbose)
            else:
              fetches = -1
              if g.result is not None:
                fetches = g.result.fetch_count
                g.select_next_payload()
              final_result = g.payload
              final_result.fetch_count = fetches
              self.logger.log(final_result.save_midi(), self.verbose)
            final_result.loop_count = loops
            final_result.save()
            info["children"][s] = final_result
            if loops > 0:
              final_result.play(play_each = self.play_final_song)
          self.logger.queried.append(c_t_i)
          self.logger.data.append(info)

          self.logger.log(f"Backing up data for spider {self.save()}", self.verbose)


  def load_objects(filename):
    json = spider.load_json(filename)
    return spider.objectize(json)

  def objectize(json):
    if json is None:
      return json
    else:
      partial = fileHelper.convert(json, spider())
      partial.logger = logger.objectize(partial.logger)
      return partial



# In[7]:


class logger(fileHelper):
  def __init__(self):
    self.file_extension = "logs"
    self.queried = []
    self.data = []

  def objectize(json):
    partial = fileHelper.convert(json, logger())
    data = []
    for node in partial.data:
      if "totalTime" not in node.keys(): #legacy spider
        for child in node["children"]:
          data.append(completion.objectize(node["children"][child]))
      else:
        data.append(completion.objectize(node))

    partial.data= data
    return partial

  def default_filename(self):
    return f"logs/logs_{timer.filetime()}"

  def log(self, msg, bool):
    if bool:
      print(msg)


class fixed_filename(spider):
  def __init__(self):
    super().__init__()
    self.fixed_time = timer.filetime()

  def default_filename(self):
    return f"spiders/initiated_{self.fixed_time}"

  def load_objects(filename):
    json = fixed_filename.load_json(filename)
    return fixed_filename.objectize(json)

  def objectize(json):
    if json is None:
      return json
    else:
      partial = fileHelper.convert(json, fixed_filename())
      partial.logger = logger.objectize(partial.logger)

      return partial
