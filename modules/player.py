"""
This module is responsible for defining the member and player classes.
"""

import datetime
import locations

class member():
  """
  Keeps track of members health/status.
  
  Members:
    name (string): member name.
    is_alive (bool): True if member is alive, False otherwise.
    is_sick (bool): True if member is sick, False if healthy.
    status (string): Text description of status.
    is_leader (bool): True if the member is the leader, false if normal member.
    turns_to_healthy (int): Number of turns left before member is fully healed.
  """
  def __init__(self, name, is_leader=False):
    self.name = name
    self.is_alive = True
    self.is_sick = False
    self.status = "Healthy"
    self.is_leader = is_leader
    self.turns_to_healthy = 5
    
  def gets_sick(self,sickness):
    """
    Changes member status to be sick and handles member dying.
    
    Arguments:
      sickness (string): Name of sickness.
      
    Returns:
      None
    """
    self.turns_to_healthy = 5
    if self.is_sick:
      self.dies(sickness)
    else:
      self.is_sick = True
      self.status = "Has {}".format(sickness)
    
  def dies(self, sickness):
    """
    Updates member status to be deceased.
    
    Argument:
      sickness (string): Name of second sickness (not used)
    
    Returns:
      None
    """
    print("{} died from multiple illnesses".format(self.name))
    self.status = "Deceased"
    self.is_alive = False
    
  def drown(self):
    """
    Updates member status to be deceased.
    
    Arguments:
      None
      
    Returns:
      None
    """
    print("{} drowned".format(self.name))
    self.status = "Deceased"
    self.is_alive = False
    
  def use_med_kit(self):
    """
    Changes the amound of time to become healthy.
    
    Arguments:
      None
    
    Returns:
      None
    """
    self.turns_to_healthy = 2
    
  def heal_if_sick(self):
    """
    Protected way to heal members.  Only heals for 1 turn.
    
    Arguments:
      None
    
    Returns:
      None
    """
    if self.is_sick:
      self.turns_to_healthy -= 1
      
      # Handle full health.
      if self.turns_to_healthy == 0:
        self.status = "Healthy"
        self.turns_to_healthy = 5
        self.is_sick = False
        print("{} is back to full health".format(self.name))
        
  def heal_to_full_if_sick(self):
    """
    Protected way to fully heal members.
    
    Arguments:
      None
      
    Returns:
      None
    """
    if self.is_sick:
      self.turns_to_healthy = 5
      self.status = "Healthy"
      self.is_sick = False
      print("{} is back to full health".format(self.name))
      
  def print_status(self):
    """
    Debug method. (not used)
    """
    print("{}: {} (Leader={}, Days to FH={})".format(self.name,self.status,self.is_leader,self.turns_to_healthy))


class player():
  """
  Keeps track of game-state variables.
  
  Members:
    inventory {}: Dictionary for all inventory items.
    next_location (int): Tracks the next location to be encountered.
    members []: List of all party members.
    current_date (datetime.date): Tracks current date.
    end_date (datetime.date): Date for end-game condition.
    miles_traveled (int): Tracks current mileage.
    locations []: List of all locations that can be encountered (chronological order).
    members_alive (int): Number of party members currently alive.
    rations (int): Rate of food consumption (per person per day).
    forts_visited (int): Tracks how many forts have already been visited.
    win_mileage (int): Defines win game condition value.
    is_halfway (bool): True if player is halfway to next landmark from previous. (for GUI)
  """
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
    self.rations = 3
    self.forts_visited = 0
    self.win_mileage = 2040
    self.is_halfway = False
    
    self.update_miles_to_next()
  
  def load_debug(self):
    """
    Loads game state variables with custom amounts for debugging purposes.
    
    Arguments:
      None
    
    Returns:
      none
    """
    self.inventory = {
        'food':1000,
        'money':1000,
        'bullets':500,
        'oxen':10,
        'kits':2,
        'parts':2
        }
    self.next_location = 0
    self.members = [member('This',is_leader=True),member('Is'),member('A'),member('Debug'),member('Test')]
    self.current_date = datetime.date(1847,3,1)
    self.end_date = datetime.date(1847,11,30)
    self.miles_traveled = 0
    self.locations = locations.parse_locations()
    self.members_alive = 5
    self.update_miles_to_next()
    self.rations = 2
    self.forts_visited = 0
    self.win_mileage = 2040
    
  def print_locations(self):
    """
    Prints all of the game location details for debugging purposes.
    
    Arguments:
      None
    
    Returns:
      None
    """
    for location in self.locations:
      location.describe()
  
  def get_from_inventory(self,key):
    """
    Returns current amount of an item in the inventory.
    
    Arguments:
      key (string): Inventory item name.
      
    Returns:
      float or int: Current amount of item.
    """
    return self.inventory[key]
  
  def update_inventory(self,key,value):
    """
    Sets the amount of an item in the inventory.
    
    Arguments:
      key (string): Inventory item name.
      value (float or int): New amount of item.
      
    Returns:
      None
    """
    self.inventory[key] = value
    
  def can_consume(self,key, amount):
    """
    Checks if player can lose an amount of an item.
    
    Arguments:
      key (string): Inventory item name.
      amount (float or int): Amount of item to lose.
      
    Returns:
      bool: True if player has more than enough of item to lose.
    """
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
    """
    Ensures oxen and food limits are not violated.
    
    Arguments:
      key (string): Inventory item name.
      amount (float or int): Amount pending addition.
      
    Returns:
      float or int: Current amount of item.
    """
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
    print('---------- Status ---------- \t ---------- Members ---------')
    print('Date:', self.current_date, "\t\t {}: {} (leader)".format(self.members[0].name,self.members[0].status))
    print('Miles Traveled:', self.miles_traveled, "\t\t {}: {}".format(self.members[1].name,self.members[1].status))
    print('Miles to next landmark:', self.miles_to_next_mark,"\t {}: {}".format(self.members[2].name,self.members[2].status))
    print('Rations: {} pounds per person'.format(self.rations),"\t {}: {}".format(self.members[3].name,self.members[3].status))
    print('Food: {} pounds'.format(self.inventory['food']),"\t\t {}: {}".format(self.members[4].name,self.members[4].status))
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
    self.is_halfway = False # Reset for GUI purposes.
  
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
  
  def should_draw_halfway(self):
    """
    Used to determine if GUI route should be updated to halfway.
    
    Arguments:
      None
      
    Returns:
      bool: True if GUI should update route to display halfway point.
    """
    # Don't draw halfway if already past halfway.
    if self.is_halfway:
      return False
    
    # Calculate if player is more than halfway to next landmark from previous.
    prev_loc = self.locations[self.next_location - 1]
    next_loc = self.locations[self.next_location]
    prev_miles = prev_loc.mileage
    next_miles = next_loc.mileage
    ratio = (self.miles_traveled - prev_miles) / (next_miles - prev_miles)
    if ratio >= 0.5:
      self.is_halfway = True
      return True
    return False
    
  
  def check_for_end_game(self,output=True):
    """
    Check game-state for any end game conditions.
    
    Arguments:
      output (bool) (optional): True if messages should be printed to console.
      
    Returns:
      bool: True if the game should end, false otherwise.
    """
    # No food.
    if self.get_from_inventory('food') <= 0:
      if output:
        print("You ran out of food")
        print("Your party starved to death")
      return True
    
    # No oxen.
    if self.get_from_inventory('oxen') <= 0:
      if output:
        print("You do not have any oxen left")
        print("You can no longer travel the trail")
      return True
    
    # Leader died.
    for member in self.members:
      if member.is_leader and not member.is_alive:
        if output:
          print("You cannot continue on the trail without your leader")
        return True

    # End date.
    if self.current_date >= self.end_date:
      if output:
        print("You did not make it to Oregon City by {}".format(self.end_date))
        print("Your party froze to death on the trail")
      return True
    return False
  
  
    
  
    