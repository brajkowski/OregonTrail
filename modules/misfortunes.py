"""
This module is responsible for all of the random events that occur in the game.
"""

import random
import puzzle
from game_io import get_input_int_protected

def randomize(player):
  """
  Main entry-point for random events from the game engine.
  Determines if a random event should occur and randomly selects one.
  
  Arguments:
    player (player.player): Used to interface with the game-state.
    
  Returns:
    None
  """
  random.seed()
  
  # Determine if random event occurs.
  chance = list(range(1,31)) # 30% chance.
  number = random.randint(1,100)
  if not(number in chance):
    return
  
  # List random event functions.
  misfortunes = [
      sickness,
      oxen_dies,
      thief_attacks,
      wagon_breaks,
      bad_weather,
      fortune
      ]
  
  # Randomly pick one event to occur.
  i_misfortune = random.randint(0,len(misfortunes)-1)
  misfortune = misfortunes[i_misfortune]
  misfortune(player)

def sickness(player):
  """
  Causes a random party-member to become ill with a random disease.
  
  Arguments:
    player (player.player): Used to interface with the game-state.
    
  Returns:
    None
  """
  random.seed()
  
  # Create names of diseases.
  diseases = [
      'typhoid',
      'cholera',
      'diarrhea',
      'measles',
      'dysentery',
      'fever']
  
  # Randomly select a party-member.
  choices = []
  for i in range(len(player.members)):
    if player.members[i].is_alive:
      choices.append(i)
  i_name = random.choice(choices)
      
  # Randomly select a disease.
  disease = random.choice(diseases)
  
  # Inform player and make party member sick.
  name = player.members[i_name].name
  print("{} has {}".format(name,disease))
  player.members[i_name].gets_sick(disease)
  
  # Reduce heal-time if player has med-kits.
  if player.get_from_inventory('kits') > 0:
    player.members[i_name].use_med_kit()
    remaining = player.consume('kits',1)
    print("You used a med-kit on {}".format(name))
    print("You have {} med-kit(s) remaining".format(remaining))
  
def oxen_dies(player):
  """
  Removes an oxen from the players inventory.
  
  Arguments:
    player (player.player): Used to interface with the game-state.
    
  Returns:
    None
  """
  print("An oxen has died")
  oxen_available = player.get_from_inventory('oxen')
  
  # Avoids printing negative numbers to player.
  if oxen_available > 1:
    remaining = player.consume('oxen',1)
    print("You have {} oxen remaining".format(remaining))

def thief_attacks(player):
  """
  Removes a random amount of food from the player's inventory.
  
  Arguments:
    player (player.player): Used to interface with the game-state.
    
  Returns:
    None
  """
  random.seed()
  
  # Determine how much food is stolen within bounds.
  amount = random.randint(10,25)
  food_available = player.get_from_inventory('food')
  if food_available >= amount:
    print("A thief has stolen {} pounds of food".format(amount))
    remaining = player.consume('food',amount)
    print("You have {} pounds of food remaining".format(remaining))
  else:
    # Avoids negative inventory.
    print("A thief stole the remainder of your food")
    player.consume('food',food_available)

def wagon_breaks(player):
  """
  Random part on wagon breaks and ends game if player cannot fix it.
  
  Arguments:
    player (player.player): Used to interface with the game-state.
    
  Returns:
    bool: True if the game should end from not being able to repair the wagon.
  """
  random.seed()
  
  # Create part names.
  parts = [
      'wheel',
      'axel',
      'tongue'
      ]
  
  # Randomly select a part name.
  part = random.choice(parts)

  # Inform player and handle wagon break end game.  
  print("A wagon {} broke".format(part))
  parts_available = player.get_from_inventory('parts')
  if parts_available >= 1:
    print("You were able to repair it with a spare part")
    remaining = player.consume('parts',1)
    print("You have {} spare part(s) remaining".format(remaining))
  else:
    print("You do not have any spare parts to fix the wagon")
    print("You can no longer continue on the trail")
    return True

def bad_weather(player):
  """
  Player is stuck while a random storm passes.

  Arguments:
    player (player.player): Used to interface with the game-state.
    
  Returns:
    None 
  """
  random.seed()
  
  # (name, days to wait)
  weather_events = [
      ('heavy rain', 1),
      ('a storm', 3),
      ('hail', 1),
      ('a blizzard', 3),
      ('a hurricane', 5)
      ]
  
  # Determine storm.
  event = random.choice(weather_events)
  days = event[1]
  name = event[0]
  
  # Inform player, advance time, and consume food for waiting.
  print("You have to halt your journey for {} days due to {}".format(days,name))
  player.advance_time(days)
  food_consumed = player.rations * days * player.members_alive
  food_available = player.get_from_inventory('food')
  if food_available >= food_consumed:
    print("You consumed {} pounds of food".format(food_consumed))
    remaining = player.consume('food',food_consumed)
    print("You have {} pounds remaining".format(remaining))
  else:
    # Avoids printing negative numbers to player.
    print("You consume {} pounds of food".format(food_available))
    player.consume('food',food_available)

def fortune(player):
  """
  Adds a random amount of a random inventory item to the player's inventory.
  
  Arguments:
    player (player.player): Used to interface with the game-state.
    
  Returns:
    None
  """
  random.seed()
  
  # (inventory item, amount received)
  treasures = [
      ('food',random.randint(100,500)),
      ('money',random.randint(200,500)),
      ('bullets',random.randint(30,100)),
      ('kits',random.randint(2,3)),
      ('parts',random.randint(2,3)),
      ]
  
  # Determine random item.
  found = random.choice(treasures)
  
  # Handle special message for food.
  if found[0] == 'food':
    current_food = player.get_from_inventory('food')
    # Handle food inventory limit.
    if current_food + found[1] > 1000:
      added_food = 1000 - current_food
      print("You found {} pounds of food in an abandoned wagon".format(found[1]))
      print("You can only add {} pounds to your wagon".format(added_food))
      player.update_inventory('food',1000)
    else:
      print("You found {} pounds of food in an abandoned wagon".format(found[1]))
      player.add_to_inventory('food',found[1])
  
  # Handle special message for money.
  elif found[0] == 'money':
    print("You found ${} in an abandoned wagon".format("%.2f" %found[1]))
    player.add_to_inventory('money',found[1])
  
  # Handle all other items.
  else:
    print("You found {} {} in an abandoned wagon".format(found[1],found[0]))
    player.add_to_inventory(found[0],found[1])

def raider_attack(player):
  """
  Entry-point from the engine.
  Random attack based on player's mileage.
  Player can fight, surrender, or run away from a raider attack with varying consequences.

  Arguments:
    player (player.player): Used to interface with the game-state.
    
  Returns:
    None
  """
  random.seed()
  mileage = player.miles_traveled
  
  # Generate probability based on mileage.
  chance = int(((mileage / 100 - 4) ** 2 + 72) / ((mileage / 100 - 4) ** 2 + 12) - 1) + 1
  numbers = list(range(1,chance + 1))
  
  if random.randint(1,100) in numbers:
    print("Raiders are attacking")
    print("Do you want to run (1), fight (2), or surrender (3)?")
    options = [1,2,3]
    response = get_input_int_protected(options)
    
    # Run.
    if response == 1:
      if player.can_consume('oxen',1):  
        player.consume('oxen',1)
      if player.can_consume('food',10):
        player.consume('food',10)
      if player.can_consume('parts',1):
        player.consume('parts',1)
      print("You managed to escape, but you left behind 1 ox, 10 pounds of food, and a spare wagon part")
    
    # Fight.
    elif response == 2:
      print("You must win the puzzle in order to defeat the raiders")
      if puzzle.did_win():
        print("You search the raiders and found 50 pounds of food and 50 bullets")
        player.add_to_inventory('food',50)
        player.add_to_inventory('bullets',50)
      else:
        print("The raiders stole a quarter of your money and 50 bullets")
        current_money = player.get_from_inventory('money')
        stolen_money = int(current_money / 4)
        player.consume('money',stolen_money)
        if player.can_consume('bullets',50):
          player.consume('bullets',50)
    
    # Surrender.
    elif response == 3:
      print("You surrendered to the raiders")
      print("The raiders stole a quarter of your money")
      current_money = player.get_from_inventory('money')
      stolen_money = int(current_money / 4)
      player.consume('money',stolen_money)

def failed_river(player):
  """
  Entry-point from engine when river crossing fails.
  Player loses a random amount up to 3 different items.
  Chance for player to drown.
  
  Arguments:
    player (player.player): Used to interface with the game-state.
    
  Returns:
    None
  """
  random.seed()
  print("Your attempt to cross the river failed")
  
  # Define probabilities and create number lists for drowning and each item.
  chance_drowning = 20
  chance_goods = [70,50,20]
  n_drowning = list(range(1,chance_drowning + 1))
  n_goods = []
  for chance in chance_goods:
    n_goods.append(list(range(1,chance + 1)))
  
  # Determine how many different items are lost.
  did_lose_good = []
  for n in n_goods:
    if random.randint(1,100) in n:  
      did_lose_good.append(True)
    else:
      did_lose_good.append(False)
      
  # Determine if party-member drowns.
  did_drown = False
  if random.randint(1,100) in n_drowning:
    did_drown = True
    
  # Handle drowning.
  if did_drown:
    choices = []
    for member in player.members:
      if member.is_alive:
        choices.append(member)
    member = random.choice(choices)
    member.drown()
  
  # Handle lost goods.
  # (inventory key, max amount lost)
  # Players can lose 1 up to a max amount of good.
  options = [('food',100),('bullets',100),('oxen',2),('parts',2)]  
  for did_lose in did_lose_good:
    if did_lose:
      option = random.choice(options)
      options.remove(option)
      amount = random.randint(1,option[1])
      # Players only lose goods if they have enough to lose.
      if player.can_consume(option[0],amount):
        # Special food message.
        if option[0] == 'food':
          print("You lost {} pounds of food".format(amount))
          player.consume('food',amount)
        else:
          print("You lost {} {}".format(amount,option[0]))
          player.consume(option[0],amount)
