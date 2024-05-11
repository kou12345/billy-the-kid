from billy_the_kid.rekognition import Rekognition
from custom_serial import CustomSerial
import time
import os


# # TODO .envでportを指定したい
# port = "/dev/cu.usbmodem1401"

# serial = CustomSerial(port=port, baudrate=9600)
# print(serial)

# serial.write("123")
# time.sleep(1)
# serial.close()


def main():
    project_arn = os.environ["PROJECT_ARN"]
    model_arn = os.environ["MODEL_ARN"]
    version_name = os.environ["VERSION_NAME"]
    min_inference_units = int(os.environ["MIN_INFERENCE_UNITS"])

    # 検出対象の画像
    image_path = "/Users/kou12345/Downloads/IMG_1161.JPG"
    min_confidence = 50

    rekognition = Rekognition()

    rekognition.start_model(project_arn, model_arn, version_name, min_inference_units)
    label_count = rekognition.show_custom_labels(model_arn, image_path, min_confidence)
    print("Custom labels detected: " + str(label_count))


if __name__ == "__main__":
    main()
