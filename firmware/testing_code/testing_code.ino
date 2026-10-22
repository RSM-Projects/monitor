void setup() {
  Serial.begin(115200);          // start serial at 115200 baud
  delay(1000);                   // give the monitor a moment to connect
  Serial.println("Hello from ESP32");

}

void loop() {
  Serial.println(millis());      // time since boot, in milliseconds
  delay(100);     

}
