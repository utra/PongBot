/*

UTRA Top Secret PongBot

TODO:
- Implement is_button_pressed, to read if we should shoot now
- Implement initialize_sweep
- Implement main sweep loop
  - Will require reading from LIDAR
- Implement aim
- Implement spin_shooting motors
  - Will require calculating required speed, and from that, voltage
- Implement push_ball

*/

// Angle between leftmost edge and rightmost edge
#define  SCAN_ANGLE   5.0

float left_edge;
float right_edge;
boolean active;

// Checks if button triggering firing is pressed
boolean is_button_pressed() {
  return false;
}

// Function to sweep from left to right. Returns [distance, angle] of closest cup
float *perform_sweep() {
  // initialize variables to keep track of
  float *closest_cup; // [distance, angle]

  //initialize_sweep(); // Set current angle to be left_edge
  // for loop to go from left edge to right edge, reading from sensor every time
  
  // closest_cup[0] = closest_distance;
  // closest_cup[1] = best_angle;
  return closest_cup;
}

// Function to shoot at a given [distance, angle] target
void shoot(float *closest_cup) {
  float distance = closest_cup[0];
  float angle = closest_cup[1];
  
  // aim(angle) // rotate to point in the right direction
  // spin_shooting_motors(distance) // calculate required speed of shooting motors
  // push_ball() // talk to solenoid, trigger pushing the ball
}


void setup() {  
  left_edge = -0.5*SCAN_ANGLE;
  right_edge = 0.5*SCAN_ANGLE;
  active = false;
}

void loop() {
  active = is_button_pressed();
  if (active) {
    float *closest_cup = perform_sweep();
    shoot(closest_cup);
  }
  delay(15);
}
