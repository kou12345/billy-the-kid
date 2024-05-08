from custom_serial import CustomSerial
import time

# TODO .envでportを指定したい
port = "/dev/cu.usbmodem1401"

serial = CustomSerial(port=port, baudrate=9600)
print(serial)

serial.write("123")
time.sleep(1)
serial.close()
