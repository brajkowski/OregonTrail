"""
This module handles printing large, formatted messages from text files to the console
and provides various options to handle and protect user input.
"""

class messages():
  """
  Loads, stores, and prints messages created as text files.
  Used for large, formatted messages that are printed to the console.
  Messages are printed using a key that is similar to the text file name.
  Parsed messages need to be delimited with '\n\n' in the text file.
  
  Members:
    __file_paths {}: Dictionary of file paths of single messages that get displayed at once.
    __file_paths_parsed {}: Dictionary of file paths of messages that get displayed at different times, in order.
    __messages {}: Dictionary for contents of messages to be stored.
    __messages_parsed {}: Dictionary for contents of parsed messages to be stored.
  """
  
  def __init__(self):
    # Define all messages keys and file paths.
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
        'locations':'../messages/locations.txt',
        'fort_store_1':'../messages/fort_store_1.txt',
        'fort_store_2':'../messages/fort_store_2.txt',
        'fort_store_3':'../messages/fort_store_3.txt',
        'fort_store_4':'../messages/fort_store_4.txt',
        'fort_store_5':'../messages/fort_store_5.txt',
        'fort_store_6':'../messages/fort_store_6.txt'
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
    
  def print_message_parsed(self,key,index):
    message = self.__messages_parsed.get(key)
    print(message[index])
    
  def get_message_parsed_count(self,key):
    """
    Gives the number of individual messages in a single parsed message.
    
    Arguments:
      key (string): Key that corresponds to a stored parsed message.
      
    Returns:
      int: Number of messages contained in the parsed message.
    """
    message = self.__messages_parsed.get(key)
    return len(message)
    
def get_input_string():
  """
  Ensures a string is obtained from standard input.
  """
  response = str(input(">>> "))
  print() # For aesthetics.
  return response

def get_input_int(low=None,high=None):
  """
  Ensures an integer is obtained from standard input, optionally, within a range.
  
  Arguments:
    low (int): Optional lower bound (inclusive).
    high (int): Optional upper bound (inclusive).
    
  Returns:
    int: User supplied value.
  """
  while True:
    try:
      response = int(input(">>> "))
      if low != None and high != None:
        if not(low <= response and response <= high):
          print('Please enter an integer between {} and {}'.format(low,high))
          response = get_input_int(low,high) # Trap via recursion.
      if low != None and high == None:
        if not (low <= response):
          print('Please enter an integer greater than or equal to {}'.format(low))
          response = get_input_int(low) # Trap via recursion.
      break
    except:
      # Handle all non-integer input.
      print("Please enter a valid integer")
  print() # For aesthetics.
  return response

def get_input_int_protected(options):
  """
  Ensures an integer is obtained from standard input from a list of valid options.
  
  Arguments:
    options []: List of valid integers.
  
  Returns:
    int: User supplied value that is contained in the valid options.
  """
  while True:
    try:
      response = int(input(">>> "))
      if not (response in options):
        raise Exception()
      break
    except Exception:
      print('Please enter a valid option')
  print() # Aesthetics.
  return response
