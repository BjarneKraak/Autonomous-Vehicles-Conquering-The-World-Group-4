
#define LEFT_SENSOR A0 //left IR sensor pin
#define RIGHT_SENSOR A1 //right IR sensor pin
#define ULTRASONIC_SERVO 11 //servo pin for turning ultrasonic sensor
#define DISTANCE 9 // servo pin for ultrasonic sensor

//include code for turning ultrasonic sensor
#include <Servo.h> 
Servo USServo;        // Create Servo object to control the servo 

//information for initializing zigbee module:
    // configure the next line with a unique ID number for every robot!
    #define SELF     1
    
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

//code for moving
#include <Movement.h> // include movement library
Movement move(13,12,false); // declare a class, use pins 13 (for left servo) and 12 (for right servo) and choose whether you want to debug or not

//global variables:
long last_time; //takes track of last time a turn was taken
int speed_factor = 8; //initial value for speed, range between 0 and 10
const int debug = false; //if debugging is turned on, many print statements will be executed

char data; //wireless data
int head_pos = 90;
int add_amount = 10;

void setup()
{
  // initialize serial communication:
  // Needed to enable printing debug information
  Serial.begin(9600);
  move.begin(9600);
  last_time = millis(); // initalize last_time value with current time
  move.stopDriving(); // make sure the robot doesn't move
  xbee_init();
  Serial.println("This is the lab_4 algorithm");
  USServo.attach(ULTRASONIC_SERVO);  // Servo is connected to digital pin 11
  
  int angle;
  char turn_dir;
  computeAngle(head_pos, &angle, &turn_dir);
  turnHead(angle,turn_dir); // turn head to center (zero degrees to the left)
}

void loop()
{
  while (Serial.available()>0) 
  {
    data = Serial.read();
  }
  switch (data)
  {
    case 'l':
    {
      turnHead(0, 'l');
      head_pos = 90;
      move.turnInf('l', 3);
      break;
    }
    case 'r':
    {
      turnHead(0, 'l');
      head_pos = 90;
      move.turnInf('r', 3);
      break;
    }
    case 'f':
    {
      move.driveInf('f',3);
      sweepHead();
      break;
    }
    case 'b':
    {
      turnHead(0, 'l');
      head_pos = 90;
      move.driveInf('b',3);
      break;
    }
    case 's':
    {
      turnHead(0, 'l');
      move.stopDriving();
      break;
    }
    case 't':
    {
      turnHead(0, 'l');
      move.stopDriving();
      int turn_dir;
      while (Serial.available()>0) 
      {
        turn_dir = Serial.read();
      }
      switch (turn_dir)
      {
        case 'l':
        {
          move.turn(30, 'l');
          move.moveStraight(15, 'f');
          delay(4000);
          break;
        }
        case 'r':
        {
          move.turn(30, 'r');
          move.moveStraight(15, 'f');
          delay(4000);
          break;
        }
      }
      data = '0'; //reset data
    }
  }
  
  char problem = checkForProblems();
  if (problem != 'N') //if there's a problem
  {
    if (debug) Serial.println("A problem occured");
    move.stopDriving();
    actToProblem(problem);
    data = '0';
       while (Serial.available()>0) 
      {
        int crap = Serial.read();
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

void turnHead(int angle, char dir){ 
  if (angle>35)
  {
    angle = 35;
  }
  if (angle<0){
    angle = 0;
  }
  switch (dir){
    case 'l':
    {
      if (debug)
      {
        Serial.println("turn head to left");
      }
      USServo.write(90+angle);   // Rotate servo counter left
      break;
    }
    case 'r':
    {
      if (debug)
      {
        Serial.println("turn head to right");
      }
      USServo.write(90-angle);     // Rotate servo right
      break;
    }
  }
  delay(10); //give time for head to turn;
}

bool sweepHeadTime(int delta_time)
{
  long cur_time = millis();
  if (cur_time - last_time > delta_time)
  {
    last_time = cur_time;
    return true;
  }
  else
  {
    return false;
  }
}

void sweepHead()
{
  if(sweepHeadTime(30))
  {
    head_pos += add_amount;
    if (head_pos<55 || head_pos>135)
    {
      add_amount = -add_amount;
    }
    turnHeadPos(head_pos);
  }

}

void computeAngle(int head_pos, int *angle, char *turn_dir){ 
  // next part of code is used to convert the angle found by ultrasound sensor (0-180 degrees), where completely right is 0 and completely left is 180
  // new angle: 0 is straight forward. Now an angle and a direction (left or right) has to be entered. angle between 0 and infinty degrees. turn direction 0 (left) or 1(right).
  if(head_pos > 90){ // if largest distance is found on left side of robot
    *turn_dir = 'l'; // robot should turn left
    *angle = head_pos - 90; 
  }
  else if(head_pos < 90){ // if largest distance is found on right side of robot
    *turn_dir = 'r'; // robot should turn right
    *angle = 90 - head_pos; 
  }
}

void turnHeadPos(int head_pos)
{
  int angle;
  char turn_dir;
  computeAngle(head_pos, &angle, &turn_dir);
  turnHead(angle,turn_dir);
}

char checkForProblems()
{
  int problem = 'N';
  int left_avg = findLeftIRAvg();
  int right_avg = findRightIRAvg();
  long distance = ultraMeasuredDistance();

  if(left_avg>700) // if there's a line on the left side
  {
    problem = 'L';
  }
  else if(right_avg>700) // if there's a line on the right side
  {
    problem = 'R';
  }
  else if(distance < 15)
  {
    problem = 'O';
  }

  return problem;
}

int findBestPos(){ 
  int pos = 0;    // variable to store the servo position
  int begin_pos = 45; // startposition for the servo connected to the ultrasound sensor
  int end_pos = 135; // endposition for the servo connected to the ultrasound sensor 
  int delta_pos = 4; // the size of the step in changing the position of the servo connected to the ultrasound sensor 
  int delay_time = 20; // time it waits between changing positions
  int larg_dist = 0; // keep track of the largest distance that is found
  int larg_pos;
  int smal_dist = 500; // keep track of the smallest distance that is found
  long distance; //keep track of distance that it takes to reflect a signal

  USServo.write(begin_pos); // move head in begin position
  delay(100); // delay for stability
  for (pos = begin_pos; pos <= end_pos; pos += delta_pos)
  { // turn the head in the given range
    USServo.write(pos); // tell servo to go to position in variable 'pos'
    delay(delay_time); // delay for delay_time
    distance = ultraMeasuredDistance(); // find the distance to the wall or object in front of the sensor
    if (distance > larg_dist)
    { // if the current distance is larger then the largestDistance that is found until now
      larg_dist = distance; // change the larg_dist into the currentdistance (which is the largest distance that is found until now)
      larg_pos = pos; // save the position at which the larg_dist occurs
    }
  }
  return larg_pos;
}

void actToProblem(char problem)
{
  switch (problem)
  {
    case 'L':
    {
      move.moveStraight(8, 'b');
      move.turn(40, 'r', 8);
      move.driveInf('f', 3);
      long cur_time = millis();
      while(millis() - cur_time < 1500)
      {
          char problem = checkForProblems();
          if (problem != 'N') //if there's a problem
          {
            if (debug) Serial.println("A problem occured");
            move.stopDriving();
            move.moveStraight(8, 'b');
          }
      }
      move.stopDriving();
      
      break;
    }
    case 'R':
    {
      move.moveStraight(8, 'b');
      move.turn(40, 'l', 8);
      move.driveInf('f', 3);
      long cur_time = millis();
      while(millis() - cur_time < 1500)
      {
          char problem = checkForProblems();
          if (problem != 'N') //if there's a problem
          {
            if (debug) Serial.println("A problem occured");
            move.stopDriving();
            move.moveStraight(8, 'b');
          }
      }
      move.stopDriving();
      break;
    }
    case 'O':
    {
      move.moveStraight(8, 'b');
      int best_pos = findBestPos();
      if (best_pos<90)
      {
        best_pos = 30;
      }
      else
      {
        best_pos = 150;
      }
      int angle;
      char turn_dir;
      computeAngle(best_pos, &angle, &turn_dir);
      move.turn(angle,turn_dir);
      move.driveInf('f', 3);
      long cur_time = millis();
      while(millis() - cur_time < 1500)
      {
          char problem = checkForProblems();
          if (problem != 'N') //if there's a problem
          {
            if (debug) Serial.println("A problem occured");
            move.stopDriving();
            move.moveStraight(8, 'b');
          }
      }
      move.stopDriving();
      break;
    }
  }
}



