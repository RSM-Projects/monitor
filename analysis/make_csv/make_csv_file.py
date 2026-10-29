import csv

import serial
import time
from pathlib import Path

PORT = "/dev/cu.usbserial-10"
BAUD_RATE =460800
OUTPUT_FILE_PATH= Path("../../data/raw/")
LABEL = "fan_on_05"

OUTPUT_FILE_PATH.mkdir(parents = True, exist_ok =True)
output_file =OUTPUT_FILE_PATH / f"{LABEL}.csv"

good_lines =0
bad_lines =0

try:
    esp32 = serial.Serial(PORT, BAUD_RATE, timeout=2)
    time.sleep(2)

    print("Connected to ESP32!")
    print("Reading vibration data... Press Ctrl+C to stop.\n")

    with open(output_file,"w",newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp_us", "raw_x", "raw_y", "raw_z"])

        while True:
            line = esp32.readline()

            if line:
                text = line.decode("utf-8", errors="replace").strip()
                numbers = text.split(",")

                if len(numbers) != 4:
                    bad_lines += 1
                    continue

                values = numbers

                try:
                    t = int(numbers[0])
                    x, y, z = map(int, numbers[1:])



                except ValueError:
                    print("Invalid sensor line; skipping.")
                    bad_lines += 1
                    continue

                writer.writerow([t, x, y, z])
                good_lines += 1
                print(t,x, y, z)

                if good_lines % 10 == 0:
                    print(f"{good_lines} samples saved (last: {t} , {x}, {y}, {z})")
                    if good_lines % 100 == 0:
                       f.flush()


except serial.SerialException as error:
    print(f"Serial connection error: {error}")

except KeyboardInterrupt:
    print("\nStopped reading sensor data.")

finally:
    if "esp32" in locals() and esp32.is_open:
        esp32.close()
    print(f"Good lines: {good_lines}, bad lines: {bad_lines}")
    print("Serial connection closed.")



