#include <Wire.h>

// TODO: constants: pins, MPU_ADDR, PWR_MGMT_1 register, ACCEL_XOUT_H register,
//       and the sensitivity for ±2 g (from the register map)
#define SDA_PIN 21
#define SCL_PIN 22

const uint8_t MPU_ADDR = 0x68;
const uint8_t PWR_MGMT_1  = 0x6B;
const uint8_t ACCEL_XOUT_H = 0x3B;

uint8_t writeRegister(uint8_t reg, uint8_t value){
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(reg);
  Wire.write(value);
  return Wire.endTransmission();
}

int readregister(uint8_t reg){
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(reg);
  if(Wire.endTransmission() != 0){ return -1;}
  Wire.requestFrom(MPU_ADDR,(uint8_t)1);
  if(Wire.available() == 0){return -1;}
  return Wire.read();

}

void setup() {
  // TODO 1: Serial and Wire start (you've done this)
  Serial.begin(115200);
  delay(1000);
  Wire.begin(SDA_PIN, SCL_PIN);

  Serial.print("PWR_MGMT_1 before: 0x");
  Serial.println(readregister(PWR_MGMT_1),HEX);

  // TODO 2: wake the sensor: write register number + value in one transmission
  uint8_t error = writeRegister(PWR_MGMT_1,0x00);
  if (error != 0) {
    Serial.print("Wake-up failed, error code: ");
    Serial.println(error);
    return;
  }

  delay(100); 

  Serial.print("PWR_MGMT_1 after: 0x");
  Serial.println(readregister(PWR_MGMT_1), HEX);


  // TODO 3: check endTransmission, and stop with a message if it fails
}

void loop() {
  // TODO 4: set the pointer to the first acceleration register
  // TODO 5: request 6 bytes and check that 6 arrived
  // TODO 6: read the bytes and build three int16_t values
  // TODO 7: convert to g and print x, y, z on one line
  // TODO 8: a small delay, for now (see the note below)
}