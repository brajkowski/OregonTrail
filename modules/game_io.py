class manager(object):
  def __init__(self):
    self.__file_paths = {
        'welcome':'../messages/welcome.txt',
        'locations':'../messages/locations.txt',
        'store_welcome':'../messages/store_welcome.txt'
        }
    
    self.__messages = {}
    self.__load_all_messages()
  
  def __load_all_messages(self):
    files = list(self.__file_paths.items())
    for pair in files:
      key = pair[0]
      file_path = pair[1]
      self.__load_message(key,file_path)
      
  def __load_message(self, key, file_path):
    with open(file_path, 'r') as file:
      message = str(file.read())
      self.__messages[key] = message
      
  def print_message(self,key):
    print(self.__messages.get(key))
    print("\n\n")
      
