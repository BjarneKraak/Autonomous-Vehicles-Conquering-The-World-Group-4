#include <Movement.h> // include movement library

Movement move(13,12,false); // declare a class, use pins 13 (for left servo) and 12 (for right servo) and choose whether you want to debug or not

void setup() {
  move.begin(9600); // attach pins to servos, if asked setup Serial communicatoin for debugging

  //example movements:
  move.moveStraight(10, 'f', 10); // move 10 cm forwards on full speed
  move.turn(20,'r',10); // turn 100 degrees to the left
  move.moveStraight(20, 'b', 10); // move 20 cm backwards on full speed
  delay(1000); // delay for 1s
  move.driveInf('f', 3); //drive infinitly forward on half speed, until other functions are called
  delay(3000);// delay for 3s
  move.stopDriving(); // stop driving
  move.turnInf('l', 2); //turn infinitly to the left on 3/10 speed, until other functions are called
  delay(2000); // delay for 2s
  move.stopDriving(); // stop turning
}

void loop()
{

}
