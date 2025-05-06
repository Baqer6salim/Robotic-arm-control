#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// Initialize PCA9685 servo driver
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

// Servo pulse parameters
#define SERVO_MIN 165 // Minimum pulse length
#define SERVO_MAX 650 // Maximum pulse length

//Predefined positions for 6 servos (angles in degrees)
int home_open[6] = {90, 105, 50, 45, 90, 10}; // home position
int pick_up_open[6] = {10, 25, 35, 70, 20 , 10}; // pick up zone (grabber is open)
int yellowpos_close[6] = {63, 38, 73, 80, 68, 55}; // yellow cube position 
int yellow_pos_rect[6] = {63, 38, 73, 80, 68, 70}; // yellow rectangle  position 
int red_obj_pos[6] = {105, 38, 80, 90, 68, 55}; // red objects (triangle,rectangl) position
int red_cyl_pos[6] = {105, 38, 80, 90, 68, 55}; // red cylinder  position
int green_pos[6] = {138, 38, 80, 95, 68, 55}; // green position
int other_pos[6] = {175, 38, 60, 95, 68, 70}; // others (blue_square) position

void setup() {
  Serial.begin(9600); // Start serial communication
  pwm.begin();
  pwm.setPWMFreq(58); // Set frequency to 60Hz for servos
  
  Serial.println("Robotic Arm Controller Ready");
  Serial.println("Available commands:");
  Serial.println("home, pickup, yellow_cube, yellow_rectangle");
  Serial.println("red_obj, red_cylinder");
  Serial.println("green_obj");
  Serial.println("blue_square");
}

bool moved = false;  // flag  for pick up operation 

void loop() {
   if (Serial.available()) {
    String  command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "home") {
      Serial.println("Moving to home position ...");
      moveToPosition(home_open, 2000,command); // Move servos to predefined position with 2-second delay
      Serial.println("ACK");
  delay(2000);
    }
    else if (command == "pickup") {
      Serial.println("Moving to pick up position ...");
      moveToPosition(pick_up_open, 3000,command); // Move servos to predefined position with 2-second delay
      Serial.println("ACK");
  delay(2000);
    }
    else if (command == "yellow_cube"){
      Serial.println("Moving to yellow position ...");
      moveToPosition(yellowpos_close, 2000,command); // Move servos to predefined position with 2-second delay
      Serial.println("ACK");
  delay(2000);

    }
  
    if (command == "yellow_rectangle") {
      Serial.println("Moving to home position ...");
      moveToPosition(yellow_pos_rect, 2000,command); // Move servos to predefined position with 2-second delay
      Serial.println("ACK");
  delay(2000);
    }
    else if (command == "red_obj"){
      Serial.println("Moving to yellow position ...");
      moveToPosition(red_obj_pos, 2000,command); // Move servos to predefined position with 2-second delay
      Serial.println("ACK");
  delay(2000);
    }
    else if (command == "red_cylinder"){
      Serial.println("Moving to yellow position ...");
      moveToPosition(red_cyl_pos, 2000,command); // Move servos to predefined position with 2-second delay
      Serial.println("ACK");
  delay(2000);
    }
    else if (command == "green_obj"){
      Serial.println("Moving to yellow position ...");
      moveToPosition(green_pos, 2000,command); // Move servos to predefined position with 2-second delay
      Serial.println("ACK");
  delay(2000);
    }
      else if (command == "blue_square"){
      Serial.println("Moving to yellow position ...");
      moveToPosition(other_pos, 2000,command); // Move servos to predefined position with 2-second delay
      Serial.println("ACK");
  delay(2000);
    }
  }
}
// Function to move servos to a specific position with a delay
void moveToPosition(int positions[], int moveDelay, String command) {

 if (command == "pickup"){
 for (int i = 5; i >= 2; i--) {
    int pulse = map(positions[i], 0, 180, SERVO_MIN, SERVO_MAX); // Map angle to pulse length
    pwm.setPWM(i, 0, pulse); // Move servo to position
    Serial.print("Servo ");
    Serial.print(i + 1);
    Serial.print(" moved to ");
    Serial.print(positions[i]);
    Serial.println(" degrees.");
    delay(moveDelay); // Delay to allow servo to reach its position
  }

if (!moved) {
    for (int i = 0; i < 2; i++) {
      int pulse = map(positions[i], 0, 180, SERVO_MIN, SERVO_MAX);
      if (i == 1) {
        int pulse1 = map(45, 0, 180, SERVO_MIN, SERVO_MAX);
        pwm.setPWM(i, 0, pulse1);
        delay(moveDelay);
        pwm.setPWM(i, 0, pulse);
        Serial.print("Servo ");
    Serial.print(i + 1);
    Serial.print(" moved to ");
    Serial.print(positions[i]);
    Serial.println(" degrees.");
        delay(moveDelay);
      } else {
        pwm.setPWM(i, 0, pulse);
        delay(moveDelay);
      }
    }
    moved = true;
  }
  return;
  }
    for (int i = 5; i >= 0; i--) {
    int pulse = map(positions[i], 0, 180, SERVO_MIN, SERVO_MAX); // Map angle to pulse length
    pwm.setPWM(i, 0, pulse); // Move servo to position
    Serial.print("Servo ");
    Serial.print(i + 1);
    Serial.print(" moved to ");
    Serial.print(positions[i]);
    Serial.println(" degrees.");
    delay(moveDelay); // Delay to allow servo to reach its position
    
  }
}
