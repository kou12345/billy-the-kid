# camera.pyからCameraクラスをimport
from billy_the_kid.camera import Camera
import cv2

"""
MacBookの場合、0を指定するとエラーになる。とりあえず1を指定すると動作する
https://github.com/opencv/opencv-python/issues/916
"""
camera = Camera(1)

while True:
    # カメラからフレームを取得
    frame = camera.get_frame()

    # フレームが正常に取得できなかった場合は終了
    if frame is None:
        break

    # 取得したフレームを表示
    cv2.imshow("Camera", frame)

    # 'q'キーが押されたらループを終了
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# カメラの解放
camera.release()

# ウィンドウを閉じる
cv2.destroyAllWindows()
