"""
@author: Ramsin Khoshabeh
"""

from ECE16Lib.Communication import Communication
from ECE16Lib.Orientation import Orientation
from time import sleep
import socket, pygame

# Setup the Socket connection to the Space Invaders game
host = "127.0.0.1"
port = 65432
mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mySocket.connect((host, port))
mySocket.setblocking(False)

class PygameController:
  comms = None
  ori = None

  def __init__(self, serial_name, baud_rate, num_samples, fs):
    self.comms = Communication(serial_name, baud_rate)
    self.ori = Orientation(num_samples, fs)

  def run(self):
    # 1. make sure data sending is stopped by ending streaming
    self.comms.send_message("stop")
    self.comms.clear()

    # 2. start streaming orientation data
    input("Ready to start? Hit enter to begin.\n")
    self.comms.send_message("start")

    # 3. Forever collect orientation and send to PyGame until user exits
    print("Use <CTRL+C> to exit the program.\n")
    lives_prev = 3
    score_prev = -1
    while True:
      try:
        lives_score_msg = mySocket.recv(1024) # receive 1024 bytes
        lives_score_msg = lives_score_msg.decode('utf-8') 
        lives, score = lives_score_msg.split(",")
        # print("lives: " + str(lives) + " score: " + str(score))
        # only send the data to MCU if there is a change either in lives or score, send it as comma-separated
        if (int(lives) < lives_prev) or (int(score) > score_prev):
          lives_score_msg = 'Lives: ' + str(lives) + ',' + 'Score: ' + str(score)
          
          if (int(lives) < lives_prev):
            self.comms.send_message("buzz\n")

          print(str(lives_score_msg))
          self.comms.send_message(str(lives_score_msg)+"\n")
          lives_prev = int(lives)
          score_prev = int(score)
      except:
        pass

      message = self.comms.receive_message()
      if(message != None):
        time, ax, ay, az, button = message.split(",")
        self.ori.add(int(time), int(ax), int(ay), int(az))
        self.ori.process()
        command =  self.ori.get_orientation()
        # NOTE: if we want to be able to fire and move at the same time,
        # we have to send the info for both in the same command
        if(int(button) == 1):
            command = command + ",FIRE" #this used to be lower case but the pygame expects upper case
        else:
            command = command + ",NoFIRE"

        if command is not None:
          mySocket.send(command.encode("UTF-8"))


if __name__== "__main__":
  serial_name = "COM4"
  baud_rate = 115200
  num_samples = 100 # 2 seconds at 50Hz (this determines how fast the thresholds readjust)
                    # (the higher the num_samples, the longer it takes)
  fs = 50
  controller = PygameController(serial_name, baud_rate, num_samples, fs)

  try:
    controller.run()
  except(Exception, KeyboardInterrupt) as e:
    print(e)
  finally:
    print("Exiting the program.")
    controller.comms.send_message("stop")
    controller.comms.close()
    mySocket.send("QUIT".encode("UTF-8"))
    mySocket.close()

  input("[Press ENTER to finish.]")