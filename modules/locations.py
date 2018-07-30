class location():
  def __init__(self, name, mileage, kind=None, height=None):
    self.name = name
    self.mileage = mileage
    self.kind = kind
    self.height = height
    
  def describe(self):
    print('Name:', self.name)
    print('Mileage:', self.mileage)
    print('Kind:', self.kind)
    print('Height:', self.height)


def parse_locations():
  path = '../messages/locations.txt'
  with open(path, 'r') as file:
    contents = file.readlines()
  contents = [format_line(line) for line in contents]
  names = []
  for i in range(0,len(contents),3):
    names.append(contents[i])
  mileages = []
  kinds = []
  heights = []

  for i in range(1,len(contents),3):
    mileage, kind, height = format_details(contents[i])
    mileages.append(mileage)
    kinds.append(kind)
    heights.append(height)
  locations = []
  for i in range(len(names)):
    locations.append(location(names[i],mileages[i],kind=kinds[i],height=heights[i]))
  return locations
    
def format_line(line):
  return line[:len(line)-1]

def format_details(line):
  details = line.split(' ')
  try:
    mileage = int(details[0][:-2])
  except IndexError:
    mileage = None
    
  try:
    kind = details[1]
  except IndexError:
    kind = None
    
  try:
    height = int(details[2][:-2])
  except IndexError:
    height = None
  return mileage, kind, height