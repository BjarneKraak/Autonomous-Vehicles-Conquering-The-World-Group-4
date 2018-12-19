
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

int i; int RightTot=0; int LeftTot=0; int LeftAvg=0; int RightAvg=0; int left_value; int right_value;
void loop()
{
  
    while(1){
      move.driveInf('f'); 
      for(i=0; i<5; i++){
      left_value = analogRead(LEFT_SENSOR);
      right_value = analogRead(RIGHT_SENSOR);
      LeftTot=left_value+LeftTot;
      RightTot=right_value+RightTot;
      }
    LeftAvg=LeftTot/5;
    RightAvg=RightTot/5;
    LeftTot=0;
    RightTot=0;

    Serial.print("Left sensor value: ");
    Serial.print(LeftAvg);
    Serial.print("; right sensor value: ");
    Serial.print(RightAvg);
    Serial.println();
    
    if(LeftAvg>700){
      move.turn(20,'l');}
    else if(RightAvg>700){
      move.turn(20,'r');}
    }
  
 

}


