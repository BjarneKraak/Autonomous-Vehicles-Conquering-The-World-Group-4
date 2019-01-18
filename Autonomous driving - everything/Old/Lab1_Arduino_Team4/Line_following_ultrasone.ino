
#define LEFT_SENSOR A0
#define RIGHT_SENSOR A1
#define DISTANCE 9 // sensor pin ultrasone
#include <Movement.h> // include movement library

Movement move(13,12,false); // declare a class, use pins 13 (for left servo) and 12 (for right servo) and choose whether you want to debug or not

//global variables:
long cur_time; // takes track of current time
long last_time; //takes track of last time a turn was taken
long last_time2; //takes track of last time a turn was taken or speed was increased
int speed_factor = 4; //initial value for speed, range between 0 and 10
bool adjustment = false;

const int debug = true;

void setup() 
{
  // initialize serial communication:
  // Needed to enable printing debug information
  Serial.begin(9600);
  move.begin(9600);
  // initalize last_time values with current time
  last_time = millis();
  last_time2 = millis();
}

void loop()
{
    while(1) // infinite while loop
    {
      move.driveInf('f', speed_factor); //drive forward with current chosen speed
      cur_time = millis(); // save current time
      //find sensor values for IR sensors:
      int left_avg = findLeftIRAvg();
      int right_avg = findRightIRAvg();
      //find distance with ultrasone sensor:
      long distance = ultraMeasuredDistance();
      
      if(distance < 26) //if car in front is too close
      {
        move.stopDriving(); // stop driving
        if (debug) Serial.print("wait for car in front of me");
        delay(500);  // wait for 500 ms
      }

      /* no crossings in lab test
      if(left_avg>700 && right_avg>700) // if there's a line on both sides aka crossing
      {
        if (debug) Serial.print("Crossing is detected, cross line");
        move.moveStraight(3,'f',8); //move straight for 3 cm before checking IR sensors again
      }
      else 
      
      */
      if(left_avg>700) // if there's a line on the left side
      {
        if (debug) Serial.println("line on left side, turn a bit left");
        //move.moveStraight(2,'b',8);
        move.turn(20,'l',3); // turn a bit to the left
        adjustment = true; //adjustment is made
      }
      else if(right_avg>700) // if there's a line on the right side
      {
        if (debug) Serial.println("line on left right, turn a bit right");
        move.turn(20,'r',3); // turn a bit to the right
        adjustment = true; //adjustment is made
      }
      
      if(adjustment) //if adjustments are made
      {
        adjustment = false; //for next time
        last_time = cur_time; //save last_time as current time
        last_time2 = cur_time;
        
        if ( cur_time - last_time < 1000) // decrease speed if time between turnings is small
        {
          speed_factor = speed_factor - 2; //decrease speed quite quick
          if (speed_factor<3) speed_factor = 2; //min 2
          if (speed_factor>7) speed_factor = 7; // max 7
          if (debug){
            Serial.print("time between turnings is small, slow down till speedfactor: ");
            Serial.println(speed_factor);
          }
        }
      }
      
      // if there's 700ms that no changes are made, speed up
      if(cur_time - last_time2 > 700)
      {
          last_time2 = millis(); 
          speed_factor = speed_factor + 1; //increase speed quite slow
          if (speed_factor<3) speed_factor = 2;//min 2
          if (speed_factor>7) speed_factor = 7;// max 7
          if (debug){
            Serial.print("time between turnings is great, speed up till speedfactor: ");
            Serial.println(speed_factor);
          }
      }
    }
}

int findLeftIRAvg() //calculate the average of 10 readings
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

int findRightIRAvg() //calculate the average of 10 readings
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

long ultraMeasuredDistance() {
    long duration;
    pinMode(9, OUTPUT); //first trigger sensor, so output needed
    digitalWrite(9, LOW); 
    delayMicroseconds(2);//2
    digitalWrite(9, HIGH); //trigger sensor
    delayMicroseconds(5);//5
    digitalWrite(9, LOW);   //stop triggering
    pinMode(9, INPUT); //wait for output of sensor, pin is now input
    duration = pulseIn(9, HIGH); //receive duration
    return duration/29/2; //calculate distance based on time
  }
