# ECE 16 Grand Challenge - Space Invaders Controller

## Team Members
Name/PID    : Rasya Soeroso/A16088908

Name/PID    : 

## Features and Improvements
**1. Fire with push button**

The firing functionality of the ship is controlled by the push button. 

In the Arduino sketch, we initialize the pin that we use to connect the push button to the MCU and set it as an input. Using `digitalRead()` function, we read the input weather it is `LOW` (when the button is pushed) or `HIGH` (when the button is released.) We set an integer variabble to record the status of the push button, `button` to 1 if the button is pushed and 0 otherwise. Then, the variable `button` is concatenated to the data samples from the accelerometer, and the data is sent to Python.

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

**3. Orientation detection improvement**

**4. Display current score and lives**

It displays the current score and lives on the OLED and update it everytime there is a change in score or lives. 

We need to send the current score and lives from the server to client. In `spaceinvaders.py` we need to obtain the address of UDP client.
```
msg, self.addr = mySocket.recvfrom(1024) # receive 1024 bytes
```
Then, we can send the current score and lives stored in the variable `lives_score_msg` to the UDP client by the following line of code.
```
mySocket.sendto(lives_score_msg.encode("UTF-8"), self.addr)
```

In the `space_invaders_controller.py`, the client receives the current score and lives from the server and everytime there is a change in either score or lives, Python will send the data to the MCU. 

Using `writeDisplayCSV()` funcition in the Arduino sketch, the OLED will be updated with the current score and lives received from Python.

**5. Hit detect buzzer**

When the ship is hit by a bullet, the motor will buzz for 2 seconds.

In the `space_invaders_controller.py`, Python will send "buzz" command to the MCU everytime the current lives is not the same as the previous lives. In other words, it tells the MCU to buzz the motor everytime `lives` is decreased by one (or the ship get hit.)

In the Arduino sketch, it checks if the received command equals to "buzz", and activate the motor with the highest intensity if "buzz" is received. Using a non-blocking timing logic, it deactivate the motor after 2 seconds. 


**6. Display top scores on game end**


