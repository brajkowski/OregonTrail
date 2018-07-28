import datetime

class player():
  def __init__(self):
    self.inventory = {
        'food':0.0,
        'money':1400.0,
        'bullets':0.0,
        'oxen':0,
        'kits':0,
        'parts':0
        }
    self.location = 0
    self.names = []
    self.current_date = datetime.date(1847,3,3)
    self.miles_traveled = 0
  
  def load_debug(self):
    self.inventory = {'food':1000,
        'money':200,
        'bullets':1000,
        'oxen':10,
        'kits':10,
        'parts':10
        }
    self.location = 0
    self.names = ['This','Is','A','Debug','Test']
    self.current_date = datetime.date(1847,3,3)
    self.miles_traveled = 0
  
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
   
  def print_status(self):
    
    print('---------- Status ----------')
    print('Date:', self.current_date)
    print('Miles Traveled:', self.miles_traveled)
    print('Miles to next landmark', 'Add next land mark') # TODO: miles to next landmarkprint()
    print('Food: {} pounds'.format(self.inventory['food']))
    print('Bullets:',self.inventory['bullets'])
    print('Cash: ${}'.format(self.inventory['money']))
    print('----------------------------')
    
  def print_inventory(self):
    pairs = list(self.inventory.items())
    print("Player Inventory:")
    for pair in pairs:
      key = pair[0]
      value = pair[1]
      print("\t{}: {}".format(key,value))
      
  def advance_time(self,days):
    delta = datetime.timedelta(days)
    self.current_date += delta
  
  def print_current_date(self):
    print(self.current_date.strftime("%A %d. %B %Y"))
  
    
  
    