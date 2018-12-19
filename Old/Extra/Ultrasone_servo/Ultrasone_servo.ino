#include <Servo.h> 
Servo USServo;        // Create Servo object to control the servo 

void setup() { 
  USServo.attach(11);  // Servo is connected to digital pin 11
} 

void loop() {
   turnServo('l');
   delay(1000);
   turnServo('r');
   delay(1000);
   turnServo('c');
   delay(1000);
}

void turnServo(char dir)
{
  switch (dir){
    case 'l':
    {
      USServo.write(125);   // Rotate servo counter left
      break;
    }
    case 'r':
    {
      USServo.write(55);     // Rotate servo right
      break;
    }
    case 'c':
    {
      USServo.write(90);    // Rotate servo to center
      break;
    }
  }
}

