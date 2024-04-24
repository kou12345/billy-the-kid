# Arduinoとのシリアル通信を行うためのクラス

import serial
import time


class Serial:
    """
    このクラスはシリアル通信インターフェースを表します。

    Args:
        port (str): シリアルデバイスが接続されているポートです。
        baudrate (int): シリアル通信のボーレートです。

    Attributes:
        ser (serial.Serial): 通信に使用されるシリアルオブジェクトです。

    """

    def __init__(self, port, baudrate):
        # コンストラクタの実装
        pass
        self.ser = serial.Serial(port, baudrate)
        time.sleep(2)

    def write(self, data):
        """
        シリアルデバイスにデータを書き込みます。

        Args:
            data (str): 書き込むデータです。

        """
        self.ser.write(data.encode())

    def read(self):
        """
        シリアルデバイスからデータを読み取ります。

        Returns:
            str: シリアルデバイスから読み取ったデータです。

        """
        return self.ser.readline().decode()

    def close(self):
        """
        シリアルデバイスをクローズします。

        """
        self.ser.close()
