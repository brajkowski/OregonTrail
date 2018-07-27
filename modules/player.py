class player(object):
  def __init__(self):
    self.inventory = {
        'food':0.0,
        'money':1400.0,
        'oxen':0,
        'kits':0,
        'parts':0
        }
    
    self.food = 0.0
    self.money = 1400.0
    self.oxen = 0
    self.kits = 0
    self.parts = 0
    
  def get_from_inventory(self,key):
    return self.inventory[key]
  
  def update_inventory(self,key,value):
    self.inventory[key] = value
    
  def can_spend(self,amount):
    if amount > self.inventory['money']:
      return False
    return True
  
  def spend_money(self,value):
    new_value = self.inventory['money'] - value
    self.inventory['money'] = new_value
    
  def print_inventory(self):
    pairs = list(self.inventory.items())
    print("Player Inventory:")
    for pair in pairs:
      key = pair[0]
      value = pair[1]
      print("\t{}: {}".format(key,value))
  
    
  
    