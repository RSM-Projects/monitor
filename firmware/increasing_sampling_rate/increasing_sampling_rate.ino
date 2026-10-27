#include <Wire.h>

#define SDA_PIN 21
#define SCL_PIN 22

const uint32_t SAMPLE_INTERVAL_US = 1000;
uint32_t nextSampleTime = 0;

const uint8_t MPU_ADDR = 0x68;
const uint8_t PWR_MGMT_1  = 0x6B;
const uint8_t ACCEL_XOUT_H = 0x3B;
const uint8_t CONFIG = 0x1A;
const uint8_t SMPLRT_DIV = 0x19;



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

  Serial.begin(460800);
  delay(1000);
  Wire.begin(SDA_PIN, SCL_PIN);
  // new change: increasing the sensor read to 400khz from from the 100khz
  Wire.setClock(400000);

  Serial.print("PWR_MGMT_1 before: 0x");
  Serial.println(readregister(PWR_MGMT_1),HEX);


  uint8_t error = writeRegister(PWR_MGMT_1,0x00);
  if (error != 0) {
    Serial.print("Wake-up failed, error code: ");
    Serial.println(error);
    return;
  }

  delay(100); 

  Serial.print("PWR_MGMT_1 after: 0x");
  Serial.println(readregister(PWR_MGMT_1), HEX);

    delay(100); 

  uint8_t error2 = writeRegister(CONFIG,0x01);
  if (error2 != 0) {
    Serial.print(" error code: ");
    Serial.println(error2);
    return;
  }

int config_output = readregister(CONFIG);

if(config_output >= 0){
    Serial.print("CONFIG after: 0x");
  Serial.println(config_output, HEX);
}

    delay(100); 

      uint8_t error3 = writeRegister(SMPLRT_DIV,0x00);
  if (error3 != 0) {
    Serial.print("error code: ");
    Serial.println(error3);
    return;
  }

    Serial.print("SMPLRT_DIV after: 0x");
  Serial.println(readregister(SMPLRT_DIV), HEX);

     delay(100); 


}

void loop() {


 if (nextSampleTime == 0) {
  nextSampleTime = micros() + SAMPLE_INTERVAL_US;
}
     if ((int32_t)(micros() - nextSampleTime) <0) return;


         uint32_t t_us = micros();

    nextSampleTime += SAMPLE_INTERVAL_US;



      if ((int32_t)(t_us - nextSampleTime) >= 0) {
    nextSampleTime = t_us + SAMPLE_INTERVAL_US;
  }

    
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


  Serial.print(t_us);
  Serial.print(",");
  Serial.print(rawX);
   Serial.print(",");
  Serial.print(rawY);
     Serial.print(",");
  Serial.println(rawZ);

}
