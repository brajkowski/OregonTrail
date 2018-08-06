"""
This module is responsible for the puzzle mini-game.
"""

import game_io as io
import random

def did_win():
  """
  Entry point into the puzzle mini-game.
  
  Arguments:
    None
    
  Returns:
    bool: True if the player wins the puzzle mini-game, False otherwise.
  """
  random.seed()
  
  # Initialize.
  number = random.randint(1,10)
  guesses = 3
  guesses_remaining = guesses
  options = [1,2,3,4,5,6,7,8,9,10]
  
  print("Guess a number between 1 and 10 ({} guesses remaining)".format(guesses_remaining))
  for i in range(guesses):
    response = io.get_input_int_protected(options)
    guesses_remaining -= 1
    
    # Handle winning and give hints.
    if response == number:
      print("You win!")
      return True
    elif response > number and i < guesses - 1:
      print("Try a lower number ({} guesses remaining)".format(guesses_remaining))
    elif response < number and i < guesses - 1:
      print("Try a higher number ({} guesses remaining)".format(guesses_remaining))
  
  # Handle losing.
  print("Better luck next time.")
  return False