"""
This module loads and parses locations from a text file and defines a class
to model the attributes of a location.
"""

class location():
  """
  Model for locations.
  
  Members:
    name (string): Name of location.
    mileage (int): Miles away from starting location.
    kind (string) (optional): 'fort', 'river' or 'None' for landmark.
    height (int) (options): River height if type is a river.
  """
  def __init__(self, name, mileage, kind=None, height=None):
    self.name = name
    self.mileage = mileage
    self.kind = kind
    self.height = height
    
  def describe(self):
    """
    Prints all of the attributes.
    
    Arguments:
      None
    
    Returns:
      None
    """
    print('Name:', self.name)
    print('Mileage:', self.mileage)
    print('Kind:', self.kind)
    print('Height:', self.height)

def parse_locations():
  """
  Loads and parses text into location objects.
  
  Arguments:
    None
    
  Returns:
    [location]: A list of location objects.
  """
  # Load file.
  path = '../messages/locations.txt'
  with open(path, 'r') as file:
    contents = file.readlines()
    
  # Remove \n.
  contents = [format_line(line) for line in contents]
  
  # Parse name.
  names = []
  for i in range(0,len(contents),3):
    names.append(contents[i])
  
  # Parse remaining attributes.
  mileages = []
  kinds = []
  heights = []
  for i in range(1,len(contents),3):
    mileage, kind, height = format_details(contents[i])
    mileages.append(mileage)
    kinds.append(kind)
    heights.append(height)
  
  # Build location list to return.
  locations = []
  for i in range(len(names)):
    locations.append(location(names[i],mileages[i],kind=kinds[i],height=heights[i]))
  return locations
    
def format_line(line):
  """
  Used to remove "\n" from a line.
  
  Arguments:
    line (string): Line from a text file.
    
  Returns:
    string: line contents without "\n" at the end.
  """
  return line[:len(line)-1]

def format_details(line):
  """
  Parses location attributes.
  
  Arguments:
    line (string): formatted line from a text file (\n removed).
    
  Returns:
    int, string, int: Parsed mileage, kind, and river height.
  """
  details = line.split(' ')
  try:
    mileage = int(details[0][:-2])
  except IndexError: # This should't happen.
    mileage = None
    
  try:
    kind = details[1]
  except IndexError: # Landmarks have no type.
    kind = None
    
  try:
    height = int(details[2][:-2])
  except IndexError: # Only rivers have a height.
    height = None
  return mileage, kind, height