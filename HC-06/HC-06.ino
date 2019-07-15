
#include <SoftwareSerial.h>
SoftwareSerial BTserial(2, 4); // RX | TX
// Connect the HC-06 TX to the Arduino RX on pin 2. 
// Connect the HC-06 RX to the Arduino TX on pin 4 through a voltage divider.


int values[10000];
int bpm_values[5];
int index = 0;

int heartSignal1 = 0;
int heartSignal2 = 0;
bool goingUp;
bool goingDown;
bool atPeak;
int start = 1; 
int pulseCount = 0;  
unsigned long startTime;
int bpm = 0;  
   
int threshold = 200; 

 
void setup() 
{
    Serial.begin(9600);
 
    // HC-06 default serial speed is 9600
    BTserial.begin(9600);  
}
 
void loop()
{

    int real_bpm = analogRead(0);
    char buffer [6];

    heartSignal1 = analogRead(0);
    delay(7.5);
    heartSignal2 = analogRead(0);

    Serial.println(heartSignal1);
    //once waveform is stabalized click start
    if(start == 1) 
    {  
      pulseCount = 0;
      bpm = 0;
      startTime = millis();
      start = 0;
    }
  
    if((millis() > startTime) && ((millis() - startTime) >= 12000)) //if 12 seconds has passed
    {
      bpm = (pulseCount * 5);
//        Serial.println("BPM: ");
//        Serial.println(bpm);
      bpm_values[index] = bpm;
      index = index + 1;
      BTserial.write(itoa(bpm, buffer, 10));
      start = 1;
    }
    if(heartSignal1 < heartSignal2) 
    {
      //upwards slope
      goingUp = true;
      atPeak = false;
    } 
    if((heartSignal1 > heartSignal2) && goingUp)
    {
      //downwards slope
      atPeak = true;
      goingUp = false;
    }
    if((heartSignal1 > threshold) && atPeak)
    {                         
      digitalWrite(2,HIGH);
      pulseCount = pulseCount + 1;
      atPeak = false;          
    } 
    else 
    {
      digitalWrite(2,LOW);    
      atPeak = false;          
    }


    //sending the bluetooth stuff
    //store the values in an array
    values[index] = real_bpm;
    Serial.println(real_bpm);
    BTserial.write(itoa(real_bpm, buffer, 10));
    delay(10);

    
 
}
