#include <Wire.h>
#include <DallasTemperature.h>
#include "Adafruit_seesaw.h"
#include <SPI.h>
#include <RH_RF69.h>
char A;
char B;

#define RF69_FREQ 915.0

Adafruit_seesaw ss;

//#if defined (__AVR_ATmega328P__)  // Feather 328P w/wing
  #define RFM69_INT     3  // 
  #define RFM69_CS      4  //
  #define RFM69_RST     2  // "A"
  #define LED           13
//#endif

// Data wire is plugged into pin 2 on the Arduino
#define ONE_WIRE_BUS 9

// Setup a oneWire instance to communicate with any OneWire devices
// (not just Maxim/Dallas temperature ICs)
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature.
DallasTemperature sensors(&oneWire);

// Singleton instance of the radio driver
RH_RF69 rf69(RFM69_CS, RFM69_INT);

int16_t packetnum = 0;  // packet counter, we increment per xmission

void TurnOnReqSystems(void);
void TurnOffReqSystems(void);


//--------------------------------------------------------------------------------------------------------------------------------
//                                                      DEFINE VARIABLES
//--------------------------------------------------------------------------------------------------------------------------------
float moistureSetPoint = 500, tempSetPoint = 85, temp = 0, heatSetPoint = 40;
float Row1AvgMoisture, Row2AvgMoisture, Row3AvgMoisture, AvgTempInside, AvgTempOutside;
unsigned int irrigationFlag[4] = {}, ventilationFlag = 0, heatFlag = 0, i = 0, j = 0, enabled_sensors = 0, error = 0, Rx = 0;
unsigned int ventilationOverride = 0, fertigationOverride = 0, irrigationOverride = 0, autoMode = 1, manualMode = 0;
unsigned int forceMasterSolenoidOn = 0, forceMasterSolenoidOff = 0, forceWaterSolenoidOn = 0, forceWaterSolenoidOff = 0;
unsigned int forceHeatSolenoidOn = 0, forceHeatSolenoidOff = 0, forceFertigationSolenoidOn = 0, forceFertigationSolenoidOff = 0;
unsigned int forceRow1SolenoidOn = 0, forceRow1SolenoidOff = 0, forceRow2SolenoidOn = 0,forceRow2SolenoidOff = 0;
unsigned int forceRow3SolenoidOn = 0, forceRow3SolenoidOff = 0, ESTOP = 0, fertigationFlag;
String messageMBeg = "$01-02-0", messageERRORBeg = "$01-03-0", messageMid = ":", messageERRORReading = "----";
String messageEnd = "*", tempMString = "", tempMString2 = "", tempMString3 = "", messageTBeg = "$01-01-0";
String tempTString = "", tempTString2 = "", tempTString3 = "", incoming = "";
double waitTime = 30000; //3600000
uint8_t addr;
//--------------------------------------------------------------------------------------------------------------------------------
//                                                      DEFINE STRUCTURES
//--------------------------------------------------------------------------------------------------------------------------------
struct sensor
{
  int high_limit;
  int low_limit;
  float reading;
  int type;
  bool ack;
  bool enable;
  int errorCode;
  String mtype;
};
typedef struct sensor Sensor;

Sensor MoistureSensors[4], TempSensors[5];

//--------------------------------------------------------------------------------------------------------------------------------
//                                                      SET UP (ONE TIME)
//--------------------------------------------------------------------------------------------------------------------------------
void setup() {
  Wire.begin();
  sensors.begin(); //start library for temp sensors
  //set inputs/outputs
  pinMode(35, INPUT); //Float Sensor
  pinMode(42, OUTPUT); //Master
  pinMode(43, OUTPUT); //Straight through
  pinMode(44, OUTPUT); //Hot Water IN
  pinMode(45, OUTPUT); //Hot Water PUMP
  pinMode(46, OUTPUT); //Fertilizer
  pinMode(47, OUTPUT); //Row 1
  pinMode(48, OUTPUT); //Row 2
  pinMode(49, OUTPUT); //Row 3
  pinMode(50, OUTPUT); //FALSE
  pinMode(51, OUTPUT); //Fan
  digitalWrite(42, LOW);
  digitalWrite(43, LOW);
  digitalWrite(44, LOW);
  digitalWrite(45, LOW);
  digitalWrite(46, LOW);
  digitalWrite(47, LOW);
  digitalWrite(48, LOW);
  digitalWrite(49, LOW);
  digitalWrite(50, LOW);
  digitalWrite(51, LOW);
  i = 1;
  while(i<4){
  MoistureSensors[i].high_limit = 900;
  MoistureSensors[i].low_limit = 100;
  i++;
  }
  i = 1;
  while(i<5){
  TempSensors[i].high_limit = 150;
  TempSensors[i].low_limit = -50;
  i++;
  }

  Serial.begin(115200);
  //while (!Serial) { delay(1); } // wait until serial console is open, remove if not tethered to computer

  pinMode(LED, OUTPUT);     
  pinMode(RFM69_RST, OUTPUT);
  digitalWrite(RFM69_RST, LOW);

  Serial.println("Feather RFM69 RX Test!");
  Serial.println();

  // manual reset
  digitalWrite(RFM69_RST, HIGH);
  delay(10);
  digitalWrite(RFM69_RST, LOW);
  delay(10);
  
  if (!rf69.init()) {
    Serial.println("RFM69 radio init failed");
    while (1);
  }
  Serial.println("RFM69 radio init OK!");
  
  // Defaults after init are 434.0MHz, modulation GFSK_Rb250Fd250, +13dbM (for low power module)
  // No encryption
  if (!rf69.setFrequency(RF69_FREQ)) {
    Serial.println("setFrequency failed");
  }

  // If you are using a high power RF69 eg RFM69HW, you *must* set a Tx power with the
  // ishighpowermodule flag set like this:
  rf69.setTxPower(20, true);  // range from 14-20 for power, 2nd arg must be true for 69HCW

  // The encryption key has to be the same as the one in the server
  uint8_t key[] = { 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,
                    0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08};
  rf69.setEncryptionKey(key);
  
  pinMode(LED, OUTPUT);

  Serial.print("RFM69 radio @");  Serial.print((int)RF69_FREQ);  Serial.println(" MHz");
  Serial.println("");
  
}
//--------------------------------------------------------------------------------------------------------------------------------
//                                                      MAIN LOOP
//--------------------------------------------------------------------------------------------------------------------------------
void loop() {
  while(ESTOP == 0){
    if(digitalRead(35) == LOW)
      digitalWrite(44, HIGH);
    delay(1000);
    Serial.begin(115200);
    delay(1000);
    Serial.print("Irrigation Override: ");
    Serial.print(irrigationOverride);
    Serial.println();
    ReadMoisture();
    delay(1000);
    Serial.begin(9600);
    delay(1000);
    ReadTemp();
    delay(1000);
    Serial.begin(115200);
    delay(1000);
    CheckMoisture();
    delay(1000);
    Serial.begin(9600);
    delay(1000);
    CheckTemp();
    delay(1000);
    Serial.begin(115200);
    delay(1000);
    CheckFertigation();
    SendData();
    ventilationOverride = 0;
    irrigationOverride = 0;
    ReadData();
    digitalWrite(44, LOW);
    if(autoMode == 1){
      TurnOnReqSystems();
      WaitAndCheck(waitTime); //set time
      TurnOffReqSystems();
    }
    else if (manualMode == 1)
      ManualMode();
  }
  while(ESTOP == 1){
    TurnOffReqSystems();
  }
}

//--------------------------------------------------------------------------------------------------------------------------------
//                                                      LARGER FUNCTIONS
//--------------------------------------------------------------------------------------------------------------------------------
//Read Moisture Sensors
void ReadMoisture(void) {
  //ADAFRUIT SENSORS
  i = 1; //start i at 1 to make realizing moisture sensors easier
  Serial.print("READ MOISTURE:");
  while (i < 4) {
    addr = 0x35 + i;
    if (!ss.begin(addr)){
      MoistureSensors[i].errorCode = 1;
    }
    else {
      MoistureSensors[i].errorCode = 0;
      MoistureSensors[i].reading = ss.touchRead(0);
    }
    Serial.println("");
    Serial.print("Moisture Sensor ");
    Serial.print(i);
    Serial.print(":");
    Serial.println("");
    Serial.print("Error Code: ");
    Serial.print(MoistureSensors[i].errorCode);
    Serial.println("");
    Serial.print("Moisture Level: ");
    Serial.print(MoistureSensors[i].reading);
    Serial.println("");
    tempMString = "";
    tempMString2 = "";
    tempMString3 = "";
    if (MoistureSensors[i].errorCode == 0){
      tempMString = messageMBeg + i;
      tempMString2 = tempMString + messageMid;
      tempMString3 = tempMString2 + (int) MoistureSensors[i].reading;
      MoistureSensors[i].mtype = tempMString3 + messageEnd;
    }
    else {
      tempMString = messageERRORBeg + i;
      tempMString2 = tempMString + messageMid;
      tempMString3 = tempMString2 + messageERRORReading;
      MoistureSensors[i].mtype = tempMString3 + messageEnd;
    }
    i++;
  }
}
//--------------------------------------------------------------------------------------------------------------------------------
//Read Temp Sensors
void ReadTemp(void) {
  sensors.requestTemperatures(); // Send the command to get temperatures
  i = 1; //start i at 1 to make realizing temp sensors easier
  Serial.begin(115200);
  delay(1000);
  Serial.println("");
  Serial.print("READ TEMP:");
  delay(1000);
  Serial.begin(9600);
  delay(1000);
  while (i < 5) {
    j = i - 1;
    TempSensors[i].reading = sensors.getTempFByIndex(j); // You can have more than one IC on the same bus. 0 refers to the first IC on the wire
    TempSensors[i].type = sensors.getUserDataByIndex(j);
    if(TempSensors[i].reading < TempSensors[i].low_limit)
      TempSensors[i].errorCode = 1;
    else
      TempSensors[i].errorCode = 0;
    Serial.begin(115200);
    delay(1000);
    Serial.println("");
    Serial.print("Temp Sensor ");
    Serial.print(i);
    Serial.print(":");
    Serial.println("");
    Serial.print("Temp: ");
    Serial.print(TempSensors[i].reading);
    Serial.print(" F");
    Serial.println("");
    Serial.print("Type: ");
    Serial.print(TempSensors[i].type);
    Serial.println("");
    Serial.print("Error Code: ");
    Serial.print(TempSensors[i].errorCode);
    Serial.println("");
    delay(1000);
    Serial.begin(9600);
    delay(1000);
    tempTString = "";
    tempTString2 = "";
    tempTString3 = "";
    if (TempSensors[i].errorCode == 0){
      tempTString = messageTBeg + i;
      tempTString2 = tempTString + messageMid;
      tempTString3 = tempTString2 + (int) TempSensors[i].reading;
      TempSensors[i].mtype = tempTString3 + messageEnd;
    }
    else if(TempSensors[i].errorCode == 1){
      tempTString = messageERRORBeg + "4";
      tempTString2 = tempTString + messageMid;
      tempTString3 = tempTString2 + messageERRORReading;
      TempSensors[i].mtype = tempTString3 + messageEnd;
    }
    i++;
  }
}
//--------------------------------------------------------------------------------------------------------------------------------
//Read Data from RPi
void ReadData(void) {
  Rx = 0;
  incoming = "";
  if (rf69.available() && Rx == 0) {
    // Should be a message for us now   
    uint8_t buf[RH_RF69_MAX_MESSAGE_LEN];
    uint8_t len = sizeof(buf);
    if (rf69.recv(buf, &len) && Rx == 0) {
      if (!len) return;
      buf[len] = 0;
      incoming = (char*)buf;
//    String data = (char*)buf;
//    String reading = (char*)buf;
//    int i = data.indexOf('$');
//    int j = data.indexOf(':');
      int k = incoming.indexOf('*');
//    data.remove(j);
//    data.remove(i, i+1);
      incoming.remove(k+1);
//    reading.remove(i,j+1);
//    Serial.println(data);
//    Serial.println(reading);
    Serial.println(incoming);

      if ((char *)buf != "") {
        // Send a reply!
        uint8_t data[] = "$!!!*";
        rf69.send(data, sizeof(data));
        rf69.waitPacketSent();
        Rx = 1;
        delay(100);
      }
    }
    else {
      Serial.println("Receive failed");
    }
  if (incoming == "$02-01-01:----*")
    ventilationOverride = 1;
  if (incoming == "$02-02-00:----*")
    irrigationOverride = 1;
  if (incoming == "$02-02-01:----*"){
    forceMasterSolenoidOn = 1;
    forceMasterSolenoidOff = 0;
  }
  if (incoming == "$02-02-02:----*"){
    forceWaterSolenoidOn = 1;
    forceWaterSolenoidOff = 0;
  }
  if (incoming == "$02-02-03:----*"){
    forceHeatSolenoidOn = 1;
    forceHeatSolenoidOff = 0;
  }
  if (incoming == "$02-02-04:----*"){
    forceFertigationSolenoidOn = 1;
    forceFertigationSolenoidOff = 0;
  }
  if (incoming == "$02-02-05:----*"){
    forceRow1SolenoidOn = 1;
    forceRow1SolenoidOff = 0;
  }
  if (incoming == "$02-02-06:----*"){
    forceRow2SolenoidOn = 1;
    forceRow2SolenoidOff = 0;
  }
  if (incoming == "$02-02-07:----*"){
    forceRow3SolenoidOn = 1;
    forceRow3SolenoidOff = 0;
  }
  if (incoming == "$02-03-01:----*")
    fertigationOverride = 1;
  if (incoming == "$02-04-01:----*")
    ESTOP = 1;
  if (incoming == "$02-05-01:----*"){
    forceMasterSolenoidOff = 1;
    forceMasterSolenoidOn = 0;
  }
  if (incoming == "$02-05-02:----*"){
    forceWaterSolenoidOff = 1;
    forceWaterSolenoidOn = 0;
  }
  if (incoming == "$02-05-03:----*"){
    forceHeatSolenoidOff = 1;
    forceHeatSolenoidOn = 0;
  }
  if (incoming == "$02-05-04:----*"){
    forceFertigationSolenoidOff = 1;
    forceFertigationSolenoidOn = 0;
  }
  if (incoming == "$02-05-05:----*"){
    forceRow1SolenoidOff = 1;
    forceRow1SolenoidOn = 0;
  }
  if (incoming == "$02-05-06:----*"){
    forceRow2SolenoidOff = 1;
    forceRow2SolenoidOn = 0;
  }
  if (incoming == "$02-05-07:----*"){
    forceRow3SolenoidOff = 1;
    forceRow3SolenoidOn = 0;
  }
  if (incoming == "$02-06-01:----*"){
    autoMode = 1;
    manualMode = 0;
  }
  if (incoming == "$02-06-02:----*"){
    autoMode = 0;
    manualMode = 1;
  }
  }
  return;
}
//--------------------------------------------------------------------------------------------------------------------------------
//Send Data to RPi
void SendData(void) {
  i = 1;
  while(i <4) {
    char radiopacket[20] = "";
    MoistureSensors[i].mtype.toCharArray(radiopacket,20);
    itoa(packetnum++, radiopacket+15, 15);
    Serial.print("Sending "); Serial.println(radiopacket);
    
    // Send a message!
    rf69.send((uint8_t *)radiopacket, strlen(radiopacket));
    rf69.waitPacketSent();
    delay(100);
    i++;
  }
  i = 1;
  while(i <5) {
    char radiopacket[20] = "";
    TempSensors[i].mtype.toCharArray(radiopacket,20);
    itoa(packetnum++, radiopacket+15, 15);
    Serial.print("Sending "); Serial.println(radiopacket);
    
    // Send a message!
    rf69.send((uint8_t *)radiopacket, strlen(radiopacket));
    rf69.waitPacketSent();
    delay(100);
    i++;
  }
}
//--------------------------------------------------------------------------------------------------------------------------------
//Check Moisture
void CheckMoisture(void) {
  //Check for bad moisture sensor
  i = 1;
  Serial.println("");
  Serial.print("CHECK MOISTURE:");
  while (i < 4) {
    if (MoistureSensors[i].errorCode == 0 && MoistureSensors[i].reading < MoistureSensors[i].high_limit && MoistureSensors[i].reading > MoistureSensors[i].low_limit)
      MoistureSensors[i].enable = 1;
    else
      MoistureSensors[i].enable = 0;
    Serial.println("");
    Serial.print("Moisture Sensor ");
    Serial.print(i);
    Serial.print(":");
    Serial.println("");
    Serial.print("Enable: ");
    Serial.print(MoistureSensors[i].enable);
    Serial.println("");
    i++;
  }

  //ROW 1
  Row1AvgMoisture = 0;
  if (MoistureSensors[1].enable == 1) {
    Row1AvgMoisture = MoistureSensors[1].reading;
  }
  else
    delay(1);
    
if ((Row1AvgMoisture <= moistureSetPoint && MoistureSensors[1].enable == 1) || irrigationOverride == 1) //do we want seperate set points for rows???
  irrigationFlag[1] = 1;
else
  irrigationFlag[1] = 0;

//ROW 2
Row2AvgMoisture = 0;
if (MoistureSensors[2].enable == 1) {
  Row2AvgMoisture = MoistureSensors[2].reading;
}
else
  delay(1);

if ((Row2AvgMoisture <= moistureSetPoint && MoistureSensors[2].enable == 1) || irrigationOverride == 1) //do we want seperate set points for rows???
  irrigationFlag[2] = 1;
else
  irrigationFlag[2] = 0;

//ROW 3
Row3AvgMoisture = 0;
if (MoistureSensors[3].enable == 1) {
  Row3AvgMoisture = MoistureSensors[3].reading;
}
else
  delay(1);

if ((Row3AvgMoisture <= moistureSetPoint && MoistureSensors[3].enable == 1) || irrigationOverride == 1) //do we want seperate set points for rows???
  irrigationFlag[3] = 1;
else
  irrigationFlag[3] = 0;
Serial.println("");
Serial.print("SYSTEM STATUS: ");
Serial.println("");
Serial.print("Row 1 Irrigation: ");
Serial.println("");
Serial.print(irrigationFlag[1]);
Serial.println("");
Serial.print("Row 2 Irrigation: ");
Serial.println("");
Serial.print(irrigationFlag[2]);
Serial.println("");
Serial.print("Row 3 Irrigation: ");
Serial.println("");
Serial.print(irrigationFlag[3]);
Serial.println("");
}
//--------------------------------------------------------------------------------------------------------------------------------
//Check Temp
void CheckTemp(void) {
  //Check for bad temp sensor,1,2 are inside, 3,4 are outside
  i = 1;
  Serial.begin(115200);
  delay(1000);
  Serial.println("");
  Serial.print("CHECK TEMP:");
  delay(1000);
  Serial.begin(9600);
  delay(1000);
  while (i < 5) {
    if (TempSensors[i].errorCode == 0 && TempSensors[i].reading < TempSensors[i].high_limit && TempSensors[i].reading > TempSensors[i].low_limit)
      TempSensors[i].enable = 1;
    else
      TempSensors[i].enable = 0;
    Serial.begin(115200);
    delay(1000);
    Serial.println("");
    Serial.print("Temp Sensor ");
    Serial.print(i);
    Serial.print(":");
    Serial.println("");
    Serial.print("Enable: ");
    Serial.print(TempSensors[i].enable);
    Serial.println("");
    delay(1000);
    Serial.begin(9600); 
    delay(1000); 
    i++;
  }

  //Inside Temp
  enabled_sensors = 0;
  i = 1;
  AvgTempInside = 0;
  while (i < 5) {
    if (TempSensors[i].enable == 1 && TempSensors[i].type == 111) {
      AvgTempInside = AvgTempInside + TempSensors[i].reading;
      enabled_sensors = enabled_sensors + 1;
    }
    else
      delay(1);
    i++;
  }
  AvgTempInside = AvgTempInside / enabled_sensors;

  //Outside Temp
  enabled_sensors = 0;
  i = 1;
  AvgTempOutside = 0;
  while (i < 5) {
    if (TempSensors[i].enable == 1 && TempSensors[i].type == 222) {
      AvgTempOutside = AvgTempOutside + TempSensors[i].reading;
      enabled_sensors = enabled_sensors + 1;
    }
    else
      delay(1);
    i++;
  }
  AvgTempOutside = AvgTempOutside / enabled_sensors;

  if ((AvgTempInside >= tempSetPoint) || ventilationOverride == 1) {
    ventilationFlag = 1;
    heatFlag = 0;
  }
  else if (AvgTempInside <= heatSetPoint) {
    heatFlag = 1;
    ventilationFlag = 0;
  }
  else {
    ventilationFlag = 0;
    heatFlag = 0;
  }
delay(1000);
Serial.begin(115200);
delay(1000);
Serial.println("");
Serial.print("SYSTEM STATUS: ");
Serial.println("");
Serial.print("Ventilation System: ");
Serial.println("");
Serial.print(ventilationFlag);
Serial.println("");
Serial.print("Heating System: ");
Serial.println("");
Serial.print(heatFlag);
Serial.println("");
Serial.println("");
delay(1000);
Serial.begin(9600);
delay(1000);
}
//--------------------------------------------------------------------------------------------------------------------------------
void CheckFertigation(void){
  if(fertigationOverride == 1)
    fertigationFlag = 1;
  else
    fertigationFlag = 0;
  fertigationOverride = 0;
  Serial.print("Fertigation System: ");
  Serial.println("");
  Serial.print(fertigationFlag);
  Serial.println("");
  Serial.println("");
}
//--------------------------------------------------------------------------------------------------------------------------------?????????????????Set Pins???????????????
//Turn On Systems
void TurnOnReqSystems(void) {
  //MASTER WATER VALVE
  if (irrigationFlag[1] == 1 || irrigationFlag[2] == 1 || irrigationFlag[3] == 1) //Turn on master valve if any row needs water
    digitalWrite(42, HIGH);
  //ROW ONE - THREE WATER VALVE
  i = 1;
  while (i < 4) {
    if (irrigationFlag[i] == 1) //Turn on valve for desired row
      digitalWrite(46 + i, HIGH);
    i++;
  }
  //VENTILATION
  if (ventilationFlag == 1) //Turn on fan
    digitalWrite(51, HIGH);
  //HEAT
  if ((heatFlag == 1) && (irrigationFlag[1] == 1 || irrigationFlag[2] == 1 || irrigationFlag[3] == 1) && (fertigationFlag == 0) && (digitalRead(35)==HIGH)){ //Turn on heating
    digitalWrite(45, HIGH);
    digitalWrite(43, LOW);
  }
  //WATER ONLY
  if ((irrigationFlag[1] == 1 || irrigationFlag[2] == 1 || irrigationFlag[3] == 1) && (heatFlag == 0) && (fertigationFlag == 0))
    digitalWrite(43, HIGH);
  else if ((irrigationFlag[1] == 1 || irrigationFlag[2] == 1 || irrigationFlag[3] == 1) && (heatFlag == 1) && (digitalRead(35)==LOW) && (fertigationFlag == 0))
    digitalWrite(43, HIGH);
  //FERTIGATION
  if (fertigationFlag == 1){
    digitalWrite(47, HIGH);
    digitalWrite(48, HIGH);
    digitalWrite(49, HIGH);
    digitalWrite(46, HIGH);
  }
}
//--------------------------------------------------------------------------------------------------------------------------------
//Turn Off Systems
void TurnOffReqSystems(void) {
  i = 1;
  while (i < 11) {
    digitalWrite(41 + i, LOW); //should we just turn off all systems here? Probably...
    i++;
  }
  ventilationFlag = 0;
  heatFlag = 0;
  irrigationFlag[4] = {0};
}
//--------------------------------------------------------------------------------------------------------------------------------
//Wait And Check HMI
void WaitAndCheck(unsigned int) {
  i = waitTime/5000;
  j = 0;
  while (j <= i && autoMode == 1 && ESTOP == 0) {
    ReadData();
    delay(5000);
    j++;
  }
}
//--------------------------------------------------------------------------------------------------------------------------------
void ManualMode(void){
  if(forceMasterSolenoidOn == 1)
    digitalWrite(42, HIGH);
  if(forceMasterSolenoidOff == 1)
    digitalWrite(42, LOW);
  if(forceWaterSolenoidOn == 1)
    digitalWrite(43, HIGH);
  if(forceWaterSolenoidOff == 1)
    digitalWrite(43, LOW);
  if(forceHeatSolenoidOn == 1)
    digitalWrite(44, HIGH);
  if(forceHeatSolenoidOff == 1)
    digitalWrite(44, LOW);
  if(forceFertigationSolenoidOn == 1)
    digitalWrite(46, HIGH);
  if(forceFertigationSolenoidOff == 1)
    digitalWrite(46, LOW);
  if(forceRow1SolenoidOn == 1)
    digitalWrite(47, HIGH);
  if(forceRow1SolenoidOff == 1)
    digitalWrite(47, LOW);
  if(forceRow2SolenoidOn == 1)
    digitalWrite(48, HIGH);
  if(forceRow2SolenoidOff == 1)
    digitalWrite(48, LOW);
  if(forceRow3SolenoidOn == 1)
    digitalWrite(49, HIGH);
  if(forceRow3SolenoidOff == 1)
    digitalWrite(49, LOW);
}
//--------------------------------------------------------------------------------------------------------------------------------
