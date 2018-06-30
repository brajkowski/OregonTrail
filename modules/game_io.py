class manager(object):
  def __init__(self):
    self.__file_paths = {
        'welcome':'../messages/welcome.txt',
        'store_welcome':'../messages/store_welcome.txt'
        }
    
    self.__file_paths_parsed = {
        'start_store':'../messages/start_store.txt',
        'locations':'../messages/locations.txt',
        }
    
    self.__messages = {}
    self.__messages_parsed = {}
    self.__load_all_messages()
    self.__load_all_messages_parsed()
    
  
  def __load_all_messages(self):
    files = list(self.__file_paths.items())
    for pair in files:
      key = pair[0]
      file_path = pair[1]
      self.__load_message(key,file_path)
      
  def __load_all_messages_parsed(self):
    files = list(self.__file_paths_parsed.items())
    for pair in files:
      key = pair[0]
      file_path = pair[1]
      self.__load_message_parsed(key,file_path)
      
  def __load_message(self, key, file_path):
    with open(file_path, 'r') as file:
      message = str(file.read())
      self.__messages[key] = message
      
  def __load_message_parsed(self, key, file_path):
    with open(file_path, 'r') as file:
      message = str(file.read())
      messages = message.split("\n\n")
      self.__messages_parsed[key] = messages

  def print_message(self,key):
    print(self.__messages.get(key))
    print('\n\n')
    
  def print_message_parsed(self,key,index):
    message = self.__messages_parsed.get(key)
    print(message[index])
    print('\n\n')
    
  def get_message_parsed_count(self,key):
    message = self.__messages_parsed.get(key)
    return len(message)
    
  def get_input_string(self):
    return str(input(">>> "))
  
  def get_input_int(self,low=None,high=None):
    while True:
      try:
        response = int(input(">>> "))
        break
      except ValueError:
        print("Please enter a valid integer.")
    return response
  
  def get_input_float(self):
    return float(input(">>> "))
      
