#ifndef Movement_h
#define Movement_h
#include <Servo.h>
#include <Arduino.h>

//Function declarations
class Movement{
	public:
    //constructor
		Movement(int left_servo_pin, int right_servo_pin, bool debug=false);

    //public methods:
    void begin(int baudrate = 9600);
		void moveStraight(int distance, char drive_dir, int speed_factor = 10);
		void turn(int angle, char char_dir, int speed_factor=10);
    void driveInf(char drive_dir, int speed_factor=10);
    void turnInf(char turn_dir, int speed_factor=10);
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

		//private functions
		int findSpeedTime(int speed_factor);
};

#endif //Movement_h
