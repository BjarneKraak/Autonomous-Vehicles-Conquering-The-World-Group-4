#include <Servo.h> 

Servo USServo;        // Create Servo object to control the servo 

void setup() { 
  USServo.attach(11);  // Servo is connected to digital pin 11
} 

void loop() {
   
 // USServo.write(125);   // Rotate servo counter left
 // delay(2000);          // Wait 2 seconds
 USServo.write(55);     // Rotate servo right
 delay(2000);
  USServo.write(90);    // Rotate servo to center
  delay(2000); 
}
