import turtle

class gui():
  def __init__(self):
    # Initialize.
    turtle.setup()
    
    self.tester = turtle.Turtle()
    self.window = self.tester.screen
    self.window.setup(1327,569) # Size of the map.

    # Load background map image.
    try:
      self.window.bgpic("../graphics/map_edit_resize.png")
    except:
      print("Error: Could not load window background.")
      
      
  def update(self):
    self.tester.forward(10)
    self.window.listen()
    
  def close(self):
    self.window.exitonclick()
    turtle.done()  
