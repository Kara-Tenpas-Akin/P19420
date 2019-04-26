// rf69 demo tx rx.pde
// -*- mode: C++ -*-
// Example sketch showing how to create a simple messageing client
// with the RH_RF69 class. RH_RF69 class does not provide for addressing or
// reliability, so you should only use RH_RF69  if you do not need the higher
// level messaging abilities.
// It is designed to work with the other example rf69_server.
// Demonstrates the use of AES encryption, setting the frequency and modem 
// configuration

#include <SPI.h>
#include <RH_RF69.h>

/************ Radio Setup ***************/

// Change to 434.0 or other frequency, must match RX's freq!
#define RF69_FREQ 915.0


//#if defined (__AVR_ATmega328P__)  // Feather 328P w/wing
  #define RFM69_INT     3  // 
  #define RFM69_CS      4  //
  #define RFM69_RST     2  // "A"
  #define LED           13
//#endif


// Singleton instance of the radio driver
RH_RF69 rf69(RFM69_CS, RFM69_INT);

int16_t packetnum = 0;  // packet counter, we increment per xmission

int incomingByte = 1;
String incoming = "a";
char cop[20];
char mystr;

int gpio = 0;

void setup() 
{
  Serial.begin(115200);
  //while (!Serial) { delay(1); } // wait until serial console is open, remove if not tethered to computer

  pinMode(8, INPUT);
  pinMode(LED, OUTPUT);     
  pinMode(RFM69_RST, OUTPUT);
  digitalWrite(RFM69_RST, LOW);
  //Serial.println("Feather RFM69 TX Test!");
  //Serial.println();
  // manual reset
  digitalWrite(RFM69_RST, HIGH);
  delay(10);
  digitalWrite(RFM69_RST, LOW);
  delay(10);
  if (!rf69.init()) {
    Serial.println("RFM69 radio init failed");
    while (1);
  }
  //Serial.println("RFM69 radio init OK!");
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
  //Serial.print("RFM69 radio @");  Serial.print((int)RF69_FREQ);  Serial.println(" MHz");
}



void loop() {
  gpio = digitalRead(8);
  if(gpio == LOW){
//Looking For Message///////////////////////////////////////////////////////////////////////////////

  //incomingByte = Serial.parseInt();
  //Serial.println("$00-00-00:0000*");
  
  delay(50);
  
  }
  if (rf69.available()) {
    // Should be a message for us now   
    uint8_t buf[RH_RF69_MAX_MESSAGE_LEN];
    uint8_t len = sizeof(buf);
    if (rf69.recv(buf, &len)) {
      if (!len) return;
      buf[len] = 0;
        Serial.println((char*)buf);
        //Serial.flush();
    //Handshake
      if (strstr((char *)buf, "01-01-01-000")) {
        // Send a reply!
        uint8_t data[] = "And hello back to you";
        rf69.send(data, sizeof(data));
        rf69.waitPacketSent();
        //Serial.println("Sent a reply");
        //Blink(LED, 40, 3); //blink LED 3 times, 40ms between blinks
      }
    } else {
      Serial.println("Receive failed");
    }
  }
/////////////////////////////////////////////////////////////////////////////////////////////////////////

//Tx Check

if(gpio == HIGH){
  incomingByte = Serial.parseInt();
  Serial.println(incomingByte);
  
  delay(100);
  
  if (incomingByte == 10){
  char radiopacket[20] = "$02-01-01:----*"; //Ventilation ON
  itoa(packetnum++, radiopacket+15, 15);
  //Serial.print("Sending "); Serial.println(radiopacket);
  
  // Send a message!
  rf69.send((uint8_t *)radiopacket, strlen(radiopacket));
  rf69.waitPacketSent();
  //Serial.print("Sent");
}

  if (incomingByte == 20){
  char radiopacket[20] = "$02-02-00:----*"; //Watersystem ON
  itoa(packetnum++, radiopacket+15, 15);
  //Serial.print("Sending "); Serial.println(radiopacket);
  
  // Send a message!
  rf69.send((uint8_t *)radiopacket, strlen(radiopacket));
  rf69.waitPacketSent();
  //Serial.print("Sent");
}

  if (incomingByte == 21){
  char radiopacket[20] = "$02-02-01:----*"; //Solenoid 1 ON
  itoa(packetnum++, radiopacket+15, 15);
  //Serial.print("Sending "); Serial.println(radiopacket);
  
  // Send a message!
  rf69.send((uint8_t *)radiopacket, strlen(radiopacket));
  rf69.waitPacketSent();
  //Serial.print("Sent");
}

  if (incomingByte == 22){
  char radiopacket[20] = "$02-02-02:----*"; //Solenoid 2 ON
  itoa(packetnum++, radiopacket+15, 15);
  //Serial.print("Sending "); Serial.println(radiopacket);
  
  // Send a message!
  rf69.send((uint8_t *)radiopacket, strlen(radiopacket));
  rf69.waitPacketSent();
  //Serial.print("Sent");
}

  if (incomingByte == 23){
  char radiopacket[20] = "$02-02-03:----*"; //Solenoid 3 ON
  itoa(packetnum++, radiopacket+15, 15);
  //Serial.print("Sending "); Serial.println(radiopacket);
  
  // Send a message!
  rf69.send((uint8_t *)radiopacket, strlen(radiopacket));
  rf69.waitPacketSent();
  //Serial.print("Sent");
}

  if (incomingByte == 24){
  char radiopacket[20] = "$02-02-04:----*"; //Solenoid 4 ON
  itoa(packetnum++, radiopacket+15, 15);
  //Serial.print("Sending "); Serial.println(radiopacket);
  
  // Send a message!
  rf69.send((uint8_t *)radiopacket, strlen(radiopacket));
  rf69.waitPacketSent();
  //Serial.print("Sent");
}

  if (incomingByte == 25){
  char radiopacket[20] = "$02-02-05:----*"; //Solenoid 5 ON
  itoa(packetnum++, radiopacket+15, 15);
  //Serial.print("Sending "); Serial.println(radiopacket);
  
  // Send a message!
  rf69.send((uint8_t *)radiopacket, strlen(radiopacket));
  rf69.waitPacketSent();
  //Serial.print("Sent");
}

  if (incomingByte == 26){
  char radiopacket[20] = "$02-02-06:----*"; //Solenoid 6 ON
  itoa(packetnum++, radiopacket+15, 15);
  //Serial.print("Sending "); Serial.println(radiopacket);
  
  // Send a message!
  rf69.send((uint8_t *)radiopacket, strlen(radiopacket));
  rf69.waitPacketSent();
  //Serial.print("Sent");
}

  if (incomingByte == 27){
  char radiopacket[20] = "$02-02-07:----*"; //Solenoid 7 ON
  itoa(packetnum++, radiopacket+15, 15);
  //Serial.print("Sending "); Serial.println(radiopacket);
  
  // Send a message!
  rf69.send((uint8_t *)radiopacket, strlen(radiopacket));
  rf69.waitPacketSent();
  //Serial.print("Sent");
}

  if (incomingByte == 30){
  char radiopacket[20] = "$02-03-01:----*"; //Fertigation ON
  itoa(packetnum++, radiopacket+15, 15);
  //Serial.print("Sending "); Serial.println(radiopacket);
  
  // Send a message!
  rf69.send((uint8_t *)radiopacket, strlen(radiopacket));
  rf69.waitPacketSent();
  //Serial.print("Sent");
}

  if (incomingByte == 40){
  char radiopacket[20] = "$02-04-01:----*"; //E-STOP ON
  itoa(packetnum++, radiopacket+15, 15);
  //Serial.print("Sending "); Serial.println(radiopacket);
  
  // Send a message!
  rf69.send((uint8_t *)radiopacket, strlen(radiopacket));
  rf69.waitPacketSent();
  //Serial.print("Sent");
}

  if (incomingByte == 50){
  char radiopacket[20] = "$02-05-00:----*"; //Water System OFF
  itoa(packetnum++, radiopacket+15, 15);
  //Serial.print("Sending "); Serial.println(radiopacket);
  
  // Send a message!
  rf69.send((uint8_t *)radiopacket, strlen(radiopacket));
  rf69.waitPacketSent();
  //Serial.print("Sent");
}

  if (incomingByte == 51){
  char radiopacket[20] = "$02-05-01:----*"; //Solenoid 1 OFF
  itoa(packetnum++, radiopacket+15, 15);
  //Serial.print("Sending "); Serial.println(radiopacket);
  
  // Send a message!
  rf69.send((uint8_t *)radiopacket, strlen(radiopacket));
  rf69.waitPacketSent();
  //Serial.print("Sent");
}

  if (incomingByte == 52){
  char radiopacket[20] = "$02-05-02:----*"; //Solenoid 2 OFF
  itoa(packetnum++, radiopacket+15, 15);
  //Serial.print("Sending "); Serial.println(radiopacket);
  
  // Send a message!
  rf69.send((uint8_t *)radiopacket, strlen(radiopacket));
  rf69.waitPacketSent();
  //Serial.print("Sent");
}

  if (incomingByte == 53){
  char radiopacket[20] = "$02-05-03:----*"; //Solenoid 3 OFF
  itoa(packetnum++, radiopacket+15, 15);
  //Serial.print("Sending "); Serial.println(radiopacket);
  
  // Send a message!
  rf69.send((uint8_t *)radiopacket, strlen(radiopacket));
  rf69.waitPacketSent();
  //Serial.print("Sent");
}

  if (incomingByte == 54){
  char radiopacket[20] = "$02-05-04:----*"; //Solenoid 4 OFF
  itoa(packetnum++, radiopacket+15, 15);
  //Serial.print("Sending "); Serial.println(radiopacket);
  
  // Send a message!
  rf69.send((uint8_t *)radiopacket, strlen(radiopacket));
  rf69.waitPacketSent();
  //Serial.print("Sent");
}

  if (incomingByte == 55){
  char radiopacket[20] = "$02-05-05:----*"; //Solenoid 5 OFF
  itoa(packetnum++, radiopacket+15, 15);
  //Serial.print("Sending "); Serial.println(radiopacket);
  
  // Send a message!
  rf69.send((uint8_t *)radiopacket, strlen(radiopacket));
  rf69.waitPacketSent();
  //Serial.print("Sent");
}

  if (incomingByte == 56){
  char radiopacket[20] = "$02-05-06:----*"; //Solenoid 6 OFF
  itoa(packetnum++, radiopacket+15, 15);
  //Serial.print("Sending "); Serial.println(radiopacket);
  
  // Send a message!
  rf69.send((uint8_t *)radiopacket, strlen(radiopacket));
  rf69.waitPacketSent();
  //Serial.print("Sent");
}

  if (incomingByte == 57){
  char radiopacket[20] = "$02-05-07:----*"; //Solenoid 7 OFF
  itoa(packetnum++, radiopacket+15, 15);
  //Serial.print("Sending "); Serial.println(radiopacket);
  
  // Send a message!
  rf69.send((uint8_t *)radiopacket, strlen(radiopacket));
  rf69.waitPacketSent();
  //Serial.print("Sent");
}

  if (incomingByte == 57){
  char radiopacket[20] = "$02-05-07:----*"; //Solenoid 7 OFF
  itoa(packetnum++, radiopacket+15, 15);
  //Serial.print("Sending "); Serial.println(radiopacket);
  
  // Send a message!
  rf69.send((uint8_t *)radiopacket, strlen(radiopacket));
  rf69.waitPacketSent();
  //Serial.print("Sent");
}

  if (incomingByte == 57){
  char radiopacket[20] = "$02-05-07:----*"; //Solenoid 7 OFF
  itoa(packetnum++, radiopacket+15, 15);
  //Serial.print("Sending "); Serial.println(radiopacket);
  
  // Send a message!
  rf69.send((uint8_t *)radiopacket, strlen(radiopacket));
  rf69.waitPacketSent();
  //Serial.print("Sent");
}


}
}
//}

///////////////////////////////////////////////////////////////////////////////


void Blink(byte PIN, byte DELAY_MS, byte loops) {
  for (byte i=0; i<loops; i++)  {
    digitalWrite(PIN,HIGH);
    delay(DELAY_MS);
    digitalWrite(PIN,LOW);
    delay(DELAY_MS);
  }
}


