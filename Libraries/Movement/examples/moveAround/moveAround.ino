#include <Movement.h> // include movement library

Movement move(12,13,false); // declare a class, use pins 12 (for left servo) and 13 (for right servo) and choose whether you want to debug or not

void setup() {
  move.begin(9600); // attach pins to servos, if asked setup Serial communicatoin for debugging

  //example movements:
  move.moveStraight(10, 'f'); // move 10 cm forwards
  move.turn(100,'r'); // turn 100 degrees to the left
  move.moveStraight(20, 'b'); // move 20 cm backwards
  delay(1000); // delay for 1s
  move.driveInf('f'); //drive infinitly forward, until other functions are called
  delay(3000);// delay for 3s
  move.stopDriving(); // stop driving
  move.turnInf('l'); //turn infinitly to the left, until other functions are called
  delay(2000); // delay for 2s
  move.stopDriving(); // stop turning
}

void loop() {
 
}
