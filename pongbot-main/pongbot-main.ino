/*

UTRA Top Secret PongBot

TODO:
- Implement is_button_pressed, to read if we should shoot now
- Implement main sweep loop
  - Will require reading from LIDAR
- Implement aim
- Implement spin_shooting motors
  - Will require calculating required speed, and from that, voltage
- Implement push_ball

NICE TO HAVE:
- Find left and right edges 'experimentally' and use those to reduce how much sweeping we have to do

*/

#include <Servo.h>
#include <Wire.h>
#define    LIDARLite_ADDRESS   0x62          // Default I2C Address of LIDAR-Lite.
#define    RegisterMeasure     0x00          // Register to write to initiate ranging.
#define    MeasureValue        0x04          // Value to initiate ranging.
#define    RegisterHighLowB    0x8f          // Register to get both High and Low bytes in 1 call.

// Angle between leftmost edge and rightmost edge
#define  SCAN_ANGLE   100
// 1000 microseconds = 180 degrees
// 27 microseconds = 5 degrees

Servo servo;  // create servo object to control a servo 
                // twelve servo objects can be created on most boards
 
int servoPos;    // variable to store the servo position 


float left_edge;
float right_edge;
boolean active;

// Checks if button triggering firing is pressed
boolean is_button_pressed() {
  return true;
}

// Start sweep off at the left edge
void initialize_sweep() {
  servo.writeMicroseconds(left_edge); 
}

// Function to sweep from left to right. Returns [distance, angle] of closest cup
float *perform_sweep() {
  Serial.println("Sweeping");
  
  // initialize variables to keep track of
  float *closest_cup = (float *) malloc(sizeof(float) * 2);
  closest_cup[0] = 100000;
  
  //initialize_sweep(); // Set current angle to be left_edge
  // for loop to go from left edge to right edge, reading from sensor every time
  for(servoPos = left_edge; servoPos <= right_edge; servoPos += 1) // goes from 0 degrees to 180 degrees 
  {                                                                // in steps of 1 degree 
    servo.writeMicroseconds(servoPos);              // tell servo to go to position in variable 'pos' 
    delay(10);                       // waits 10ms for the servo to reach the position 
    
    // Read from lidar
    int reading = read_lidar();
    Serial.println(reading);

      // Check if reading is closer than what we've seen  
      if (reading < closest_cup[0]) {
        closest_cup[0] = reading;
        closest_cup[1] = servoPos;
      }
    
   }

  return closest_cup;
}

int read_lidar() {
      int reading = 0;
      Serial.println("Starting to read");
      Wire.beginTransmission((int)LIDARLite_ADDRESS); // transmit to LIDAR-Lite
      Wire.write((int)RegisterMeasure); // sets register pointer to  (0x00)  
      Wire.write((int)MeasureValue); // sets register pointer to  (0x00)  
      Wire.endTransmission(); // stop transmitting
      Serial.println("Stopped transmitting first byte");    
      delay(20); // Wait 20ms for transmit
    
      Wire.beginTransmission((int)LIDARLite_ADDRESS); // transmit to LIDAR-Lite
      Wire.write((int)RegisterHighLowB); // sets register pointer to (0x8f)
      Wire.endTransmission(); // stop transmitting
      Serial.println("Stopped transmitting second byte");    
    
      delay(20); // Wait 20ms for transmit
    
      Wire.requestFrom((int)LIDARLite_ADDRESS, 2); // request 2 bytes from LIDAR-Lite
      Serial.println("Requested two bytes");    
      
      if(2 <= Wire.available()) // if two bytes were received
      {
        reading = Wire.read(); // receive high byte (overwrites previous reading)
        reading = reading << 8; // shift high byte to be high 8 bits
        reading |= Wire.read(); // receive low byte as lower 8 bits
        Serial.println(reading);
        return reading;
      }
}

// Function to shoot at a given [distance, angle] target
void shoot(float *closest_cup) {
  float distance = closest_cup[0];
  float angle = closest_cup[1];
    
  aim(angle); // rotate to point in the right direction
  // spin_shooting_motors(distance) // calculate required speed of shooting motors
  // push_ball() // talk to solenoid, trigger pushing the ball
}

void aim (float angle){
    servo.writeMicroseconds(angle);
    delay(100);                       // waits 10ms for the servo to reach the position 
}


void setup() {  
  Wire.begin(); // join i2c bus
  Serial.begin(9600); // start serial communication at 9600bps
  
  left_edge = 1500 - 0.5*SCAN_ANGLE;
  right_edge = 1500 + 0.5*SCAN_ANGLE;
  active = false;
  
  Serial.println("Started");
  delay(1000);
  
  // Attach pin 9 output to servo
  servo.attach(9);
}

void loop() {
  active = is_button_pressed();
  if (active) {
    float *closest_cup = perform_sweep();
    shoot(closest_cup);
  }
  delay(15);
}
