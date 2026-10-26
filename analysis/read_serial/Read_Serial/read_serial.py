import serial
import time

PORT = "/dev/cu.usbserial-10"
BAUD_RATE = 115200

try:
    esp32 = serial.Serial(PORT, BAUD_RATE, timeout=2)
    time.sleep(2)

    print("Connected to ESP32!")
    print("Reading vibration data... Press Ctrl+C to stop.\n")

    while True:
      line = esp32.readline()

      if line:
        text = line.decode("utf-8", errors="replace").strip()
        print(text)

except serial.SerialException as error:
    print(f"Serial connection error: {error}")

except KeyboardInterrupt:
    print("\nStopped reading sensor data.")

finally:
  if "esp32" in locals() and esp32.is_open:
    esp32.close()
  print("Serial connection closed.")



