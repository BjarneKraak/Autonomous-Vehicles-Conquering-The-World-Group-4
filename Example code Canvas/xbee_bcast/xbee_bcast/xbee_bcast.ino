// this program uses the Arduino XBee shield, more info at the link below.
// https://www.arduino.cc/en/Guide/ArduinoXbeeShield

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


// initialize the LED light on the board
void led_init(void)
{
  // set the pin mode for the LED light pin to OUTPUT
  pinMode(LED_BUILTIN,   OUTPUT);
  // turn the LED off
  digitalWrite(LED_BUILTIN,   LOW);
}


// the xbee_init function initializes the XBee Zigbee module
// When the program is *running*, the switch on the wireless proto shield should be in the position 'MICRO'.
// During programming of the Arduino, the switch should be in the position 'USB'.
// It will only work if the XBee module is set to communicate at 9600 baud. If it is not, the module needs to be reprogrammed
// on the USB XBee dongle using the XCTU program.
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

// This function is called only once, at the start of the program
void setup(void)
{
  // initialize the XBee wireless module
  xbee_init();
  // initialize the LED light on the Arduino board
  led_init();
  // send something on the wireless network
  Serial.println("This is the XBee - Broadcast program.");
}


// This function is called over and over again when the program is running
void loop(void)
{
  // define an integer counter variable, 'static' means that it will retain its value when the function ends and is called again.
  static int count = 0;

  // toggle the LED on and off for some visual feedback
  if (count % 2 == 0)
  {
    digitalWrite(LED_BUILTIN, 1);
  } else {
    digitalWrite(LED_BUILTIN, 0);
  }
  
  // send my ID and the current value of the counter on the wireless network
  Serial.print("Robot nr: ");
  Serial.print(SELF);
  Serial.print(", counter value: ");
  Serial.println(count);

  // increase the counter by 1
  count += 1;

  // check if there is some incoming data from the wireless network
  if (Serial.available()>0) {
    // uncommenting the Serial.print / Serial.write lines below will echo the incoming data back onto the network, 
    // this could be usefull for debugging, because the incoming data will not show up on
    // the monitor in the Arduino IDE, but the data that is sent will.
    // Note however, that if you have multiple robots in the network these echos are going to ping pong across the network!!
    
    // Serial.print("Echo incoming data: ");
    
    // as long as there is more data in the input buffer...
    while (Serial.available()>0){
      // declare a variable to hold the data coming in from the serial link
      // note that it is a number (int 0-255), characters are usually encoded to numbers using ASCII codes
      int incomingByte = 0;
      // read the incoming data from the serial connection
      incomingByte = Serial.read();
      // echo it back to the serial connection. Note that we use 'write' and not 'print', because we do not want it to show up 
      // as a readable version of the number, but as the original character.

      Serial.write(incomingByte);
    }
    // end the echoing of the incoming data with a new line
    // Serial.println("");
  }
  // delay for a second before the loop function is called again
  delay(1000);
}

