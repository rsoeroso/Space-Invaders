/*
 * Global variables
 */
// Acceleration values recorded from the readAccelSensor() function
int ax = 0; int ay = 0; int az = 0;
int ppg = 0;        // PPG from readPhotoSensor() (in Photodetector tab)
int sampleTime = 0; // Time of last sample (in Sampling tab)
bool sending;
const int BUTTON_PIN = 14; // change according to your circuit configuration - Rasya
int button = 0; // 0=released, 1=pushed
String command_buzz = "";
unsigned long buzzStart = 0;
unsigned long buzzEnd = 0;

/*
 * Initialize the various components of the wearable
 */
void setup() {
  pinMode(BUTTON_PIN, INPUT);
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  setupPhotoSensor();
  setupMotor();
  sending = false;

  writeDisplay("Ready...", 1, true);
  writeDisplay("Set...", 2, false);
  writeDisplay("Play!", 3, false);
}

/*
 * The main processing loop
 */
void loop() {
  buzzEnd = millis();
  // Parse command coming from Python (either "stop" or "start")
  String command = receiveMessage();
  if(command == "stop") {
    sending = false;
    writeDisplay("Controller: Off", 0, true);
  }
  else if(command == "start") {
    sending = true;
    writeDisplay("Controller: On", 0, true);
  }
<<<<<<< HEAD
  else if(command == ""){
    // do nothing
  }
  else if(command == "buzz"){
    buzz();
    buzzStart = millis();
  }
  else{
    // Display current lives and score 
    writeDisplay(" ", 0, true);
    writeDisplay(" ", 1, true);
    writeDisplay(" ", 2, true);
    writeDisplay(" ", 3, true);
    writeDisplayCSV(command, 1);
  }

  // stop buzzing after 2 seconds
  if (buzzEnd - buzzStart >= 2000){
    deactivateMotor();
  }
  
  //low means pushed 
=======
  //low means pushed for me, check on your board
>>>>>>> 8085db82a43fcaaedf2cd467f9ebff4b96669849
  if (digitalRead(BUTTON_PIN) == LOW){
    button = 1;
  }
  else{
    button = 0;
  }

  // Send the orientation of the board
  if(sending && sampleSensors()) {
    String response = String(sampleTime) + ",";
    response += String(ax) + "," + String(ay) + "," + String(az);
    response += "," + String(button);
    sendMessage(response);
  }
}
