import math
from billy_the_kid.camera import Camera
from billy_the_kid.rekognition import Rekognition
from custom_serial import CustomSerial
import time
import os


"""
カメラが起動する
撮影して画像を保存する
推論する
サーボモータの角度を計算する
シリアル通信でサーボモータに角度を送信する

撮影して画像を保存する
推論する
サーボモータの角度を計算する
シリアル通信でサーボモータに角度を送信する
（角度がゼロの場合は、発射する） 
"""


def calculate_servo_angles(
    coordinate, actual_width, actual_height, distance
) -> tuple[float, float]:
    """
    物体の座標、実際の幅、高さ、距離を元に、サーボモーターの回転角度を計算する関数。

    Args:
        coordinate (dict): 物体の座標情報を持つ辞書。以下のキーを持つ:
            - "Width" (int): 物体の幅（ピクセル単位）
            - "Height" (int): 物体の高さ（ピクセル単位）
            - "Left" (int): 物体の左端の座標（ピクセル単位）
            - "Top" (int): 物体の上端の座標（ピクセル単位）
        actual_width (float): 実際の幅（cm）
        actual_height (float): 実際の高さ（cm）
        distance (float): 物体までの距離（cm）

    Returns:
        tuple: サーボモーターの回転角度 (servo_angle_x, servo_angle_y)。
            - servo_angle_x (float): 水平方向の回転角度（度数法）
            - servo_angle_y (float): 垂直方向の回転角度（度数法）
    """

    # カメラの中心座標を計算
    center_x = coordinate["Width"] // 2
    center_y = coordinate["Height"] // 2

    # 物体の中心座標を計算
    object_center_x = coordinate["Left"] + coordinate["Width"] // 2
    object_center_y = coordinate["Top"] + coordinate["Height"] // 2

    # 中心座標の差を計算
    delta_x = object_center_x - center_x
    delta_y = object_center_y - center_y

    # 実際のサイズとピクセル数の比率を計算
    ratio_x = actual_width / coordinate["Width"]
    ratio_y = actual_height / coordinate["Height"]

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


def find_nearest_coordinate(
    coordinates: list, actual_width: float, actual_height: float, distance: float
):
    """
    与えられた座標リストの中から、実際の幅、高さ、距離を考慮して、サーボモーターの角度の合計が最小となる座標を見つける関数。

    Args:
        coordinates (list): 座標のリスト。各座標は (x, y) の形式で表される。
        actual_width (float): 実際の幅。
        actual_height (float): 実際の高さ。
        distance (float): 距離。

    Returns:
        tuple: サーボモーターの角度の合計が最小となる座標。(x, y) の形式で返される。

    """
    min_angle = float("inf")
    nearest_coordinate = None

    for coordinate in coordinates:
        servo_angle_x, servo_angle_y = calculate_servo_angles(
            coordinate, actual_width, actual_height, distance
        )
        total_angle = abs(servo_angle_x) + abs(servo_angle_y)

        if total_angle < min_angle:
            min_angle = total_angle
            nearest_coordinate = coordinate

    return nearest_coordinate


def main():
    # 環境変数
    PROJECT_ARN = os.environ["PROJECT_ARN"]
    MODEL_ARN = os.environ["MODEL_ARN"]
    VERSION_NAME = os.environ["VERSION_NAME"]
    MIN_INFERENCE_UNITS = int(os.environ["MIN_INFERENCE_UNITS"])

    PORT = "/dev/cu.usbmodem1401"

    ACTUAL_WIDTH = 5.0  # 推論対象の実際の高さ（cm）
    ACTUAL_HEIGHT = 5.0  # 推論対象の実際の高さ（cm）
    DISTANCE = 30.0  # 推論対象までの距離（cm）
    IMAGE_PATH = "img/camera.jpg"  # 画像の保存先

    MIN_CONFIDENCE = 50  # 信頼度の閾値

    rekognition = Rekognition()
    rekognition.start_model(PROJECT_ARN, MODEL_ARN, VERSION_NAME, MIN_INFERENCE_UNITS)

    """
    MacBookの場合、0を指定するとエラーになる。とりあえず1を指定すると動作する
    https://github.com/opencv/opencv-python/issues/916
    """
    camera = Camera(1)

    while True:
        camera.process_frame(IMAGE_PATH)

        coordinates = rekognition.get_custom_labels(
            MODEL_ARN, IMAGE_PATH, MIN_CONFIDENCE
        )

        # 推論結果を元にサーボモータの回転角を決定する
        nearest_coordinate = find_nearest_coordinate(
            coordinates, ACTUAL_WIDTH, ACTUAL_HEIGHT, DISTANCE
        )
        if nearest_coordinate is None:
            print("nearest_coordinate is None")
            return

        servo_angle_x, servo_angle_y = calculate_servo_angles(
            nearest_coordinate, ACTUAL_WIDTH, ACTUAL_HEIGHT, DISTANCE
        )
        print(f"サーボモータ回転角度: X={servo_angle_x}, Y={servo_angle_y}")

        # serial = CustomSerial(port=port, baudrate=9600)
        if servo_angle_x == 0 and servo_angle_y == 0:
            print("発射します")
            # TODO シリアル通信で発射信号を送信する
            # serial.write("fire")
            # time.sleep(1)
            # serial.close()

            return
        else:
            print("発射しません")
            # TODO シリアル通信で回転角を送信する
            # serial.write(f"{servo_angle_x},{servo_angle_y})
            # time.sleep(1)
            # serial.close()


if __name__ == "__main__":
    main()
