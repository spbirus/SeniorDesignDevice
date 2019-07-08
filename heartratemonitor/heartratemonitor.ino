//THIS IS THE ONE THAT SHOULD WORK WITH THE NEW BLUETOOTH MODULES


#include<SoftwareSerial.h>
#include<BLEPeripheral.h>

#define TxD 10
#define RxD 9

SoftwareSerial bluetoothSerial(TxD, RxD);

BLEPeripheral blePeripheral = BLEPeripheral(6,4,5);  // BLE Peripheral Device (the board you're programming)
BLEService heartService("00002a00-0000-1000-8000-00805f9b34fb"); // BLE LED Service

// BLE heart rate Switch Characteristic - custom 128-bit UUID, read and writable by central
BLEUnsignedCharCharacteristic switchCharacteristic("00002a01-0000-1000-8000-00805f9b34fb", BLERead | BLEWrite);

void setup(void)
{
  bluetoothSerial.begin(9600);
  Serial.begin(9600);
  Serial.println("begin setup");
  
  // set advertised local name and service UUID:
  blePeripheral.setLocalName("HeartRate");
  blePeripheral.setAdvertisedServiceUuid(heartService.uuid());
  Serial.println("setup peripheral");
  
  // add service and characteristic:
  blePeripheral.addAttribute(heartService);
  blePeripheral.addAttribute(switchCharacteristic);

  Serial.println("setup switch characteristic");
  // set the initial value for the characeristic:
  switchCharacteristic.setValue(0);

  // begin advertising BLE service:
  blePeripheral.begin();
  Serial.println("end setup");
}

/** Send randomized heart rate data continuously **/
void loop(void)
{
//  BLECentral central = blePeripheral.central();

  int heart_rate = random(50, 100);

  Serial.println("Heart rate update");
  Serial.println(heart_rate);
  switchCharacteristic.setValue(heart_rate);
//  bluetoothSerial.write(heart_rate);

//  // if a central is connected to peripheral:
//  if (central) {
//    Serial.print("Connected to central: ");
//    // print the central's MAC address:
//    Serial.println(central.address());
//
//    // while the central is still connected to peripheral:
//    while (central.connected()) {
//      Serial.println("Heart rate update");
//      Serial.println(heart_rate);
//      bluetoothSerial.write(heart_rate);
//    }
//
//    // when the central disconnects, print it out:
//    Serial.print(F("Disconnected from central: "));
//    Serial.println(central.address());
//  }

  /* Delay before next measurement update */
  delay(1000);
}
