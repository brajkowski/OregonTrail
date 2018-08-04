"""
This module is the entry point for the game.  It handles the high level
game logic and acts as a controller for all of modules.
"""

import graphics
import game_io as io
import player
import random
import hunting
import misfortunes
from time import sleep

class engine():
  """
  Holds high level game state variables and lower level objects from modules.
  Runs the main game loop.
  
  Members:
    sleep (int): Amount of time to sleep between turns. Gives user time to read event messages.
    should_close (bool): Allows game to exit.
    did_win (bool): True if the player reached a win condition.
    did_quit (bool): True if the player ended the game early.
  """
  def __init__(self):


    self.messages = io.messages()
    self.player = player.player()
    self.sleep = 2
    self.should_close = False
    self.did_win = False
    self.did_quit = False
    self.gui = graphics.gui(player)
    
  def run_tests(self, debug=False):
    """
    Alternate way to run the engine to allow for debugging.
    
    Arguments:
      debug (bool) (optional): True will run the debug console input.
      
    Returns:
      None
    """
    self.player.load_debug()
    while not self.should_close: 
      self.gui.window.mainloop()
      self.gui.save_coordinates()
      #self.player.inventory['food'] = 1000
      #self.take_turn()
      
      # Run debug console input.
      if debug:
        debug_input = input("$ ")
        if debug_input == 'q':
          self.should_close = True
        if debug_input == '1':
          self.should_close = misfortunes.sickness(self.player)
        if debug_input == '2':
          self.player.update_inventory('kits',2)
    self.close()
      
  def new_game(self):
    """
    Welcomes user and allows them to enter player/member names.
    
    Arguments:
      None
      
    Returns:
      None
    """
    self.messages.print_message('welcome')
    sleep(self.sleep)
    
    # Party leader.
    print('What is your name?')
    self.player.members.append(player.member(io.get_input_string(),is_leader=True))
    
    # Party members.
    counts = ['first','second','third','fourth']
    for i in range(4):
      print('Please enter the name of your {} party member.'.format(counts[i]))
      self.player.members.append(player.member(io.get_input_string()))
  
  def store(self, fort=False):
    """
    Prints prices to player and allows them to make purchases.
    
    Arguments:
      fort (bool) (optional): True if the store is a fort store, otherwise its the start store.
    
    Returns:
      None
    """
    # Handle different messages to be printed.
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
    
    # Change prices and quantities for fort stores.
    if fort:
      increase = self.player.forts_visited * 0.25 # Prices increase further along trail.
      prices[0] = round(prices[0] / 2 + increase * prices[0],2)
      for i in range(1,len(prices)):
        prices[i] += round(prices[i] * increase,2)
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
    """
    Prompts user to proceed with standard start data or change to a custom date.
    
    Arguments:
      None
    
    Returns:
      None
    """
    print('Would you like to take off on {} (1) or on a different date (2)?'.format(self.player.current_date))
    options = [1,2]
    response = io.get_input_int_protected(options)
    if response == 1:
      return
    print("You can choose to start between March 1 and May 1")
    
    # Get month.
    print('Please enter what month you would like to start. \
          \n \t March (3) \
          \n \t April (4) \
          \n \t May   (5) \
          ')
    options = [3,4,5]
    response = io.get_input_int_protected(options)
    
    # Change dates allowed per game spec and real calendar days.
    days_allowed = 31
    if response == 4:
      days_allowed = 30
    if response == 5:
      days_allowed = 1
    
    # Get day.
    self.player.current_date = self.player.current_date.replace(month=response)
    print('Please enter what day you would like to start.')
    response = io.get_input_int(low = 1, high = days_allowed)
    self.player.current_date = self.player.current_date.replace(day=response)
  
  def take_turn(self):
    """
    Main menu for game. Allows user to pick what to do, updates mileage,
    checks for end-game scenarios, and chance for raider attack.
    
    Arguments:
      None
      
    Returns:
      None
    """
    sleep(self.sleep)
    self.player.print_status()
    
    # Handle turn options.
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
      self.did_quit = True
      return
    
    # Update mileage, check for end game and chance for raiders.
    self.player.update_miles_to_next()
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
    """
    Calls hunting module to hunt and handles updating amount of food.
    Allows player to adjust rations.
    
    Arguments:
      None
      
    Returns:
      None
    """
    current_food = self.player.get_from_inventory('food')
    
    # Hunt.
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
    
    # Consume food.
    food_consumed = self.player.members_alive * self.player.rations
    print("You consumed {} pounds of food".format(food_consumed))
    current_food -= food_consumed
    
    # Handle adding food to inventory.
    if current_food + hunted_food > 1000:
      print("The wagon can only hold 1000 pounds of food")
      left_food = hunted_food + current_food - 1000
      print("You left {} pounds of food behind".format(left_food))
      self.player.update_inventory('food', 1000)
    else:
      total_food = current_food + hunted_food
      self.player.update_inventory('food',total_food)
      
    # Advance one day and fully heal members.
    self.player.advance_time(1)
    self.player.heal_all_to_full_if_sick()
    
  def travel(self):
    """
    Travel random distance based on number of oxen.
    Handles encountered landmarks and win-condition.
    Adjusts food/mileage.
    
    Arguments:
      None
    
    Returns:
      None
    """
    random.seed()
    
    # Random mileage based on amount of oxen.
    lower = 70 + int(self.player.inventory['oxen']*5) # Lower bound ranges from 70-120.
    miles_to_travel = random.randint(lower,140)
    days_elapsed = 14
    food_consumed = self.player.members_alive * self.player.rations * days_elapsed

    # Travel and encounter landmark.
    if miles_to_travel >= self.player.miles_to_next_mark:
      location = self.player.get_next_location()
      original_miles = miles_to_travel
      miles_to_travel = self.player.miles_to_next_mark
      
      # Adjust food/days for arriving early.
      adjustment = float(miles_to_travel / original_miles)
      food_adjusted = int(food_consumed*adjustment)
      days_adjusted = int(days_elapsed*adjustment)
      
      # Update game-state with adjusted values.
      self.player.advance_time(days_adjusted)
      self.player.consume('food', food_adjusted)
      self.player.travel(miles_to_travel)
      self.player.heal_all_if_sick()
      self.player.update_miles_to_next()
      
      # Check for win condition.
      if self.player.miles_traveled >= self.player.win_mileage:
        self.should_close = True
        self.did_win = True
        # Check if lose condition should preceed win condition.
        if self.player.check_for_end_game(output=False):
          self.did_win = False
        else:
          print("You arrived at {}".format(location.name))
        return
      
      print('You were prepared to travel {} miles but arrived at {}'.format(original_miles, location.name))
      print('You consumed {} pounds of food'.format(food_adjusted))
      print('You traveled {} day(s)'.format(int(days_elapsed*adjustment)))

      # Handle encountering the landmark.
      if location.kind == 'Fort':
        self.at_fort()
      elif location.kind == 'River':
        self.at_river(location)
      elif location.kind == None:
        self.at_landmark()
      self.player.update_next_location()
    
    # Travel without encountering landmark.
    else:  
      print('You traveled {} miles in {} days'.format(miles_to_travel,days_elapsed))
      self.player.advance_time(days_elapsed)
      self.player.consume('food', food_consumed)
      print('You consumed {} pounds of food'.format(food_consumed))
      self.player.travel(miles_to_travel)
      self.player.heal_all_if_sick()
       
  def at_fort(self):
    """
    Handles fort options.
    
    Arguments:
      None
      
    Returns:
      None
    """
    # Allow infinite resting/shopping.
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
      
      # Check for lose conditions.
      if self.player.check_for_end_game(output=False):
        self.should_close = True

  def at_river(self, location):
    """
    Handles river options.  Calls misfortunes if player fails river crossing.
    
    Arguments:
      None
      
    Returns:
      None
    """
    river_height = location.height
    
    # Allow infinite resting and attempts at crossing river.
    while not self.should_close:
      self.player.print_status()
      print("River Height: {} feet".format(river_height))
      self.messages.print_message('river_options')
      options = [1,2,3,4]
      response = io.get_input_int_protected(options)
      # Rest.
      if response == 1:
        self.rest()
      
      # Ford.
      elif response == 2:
        if river_height > 3: # Fail fording rivers higher than 3ft.
          misfortunes.failed_river(self.player)
        else:
          print("You successfully forded the river")
          return
      
      # Chaulk and float.
      elif response == 3:
        # 65% chance of succesful floating.
        chance = 65
        n_chance = list(range(1,chance + 1))
        if random.randint(1,100) in n_chance:
          print("You successfully floated the river")
          return
        else:
          misfortunes.failed_river(self.player)
      
      # Ferry.
      elif response == 4:
        if self.player.can_consume('money',5):
          print("You took the ferry across")
          self.player.consume('money',5)
          return
        else:
          print("You do not have enough money")
      
      # Check for end game conditions.
      if self.player.check_for_end_game(output=False):
        self.should_close = True
   
  def at_landmark(self):
    """
    Handles landmark options.
    
    Arguments:
      None
      
    Returns:
      None
    """
    # Allow infinite resting.
    while not self.should_close:
      self.player.print_status()
      self.messages.print_message('landmark_options')
      options = [1,2]
      response = io.get_input_int_protected(options)
      
      # Rest.
      if response == 1:
        self.rest()
      
      # Continue.
      elif response == 2:
        return
      
      # Check for end game.
      if self.player.check_for_end_game(output=False):
        self.should_close = True
    
  def rest(self):
    """
    Advances time a random amount and consumes the appropiate amount of food.
    
    Arguments:
      None
    
    Returns:
      None
    """
    random.seed()
    
    # Rest between 1,3 days, calculate food consumed.
    days_to_sleep = random.randint(1,3)
    food_consumed = self.player.members_alive * self.player.rations * days_to_sleep
    print('You decided to rest for {} day(s)'.format(days_to_sleep))
    print('You consumed {} pounds of food'.format(food_consumed))
    
    # Update game-state.
    self.player.advance_time(days_to_sleep)
    self.player.consume('food', food_consumed)
    self.player.heal_all_to_full_if_sick()
    
  def run(self):
    """
    Main game loop.
    
    Arguments:
      None
      
    Returns:
      None
    """
    self.new_game()
    self.store()
    self.pick_start_date()
    while not self.should_close:
      self.take_turn()
    self.close()
    
  def close(self):
    """
    Report game win/lose/quit to player and perform any cleanup.
    Exit point for program.
    
    Arguments:
      None
      
    Returns:
      None
    """
    if self.did_win:
      print("Congratulations you successfully navigated the trail!")
    elif not self.did_quit:
      print("Sorry, you have lost the game. Play again soon!")
    elif self.did_quit:
      print("Sorry you had to leave early. Play again soon!")
    input("Enter any key to exit \n>>> ")
    
    # Perform cleanup.
    self.gui.close()

def main():
  """
  Program entry point.
  
  Arguments:
    None
  
  Returns:
    None
  """
  e = engine()
  #e.run()
  e.run_tests(debug=True)
  
# Define program entry point.
if __name__ == "__main__":
  main()
