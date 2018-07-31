class messages():
  def __init__(self):
    self.__file_paths = {
        'welcome':'../messages/welcome.txt',
        'store_welcome':'../messages/store_welcome.txt',
        'turn_options':'../messages/turn_options.txt',
        'rations':'../messages/rations.txt',
        'fort_options':'../messages/fort_options.txt',
        'landmark_options':'../messages/landmark_options.txt',
        'river_options':'../messages/river_options.txt'
        }
    
    self.__file_paths_parsed = {
        'start_store':'../messages/start_store.txt',
        'fort_store':'../messages/fort_store.txt',
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
    print('\n')
    
  def print_message_parsed(self,key,index):
    message = self.__messages_parsed.get(key)
    print(message[index])
    #print('\n')
    
  def get_message_parsed_count(self,key):
    message = self.__messages_parsed.get(key)
    return len(message)
    
def get_input_string():
  response = str(input(">>> "))
  print()
  return response

def get_input_string_protected(options):
  while True:
    try:
      response = str(input(">>> "))
      if not (response in options):
        raise Exception()
      break
    except Exception:
      print('Please enter a valid option.')
  return response

def get_input_int(low=None,high=None):
  while True:
    try:
      response = int(input(">>> "))
      if low != None and high != None:
        if not(low <= response and response <= high):
          print('Please enter an integer between {} and {}.'.format(low,high))
          response = get_input_int(low,high)
      if low != None and high == None:
        if not (low <= response):
          print('Please enter an integer greater than or equal to {}'.format(low))
          response = get_input_int(low)
      break
    except:
      print("Please enter a valid integer.")
  print()
  return response

def get_input_int_protected(options):
  while True:
    try:
      response = int(input(">>> "))
      if not (response in options):
        raise Exception()
      break
    except Exception:
      print('Please enter a valid option.')
  return response


def get_input_float():
  return float(input(">>> "))
      
