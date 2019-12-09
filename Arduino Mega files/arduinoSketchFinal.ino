const int ledPin = 13;
const int pSensor11 = A0;
const int pSensor12 = A1;
const int pSensor21 = A3;
const int pSensor22 = A4;
const int threshold = 700;

int sensorReading11 = 0;
int sensorReading12 = 0;
int sensorReading21 = 0;
int sensorReading22 = 0;
int ledState = LOW;
int p11s = 0;
int p12s = 0;
int p21s = 0;
int p22s = 0;
bool p12jcrossed = false;
bool p11jcrossed = false;
bool p21jcrossed = false;
bool p22jcrossed = false;

void setup() {
  // put your setup code here, to run once:

   pinMode(ledPin, OUTPUT);
   Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:

  sensorReading11 = analogRead(pSensor11);
  sensorReading12 = analogRead(pSensor12);
  sensorReading21 = analogRead(pSensor21);
  sensorReading22 = analogRead(pSensor22);

  //******* Parking 1 *******
  
  //if something crosses over sensor 11
  if(sensorReading11 >= threshold){

    //if sensor 1 pressed after 2 during reversing
    if(p12s == 0 && p11s == 1 && p12jcrossed){
      Serial.println("Parking 1 left");
      p11s = 0;
      p12jcrossed = false;
    }
    else{
      p11s = 1;
      p11jcrossed = true;
    }
    //digitalWrite(ledPin, ledState);
    //Serial.println("Sensor 1 pressed");
  }

  //if something crosses over sensor12
  if(sensorReading12 >= threshold){
    
    //if sensor 2 pressed after 1 during parking
    if(p11s == 1 && p12s ==0 && p11jcrossed){
      Serial.println("Parking 1 occupied");
      p12s = 1;
      p11jcrossed = false;
    }
    else if(p11s == 1){
      p12s = 0;
      p12jcrossed = true;
    }
  }
  
  //******* Parking 2 *******
  
  //if something crosses over sensor 21
  if(sensorReading21 >= threshold){

    //if sensor 1 pressed after 2 during reversing
    if(p22s == 0 && p21s == 1 && p22jcrossed){
      Serial.println("Parking 2 left");
      p21s = 0;
      p22jcrossed = false;
    }
    else{
      p21s = 1;
      p21jcrossed = true;
    }
    //digitalWrite(ledPin, ledState);
    //Serial.println("Sensor 1 pressed");
  }

  //if something crosses over sensor12
  if(sensorReading22 >= threshold){
    
    //if sensor 2 pressed after 1 during parking
    if(p21s == 1 && p22s ==0 && p21jcrossed){
      Serial.println("Parking 2 occupied");
      p22s = 1;
      p21jcrossed = false;
    }
    else if(p21s == 1){
      p22s = 0;
      p22jcrossed = true;
    }
  }

  delay(100);

}
