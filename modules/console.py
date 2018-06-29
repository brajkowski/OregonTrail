class io_manager:
  def __init__(self):
    self.welcome_path = "../messages/welcome.txt"
    self.locations_path = "../messages/locations.txt"
    
    self.welcome_message = []
    self.locations = []
    
  def load_message(self,path,target_list):
    with open(path) as file:
      line = str(file.readline())
      line = self.remove_newline(line)
      while line != "":
        target_list.append(line)
        line = str(file.readline())
        line = self.remove_newline(line)
        
  def print_welcome(self):
    for line in self.welcome_message:
      print(line)
      
  def remove_newline(self,line):
    if line[-1:] == "\n":
      return line[:len(line)-1]
    return line
  
  def load_all_messages(self):
    self.load_message(self.welcome_path,self.welcome_message)
    self.load_message(self.locations_path,self.locations)
    
  def print_all_locations(self):
    for line in self.locations:
      print(line)
