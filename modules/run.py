import gui
import console

def main():
  io = console.io_manager()
  io.load_all_messages()
  io.print_welcome()
  print()
  io.print_all_locations()
  gui.run()

  
  
if __name__ == "__main__":
  main()
