
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
long cur_time; // takes track of current time
long last_time; //takes track of last time a turn was taken
int speed_factor = 8; //initial value for speed, range between 0 and 10
const int debug = false; //if debugging is turned on, many print statements will be executed

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
  turnHead(0,'l'); // turn head to center (zero degrees to the left)
}

void loop()
{
  move.driveInf('f', speed_factor); //drive forward with current chosen speed
  cur_time = millis(); // save current time
  
  //find sensor values for IR sensors and ultrasonic Distance:
  int left_avg = findLeftIRAvg();
  int right_avg = findRightIRAvg();
  long distance = ultraMeasuredDistance();

  if(distance < 15) //if car in front is too close
  {
    move.stopDriving(); // stop driving
    delay(1000);
    if (debug) Serial.print("wait for object in front of me");
  }

  if(left_avg>700) // if there's a line on the left side
  {
    if (debug) Serial.println("line on left side detected");
    move.moveStraight(10, 'b', 8);
    move.turn(40,'r',5); // turn a bit to the left

  }
  else if(right_avg>700) // if there's a line on the right side
  {
    if (debug) Serial.println("line on left right detected");
    move.moveStraight(10, 'b', 8);
    move.turn(40,'l',5); // turn a bit to the right
  }

  if (cur_time - last_time > 700)
  {
    last_time = cur_time;
    // something to do when time has elapsed
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
  //Serial.print(ATCROSSING);
  while (Serial.available()>0) {
    int crap = Serial.read();
  }
  //channel is free
  Serial.print('1'); // robot is at crossing

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
    move.driveInf('f', 4);
    int left_avg = findLeftIRAvg();
    int right_avg = findRightIRAvg();
    long distance = ultraMeasuredDistance();

    if(distance < 15) //if car in front is too close
    {
      move.stopDriving(); // stop driving
      if (debug) Serial.print("wait for car in front of me");
      delay(500);  // wait for 500 ms
    }

    if(left_avg>700) // if there's a line on the left side
    {
      move.moveStraight(8, 'b', 8);
      if (debug) Serial.println("line on left side, turn a bit left");
      move.turn(40,'r',3); // turn a bit to the left
    }
    else if(right_avg>700) // if there's a line on the right side
    {
      move.moveStraight(8, 'b', 8);
      if (debug) Serial.println("line on left side, turn a bit right");
      move.turn(20,'l',3); // turn a bit to the right
    }
  }
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
}
