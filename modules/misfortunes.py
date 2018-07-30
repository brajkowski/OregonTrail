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
      theif_attacks,
      wagon_breaks,
      bad_weather,
      fortune
      ]
  i_misfortune = random.randint(0,len(misfortunes)-1)
  misfortune = misfortunes[i_misfortune]
  if misfortune == sickness:
    misfortune(player.names)
  else:
    misfortune()

# TODO: Define all misfortune functions.
def sickness(names):
  random.seed()
  diseases = [
      'typhoid',
      'cholera',
      'diarrhea',
      'measles',
      'dysentery',
      'fever']
  
  i_disease = random.randint(0,len(diseases)-1)
  i_name = random.randint(0,len(names)-1)
  disease = diseases[i_disease]
  name = names[i_name]
  print("{} has {}".format(name,disease))
  return (name, disease)
  
# TODO: Flesh out.
def oxen_dies():
  print("An oxen has died")
  return

# TODO: Flesh out.
def theif_attacks():
  random.seed()
  amount = random.randint(10,25)
  print("A theif has stolen {} pounds of food".format(amount))
  return amount

# TODO: Flesh out.
def wagon_breaks():
  random.seed()
  parts = [
      'wheel',
      'axel',
      'tongue'
      ]
  i_part = random.randint(0,len(parts)-1)
  part = parts[i_part]
  print("A wagon {} broke".format(part))
  return

# TODO: Flesh out.
def bad_weather():
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
  print("You have to halt your journey for {} days due to {}".format(event[1],event[0]))
  return event

# TODO: Optional.  
def fortune():
  pass