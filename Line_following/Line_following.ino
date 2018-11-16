
#define LEFT_SENSOR A0
#define RIGHT_SENSOR A1
#include <Movement.h> // include movement library

Movement move(13,12,false); // declare a class, use pins 13 (for left servo) and 12 (for right servo) and choose whether you want to debug or not

//global variables:
long cur_time;
long last_time;
long last_time2;
int speed_factor = 4; //official range between 0 and 10
bool adjustment = false;

const int debug = true;

void setup() 
{
  // initialize serial communication:
  // Needed to enable printing debug information
  Serial.begin(9600);
  move.begin(9600);

  last_time = millis();
  last_time2 = millis();
}

void loop()
{
    while(1)
    {
      move.driveInf('f', speed_factor); 
      cur_time = millis();
      int left_avg = findLeftIRAvg();
      int right_avg = findRightIRAvg();

      /*
      Serial.print("Left sensor value: ");
      Serial.print(left_avg);
      Serial.print("; right sensor value: ");
      Serial.print(right_avg);
      Serial.println();
      */
    
      if(left_avg>700)
      {
        if (debug) Serial.println("line on left side, turn a bit left");
        move.turn(20,'l',3);
        adjustment = true;
      }
      else if(right_avg>700)
      {
        adjustment = false;
        if (debug) Serial.println("line on left right, turn a bit right");
        move.turn(20,'r',3);
        adjustment = true;
      }
      
      if(adjustment) //if adjustments are made
      {
        adjustment = false;
        last_time = cur_time;
        last_time2 = cur_time;
        
        if ( cur_time - last_time < 1000) // decrease speed if time between turnings is small
        {
          speed_factor = speed_factor - 2;
          if (speed_factor<3) speed_factor = 2;
          if (speed_factor>7) speed_factor = 7;
          if (debug){
            Serial.print("time between turnings is small, slow down till speedfactor: ");
            Serial.println(speed_factor);
          }
        }
      }
      
      // if there's 900ms that no changes are made, speed up
      if(cur_time - last_time2 > 900)
      {
          last_time2 = millis();
          speed_factor = speed_factor + 1;
          if (speed_factor<3) speed_factor = 2;
          if (speed_factor>7) speed_factor = 7;
          if (debug){
            Serial.print("time between turnings is great, speed up till speedfactor: ");
            Serial.println(speed_factor);
          }
      }
    }
}

int findLeftIRAvg()
{
  int left_tot = 0;
  for(int i=0; i<10; i++)
  {
    int left_value = analogRead(LEFT_SENSOR);
    left_tot=left_value+left_tot;
  }
  int left_avg = left_tot/10;
  return left_avg;
}

int findRightIRAvg()
{
  int right_tot = 0;
  for(int i=0; i<10; i++)
  {
    int right_value = analogRead(RIGHT_SENSOR);
    right_tot=right_value+right_tot;
  }
  int right_avg = right_tot/10;
  return right_avg;
}


