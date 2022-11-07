#define EN        8       // stepper motor enable, low level effective

#define X_DIR     5       //X axis, stepper motor direction control 
#define Y_DIR     6       //y axis, stepper motor direction control
#define Z_DIR     7       //zaxis, stepper motor direction control

#define X_STP     2       //x axis, stepper motor control
#define Y_STP     3       //y axis, stepper motor control
#define Z_STP     4       //z axis, stepper motor control
/*
// Function: step   -control the direction and number of steps of the stepper motor
// Parameter: dir  -direction control, dirPin corresponds to DIR pin, stepperPin corresponds to 


step pin, steps is the number of steps.
// no return value
*/
#include <Servo.h>
Servo myservo;


void step(boolean dir, byte dirPin, byte stepperPin, int steps)
{
  digitalWrite(dirPin, dir);
  delay(50);
  for (int i = 0; i < steps; i++) {
    digitalWrite(stepperPin, HIGH);
    delayMicroseconds(800);  
    digitalWrite(stepperPin, LOW);
    delayMicroseconds(800);  
  }
}


void setup(){// set the IO pins for the stepper motors as output 
  Serial.begin(115200);
  myservo.attach(13);
  myservo.write(90);
  pinMode(X_DIR, OUTPUT); pinMode(X_STP, OUTPUT);
  pinMode(Y_DIR, OUTPUT); pinMode(Y_STP, OUTPUT);
  pinMode(Z_DIR, OUTPUT); pinMode(Z_STP, OUTPUT);
  pinMode(EN, OUTPUT);
  digitalWrite(EN, LOW);
}

int mode=0;

void loop(){
  
  
  signed int xyz;          //x 축 최대 가동범위 2050
  while (Serial.available()==0);
  xyz = Serial.parseInt();

//  if (xyz == 10) mode=0;
//  else if (xyz==20) mode=1;

  
  if (abs(xyz)>10000 && abs(xyz)<20000){
    int x;
    if (xyz<0){
    x = xyz +10000;
//    Serial.println(x);
    step(true, X_DIR, X_STP, abs(x)); // x axis motor rotates CCW for 1 circle
    }
    else{
    x = xyz - 10000;
//    Serial.println(x);
    step(false, X_DIR, X_STP, abs(x)); // x axis motor rotates CW for 1 circle
    }
    if (mode==0) {delay(100);Serial.println("END");}
    
  }  

         // y축 최대 가동 범위 2700
  else if(abs(xyz)>20000 && abs(xyz)<30000){
    int y;
    if (xyz<0){
      y = xyz +20000;
//      Serial.println(y);
      step(false, Y_DIR, Y_STP, abs(y)); // x axis motor rotates CCW for 1 circle
    }
    else{
      y = xyz-20000;
//      Serial.println(y);
      step(true, Y_DIR, Y_STP, abs(y)); // x axis motor rotates CW for 1 circle
    }
    if (mode==0) {delay(150);    Serial.println("END");}
  }  

 
  else if (abs(xyz)>30000){
    int z; 
    if (xyz<0){
      z = xyz+30000;
//      Serial.println(z);
      step(false, Z_DIR, Z_STP, abs(z)); // x axis motor rotates CCW for 1 circle
    }
    else{
      z = xyz-30000;
//      Serial.println(z);
      step(true, Z_DIR, Z_STP, abs(z)); // x axis motor rotates CW for 1 circle
    }
    delay(150);
    Serial.println("END");
  }  

  else if (xyz == 0 || xyz== 1){
    if (xyz == 0){  
//      Serial.println("잡기");
      myservo.write(110);
      delay(900);
      myservo.write(90);
      delay(500);
    }
    else if (xyz== 1){    
//      Serial.println("놓기"); 
      myservo.write(70);
      delay(1000);
      myservo.write(90);
      delay(500);
    }
    delay(100);
    Serial.println("END");
  }





//  step(false, X_DIR, X_STP, x); // x axis motor rotates CCW for 1 circle, as in 200 steps
//  step(false, Y_DIR, Y_STP, 200); // y axis motor rotates CCW for 1 circle, as in 200 steps
//  step(false, Z_DIR, Z_STP, 200); // z axis motor rotates CCW for 1 circle, as in 200 steps
//  delay(1000);
//  step(true, X_DIR, X_STP, 400); // X axis motor rotates CW for 1 circle, as in 200 steps
//  step(true, Y_DIR, Y_STP, 200); // y axis motor rotates CW for 1 circle, as in 200 steps
//  step(true, Z_DIR, Z_STP, 300); // z axis motor rotates CW for 1 circle, as in 200 steps
//  delay(1000);
  Serial.read();  

}
