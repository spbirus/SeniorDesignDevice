//  Arduino, HM-10, App Inventor 2
//
//  Example Project Part 1: Turn an LED on and off basic
//  By Martyn Currey. www.martyncurrey.com
//
//  Pins
//  BT VCC to Arduino 5V out. 
//  BT GND to GND
//  Arduino D8 (ASS RX) - BT TX no need voltage divider 
//  Arduino D9 (ASS TX) - BT RX through a voltage divider
//  Arduino D2 - Resistor + LED
 
// https://www.pjrc.com/teensy/td_libs_AltSoftSerial.html
#include <AltSoftSerial.h>
AltSoftSerial ASSserial; 
 
byte LEDPin = 2;
char c=' ';
 
 
void setup() 
{
    Serial.begin(9600);
    Serial.print("Sketch:   ");   Serial.println(__FILE__);
    Serial.print("Uploaded: ");   Serial.println(__DATE__);
    Serial.println(" ");
 
    ASSserial.begin(9600);  
    Serial.println("ASSserial started at 9600");
    Serial.println(" ");
 
    pinMode(LEDPin, OUTPUT); 
 
}
 
void loop()
{
    int heart_rate = random(50, 100);
    ASSserial.write(heart_rate);
    Serial.println(heart_rate);
     // Read from the Bluetooth module and turn the LED on and off
    if (ASSserial.available())
    {
        c = ASSserial.read();
        Serial.println(c);
 
        // The ascii code for 0 is dec 48
        // The ascii code for 1 is dec 49
        if ( c== 48) { digitalWrite(LEDPin, LOW); }
        if ( c== 49) { digitalWrite(LEDPin, HIGH); }
    }
}
