from billy_the_kid.camera import Camera
from billy_the_kid.rekognition import Rekognition
from custom_serial import CustomSerial
import time
import os


def main():
    # 環境変数
    project_arn = os.environ["PROJECT_ARN"]
    model_arn = os.environ["MODEL_ARN"]
    version_name = os.environ["VERSION_NAME"]
    min_inference_units = int(os.environ["MIN_INFERENCE_UNITS"])

    port = "/dev/cu.usbmodem1401"

    """
    MacBookの場合、0を指定するとエラーになる。とりあえず1を指定すると動作する
    https://github.com/opencv/opencv-python/issues/916
    """
    camera = Camera(1)
    # カメラを起動 画像を撮影し、保存する
    camera.run()

    # 検出対象の画像
    image_path = "img/camera.jpg"
    min_confidence = 50

    rekognition = Rekognition()

    rekognition.start_model(project_arn, model_arn, version_name, min_inference_units)

    # TODO 検出を定期的に行う
    label_count = rekognition.show_custom_labels(model_arn, image_path, min_confidence)
    print("Custom labels detected: " + str(label_count))

    # TODO 推論結果を元にサーボモータの回転角を決定する

    # TODO シリアル通信で回転角を送信する
    # serial = CustomSerial(port=port, baudrate=9600)

    # serial.write("123")
    # time.sleep(1)
    # serial.close()


if __name__ == "__main__":
    main()
