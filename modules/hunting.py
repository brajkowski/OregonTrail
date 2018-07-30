import random
import game_io as io
import puzzle

def hunt(player, debug=False):
  food = 0
  
  # Generate random food given for deer, bear, moose
  deer = random.randint(35,60)
  bear = random.randint(100,300)
  moose = random.randint(300,700)
  
  # Name, odds, food given, bullets consumed
  animals = [
      ('rabbit',2,2,10),
      ('fox',4,5,8),
      ('deer',5,deer,5),
      ('bear',10,bear,10),
      ('moose',20,moose,10)
      ]
  
  encountered = []
  for animal in animals:
    if did_encounter(animal[1]):
      encountered.append(animal)
  
  if debug == True:
    encountered = []
    for animal in animals:
      encountered.append(animal)
  
  if len(encountered) == 0:
    print("You didn't encounter any animals")
    return food
  else:
    print(create_string(encountered))
  
  for animal in encountered:
    print("Do you want to hunt the {}? (1) Yes (2) No".format(animal[0]))
    options = [1,2]
    response = io.get_input_int_protected(options)
    if response == 1:
      if player.get_from_inventory('bullets') >= 10:
        print("Win the guessing game to successfully hunt")
        if puzzle.did_win():
          food += animal[2]
          player.consume('bullets', animal[3])
          print("Food collected: {}".format(animal[2]))
          print("Bullets remaining: {}".format(player.get_from_inventory('bullets')))
      else:
        print("You need 10 or more bullets to hunt")
        return food
  return food
    
  
def did_encounter(chance):
  random.seed()
  num = random.randint(1,100)
  if num % chance == 0:
    return True
  return False

def create_string(encountered):
  string = "You encountered a "
  if len(encountered) == 1:
    return string + encountered[0][0]
  
  for i in range(len(encountered)):
    if i == len(encountered) - 1:
      return string + " and a {}".format(encountered[i][0])
    if i == 0:
      string += encountered[i][0]
    else:
      string += ", {}".format(encountered[i][0])