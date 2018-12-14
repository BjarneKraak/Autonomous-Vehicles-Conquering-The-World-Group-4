// Example Arduino Sketch

// We will use the Servo library to control the motors
// See https://www.arduino.cc/en/Reference/Servo for more information.
#include <Servo.h>

// In this sketch we use two servo motors for the two wheels
Servo servoLeft;                // Left wheel servo
Servo servoRight;               // Right wheel servo

// set the Arduino I/O pins for the two servo motors
const int rightServoPin = 13;       
const int leftServoPin = 12;

// this function sets the speed for both motors and waits for a 
// given amount of time
void move_servos(int speed_left, int speed_right, int millisec)
{
    servoLeft.write(speed_left);
    servoRight.write(speed_right);
    delay(millisec);
}

// All your sketches should have a 'setup' function
// This function is called only once, at the start of the program
void setup() 
{
  // initialize serial communication:
  // The following statement is only needed if you want to print debug information to the pc using 'Serial.print'
  Serial.begin(9600);
  
  // Attach the servo motors
  // We need to tell the servo library to which pins on the Arduino the servo motors are connected
  servoLeft.attach(leftServoPin);
  servoRight.attach(rightServoPin);
  

  // Stop the servo motors.
  // Note that setting the value to 90 should stop the motor
  // Values between 90 and 180 move the motor in one direction at increasing speed
  // Values lower than 90, down to 0 move in the opposite direction at increasaing speed
  // See also: https://www.arduino.cc/en/Reference/ServoWrite}
  servoLeft.write(90);
  servoRight.write(90);
}

int counter = 0;

// All sketches should have a 'loop' function.
// This function is called over and over again when the program is running
// When it ends it immediately starts again.
void loop()
{
    // short test run of the motors

    // wait still for 2 seconds (2000 milliseconds)
    delay(2000);

    // move forward slowly for 1 second
    // note that since the servos are mounted on opposite sides, 
    // the left and right servos need to turn in opposite directions!
    servoLeft.write(85);
    servoRight.write(95);
    delay(1000);

    // wait still for 1 second
    servoLeft.write(90);
    servoRight.write(90);
    delay(1000);

    // move backward slowly for 1 second
    servoLeft.write(95);
    servoRight.write(85);
    delay(1000);

    // now lets turn a bit by moving the servos in the same direction
    // we could have used the same kind of statements as above, but we 
    // use a function now to show how that works
    move_servos(88, 88, 1000);

    // and turn the other way
    move_servos(92, 92, 1000);
    
    // Stop moving
    servoLeft.write(90);
    servoRight.write(90);

    // Write some information to the serial (USB) connection.
    // This can be used for debugging.
    counter++;
    Serial.print("Completed move number: ");
    Serial.println(counter);
}


