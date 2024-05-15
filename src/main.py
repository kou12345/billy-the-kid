import math
from billy_the_kid.camera import Camera
from billy_the_kid.rekognition import Rekognition
from custom_serial import CustomSerial
import time
import os


def calculate_servo_angles(
    coordinates, image_width, image_height, actual_width, actual_height, distance
):
    # カメラの中心座標を計算
    center_x = image_width // 2
    center_y = image_height // 2

    # 物体の中心座標を計算
    object_center_x = coordinates["Left"] + coordinates["Width"] // 2
    object_center_y = coordinates["Top"] + coordinates["Height"] // 2

    # 中心座標の差を計算
    delta_x = object_center_x - center_x
    delta_y = object_center_y - center_y

    # 実際のサイズとピクセル数の比率を計算
    ratio_x = actual_width / coordinates["Width"]
    ratio_y = actual_height / coordinates["Height"]

    # 中心座標の差を実際の距離に変換
    actual_delta_x = delta_x * ratio_x
    actual_delta_y = delta_y * ratio_y

    # サーボモータの回転角度を計算
    servo_angle_x = math.atan2(actual_delta_x, distance) * 180 / math.pi
    servo_angle_y = math.atan2(actual_delta_y, distance) * 180 / math.pi

    return servo_angle_x, servo_angle_y


# TODO この関数を試す
# TODO 基準距離での的のサイズを確認する


def calculate_distance(
    reference_distance, reference_target_size_pixels, new_target_size_pixels
):
    new_distance = (
        reference_distance * reference_target_size_pixels
    ) / new_target_size_pixels
    return new_distance


# # 使用例
# reference_distance = 10.0  # 基準距離（単位は任意）
# reference_target_size_pixels = 200  # 基準距離での的の画像上のサイズ（ピクセル数）
# new_target_size_pixels = 100  # 新しい画像上での的のサイズ（ピクセル数）

# new_distance = calculate_distance(
#     reference_distance, reference_target_size_pixels, new_target_size_pixels
# )
# print(f"新しい距離: {new_distance:.2f} （単位は基準距離と同じ）")


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
    # camera = Camera(1)
    # カメラを起動 画像を撮影し、保存する
    # camera.run()

    # 検出対象の画像
    # image_path = "img/camera.jpg"
    # image_path = "/Users/kou12345/Downloads/IMG_1161.JPG"  # 正しく表示される
    # image_path = "/Users/kou12345/Downloads/IMG_1173.JPG"
    image_path = "/Users/kou12345/Downloads/IMG_1159.JPG"

    min_confidence = 50

    rekognition = Rekognition()

    rekognition.start_model(project_arn, model_arn, version_name, min_inference_units)

    # TODO 検出を定期的に行う
    coordinates = rekognition.get_custom_labels(model_arn, image_path, min_confidence)

    print(coordinates)
    """
    coordinatesの値
    [
        {
            "Name":"yellow target",
            "Confidence":64.64700317382812,
            "Width":420.65857315063477,
            "Height":418.461138010025,
            "Left":1387.0886764526367,
            "Top":1562.5915517807007
            "ImageWidth": imgWidth,
            "ImageHeight": imgHeight,
        }
    ]
    """

    actual_width = 5.0  # 推論対象の実際の幅（cm）
    actual_height = 5.0  # 推論対象の実際の高さ（cm）
    distance = 30.0  # 推論対象までの距離（cm）

    # 推論結果を元にサーボモータの回転角を決定する
    # TODO coordinatesが複数ある場合は一番近いものを選択する
    for coordinate in coordinates:
        servo_angle_x, servo_angle_y = calculate_servo_angles(
            coordinate,
            coordinate["ImageWidth"],
            coordinate["ImageHeight"],
            actual_width,
            actual_height,
            distance,
        )
        print(f"サーボモータ回転角度: X={servo_angle_x}, Y={servo_angle_y}")

        # 的までの距離を計算
        print(
            calculate_distance(
                coordinate["Width"],
                coordinate["Height"],
                actual_width,
                actual_height,
                1000,
            )
        )

    # TODO シリアル通信で回転角を送信する
    # serial = CustomSerial(port=port, baudrate=9600)

    # serial.write("123")
    # time.sleep(1)
    # serial.close()


if __name__ == "__main__":
    main()
