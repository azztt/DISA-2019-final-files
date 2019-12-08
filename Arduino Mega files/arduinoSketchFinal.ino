const int ledPin = 13;
const int pSensor11 = A0;
const int pSensor12 = A2;
const int threshold = 700;

int sensorReading1 = 0;
int sensorReading2 = 0;
int ledState = LOW;
int p1s = 0;
int p2s = 0;
bool p2jcrossed = false;
bool p1jcrossed = false;

void setup() {
  // put your setup code here, to run once:

   pinMode(ledPin, OUTPUT);
   Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:

  sensorReading1 = analogRead(pSensor11);
  sensorReading2 = analogRead(pSensor12);

  //if something crosses over sensor 11
  if(sensorReading1 >= threshold){

    //if sensor 1 pressed after 2 during reversing
    if(p2s == 0 && p1s == 1 && p2jcrossed){
      Serial.println("Parking 1 left");
      p1s = 0;
      p2jcrossed = false;
    }
    else{
      p1s = 1;
      p1jcrossed = true;
    }
    //digitalWrite(ledPin, ledState);
    //Serial.println("Sensor 1 pressed");
  }

  //if something crosses over sensor12
  if(sensorReading2 >= threshold){
    
    //if sensor 2 pressed after 1 during parking
    if(p1s == 1 && p2s ==0 && p1jcrossed){
      Serial.println("Parking 1 occupied");
      p2s = 1;
      p1jcrossed = false;
    }
    else if(p1s == 1){
      p2s = 0;
      p2jcrossed = true;
    }
  }

  delay(100);

}