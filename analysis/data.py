import serial
import time

ser = serial.Serial('COM6', 115200)
time.sleep(2)  # give Arduino time to reset

# Start experiment
ser.write(b'g\n')

with open('data.csv', 'w') as f:
    try:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode().strip()
                f.write(line + '\n')
    except KeyboardInterrupt:
        pass

# Stop experiment
ser.write(b's\n')
ser.close()
