# ECE 16 Grand Challenge - Space Invaders Controller

## Team Members
Name/PID    : Rasya Soeroso/A16088908

Name/PID    : Maxime Ghesquiere/A15400735

## Features and Improvements
**1. Fire with push button**

The firing functionality of the ship is controlled by the push button.

In the Arduino sketch, we initialize the pin that we use to connect the push button to the MCU and set it as an input. Using `digitalRead()` function, we read the input weather it is `LOW` (when the button is pushed) or `HIGH` (when the button is released.) We set an integer variable to record the status of the push button, `button` to 1 if the button is pushed and 0 otherwise. Then, the variable `button` is concatenated to the data samples from the accelerometer, and the data is sent to Python.

In the `space_invaders_controller.py`, Python receive a string of message from the MCU and parse the data into the corresponding variables. Since we want to be able to fire and move at the same time, we need to send both movement and firing command in the same variable.

In the `spaceinvaders.py`, we modify the code as below so we are able to fire and move at the same time.
```
def check_input_udp_socket(self):
        try:
            msg, self.addr = mySocket.recvfrom(1024) # receive 1024 bytes
            .
            .
            .
            move_command , weapon_command = msg.split(",")
            if weapon_command == "FIRE":
                .
                .
                .
                self.player.update_udp_socket(move_command)
            else:
                self.player.update_udp_socket(move_command)
        except BlockingIOError:
            pass # do nothing if there's no data
```

**2. Tilt angle speed control**

In the Arduino sketch, we obtain the accelerometer values using `analogRead()` function and send them to the python controller.

In `space_invaders_controller.py`, when data is available it is added to the Orientation object defined in `Orientation.py`. This object stores 2s worth of data in circular lists. When the `ori.process()` is called the code takes the last accelerometer values, and if the x value is further from 0 than either the y or z values, it determines the controller is tilted. This assumption comes from the fact that *abs(delta_x) = abs(delta_y) + abs(delta_z)* while at rest, since the only acceleration on the system is gravity in such a case. As such, if the controller is tilted, x will be further from zero than at least one of the other 2 values. (not necessarily both since if y doesn't change, x and z will be equally far from zero).

If a tilt is detected, the x value is compared to a set of thresholds to determine just how tilted the controller is. The more tilted the controller, the higher the output command's speed. The commands are `RIGHTH`, `RIGHTM`, `RIGHTL`, `LEFTH`, `LEFTM`, `LEFTL`.

In `space_invaders.py`, the code was altered in the following way to allow for multiple movement options:
```
def update_udp_socket(self, direction):
      if direction == "LEFTL" and self.rect.x > 10:
          self.rect.x -= self.speed
      if direction == "LEFTM" and self.rect.x > 10:
          self.rect.x -= 2 * self.speed
      if direction == "LEFTH" and self.rect.x > 10:
          self.rect.x -= 3 * self.speed
      if direction == "RIGHTL" and self.rect.x < 740:
          self.rect.x += self.speed
      if direction == "RIGHTM" and self.rect.x < 740:
          self.rect.x += 2 * self.speed
      if direction == "RIGHTH" and self.rect.x < 740:
          self.rect.x += 3 * self.speed
      game.screen.blit(self.image, self.rect)
```

**3. Orientation detection improvement**

The `Orientation.py` object also performs the task of periodically readjusting the thresholds it uses. Every 2s, the average accelerometer value for each axis is calculated from the circular lists stored in the object. Half of this mean is then subtracted from all values in memory, and added to the `X_ZERO`, `Y_ZERO` and `Z_ZERO` values. The Thresholds are then recalculated from these ZERO values. The assumption here is that given the limited size of the game arena, one would not intend to tilt the controller at a constant nonzero angle for 2s. Therefore, every 2s, the code subtracts half the average tilt from the thresholds, this adjusts the thresholds towards the current tilt being treated as horizontal.

**4. Display current score and lives**

It displays the current score and lives on the OLED and update it every time there is a change in score or lives.

We need to send the current score and lives from the server to client. In `spaceinvaders.py` we need to obtain the address of UDP client.
```
msg, self.addr = mySocket.recvfrom(1024) # receive 1024 bytes
```
Then, we can send the current score and lives stored in the variable `lives_score_msg` to the UDP client by the following line of code.
```
mySocket.sendto(lives_score_msg.encode("UTF-8"), self.addr)
```

In the `space_invaders_controller.py`, the client receives the current score and lives from the server and every time there is a change in either score or lives, Python will send the data to the MCU.

Using `writeDisplayCSV()` function in the Arduino sketch, the OLED will be updated with the current score and lives received from Python.

**5. Hit detect buzzer**

When the ship is hit by a bullet, the motor will buzz for 2 seconds.

In the `space_invaders_controller.py`, Python will send "buzz" command to the MCU every time the current lives is not the same as the previous lives. In other words, it tells the MCU to buzz the motor every time `lives` is decreased by one (or the ship get hit.)

In the Arduino sketch, it checks if the received command equals to "buzz", and activate the motor with the highest intensity if "buzz" is received. Using a non-blocking timing logic, it deactivate the motor after 2 seconds.


**6. Display top scores on game end**

Using the same method as in *4. Display current score and Lives*, the socket is set up to allow information to be sent back to the client.

In `space_invaders.py`, when the `gameOver` variable is set to true, we call:
```
game_over_message = "gameover"
if self.addr is not None:
    # print("sending to client...", self.addr)
    mySocket.sendto(game_over_message.encode("UTF-8"), self.addr)
```

In the `space_invaders_controller.py`, the client receives the *gameover* command from the server when the game ends. At this point, the previous scores are extracted from a csv file in the scores folder using `data = np.genfromtxt(filename, delimiter=",")`. Then the current endgame score is added to this np.array and the array is sorted. The three highest scores are extracted and sent to the Arduino sketch. Then any scores of 0 are removed from the array to save memory, and if the array is longer than 30 scores, only the top 20 scores are retained. The array is then saved back to the same csv file using `np.savetxt(filename, scores_arr2, delimiter=",")`.

Using `writeDisplayCSV()` function in the Arduino sketch, the OLED will be updated with the top 3 scores from Python.
