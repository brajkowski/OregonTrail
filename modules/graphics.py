import turtle

class gui():
  def __init__(self, player):
    # Initialize.
    self.player = player
    turtle.setup()
    
    self.path = turtle.Turtle()
    self.path.hideturtle()
    self.path.width(5)
    self.path.color('red')
    #self.path.onclick(self.store_coordinate)
    self.window = self.path.screen
    #self.window.onscreenclick(self.store_coordinate)
    self.window.setup(1327,569) # Size of the map.
    self.location_coordinates = []
    self.current_coordinate = 0
    
    self.load_coordinates()

    # Load background map image.
    try:
      self.window.bgpic("../graphics/map_edit_resize.png")
    except:
      print("Error: Could not load window background.")
      
    # Set turtle at starting point.
    self.path.penup()
    self.path.goto(self.location_coordinates[0])
    self.path.pendown()
      
  def store_coordinate(self,x,y):
    print(x,y)
    self.location_coordinates.append((x,y))
    
  def save_coordinates(self):
    with open("../graphics/location_coords.txt",'w') as file:
      for location in self.location_coordinates:
        file.write("{},{}\n".format(int(location[0]),int(location[1])))
  
  def load_coordinates(self):
    location_coordinates = []
    with open("../graphics/location_coords.txt",'r') as file:
      for line in file:
        coordinate = line[:-1] # Remove \n
        coordinates = coordinate.split(',')
        #print(int(coordinates[0][:-2]),int(coordinates[1][:-2]))
        location_coordinates.append((int(coordinates[0]),int(coordinates[1])))
    self.location_coordinates = location_coordinates
  
  def print_coordinates(self):
    for coordinate in self.location_coordinates:
      print(coordinate)
    
  def draw_all(self):
    self.path.penup()
    for coordinate in self.location_coordinates:
      self.path.setposition(coordinate[0],coordinate[1])
      self.path.pendown()
  
  def draw_next_coord(self):
    self.current_coordinate += 1
    try:
      coordinate = self.location_coordinates[self.current_coordinate]
    except IndexError:
      print("At final location")
      return
    x = coordinate[0]
    y = coordinate[1]
    self.path.setposition(x,y)
     
  def close(self):
    turtle.bye()
