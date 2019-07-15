#include <math.h>
#include <SoftwareSerial.h>
SoftwareSerial BTserial(2, 4); // RX | TX
// Connect the HC-06 TX to the Arduino RX on pin 2. 
// Connect the HC-06 RX to the Arduino TX on pin 4 through a voltage divider.

// heart rate caluclation stuff
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


/******************************************************************
 * Network Configuration - customized per network 
 ******************************************************************/

const int InputNodes = 10;
const int HiddenNodes = 4;
const int OutputNodes = 1;
const float InitialWeightMax = 0.5;


/******************************************************************
 * End Network Configuration
 ******************************************************************/


int i, j, p, q, r;
int ReportEvery1000;
long  TrainingCycle;
float Rando;
float Error;
float Accum;


float Hidden[HiddenNodes];
float Output[OutputNodes];
float HiddenDelta[HiddenNodes];
float OutputDelta[OutputNodes];
float ChangeHiddenWeights[InputNodes+1][HiddenNodes];
float ChangeOutputWeights[HiddenNodes+1][OutputNodes];


const byte HiddenWeights[InputNodes][HiddenNodes] = {
  {0.88031986, 0.31096487, 0.97476878, 0.89757280},
  {0.65730385, 0.58499665, 0.63743563, 0.66019546},
  {0.44404419, 0.34799544, 0.23871403, 0.19925869},
  {0.44374342, 0.84038301, 0.26308567, 0.01014188},
  {0.66742105, 0.57629258, 0.93926217, 0.58232634},
  {0.49929492, 0.40760946, 0.85562062, 0.10584793},
  {0.52313374, 0.27585958, 0.49125396, 0.38543970},
  {0.06335292, 0.86315702, 0.46117916, 0.89627523},
  {0.57239570, 0.21966519, 0.40751979, 0.53306157},
  {0.83030938, 0.15297654, 0.75742923, 0.73294024}
}; 

const byte OutputWeights[HiddenNodes][OutputNodes] = {
  {-322.31152966},
  {-323.01553423},
  {-322.40726739},
  {-322.72501762},
}; 


void setup(){
  Serial.begin(9600);
 
  // HC-06 default serial speed is 9600
  BTserial.begin(9600);  
 
}  

void loop (){

    char buffer [6];

    heartSignal1 = analogRead(0);
    delay(7.5);
    heartSignal2 = analogRead(0);

//    Serial.println(heartSignal1);
    //once waveform is stabalized click start
    if(start == 1) 
    {  
      pulseCount = 0;
      bpm = 0;
      startTime = millis();
      start = 0;
    }
  
    if((millis() > startTime) && ((millis() - startTime) >= 6000)) //if 6 seconds has passed
    {
      bpm = (pulseCount * 10);
        Serial.println("BPM: ");
        Serial.println(bpm);
      bpm_values[index] = bpm;
      index = index + 1;
//      BTserial.write(itoa(bpm, buffer, 10));
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

    if(index = 10){
      index = 0;
      InputToOutput(bpm_values);
      BTserial.write(itoa(Output[0], buffer, 10));
    }
    

    //sending the bluetooth stuff
    //store the values in an array
//    values[index] = real_bpm;
//    Serial.println(real_bpm);
//    BTserial.write(itoa(real_bpm, buffer, 10));

  
  

}

void InputToOutput(int in[])
{
  /******************************************************************
  Compute hidden layer activations
  ******************************************************************/
  for ( i = 0 ; i < HiddenNodes ; i++ ) {
    Accum = HiddenWeights[InputNodes][i] ;
  
    for ( j = 0 ; j < InputNodes ; j++ ) { 
      Accum += in[j] * HiddenWeights[j][i] ;
    }
    Hidden[i] = 1.0 / (1.0 + exp(-Accum)) ;
  }
  
  /******************************************************************
  Compute output layer activations and calculate errors  
  ******************************************************************/  
  for ( i = 0 ; i < OutputNodes ; i++ ) { 
    Accum = OutputWeights[HiddenNodes][i] ;  
    for ( j = 0 ; j < HiddenNodes ; j++ ) { 
      Accum += Hidden[j] * OutputWeights[j][i] ; 
    }
    Output[i] = 1.0 / (1.0 + exp(-Accum)) ;
//    Serial.println("Output: ");
//    Serial.println(Output[i]);
  }
}
