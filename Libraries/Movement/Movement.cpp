#include <Movement.h> // include header file

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

void Movement::moveStraight(int distance, char drive_dir){
  float mv_time = (distance * 68); // calcute time to move depending on enterend distance
  if(drive_dir == 'f') { // if robot should move forward
    maneuver(200, 200, mv_time); // move forward for mv_time ms
    maneuver(0, 0, 1); // stop moving
    if (_debug){ // if debug is on, print following:
      Serial.print("move forwards for ");
      Serial.print(mv_time);
      Serial.println("ms");
    }
  }
  else if(drive_dir == 'b') { // if robot should move backwards
    maneuver(-200, -200, mv_time); // move backwards for mv_time ms
    maneuver(0, 0, 1); // stop moving
    if (_debug){ // if debug is on, print following:
      Serial.print("move backwards for ");
      Serial.print(mv_time);
      Serial.println("ms");
    }
  }
}

void Movement::maneuver(int speed_left, int speed_right, int ms_time){
  // speedLeft, speedRight ranges: Backward  Linear  Stop  Linear   Forward
  //                               -200      -100......0......100       200
  servo_left.writeMicroseconds(1500 + speed_left);   // Set Left servo speed
  servo_right.writeMicroseconds(1500 - speed_right); // Set right servo speed
  delay(ms_time);                                   // Delay for msTime
}

void Movement::turn(int angle, char turn_dir){ // turning function, angle and direction needs to be entered
  int turn_time = ((angle * 6.0)); // variable that contains time to turn depended on angle
  if(turn_dir == 'r') { // if robot should turn right
    maneuver(200, -200, turn_time); // turn right for turn_time ms
    maneuver(0, 0, 1); // stop moving
    if (_debug){// if debug is on, print following:
      Serial.print("turn to the right for ");
      Serial.print(turn_time);
      Serial.println("ms");
    }
  }
  else if (turn_dir == 'l') { // if robot should turn left
    maneuver(-200, 200, turn_time); // turn left for turn_time ms
    maneuver(0, 0, 1); // stop moving
    if (_debug){// if debug is on, print following:
      Serial.print("turn to the left for ");
      Serial.print(turn_time);
      Serial.println("ms");
    }
  }
}

void Movement::driveInf(char drive_dir){
  if(drive_dir == 'f') { // if robot should move forward
    maneuver(200, 200, 1); // move forward
    if (_debug){// if debug is on, print following:
      Serial.println("move forwards until stop is called");
    }
  }
  else if(drive_dir == 'b') { // if robot should move backwards
    maneuver(-200, -200, 1); // move backwards
    if (_debug){// if debug is on, print following:
      Serial.println("move backwards until stop is called");
    }
  }
}

void Movement::turnInf(char turn_dir){
  if(turn_dir == 'r') { // if robot should turn right
    maneuver(200, -200, 1); // turn right
    if (_debug){// if debug is on, print following:
      Serial.print("turn to the right until stopDriving is called");
    }
  }
  else if(turn_dir == 'l') { //if robot should turn left
    maneuver(-200,200,1); //turn left
    if (_debug){// if debug is on, print following:
      Serial.print("turn to the left until stopDriving is called");
    }
  }
}

void Movement::stopDriving(){
  servo_left.write(90);
  servo_right.write(90);
  if (_debug){// if debug is on, print following:
    Serial.println("stopped with driving");
  }
}
