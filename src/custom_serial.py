import serial
import time


class CustomSerial:
    def __init__(self, port: str, baudrate: int) -> None:
        self.ser = serial.Serial(port, baudrate)
        # Wait for the serial connection to be established
        time.sleep(2)

    def write(self, data: str) -> None:
        encoded_data = data.encode("utf-8")
        self.ser.write(encoded_data)
        # Send a newline character to indicate the end of data
        self.ser.write(b"\n")

    def read(self) -> str:
        return self.ser.readline().decode()

    def close(self) -> None:
        self.ser.close()
