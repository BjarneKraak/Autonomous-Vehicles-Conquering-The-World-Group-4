
#define LEFT_SENSOR A0
#define RIGHT_SENSOR A1
#include <Movement.h> // include movement library

Movement move(13,12,false); // declare a class, use pins 12 (for left servo) and 13 (for right servo) and choose whether you want to debug or not

void setup() 
{
  // initialize serial communication:
  // Needed to enable printing debug information
  Serial.begin(9600);
  move.begin(9600);
}

void loop()
{
    while(1){
      move.driveInf('f'); 
      int left_avg = findLeftIRAvg();
      int right_avg = findRightIRAvg();

      Serial.print("Left sensor value: ");
      Serial.print(left_avg);
      Serial.print("; right sensor value: ");
      Serial.print(right_avg);
      Serial.println();

      if(left_avg>700 && right_avg>700){
      Serial.print("AAAAAAAAAAAAAA");
      move.moveStraight(50,'f');
      }
      else if(left_avg>700){
        move.turn(20,'l');
        }
      else if(right_avg>700){
        move.turn(20,'r');
        }
    }
}

int findLeftIRAvg(){
  int left_tot = 0;
  for(int i=0; i<10; i++){
    int left_value = analogRead(LEFT_SENSOR);
    left_tot=left_value+left_tot;
  }
  int left_avg = left_tot/10;
  return left_avg;
}

int findRightIRAvg(){
  int right_tot = 0;
  for(int i=0; i<10; i++){
    int right_value = analogRead(RIGHT_SENSOR);
    right_tot=right_value+right_tot;
  }
  int right_avg = right_tot/10;
  return right_avg;
}


