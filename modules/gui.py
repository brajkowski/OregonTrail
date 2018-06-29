import turtle

def run():
  # Initialize.
  turtle.setup()
  
  tester = turtle.Turtle()
  window = tester.screen
  window.setup(1327,569) # Size of the map.
  window
  
  # Load background map image.
  try:
    window.bgpic("../graphics/map_edit_resize.png")
  except:
    print("Error: Could not load window background.")
    
  # Shutdown.
  window.exitonclick()
  turtle.done()
