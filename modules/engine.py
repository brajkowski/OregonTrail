import gui
import game_io
import player

class engine(object):
  def __init__(self):
    self.io = game_io.manager()
    self.p = player.player()
    
  def run_tests(self):
    # Add any random tests here.
    pass
  
  def start_store(self):
    key = 'start_store'
    self.io.print_message(key)
    message_count = self.io.get_message_parsed_count(key)
    prices = [40,0.5,2,10,15]
    quants = [2,1,20,1,1]
    subtotal = 0.0
    
    # Handle special case for buying yokes.
    while True:
      try:
        self.io.print_message_parsed(key,0)
        response = self.io.get_input_int()
        amount = response * prices[0]
        if not(100 <= amount and amount <= 200):
          raise Exception()
        break
      except Exception:
        print("You spent ${} on oxen.".format(amount))
        print()
        
    subtotal += amount
    print("Sub-total: {}".format(subtotal))
    for i in range(1,message_count):
      self.io.print_message_parsed(key,i)
      response = self.io.get_input_int()
      amount = response * prices[i]
      subtotal += amount
      print("Sub-total: {}".format(subtotal))
    print("Total: {}".format(subtotal))
      
      
      
    

  def start(self):
    self.io.print_message('welcome')
    self.start_store()
  

def main():
  e = engine()
  e.start()
  
  
if __name__ == "__main__":
  main()
