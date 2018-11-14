#include <Movement.h> // include movement library

Movement move(12,13,false); // declare a class, use pins 12 (for left servo) and 13 (for right servo) and choose whether you want to debug or not

void setup() {
  move.begin(9600); // attach pins to servos, if asked setup Serial communicatoin for debugging

  //example movements:
  move.moveStraight(10, 'f'); // move 10 cm forwards
  move.turn(90, 'l');
  move.turnInf('r');
  //move.stopDriving;

}

void loop() {
 
}
