import random

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
  if misfortune == sickness:
    return misfortune(player)
  else:
    return misfortune(player)

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
  should_end_game = player.members[i_name].gets_sick(disease)
  if player.get_from_inventory('kits') > 0:
    player.members[i_name].use_med_kit()
    remaining = player.consume('kits',1)
    print("You used a med-kit on {}".format(name))
    print("You have {} med-kit(s) remaining".format(remaining))
  if should_end_game:
    print("You cannot continue on the trail without the leader")
  return should_end_game
  
def oxen_dies(player):
  print("An oxen has died")
  oxen_available = player.get_from_inventory('oxen')
  if oxen_available > 1:
    remaining = player.consume('oxen',1)
    print("You have {} oxen remaining".format(remaining))
    return False
  else:
    print("You do not have any oxen left")
    print("You can no longer continue on the trail")
    return True

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
  return False

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
    return False
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
    return False
  else:
    print("You ran out of food")
    print("All party members starved")
    return True

# TODO: Flesh out - optional.  
def fortune(player):
  print("Fortune event here")
  return False