#include <Wire.h>

// TODO: constants: pins, MPU_ADDR, PWR_MGMT_1 register, ACCEL_XOUT_H register,
//       and the sensitivity for ±2 g (from the register map)
#define SDA_PIN 21
#define SCL_PIN 22

const uint8_t MPU_ADDR = 0x68;
const uint8_t PWR_MGMT_1  = 0x6B;
const uint8_t ACCEL_XOUT_H = 0x3B;

const float ACCEL_SENS = 16384;

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
 // TODO 1: begin a transmission, write ACCEL_XOUT_H, end it
  //         (check the return value, like in readRegister)


    Wire.beginTransmission(MPU_ADDR);
  Wire.write(ACCEL_XOUT_H);
  if(Wire.endTransmission() != 0){  
    Serial.println("Failed to set register pointer");
    return;
    }
   Wire.requestFrom(MPU_ADDR, (uint8_t)6);
  if (Wire.available() != 6) {
    Serial.println("Did not receive 6 bytes");
    return;
  }
  uint8_t xh = Wire.read();
  uint8_t xl = Wire.read();
  uint8_t yh = Wire.read();
  uint8_t yl = Wire.read();
  uint8_t zh = Wire.read();
  uint8_t zl = Wire.read();



int16_t rawX = (int16_t)((xh << 8) | xl);
  int16_t rawY = (int16_t)((yh << 8) | yl);
  int16_t rawZ = (int16_t)((zh << 8) | zl);

  // 4. Convert to g (float division)
  float x = rawX / ACCEL_SENS;
  float y = rawY / ACCEL_SENS;
  float z = rawZ / ACCEL_SENS;

  // 5. Print on one line
  Serial.print("X: ");
  Serial.print(x, 3);
  Serial.print("  Y: ");
  Serial.print(y, 3);
  Serial.print("  Z: ");
  Serial.println(z, 3);

  // 6. Small delay for now
  delay(100);
}
