// Example Arduino Sketch that uses the line following sensors

// The line follow sensors are connected to the A0 and A1 analog inputs
// of the Arduino board (check the wires and look at the breadboard)
#define LEFT_SENSOR A0
#define RIGHT_SENSOR A1


// All your sketches should have a 'setup' function
// This function is called only once, at the start of the program
void setup() 
{
  // initialize serial communication:
  // Needed to enable printing debug information
  Serial.begin(9600);
}


// All sketches should have a 'loop' function.
// This function is called over and over again when the program is running
// When it ends it immediately starts again.
void loop()
{

  // Read the sensor values. The sensors can be used as analog or as digital inputs.
  // Here we use them as analog inputs
  // The analogRead function returns a value between 0 and 1023 depending on the input to the sensor.
  // When the surface is darker, the value will be lower and when the surface is lighter, the value will be higher.
  int left_value = analogRead(LEFT_SENSOR);
  int right_value = analogRead(RIGHT_SENSOR);

  // Write the sensor input values to the debugging channel
  Serial.print("Left sensor value: ");
  Serial.print(left_value);
  Serial.print("; right sensor value: ");
  Serial.print(right_value);
  Serial.println();
  
}


