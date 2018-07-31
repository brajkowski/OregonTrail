import datetime
import locations

class member():
  def __init__(self, name, is_leader=False):
    self.name = name
    self.is_alive = True
    self.is_sick = False
    self.status = "Healthy"
    self.is_leader = is_leader
    self.turns_to_healthy = 5
    
  def gets_sick(self,sickness):
    self.turns_to_healthy = 5
    if self.is_sick:
      should_end_game = self.dies(sickness)
      return should_end_game
    else:
      self.is_sick = True
      self.status = "Has {}".format(sickness)
      return False
    
  def dies(self, sickness):
    print("{} died from multiple illnesses".format(self.name))
    self.status = "Deceased"
    self.is_alive = False
    if self.is_leader:
      return True
    else:
      return False
    
  def use_med_kit(self):
    self.turns_to_healthy = 2
    
  def heal_if_sick(self):
    if self.is_sick:
      self.turns_to_healthy -= 1
      if self.turns_to_healthy == 0:
        self.status = "Healthy"
        self.turns_to_healthy = 5
        self.is_sick = False
        print("{} is back to full health".format(self.name))
        
  def heal_to_full_if_sick(self):
    if self.is_sick:
      self.turns_to_healthy = 5
      self.status = "Healthy"
      self.is_sick = False
      print("{} is back to full health".format(self.name))
      
  def print_status(self):
    print("{}: {} (Leader={}, Days to FH={})".format(self.name,self.status,self.is_leader,self.turns_to_healthy))

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
    self.next_location = 0
    self.members = []
    self.current_date = datetime.date(1847,3,3)
    self.miles_traveled = 0
    self.locations = locations.parse_locations()
    self.members_alive = 5
    self.update_miles_to_next()
    self.rations = 3
  
  def load_debug(self):
    self.inventory = {'food':10000000,
        'money':200,
        'bullets':1000,
        'oxen':10,
        'kits':0,
        'parts':10
        }
    self.next_location = 0
    self.members = [member('This',is_leader=True),member('Is'),member('A'),member('Debug'),member('Test')]
    self.current_date = datetime.date(1847,4,9)
    self.miles_traveled = 0
    self.locations = locations.parse_locations()
    self.members_alive = 5
    self.update_miles_to_next()
    self.rations = 3
  
  def print_locations(self):
    for location in self.locations:
      location.describe()
  
  def get_from_inventory(self,key):
    return self.inventory[key]
  
  def update_inventory(self,key,value):
    self.inventory[key] = value
    
  def can_consume(self,key, amount):
    if amount > self.inventory[key]:
      return False
    return True
  
  def consume(self, key, amount):
    new_value = self.inventory[key] - amount
    self.inventory[key] = new_value
    return new_value
  
  def add_to_inventory(self,key,amount):
    self.inventory[key] += amount
  
  # Deprecated.
  #def spend_money(self,value):
  #  new_value = self.inventory['money'] - value
  #  self.inventory['money'] = new_value
   
  def print_status(self):
    #miles_to_next = self.locations[self.next_location].mileage - self.miles_traveled
    print('---------- Status ----------')
    print('Date:', self.current_date)
    print('Miles Traveled:', self.miles_traveled)
    print('Miles to next landmark:', self.miles_to_next_mark)
    print('Food: {} pounds'.format(self.inventory['food']))
    print('Rations: {} pounds per person'.format(self.rations))
    print('Bullets:',self.inventory['bullets'])
    print('Cash: ${}'.format(self.inventory['money']))
    print('----------------------------')
    print("--DEBUG MEMBER STATUS--")
    for member in self.members:
      member.print_status()
    print("----")
    
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
  
  def update_miles_to_next(self):
    self.miles_to_next_mark = self.locations[self.next_location].mileage - self.miles_traveled
    
  def update_next_location(self):
    self.next_location += 1
  
  def print_current_date(self):
    print(self.current_date.strftime("%A %d. %B %Y"))
    
  def get_next_location(self):
    return self.locations[self.next_location]
  
  def travel(self, miles):
    self.miles_traveled += miles
    
  def heal_all_if_sick(self):
    for member in self.members:
      member.heal_if_sick()
  
  def heal_all_to_full_if_sick(self):
    for member in self.members:
      member.heal_to_full_if_sick()
  
    
  
    