import graphics
import game_io as io
import player
import random
import hunting
import misfortunes
from time import sleep

class engine():
  def __init__(self):
    self.gui = graphics.gui()
    self.messages = io.messages()
    self.player = player.player()
    self.sleep = 2
    self.should_close = False
    self.did_win = False
    self.rations = 3
    
  def run_tests(self, debug=False):
    self.player.load_debug()
    while not self.should_close: 
      #self.player.inventory['food'] = 1000
      self.take_turn()
      if debug:
        debug_input = input("$ ")
        if debug_input == 'q':
          self.should_close = True
        if debug_input == '1':
          self.should_close = misfortunes.sickness(self.player)
        if debug_input == '2':
          self.player.update_inventory('kits',2)
      
  def new_game(self):
    self.messages.print_message('welcome')
    sleep(self.sleep)
    print('What is your name?')
    self.player.members.append(player.member(io.get_input_string(),is_leader=True))
    counts = ['first','second','third','fourth']
    for i in range(4):
      print('Please enter the name of your {} party member.'.format(counts[i]))
      self.player.members.append(player.member(io.get_input_string()))
  
  def store(self, fort=False):
    if not fort:
      key = 'start_store'
      self.messages.print_message('store_welcome')
    elif fort:
      self.player.forts_visited += 1
      key ='fort_store'
      key += "_{}".format(self.player.forts_visited)
    
    message_count = self.messages.get_message_parsed_count(key)
    
    # Manually set order and attributes for buying items.
    keys = ['oxen','food','bullets','parts','kits']
    prices = [40,0.5,2,10,15]
    quants = [2,1,20,1,1]
    subtotal = 0.0
    if fort:
      increase = self.player.forts_visited * 0.25
      prices[0] = round(prices[0] / 2 + increase * prices[0],2)
      for i in range(1,len(prices)):
        prices[i] += round(prices[i] * increase,2)
      #prices = [120,1.5,6,30,45]
      quants = [1,1,20,1,1]

    # Handle special case for buying yokes.
    if not fort:
      while True:
        try:
          self.messages.print_message_parsed(key,0)
          response = io.get_input_int(low=0)
          amount = response * prices[0]
          if not(100 <= amount and amount <= 200):
            raise Exception()
          break 
        except Exception:
          print("You tried to spend ${} on oxen.".format("%.2f" %amount))
      subtotal += amount
      self.player.update_inventory(keys[0],response*quants[0])
      self.player.consume('money', amount)
      print("Sub-total: ${}".format("%.2f" %subtotal))
    
    # Handle the rest of the store buying options.
    if not fort:
      start_range = range(1,message_count)
    elif fort:
      start_range = range(0,message_count)
    for i in start_range:
      self.messages.print_message_parsed(key,i)
      while True:
        try:
          response = io.get_input_int(low=0)
          quant = response * quants[i]
          amount = response * prices[i]
          if not self.player.can_consume('money',amount):
            raise AssertionError
          if not self.player.can_add_to_inventory(keys[i],quant):
            raise ValueError
          break
        except AssertionError:
          print("You don't enough money, please enter a new amount.")
        except ValueError:
          pass
      subtotal += amount
      self.player.add_to_inventory(keys[i],response*quants[i])
      self.player.consume('money', amount)      
      print("Sub-total: ${}".format("%.2f" %subtotal))
    print("Total: ${}".format("%.2f" %subtotal))
    
    
  def pick_start_date(self):
    print('Would you like to take off on {} (1) or on a different date (2)?'.format(self.player.current_date))
    options = [1,2]
    response = io.get_input_int_protected(options)
    if response == 1:
      return
    print("You can choose to start between March 1 and May 1")
    print('Please enter what month you would like to start. \
          \n \t March (3) \
          \n \t April (4) \
          \n \t May   (5) \
          ')
    options = [3,4,5]
    response = io.get_input_int_protected(options)
    days_allowed = 31
    if response == 4:
      days_allowed = 30
    if response == 5:
      days_allowed = 1
    self.player.current_date = self.player.current_date.replace(month=response)
    print('Please enter what day you would like to start.')
    response = io.get_input_int(low = 1, high = days_allowed)
    self.player.current_date = self.player.current_date.replace(day=response)
  
  def take_turn(self):
    sleep(self.sleep)
    self.player.print_status()
    self.messages.print_message('turn_options')
    options = [1,2,3,4]
    response = io.get_input_int_protected(options)
    if response == 1:
      self.rest()
    elif response == 2:
      self.travel()
    elif response == 3:
      self.hunt()
    elif response == 4:
      self.should_close = True
    
    # Perform general turn events here.
    self.player.update_miles_to_next()
    #current_food = self.player.get_from_inventory('food')
    #if current_food <= 0:
    #  print("You ran out of food")
    #  print("Your party starved to death")
    #  self.should_close = True
    if self.player.check_for_end_game():
      self.should_close = True
      return
    if misfortunes.randomize(self.player):
      self.should_close = True
      return
    if self.player.check_for_end_game():
      self.should_close = True
      return
    misfortunes.raider_attack(self.player)
      
  def hunt(self):
    current_food = self.player.get_from_inventory('food')
    hunted_food = hunting.hunt(self.player)
    print("You returned with {} pounds of food".format(hunted_food))
    
    # Adjust rations.
    self.messages.print_message('rations')
    options = [1,2,3]
    response = io.get_input_int_protected(options)
    if response == 1:
      self.player.rations = 2
    elif response == 2:
      self.player.rations = 3
    elif response == 3:
      self.player.rations = 5
      
    food_consumed = self.player.members_alive * self.player.rations
    print("You consumed {} pounds of food".format(food_consumed))
    current_food -= food_consumed
    
    if current_food + hunted_food > 1000:
      print("The wagon can only hold 1000 pounds of food")
      left_food = hunted_food + current_food - 1000
      print("You left {} pounds of food behind".format(left_food))
      self.player.update_inventory('food', 1000)
    else:
      total_food = current_food + hunted_food
      self.player.update_inventory('food',total_food)
    self.player.advance_time(1)
    self.player.heal_all_to_full_if_sick()
    
  def travel(self):
    random.seed()
    miles_to_travel = random.randint(70,140)
    days_elapsed = 14
    food_consumed = self.player.members_alive * self.player.rations * days_elapsed


    
    if miles_to_travel >= self.player.miles_to_next_mark:
      location = self.player.get_next_location()
      print('You were prepared to travel {} miles but arrived at {}'.format(miles_to_travel, location.name))
      original_miles = miles_to_travel
      miles_to_travel = self.player.miles_to_next_mark
      adjustment = float(miles_to_travel / original_miles)
      
      food_adjusted = int(food_consumed*adjustment)
      days_adjusted = int(days_elapsed*adjustment)
      
      self.player.advance_time(days_adjusted)
      self.player.consume('food', food_adjusted)
      print('You consumed {} pounds of food'.format(food_adjusted))
      self.player.travel(miles_to_travel)
      print('You traveled {} day(s)'.format(int(days_elapsed*adjustment)))
      self.player.heal_all_if_sick()
      self.player.update_miles_to_next()
      
      if self.player.miles_traveled >= self.player.win_mileage:
        self.should_close = True
        self.did_win = True
        return
     
      
      if location.kind == 'Fort':
        self.at_fort()
      elif location.kind == 'River':
        self.at_river(location)
      elif location.kind == None:
        self.at_landmark()
      self.player.update_next_location()
      
    else:  
      print('You traveled {} miles in {} days'.format(miles_to_travel,days_elapsed))
      self.player.advance_time(days_elapsed)
      self.player.consume('food', food_consumed)
      print('You consumed {} pounds of food'.format(food_consumed))
      self.player.travel(miles_to_travel)
      self.player.heal_all_if_sick()
    
    
  def at_fort(self):
    while not self.should_close:
      self.player.print_status()
      self.messages.print_message('fort_options')
      options = [1,2,3]
      response = io.get_input_int_protected(options)
      if response == 1:
        self.rest()
      elif response == 2:
        self.store(fort=True)
      elif response == 3:
        return
      if self.player.check_for_end_game(output=False):
        self.should_close = True

  def at_river(self, location):
    river_height = location.height
    while not self.should_close:
      self.player.print_status()
      print("River Height: {} feet".format(river_height))
      self.messages.print_message('river_options')
      options = [1,2,3,4]
      response = io.get_input_int_protected(options)
      if response == 1:
        self.rest()
      elif response == 2:
          if river_height > 3:
            misfortunes.failed_river(self.player)
          else:
            print("You successfully forded the river")
            return
      elif response == 3:
          chance = 65
          n_chance = list(range(1,chance + 1))
          if random.randint(1,100) in n_chance:
            print("You successfully floated the river")
            return
          else:
            misfortunes.failed_river(self.player)
      elif response == 4:
          if self.player.can_consume('money',5):
            print("You took the ferry across")
            self.player.consume('money',5)
            return
          else:
            print("You do not have enough money")
      if self.player.check_for_end_game(output=False):
        self.should_close = True
   
  def at_landmark(self):
    while not self.should_close:
      self.player.print_status()
      self.messages.print_message('landmark_options')
      options = [1,2]
      response = io.get_input_int_protected(options)
      if response == 1:
        self.rest()
      elif response == 2:
        return
      if self.player.check_for_end_game(output=False):
        self.should_close = True
    
  def rest(self):
    random.seed()
    days_to_sleep = random.randint(1,3)
    food_consumed = self.player.members_alive * self.player.rations * days_to_sleep
    print('You decided to rest for {} day(s)'.format(days_to_sleep))
    print('You consumed {} pounds of food'.format(food_consumed))
    
    self.player.advance_time(days_to_sleep)
    self.player.consume('food', food_consumed)
    self.player.heal_all_to_full_if_sick()
    
  def run(self):
    self.new_game()
    self.store()
    self.pick_start_date()
    while not self.should_close:
      self.take_turn()
    self.close()
    
  def close(self):
    if self.did_win:
      print("Congratulations you win!")
    else:
      print("Sorry, you have lost the game. Play again soon!")
    self.gui.close()

def main():
  e = engine()
  #e.run()
  e.run_tests(debug=False)
  
  
if __name__ == "__main__":
  main()
