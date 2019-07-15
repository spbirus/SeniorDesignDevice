#include <math.h>

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
//float HiddenWeights[InputNodes+1][HiddenNodes];
//float OutputWeights[HiddenNodes+1][OutputNodes];
float HiddenDelta[HiddenNodes];
float OutputDelta[OutputNodes];
float ChangeHiddenWeights[InputNodes+1][HiddenNodes];
float ChangeOutputWeights[HiddenNodes+1][OutputNodes];

int test[InputNodes] = {80, 86, 76, 65, 78, 69, 70, 90, 100, 120};

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

//  /******************************************************************
//  * Initialize HiddenWeights
//  ******************************************************************/
//  for( i = 0 ; i < HiddenNodes ; i++ ) {    
//    for( j = 0 ; j <= InputNodes ; j++ ) {
//      Rando = int(random(100)); 
//      HiddenWeights[j][i] = 2.0 * ( Rando - 0.5 ) * InitialWeightMax ;
//    }
//  }
//  /******************************************************************
//  * Initialize OutputWeights
//  ******************************************************************/
//  for( i = 0 ; i < OutputNodes ; i ++ ) {    
//    for( j = 0 ; j <= HiddenNodes ; j++ ) {  
//      Rando = int(random(100));    
//      OutputWeights[j][i] = 2.0 * ( Rando - 0.5 ) * InitialWeightMax ;
//    }
//  }
  Serial.println("Initial/Untrained Outputs: ");
  toTerminal();
 
}  

void loop (){
  
  InputToOutput(test);

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
    Serial.println("Output: ");
    Serial.println(Output[i]);
  }
}

void toTerminal()
{


}
