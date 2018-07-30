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
    self.rations = 3
    
  def run_tests(self):
    self.player.load_debug()
    while not self.should_close:
      self.take_turn()
      misfortunes.randomize(self.player)
      """
      misfortunes.sickness(self.player.names)
      misfortunes.bad_weather()
      misfortunes.oxen_dies()
      misfortunes.theif_attacks()
      misfortunes.wagon_breaks()
      """
    pass
  
  def new_game(self):
    self.messages.print_message('welcome')
    sleep(self.sleep)
    print('What is your name?')
    self.player.names.append(io.get_input_string())
    counts = ['first','second','third','fourth']
    for i in range(4):
      print('Please enter the name of your {} party member.'.format(counts[i]))
      self.player.names.append(io.get_input_string())
  
  def start_store(self):
    self.gui.update()
    key = 'start_store'
    self.messages.print_message('store_welcome')
    sleep(self.sleep)
    
    message_count = self.messages.get_message_parsed_count(key)
    
    # Manually set order and attributes for buying items.
    keys = ['oxen','food','bullets','parts','kits']
    prices = [40,0.5,2,10,15]
    quants = [2,1,20,1,1]
    subtotal = 0.0
    
    # Handle special case for buying yokes.
    while True:
      try:
        self.messages.print_message_parsed(key,0)
        response = io.get_input_int(low=0)
        amount = response * prices[0]
        if not(100 <= amount and amount <= 200):
          raise Exception()
        break 
      except Exception:
        print("You spent ${} on oxen.".format(amount))
        print()
    subtotal += amount
    self.player.update_inventory(keys[0],response*quants[0])
    self.player.consume('money', amount)
    print("Sub-total: ${}".format(subtotal))
    
    # Handle the rest of the store buying options.
    for i in range(1,message_count):
      self.messages.print_message_parsed(key,i)
      while True:
        try:
          response = io.get_input_int(low=0)
          amount = response * prices[i]
          if not self.player.can_consume('money',amount):
            raise Exception()
          break
        except Exception:
          print("You don't enough money, please enter a new amount.")
      subtotal += amount
      self.player.update_inventory(keys[i],response*quants[i])
      self.player.consume('money', amount)
      
      print("Sub-total: ${}".format(subtotal))
    print("Total: ${}".format(subtotal))
    
    self.player.print_inventory()
      
  def pick_start_date(self):
    print('Would you like to take off on {} (1) or on a different date (2)?'.format(self.player.current_date))
    options = [1,2]
    response = io.get_input_int_protected(options)
    if response == 1:
      return
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
    self.player.current_date = self.player.current_date.replace(month=response)
    print('Please enter what day you would like to start.')
    response = io.get_input_int(low = 1, high = days_allowed)
    self.player.current_date = self.player.current_date.replace(day=response)
  
  def take_turn(self):
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
      
  
  # TODO: Develop turn options.
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
    # TODO: Add recovery.
      
  def travel(self):
    random.seed()
    miles_to_travel = random.randint(70,140)
    days_elapsed = 14
    food_consumed = self.player.members_alive * self.player.rations * days_elapsed
    
    if miles_to_travel > self.player.miles_to_next_mark:
      location = self.player.get_next_location()
      print('You were prepared to travel {} miles but arrived at {}'.format(miles_to_travel, location.name))
      miles_to_travel = self.player.miles_to_next_mark
      self.player.update_next_location()
    else:  
      print('You traveled {} miles in {} days'.format(miles_to_travel,days_elapsed))
    print('You consumed {} pounds of food'.format(food_consumed))
    
    self.player.advance_time(days_elapsed)
    self.player.consume('food', food_consumed)
    self.player.travel(miles_to_travel)
    
  def rest(self):
    random.seed()
    days_to_sleep = random.randint(1,3)
    food_consumed = self.player.members_alive * self.player.rations * days_to_sleep
    print('You decided to rest for {} day(s)'.format(days_to_sleep))
    print('You consumed {} pounds of food'.format(food_consumed))
    
    self.player.advance_time(days_to_sleep)
    self.player.consume('food', food_consumed)
    # TODO: Add recovery.
    
  def run(self):
    self.new_game()
    #sleep(self.sleep)
    self.start_store()
    self.pick_start_date()
    while not self.should_close:
      self.take_turn()
    self.close()
    
  def close(self):
    self.gui.close()

def main():
  e = engine()
  #e.run()
  e.run_tests()
  
  
if __name__ == "__main__":
  main()
