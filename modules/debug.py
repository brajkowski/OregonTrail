class log(object):
  def __init__(self, path):
    self.log = []
    self.output_path = path
    
  def add(self, message):
    self.log.append(message)
  
  def print_console(self):
    for message in self.log:
      print(message)
      
  def print_file(self):
    for message in self.log:
      print(message,file=self.path)
    