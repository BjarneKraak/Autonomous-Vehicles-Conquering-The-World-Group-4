#ifndef Movement_h
#define Movement_h
#include <Servo.h>
#include <Arduino.h>

//Function declarations
class Movement{
	public:
    //constructor
		Movement(int left_servo_pin = 12, int right_servo_pin = 13, bool debug=false);

    //public methods:
    void begin(int baudrate = 9600);
		void moveStraight(int distance, char drive_dir);
		void turn(int angle, char char_dir);
    void driveInf(char drive_dir);
    void turnInf(char turn_dir);
    void stopDriving();
	  void maneuver(int speed_left, int speed_right, int ms_time);
	
	private:
    // private methods
		Servo servo_left;
		Servo servo_right;
    
    //private variables
    int _left_servo_pin;
    int _right_servo_pin;
    int _debug;
};

#endif //Movement_h
