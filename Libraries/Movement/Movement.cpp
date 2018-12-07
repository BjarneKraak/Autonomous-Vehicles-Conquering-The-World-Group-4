#include <Movement.h>  // include header file

Movement::Movement(int left_servo_pin, int right_servo_pin, bool debug){
  _left_servo_pin = left_servo_pin; //copy variables to private variables so they can be used in all functions
  _right_servo_pin = right_servo_pin;
  _debug = debug;
}

void Movement::begin(int baudrate){ // begin
  servo_left.attach(_left_servo_pin); //attach left servo
  servo_right.attach(_right_servo_pin); //attach right servo

  if (_debug){ // if debug is on
    Serial.begin(baudrate); // initiate serial communicatian
    Serial.println("Movement library initiated"); //print
  }
}

void Movement::moveStraight(int distance, char drive_dir, int speed_factor){
  int speed_time = findSpeedTime(speed_factor);
  float mv_time = (distance * 68); // calcute time to move depending on enterend distance
  if(drive_dir == 'f') { // if robot should move forward
    maneuver(speed_time, speed_time, mv_time); // move forward for mv_time ms
    maneuver(0, 0, 1); // stop moving
    if (_debug){ // if debug is on, print following:
      Serial.print("move forwards for ");
      Serial.print(mv_time);
      Serial.println("ms");
    }
  }
  else if(drive_dir == 'b') { // if robot should move backwards
    maneuver(-speed_time, -speed_time, mv_time); // move backwards for mv_time ms
    maneuver(0, 0, 1); // stop moving
    if (_debug){ // if debug is on, print following:
      Serial.print("move backwards for ");
      Serial.print(mv_time);
      Serial.println("ms");
    }
  }
}

void Movement::turn(int angle, char turn_dir, int speed_factor){ // turning function, angle and direction needs to be entered
  int speed_time = findSpeedTime(speed_factor);
  int turn_time = ((angle * 6.0)); // variable that contains time to turn depended on angle
  if(turn_dir == 'r') { // if robot should turn right
    maneuver(speed_time, -speed_time, turn_time); // turn right for turn_time ms
    maneuver(0, 0, 1); // stop moving
    if (_debug){// if debug is on, print following:
      Serial.print("turn to the right for ");
      Serial.print(turn_time);
      Serial.println("ms");
    }
  }
  else if (turn_dir == 'l') { // if robot should turn left
    maneuver(-speed_time, speed_time, turn_time); // turn left for turn_time ms
    maneuver(0, 0, 1); // stop moving
    if (_debug){// if debug is on, print following:
      Serial.print("turn to the left for ");
      Serial.print(turn_time);
      Serial.println("ms");
    }
  }
}

void Movement::driveInf(char drive_dir, int speed_factor){
  int speed_time = findSpeedTime(speed_factor);
  if(drive_dir == 'f') { // if robot should move forward
    maneuver(speed_time, speed_time, 1); // move forward
    if (_debug){// if debug is on, print following:
      Serial.println("move forwards until stop is called");
    }
  }
  else if(drive_dir == 'b') { // if robot should move backwards
    maneuver(-speed_time, -speed_time, 1); // move backwards
    if (_debug){// if debug is on, print following:
      Serial.println("move backwards until stop is called");
    }
  }
}

void Movement::turnInf(char turn_dir, int speed_factor){
  int speed_time = findSpeedTime(speed_factor);
  if(turn_dir == 'r') { // if robot should turn right
    maneuver(speed_time, -speed_time, 1); // turn right
    if (_debug){// if debug is on, print following:
      Serial.print("turn to the right until stopDriving is called");
    }
  }
  else if(turn_dir == 'l') { //if robot should turn left
    maneuver(-speed_time,speed_time,1); //turn left
    if (_debug){// if debug is on, print following:
      Serial.print("turn to the left until stopDriving is called");
    }
  }
}

void Movement::stopDriving(){
  //servo_left.write(90);
  //servo_right.write(90);
  servo_left.writeMicroseconds(1475);   // Set Left servo speed
  servo_right.writeMicroseconds(1475);
  if (_debug){// if debug is on, print following:
    Serial.println("stopped with driving");
  }
}

void Movement::maneuver(int speed_left, int speed_right, int ms_time){
  // speedLeft, speedRight ranges: Backward  Linear  Stop  Linear   Forward
  //                               -200      -100......0......100       200
  servo_left.writeMicroseconds(1475 + speed_left);   // Set Left servo speed
  servo_right.writeMicroseconds(1475 - speed_right); // Set right servo speed
  delay(ms_time);                                   // Delay for msTime
}

int Movement::findSpeedTime(int speed_factor){
  // speed_factor between 0 and 10
  if (speed_factor<0)
  {
    speed_factor = 0;
  }
  if (speed_factor>10)
  {
    speed_factor = 10;
  }
  int speed_time;
  speed_time = map(speed_factor, 0, 10, 0, 200);
  return speed_time;
}
