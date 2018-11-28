#include <Movement.h> // include movement library

Movement move(13,12,false); // declare a class, use pins 13 (for left servo) and 12 (for right servo) and choose whether you want to debug or not

void setup() {
  move.begin(9600); // attach pins to servos, if asked setup Serial communicatoin for debugging

  //example movements:
  move.stopDriving(); // stop turning
}

void loop()
{

}
