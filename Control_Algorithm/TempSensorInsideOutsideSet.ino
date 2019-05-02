#include <OneWire.h>
#include <DallasTemperature.h>
#include "Adafruit_seesaw.h"

Adafruit_seesaw ss;
 
// Data wire is plugged into pin 2 on the Arduino
#define ONE_WIRE_BUS 9
 
// Setup a oneWire instance to communicate with any OneWire devices 
// (not just Maxim/Dallas temperature ICs)
OneWire oneWire(ONE_WIRE_BUS);
 
// Pass our oneWire reference to Dallas Temperature.
DallasTemperature sensors(&oneWire);
 
void setup(void)
{
  // start serial port
  Serial.begin(9600);
  Serial.println("Dallas Temperature IC Control Library Demo");

  // Start up the library
  sensors.begin();
}
 
//-----------------------------------------------------------ONLY USE WITH ONE SENSOR HOOKED UP AT A TIME-------------------------------------------------------------------------
// this code will set the user byte and then read it back to you to confirm
 
void loop(void)
{
  // call sensors.requestTemperatures() to issue a global temperature
  // request to all devices on the bus
  Serial.begin(9600);
  Serial.println("\n");
  Serial.print("Requesting temperatures...");
  sensors.requestTemperatures(); // Send the command to get temperatures
  Serial.println("DONE");
  //Serial.println("\n");

  Serial.print("Temperature 1 is: ");
  float temp = sensors.getTempFByIndex(0); // Why "byIndex"? 
    // You can have more than one IC on the same bus. 
    // 0 refers to the first IC on the wire
  Serial.print(temp);
  Serial.print(" F");
  Serial.println("\n");
//-------------------------------------------------------------------------------Set 111 for inside and 222 for outside, comment the other out with //-----------------------------
  sensors.setUserDataByIndex(0, 111); //use this for inside sensor
//  sensors.setUserDataByIndex(0, 222); //use this for outside sensor

  int user1 = sensors.getUserDataByIndex(0);
  
  Serial.print("Temperature Sensor 1 user byte is: "); 
  Serial.print(user1);
  Serial.println("\n");
  
  delay(5000);
}
