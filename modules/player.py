class player(object):
  def __init__(self):
    self.inventory = {
        'food':0.0,
        'money':1600.0,
        'oxen':0,
        'kits':0,
        'parts':0
        }
    
    self.food = 0.0
    self.money = 1600.0
    self.oxen = 0
    self.kits = 0
    self.parts = 0
    
  def get_from_inventory(self,key):
    return self.inventory[key]
  
  
    
  def print_inventory(self):
    pairs = list(self.inventory.items())
    for pair in pairs:
      key = pair[0]
      value = pair[1]
      print("\t{}: {}".format(key,value))
    
  
    