import game_io as io
import random

def did_win():
  random.seed()
  number = random.randint(1,10)
  guesses = 3
  options = [1,2,3,4,5,6,7,8,9,10]
  for i in range(guesses):
    print("Guess a number between 1 and 10 ({} guesses remaining)".format(guesses))
    response = io.get_input_int_protected(options)
    if response == number:
      print("You win!")
      return True
    guesses -= 1
  print("Better luck next time.")
  return False