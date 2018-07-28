import graphics
import game_io
import player
import locations
from time import sleep

class engine():
  def __init__(self):
    self.gui = graphics.gui()
    self.io = game_io.manager()
    self.player = player.player()
    self.sleep = 2
    
  def run_tests(self):
    self.player.load_debug()
    self.player.print_locations()
    pass
  
  def new_game(self):
    self.io.print_message('welcome')
    sleep(self.sleep)
    print('What is your name?')
    self.player.names.append(self.io.get_input_string())
    counts = ['first','second','third','fourth']
    for i in range(4):
      print('Please enter the name of your {} party member.'.format(counts[i]))
      self.player.names.append(self.io.get_input_string())
  
  def start_store(self):
    self.gui.update()
    key = 'start_store'
    self.io.print_message('store_welcome')
    sleep(self.sleep)
    
    message_count = self.io.get_message_parsed_count(key)
    
    # Manually set order and attributes for buying items.
    keys = ['oxen','food','bullets','parts','kits']
    prices = [40,0.5,2,10,15]
    quants = [2,1,20,1,1]
    subtotal = 0.0
    
    # Handle special case for buying yokes.
    while True:
      try:
        self.io.print_message_parsed(key,0)
        response = self.io.get_input_int(low=0)
        amount = response * prices[0]
        if not(100 <= amount and amount <= 200):
          raise Exception()
        break 
      except Exception:
        print("You spent ${} on oxen.".format(amount))
        print()
    subtotal += amount
    self.player.update_inventory(keys[0],response*quants[0])
    self.player.spend_money(amount)
    print("Sub-total: ${}".format(subtotal))
    
    # Handle the rest of the store buying options.
    for i in range(1,message_count):
      self.io.print_message_parsed(key,i)
      while True:
        try:
          response = self.io.get_input_int(low=0)
          amount = response * prices[i]
          if not self.player.can_spend(amount):
            raise Exception()
          break
        except Exception:
          print("You don't enough money, please enter a new amount.")
      subtotal += amount
      self.player.update_inventory(keys[i],response*quants[i])
      self.player.spend_money(amount)
      
      print("Sub-total: ${}".format(subtotal))
    print("Total: ${}".format(subtotal))
    
    self.player.print_inventory()
      
  def pick_start_date(self):
    print('Would you like to take off on {} (1) or on a different date (2)?'.format(self.player.current_date))
    options = [1,2]
    response = self.io.get_input_int_protected(options)
    if response == 1:
      return
    print('Please enter what month you would like to start. \
          \n \t March (3) \
          \n \t April (4) \
          \n \t May   (5) \
          ')
    options = [3,4,5]
    response = self.io.get_input_int_protected(options)
    days_allowed = 31
    if response == 4:
      days_allowed = 30
    self.player.current_date = self.player.current_date.replace(month=response)
    print('Please enter what day you would like to start.')
    response = self.io.get_input_int(low = 1, high = days_allowed)
    self.player.current_date = self.player.current_date.replace(day=response)
  
  def take_turn(self):
    self.player.print_status()
    self.io.print_message('turn_options')
    options = [1,2,3]
    response = self.io.get_input_int_protected(options)
    print('Debug: user chose to:',response)
    # TODO: handle turn options
    
  
  def run(self):
    self.new_game()
    #sleep(self.sleep)
    self.start_store()
    self.pick_start_date()
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
