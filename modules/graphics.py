"""
This module is responsible for updating a map that shows the player's progress in the game using Turtle graphics.
"""

import turtle

class gui():
  """
  Holds all turtle information and coordinate list that corresponds to map markers.
  
  player (player.player): Reference to player object to access inventory.
  path (turtle.Turtle): Turtle used to draw the player's path.
  window (turtle.screen): Reference to window used for turtle drawing.
  location_coordinates []: List of coordinates corresponding to map markers.
  current_coordinate (int): Tracks which coordinate has been drawn.
  """
  def __init__(self, player):
    # Initialize.
    self.player = player
    turtle.setup()
    
    # Set up path drawing turtle.
    self.path = turtle.Turtle()
    self.path.hideturtle()
    self.path.width(5)
    self.path.color('red')
    
    # Configure window.
    self.window = self.path.screen
    self.window.setup(1327,569) # Size of the map image.
    self.location_coordinates = []
    self.current_coordinate = 0
    
    # Uncomment to create new location_coords from turtle by clicking.
    #self.path.onclick(self.store_coordinate)
    #self.window.onscreenclick(self.store_coordinate)
    
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
    """
    Adds coordinate to the coordinate list. Mainly used as the event handler for turtle window click.
    
    Arguments:
      x (int or float): x coordinate
      y (int or float): y coordinate
    """
    print(x,y)
    self.location_coordinates.append((x,y))
    
  def save_coordinates(self):
    """
    Writes the current location_coordinates to file.
    """
    with open("../graphics/location_coords.txt",'w') as file:
      for location in self.location_coordinates:
        file.write("{},{}\n".format(int(location[0]),int(location[1])))
  
  def load_coordinates(self):
    """
    Loads location_coordinates from file.
    """
    location_coordinates = []
    with open("../graphics/location_coords.txt",'r') as file:
      for line in file:
        coordinate = line[:-1] # Remove \n
        coordinates = coordinate.split(',')
        location_coordinates.append((int(coordinates[0]),int(coordinates[1])))
    self.location_coordinates = location_coordinates
  
  def print_coordinates(self):
    """
    Prints all stored coordinates to console.
    """
    for coordinate in self.location_coordinates:
      print(coordinate)
    
  def draw_all(self):
    """
    Draws all of the stored coordinates in order.
    """
    self.path.penup()
    for coordinate in self.location_coordinates:
      self.path.setposition(coordinate[0],coordinate[1])
      self.path.pendown()
  
  def draw_next_coord(self):
    """
    Draws the next coordinate in the stored list and updates the current coordinate.
    """
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
