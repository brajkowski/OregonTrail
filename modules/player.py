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
      self.dies(sickness)
    else:
      self.is_sick = True
      self.status = "Has {}".format(sickness)
    
  def dies(self, sickness):
    print("{} died from multiple illnesses".format(self.name))
    self.status = "Deceased"
    self.is_alive = False
    
  def drown(self):
    print("{} drowned".format(self.name))
    self.status = "Deceased"
    self.is_alive = False
    
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
        'food':0,
        'money':1400.00,
        'bullets':0,
        'oxen':0,
        'kits':0,
        'parts':0
        }
    self.next_location = 0
    self.members = []
    self.current_date = datetime.date(1847,3,3)
    self.end_date = datetime.date(1847,11,30)
    self.miles_traveled = 0
    self.locations = locations.parse_locations()
    self.members_alive = 5
    self.update_miles_to_next()
    self.rations = 3
    self.forts_visited = 0
    self.win_mileage = 2040
  
  def load_debug(self):
    self.inventory = {'food':1000,
        'money':10000000,
        'bullets':500,
        'oxen':10,
        'kits':3,
        'parts':3
        }
    self.next_location = 0
    self.members = [member('This',is_leader=True),member('Is'),member('A'),member('Debug'),member('Test')]
    self.current_date = datetime.date(1847,4,9)
    self.end_date = datetime.date(1847,11,30)
    self.miles_traveled = 0
    self.locations = locations.parse_locations()
    self.members_alive = 5
    self.update_miles_to_next()
    self.rations = 3
    self.forts_visited = 0
    self.win_mileage = 2040
    
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
  
  def can_add_to_inventory(self,key,amount):
    if key == 'oxen':
      limit = 10
      current = self.get_from_inventory('oxen')
      if self.get_from_inventory('oxen') + amount > limit:
        print('You cannot have that many oxen')
        print('You have {} oxen and have a total of {} spots'.format(current,limit))
        print('Please enter a new amount')
        return False
      else:
        return True
    elif key == 'food':
      limit = 1000
      current = self.get_from_inventory('food')
      if self.get_from_inventory('food') + amount > limit:
        print('You cannot hold that much food')
        print('You have {} pounds and can hold {} pounds'.format(current,limit))
        print('Please enter a new amount')
        return False
      else:
        return True
    else:
      return True
   
  def print_status(self):
    print()
    print('---------- Status ----------')
    print('Date:', self.current_date)
    print('Miles Traveled:', self.miles_traveled)
    print('Miles to next landmark:', self.miles_to_next_mark)
    print('Rations: {} pounds per person'.format(self.rations))
    print('Food: {} pounds'.format(self.inventory['food']))
    print('Bullets: {}'.format(self.inventory['bullets']))
    print('Cash: ${}'.format("%.2f" %self.inventory['money']))
    print('Oxen: {}'.format(self.inventory['oxen']))
    print('Med-Kits: {}'.format(self.inventory['kits']))
    print('Spare Parts: {}'.format(self.inventory['parts']))
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
      
  def check_for_end_game(self,output=True):
    if self.get_from_inventory('food') <= 0:
      if output:
        print("You ran out of food")
        print("Your party starved to death")
      return True
    if self.get_from_inventory('oxen') <= 0:
      if output:
        print("You do not have any oxen left")
        print("You can no longer travel the trail")
      return True
    for member in self.members:
      if member.is_leader and not member.is_alive:
        if output:
          print("You cannot continue on the trail without your leader")
        return True

    if self.current_date >= self.end_date:
      if output:
        print("You did not make it to Oregon City by {}".format(self.end_date))
        print("Your party froze to death on the trail")
      return True
    return False
  
  
    
  
    