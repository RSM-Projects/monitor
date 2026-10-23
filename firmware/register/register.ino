#include <Wire.h>

// TODO: define constants for the sensor address and the WHO_AM_I register
// (look both up in the register map PDF)
#define SDA_PIN 21
#define SCL_PIN 22

const uint8_t MPU_ADDR = 0x68;
const uint8_t WHO_AM_I_REG = 0x75;

void setup() {
  // TODO 1: start Serial at 115200 and add a short delay
  Serial.begin(115200); 
  delay(1000);
  // TODO 2: start I2C on SDA = 21, SCL = 22
  //         (check the Wire.begin documentation for how to pass pins)
  Wire.begin(SDA_PIN,SCL_PIN);

  // TODO 3: begin a transmission to the sensor's address
   Wire.beginTransmission(MPU_ADDR);
  
  // TODO 4: write the register number you want to read
   Wire.write(WHO_AM_I_REG);
  // TODO 5: end the transmission (what does its return value tell you?)
  int error;
 error = Wire.endTransmission();
 if(error == 0){
    Serial.println("sensor is responding");
  }
  else{
    Serial.println("error: sensor is not responding");
    return;

  }
  delay(100);
  // TODO 6: request 1 byte from the sensor
  uint8_t value;
  Wire.requestFrom(MPU_ADDR, 1);
  // TODO 7: check that a byte actually arrived before reading it
  int check_byte;
  check_byte = Wire.available();
   if(check_byte == 0){
    Serial.println("no byte recieved");
    return;
  }
  else{
    Serial.println("byte is recieved");
    
  }
  // TODO 8: read the byte and print it in hex
 value = Wire.read();
 Serial.print("WHO_AM_I: 0x");
  Serial.println(value,HEX);

}

void loop() {

}