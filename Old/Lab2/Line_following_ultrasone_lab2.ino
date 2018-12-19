
#define LEFT_SENSOR A0
#define RIGHT_SENSOR A1
#define ULTRASONE_SERVO 11 //
#define DISTANCE 9 // sensor pin ultrasone
#define ATCROSSING 1
#define DRIVING 0

#include <Movement.h> // include movement library

#include <Servo.h> 
Servo USServo;        // Create Servo object to control the servo 

// configure the next line with a unique ID number for every robot!
#define SELF     3

// Define the pan (personal area network) number
// It must be unique for every team and the same for all robots in one team!
// For team number N use: "A00N"
#define PAN_ID           "A004"

// define a channel ID to use for communication
// It must be the same for all robots in one team!
// It is represented by a 2-digit hexadecimal number between 0B and 1F.
#define CHANNEL_ID       "D"


// some macros needed for the xbee_init function. Do not touch :-).
#define STRING(name) #name
#define TOSTRING(x) STRING(x)

Movement move(13,12,false); // declare a class, use pins 13 (for left servo) and 12 (for right servo) and choose whether you want to debug or not

//global variables:
long cur_time; // takes track of current time
long last_time; //takes track of last time a turn was taken
long last_time2; //takes track of last time a turn was taken or speed was increased
long last_time3; //takes track of last time a turn of the head was taken
int speed_factor = 4; //initial value for speed, range between 0 and 10
bool adjustment = false;

const int debug = false;

int entered_main_loop = true;

void setup()
{
  // initialize serial communication:
  // Needed to enable printing debug information
  Serial.begin(9600);
  move.begin(9600);
  // initalize last_time values with current time
  last_time = millis();
  last_time2 = millis();
  last_time3 = millis();

  move.stopDriving();
  xbee_init();
  Serial.println("This is the XBee - Broadcast program.");
  USServo.attach(ULTRASONE_SERVO);  // Servo is connected to digital pin 11
  turnServo('c');
}

void loop()
{
      if (entered_main_loop){
        //Serial.println("start main loop");
        entered_main_loop = false;
      }
      move.driveInf('f', speed_factor); //drive forward with current chosen speed
      cur_time = millis(); // save current time
      //find sensor values for IR sensors:
      int left_avg = findLeftIRAvg();
      int right_avg = findRightIRAvg();
      //find distance with ultrasone sensor:
      long distance = ultraMeasuredDistance();

      if(distance < 15) //if car in front is too close
      {
        move.stopDriving(); // stop driving
        if (debug) Serial.print("wait for car in front of me");
        delay(1500);  // wait for 500 ms
      }

      if(left_avg>700 && right_avg>700) // crossing is near
      {
        //Serial.write("Arrived at crossing");
        arrivedAtCrossing();
      }
      else if(left_avg>700) // if there's a line on the left side
      {
        if (debug) Serial.println("line on left side, turn a bit left");
        move.turn(20,'l',3); // turn a bit to the left
        turnServo('l');
        last_time3 = millis();
        adjustment = true; //adjustment is made
      }
      else if(right_avg>700) // if there's a line on the right side
      {
        if (debug) Serial.println("line on left right, turn a bit right");
        move.turn(20,'r',3); // turn a bit to the right
        turnServo('r');
        last_time3 = millis();
        adjustment = true; //adjustment is made
      }

      if (cur_time - last_time3 > 700)
      {
        last_time3 = cur_time;
        Serial.println("turn head back");
        turnServo('c');
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

void xbee_init(void)
{
  Serial.begin(9600);                         // set the baud rate to 9600 to match the baud rate of the xbee module
  Serial.flush();                             // make sure the buffer of the serial connection is empty
  Serial.print("+++");                        // sending the characters '+++' will bring the XBee module in its command mode (see https://cdn.sparkfun.com/assets/resources/2/9/22AT_Commands.pdf)
  delay(2000);                                // it will only go in command mode if there is a long enough pause after the '+++' characters. Wait two seconds.
  Serial.print("ATCH " CHANNEL_ID "\r");      // set the channel to CHANNEL_ID
  Serial.print("ATID " PAN_ID "\r");          // set the network PAN ID to PAN_ID
  Serial.print("ATMY " TOSTRING(SELF) "\r");  // set the network ID of this module to SELF
  Serial.print("ATDH 0000\rATDL FFFF\r");     // configure the modue to broadcast all messages to all other nodes in the PAN
  Serial.print("ATCN\r");                     // exit command mode and return to transparent mode, communicate all data on the serial link onto the wireless network
}

void arrivedAtCrossing()
{
  move.stopDriving();
  turnServo('c');
  //Serial.print(ATCROSSING);
  while (Serial.available()>0) {
    int crap = Serial.read();
  }
  //channel is free
  Serial.print(ATCROSSING); // robot is at crossing

  //listen for data:
  int incomingByte = 0;
  while (incomingByte != '1') {
    if (Serial.available()>0){
      // read the incoming data from the serial connection
      incomingByte = Serial.read();
    }
  }
  // incommingByte == ATCROSSING
  move.moveStraight(3,'f',8); //move straight for 3 cm before checking IR sensors again
  goSimpleLineFollowing();
}

void goSimpleLineFollowing()
{
  int crossing_counter = 2;
  while(crossing_counter>0)
  {
    move.driveInf('f', 8);
    int left_avg = findLeftIRAvg();
    int right_avg = findRightIRAvg();
    long distance = ultraMeasuredDistance();

    if(distance < 15) //if car in front is too close
    {
      move.stopDriving(); // stop driving
      if (debug) Serial.print("wait for car in front of me");
      delay(1500);  // wait for 500 ms
    }

    if(left_avg>700 && right_avg>700) // if there's a line on both sides aka crossing
    {
      crossing_counter--;
      //Serial.println("Crossing is detected, cross line");
      move.moveStraight(3,'f',8); //move straight for 3 cm before checking IR sensors again
    }
    else if(left_avg>700) // if there's a line on the left side
    {
      if (debug) Serial.println("line on left side, turn a bit left");
      move.turn(20,'l',3); // turn a bit to the left
    }
    else if(right_avg>700) // if there's a line on the right side
    {
      if (debug) Serial.println("line on left right, turn a bit right");
      move.turn(20,'r',3); // turn a bit to the right
    }
  }
  entered_main_loop = true;

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
