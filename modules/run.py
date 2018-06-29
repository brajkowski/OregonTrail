import gui
import game_io

def remove_newline(self,line):
  if line[-1:] == "\n":
    return line[:len(line)-1]
  return line

def main():
  io_manager = game_io.manager()
  io_manager.print_message("welcome")
  io_manager.print_message('locations')
  io_manager.print_message('store_welcome')

  #gui.run()

  
  
if __name__ == "__main__":
  main()
