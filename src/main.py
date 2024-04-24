from serial import Serial
import time


serial = Serial(port="...", baudrate=9600)

serial.write("Hello, Arduino!\n")
time.sleep(1)
serial.close()
