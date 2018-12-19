#include <Movement.h>
#include <Gripper.h>

Movement movement(12,13);
Gripper grip;

int left_IR_pin = A0;
int right_IR_pin = A1;

void setup() {
  // put your setup code here, to run once:
  movement.begin(9600);
  pinMode(left_IR_pin, INPUT);
  pinMode(right_IR_pin, INPUT);
  Serial.begin(9600);
  grip.begin();
  
  grip.gripRock();
}

void loop() {
  while(1){
  movement.driveInf('f');
    if (lineDetectedLeft() && lineDetectedRight()){
      movement.moveStraight(15, 'f');
      movement.turn(80,'r');
      break;
    }
    else if (lineDetectedLeft() && !lineDetectedRight()){
      //movement.moveStraight(7, 'b');
      while(!lineDetectedRight()){
        movement.maneuver(0,50,500);
      }
      while(lineDetectedRight()){
        movement.maneuver(50,50,20);
      }
      break;
      //delay(500);
    }
    else if(lineDetectedRight()&& !lineDetectedLeft()){
      //movement.moveStraight(7, 'b');
      while(!lineDetectedLeft()){
        movement.maneuver(50,0,500);
      }
      while(lineDetectedLeft()){
        movement.maneuver(50,50,20);
      }
      break;
      //delay(500);
    }
  }
  while(1){
  movement.driveInf('f');
  if (lineDetectedLeft() && lineDetectedLeft()){
    movement.moveStraight(5, 'f');
    movement.turn(80,'r');
  }
  else if (lineDetectedLeft() && !lineDetectedRight()){
    movement.moveStraight(7, 'b');
    movement.turn(30,'l');
    //delay(500);
  }
  else if(lineDetectedRight()&& !lineDetectedLeft()){
    movement.moveStraight(7, 'b');
    movement.turn(30,'r');
    //delay(500);
    }
  }
}

bool lineDetectedLeft(){
  int value = analogRead(left_IR_pin);
  Serial.println(value);
  //delay(250);
  if(value > 600){
    
    Serial.println("Line detected on left side");
    return true;
  }
  else {
    Serial.println("Line NOT detected on left side");
    return false;
  }
}

bool lineDetectedRight(){
  int value = analogRead(right_IR_pin);
  Serial.println(value);
  //delay(250);
  if(value > 600){
    Serial.println("Line detected on right side");
    return true;
  }
  else {
    Serial.println("Line NOT detected on right side");
    return false;
  }
}
