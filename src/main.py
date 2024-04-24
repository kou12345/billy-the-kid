from custom_serial import CustomSerial
import time


serial = CustomSerial(port="COM20", baudrate=9600)
print(serial)

serial.write("123")
time.sleep(1)
serial.close()
