"""
This modules is responsible for the hunting mini-game.
"""

import random
import game_io as io
import puzzle

def hunt(player):
  """
  Entry-point into hunting module from the engine.
  Defines animals, encounter chance, food given, and bullets required.
  
  Arguments:
    player (player.player): Used to interface with the game-state.
  
  Returns:
    int: Amount of food obtained from hunting.
  """
  food = 0
  
  # Generate random food given for deer, bear, moose.
  deer = random.randint(35,60)
  bear = random.randint(100,300)
  moose = random.randint(300,700)
  
  # (Name, % chance, food given, bullets consumed)
  animals = [
      ('rabbit',50,2,10),
      ('fox',25,5,8),
      ('deer',20,deer,5),
      ('bear',10,bear,10),
      ('moose',5,moose,10)
      ]
  
  # Generate encountered animals
  encountered = []
  for animal in animals:
    if did_encounter(animal[1]):
      encountered.append(animal)
  
  # Handle no animals encountered.
  if len(encountered) == 0:
    print("You didn't encounter any animals")
    return food
  
  # Prompt user to hunt each animal and play hunting puzzle.
  else:
    print(create_string(encountered))
  for animal in encountered:
    print("Do you want to hunt the {}? (1) Yes (2) No".format(animal[0]))
    options = [1,2]
    response = io.get_input_int_protected(options)
    if response == 1:
      # Only allow hunt if player has enough bullets.
      if player.get_from_inventory('bullets') >= 10:
        print("Win the guessing game to successfully hunt")
        if puzzle.did_win():
          food += animal[2]
          player.consume('bullets', animal[3])
          print("Food collected: {} pounds".format(animal[2]))
          print("Bullets remaining: {}".format(player.get_from_inventory('bullets')))
      else:
        print("You need 10 or more bullets to hunt")
        return food
  return food
    
  
def did_encounter(chance):
  """
  Decides whether animal is encountered based on a given probability.
  
  Arguments:
    chance (int): Probability that the animal is encountered.
    
  Returns:
    bool: True if animal is encountered, false if not encountered.
  """
  random.seed()
  
  # Generate number list based on chance and see if random number is inside.
  num = random.randint(1,100)
  if num in list(range(1,chance + 1)):
    return True
  return False

def create_string(encountered):
  """
  Creates formatted message of encountered animals for console output.
  
  Arguments:
    encountered []: List of animals encountered while hunting.
    
  Returns:
    string: Formatted message informing user of all the animals encountered.
  """
  string = "You encountered a "
  
  # Single animal.
  if len(encountered) == 1:
    return string + encountered[0][0]
  
  # Multiple animals.
  for i in range(len(encountered)):
    if i == len(encountered) - 1:
      return string + " and a {}".format(encountered[i][0])
    if i == 0:
      string += encountered[i][0]
    else:
      string += ", {}".format(encountered[i][0])