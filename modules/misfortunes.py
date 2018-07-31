import random
import puzzle
from game_io import get_input_int_protected

def randomize(player):
  random.seed()
  chance = list(range(1,31)) # 30% chance
  number = random.randint(1,100)
  if not(number in chance):
    return
  
  misfortunes = [
      sickness,
      oxen_dies,
      thief_attacks,
      wagon_breaks,
      bad_weather,
      fortune
      ]
  i_misfortune = random.randint(0,len(misfortunes)-1)
  misfortune = misfortunes[i_misfortune]
  misfortune(player)

def sickness(player):
  random.seed()
  diseases = [
      'typhoid',
      'cholera',
      'diarrhea',
      'measles',
      'dysentery',
      'fever']
  
  choices = []
  for i in range(len(player.members)):
    if player.members[i].is_alive:
      choices.append(i)
  i_disease = random.randint(0,len(diseases)-1)
  i_name = random.choice(choices)
  disease = diseases[i_disease]
  name = player.members[i_name].name
  print("{} has {}".format(name,disease))
  player.members[i_name].gets_sick(disease)
  if player.get_from_inventory('kits') > 0:
    player.members[i_name].use_med_kit()
    remaining = player.consume('kits',1)
    print("You used a med-kit on {}".format(name))
    print("You have {} med-kit(s) remaining".format(remaining))
  
def oxen_dies(player):
  print("An oxen has died")
  oxen_available = player.get_from_inventory('oxen')
  if oxen_available > 1:
    remaining = player.consume('oxen',1)
    print("You have {} oxen remaining".format(remaining))

def thief_attacks(player):
  random.seed()
  amount = random.randint(10,25)
  food_available = player.get_from_inventory('food')
  if food_available >= amount:
    print("A thief has stolen {} pounds of food".format(amount))
    remaining = player.consume('food',amount)
    print("You have {} pounds of food remaining".format(remaining))
  else:
    print("A thief stole the remainder of your food")
    player.consume('food',food_available)

def wagon_breaks(player):
  random.seed()
  parts = [
      'wheel',
      'axel',
      'tongue'
      ]
  i_part = random.randint(0,len(parts)-1)
  part = parts[i_part]
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
  random.seed()
  
  # Weather event, days to wait
  weather_events = [
      ('heavy rain', 1),
      ('a storm', 3),
      ('hail', 1),
      ('a blizzard', 3),
      ('a hurricane', 5)
      ]
  i_event = random.randint(0,len(weather_events)-1)
  event = weather_events[i_event]
  days = event[1]
  name = event[0]
  print("You have to halt your journey for {} days due to {}".format(days,name))
  player.advance_time(days)
  food_consumed = player.rations * days * player.members_alive
  food_available = player.get_from_inventory('food')
  if food_available >= food_consumed:
    print("You consumed {} pounds of food".format(food_consumed))
    remaining = player.consume('food',food_consumed)
    print("You have {} pounds remaining".format(remaining))
  else:
    print("You consume {} pounds of food".format(food_available))
    player.consume('food',food_available)

def fortune(player):
  treasures = [
      ('food',random.randint(100,500)),
      ('money',random.randint(200,500)),
      ('bullets',random.randint(30,100)),
      ('kits',random.randint(2,3)),
      ('parts',random.randint(2,3)),
      ]
  found = random.choice(treasures)
  if found[0] == 'food':
    current_food = player.get_from_inventory('food')
    if current_food + found[1] > 1000:
      added_food = 1000 - current_food
      print("You found {} pounds of food in an abandoned wagon".format(found[1]))
      print("You can only add {} pounds to your wagon".format(added_food))
      player.update_inventory('food',1000)
      return
    else:
      print("You found {} pounds of food in an abandoned wagon".format(found[1]))
      player.add_to_inventory('food',found[1])
  elif found[0] == 'money':
    print("You found ${} in an abandoned wagon".format("%.2f" %found[1]))
    player.add_to_inventory('money',found[1])
  else:
    print("You found {} {} in an abandoned wagon".format(found[1],found[0]))
    player.add_to_inventory(found[0],found[1])

def raider_attack(player):
  mileage = player.mileage
  chance = int(((mileage / 100 - 4) ** 2 + 72) / ((mileage / 100 - 4) ** 2 + 12) - 1) + 1
  numbers = list(range(1,chance + 1))
  if random.randint(1,100) in numbers:
    print("Raiders are attacking")
    print("Do you want to run (1), fight (2), or surrender (3)?")
    options = [1,2,3]
    response = get_input_int_protected(options)
    if response == 1:
      if player.can_consume('oxen',1):  
        player.consume('oxen',1)
      if player.can_consume('food',10):
        player.consume('food',10)
      if player.can_consume('parts',1):
        player.consume('parts',1)
      print("You managed to escape, but you left behind 1 ox, 10 pounds of food, and a spare wagon part")
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
    elif response == 3:
      print("You surrendered to the raiders")
      print("The raiders stole a quarter of your money")
      current_money = player.get_from_inventory('money')
      stolen_money = int(current_money / 4)
      player.consume('money',stolen_money)

def failed_river(player):
  print("Your attempt to cross the river failed")
  chance_drowning = 20
  chance_goods = [70,50,20]
  
  n_drowning = list(range(1,chance_drowning + 1))
  n_goods = []
  for chance in chance_goods:
    n_goods.append(list(range(1,chance + 1)))
  
  did_lose_good = []
  for n in n_goods:
    if random.randint(1,100) in n:  
      did_lose_good.append(True)
    else:
      did_lose_good.append(False)
  did_drown = False
  if random.randint(1,100) in n_drowning:
    did_drown = True
    
  if did_drown:
    choices = []
    for member in player.members:
      if member.is_alive:
        choices.append(member)
    member = random.choice(choices)
    member.drown()
  
  # Inventory key, max amount lost
  options = [('food',100),('bullets',100),('oxen',2),('parts',2)]  
  for did_lose in did_lose_good:
    if did_lose:
      option = random.choice(options)
      options.remove(option)
      amount = random.randint(1,option[1])
      if player.can_consume(option[0],amount):
        if option[0] == 'food':
          print("You lost {} pounds of food".format(amount))
          player.consume('food',amount)
        else:
          print("You lost {} {}".format(amount,option[0]))
          player.consume(option[0],amount)
      
      
      
  
  
    