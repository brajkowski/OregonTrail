import turtle

class gui():
  def __init__(self, player):
    # Initialize.
    self.player = player
    turtle.setup()
    
    self.tester = turtle.Turtle()
    self.tester.onclick(self.store_coordinate)
    self.window = self.tester.screen
    self.window.onscreenclick(self.store_coordinate)
    self.window.setup(1327,569) # Size of the map.
    self.location_coordinates = []

    # Load background map image.
    try:
      self.window.bgpic("../graphics/map_edit_resize.png")
    except:
      print("Error: Could not load window background.")
      
  def store_coordinate(self,x,y):
    print(x,y)
    self.location_coordinates.append((x,y))
    
  def save_coordinates(self):
    with open("../graphics/location_coords.txt",'w') as file:
      for location in self.location_coordinates:
        file.write("{}{},".format(location[0],location[1]))
  
  def clear(self):
    self.window.clear()
  
  def draw(self):
    self.tester.forward(100)
    
  def close(self):
    turtle.bye()
