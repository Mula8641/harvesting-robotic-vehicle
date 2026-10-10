#include <dummy.h>

#include <ESP32Servo.h>

// Define the servo pins
Servo base_servo;
Servo shoulder_servo;
Servo elbow_servo;
Servo wrist_servo;
Servo gripper_servo;

// Define the servo positions
int base_pos = 60;
int shoulder_pos = 90;
int elbow_pos = 80;
int wrist_pos = 110;
int gripper_pos = 120;

void setup() {
  // Start the serial communication
  Serial.begin(115200);

  // Attach the servos to their respective pins
  base_servo.attach(16);
  shoulder_servo.attach(17);
  elbow_servo.attach(5);
  wrist_servo.attach(18);
  gripper_servo.attach(19);

  // Set the initial servo positions
  base_servo.write(base_pos);
  shoulder_servo.write(shoulder_pos);
  elbow_servo.write(elbow_pos);
  wrist_servo.write(wrist_pos);
  gripper_servo.write(gripper_pos);
}

void reset_pos(){
  // Set the initial servo positions
  base_servo.write(60);
  shoulder_servo.write(90);
  elbow_servo.write(80);
  wrist_servo.write(110);
  gripper_servo.write(130);  
}

void loop() {
  // Check if there is serial data available
  if (Serial.available() > 0) {
    // Read the serial command
    String command = Serial.readStringUntil('\n');

    // Parse the command
    if (command.charAt(0) == 'T') {
      // If the command is a tracking command, extract the X and Y positions
      int x_pos = command.substring(2, 5).toInt();
      int y_pos = command.substring(6, 9).toInt();

      // Map the X and Y positions to servo positions
      base_pos = map(x_pos, 0, 255, 20, 160);
      shoulder_pos = map(y_pos, 0, 255, 50, 150);
      elbow_pos = map(y_pos, 0, 255, 50, 180);

      // Set the servo positions
      base_servo.write(base_pos);
      shoulder_servo.write(shoulder_pos);
      elbow_servo.write(elbow_pos);
      
    } else if (command.charAt(0) == 'P') {
      // If the command is a pick command, extract the Z position
      int z_pos = command.substring(6, 9).toInt();

      // Map the Z position to a servo position
      wrist_pos = map(z_pos, 0, 255, 50, 150);

      // Set the servo position
      wrist_servo.write(wrist_pos);

      // Close the gripper
      gripper_pos = 120;
      gripper_servo.write(gripper_pos);
      delay(1500);

      // Move the arm back up
      base_pos = 60;
      base_servo.write(base_pos);
      shoulder_pos = 140;
      shoulder_servo.write(shoulder_pos);
      elbow_pos = 180;
      elbow_servo.write(elbow_pos);
      wrist_pos = 80;
      wrist_servo.write(wrist_pos);
      gripper_pos = 75;
      gripper_servo.write(gripper_pos);
      delay(2000);
      reset_pos();
    }
  }
}
