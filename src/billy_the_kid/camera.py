import cv2


class Camera:
    def __init__(self, camera_id):
        self.camera_id = camera_id
        self.cap = cv2.VideoCapture(camera_id)

    def read(self):
        # カメラから1フレームを読み込む
        # 読み込みに成功した場合はフレームを返し、失敗した場合はNoneを返す
        return self.cap.read()

    def release(self):
        # カメラリソースを解放する
        self.cap.release()

    def get_frame(self):
        # カメラから1フレームを取得する
        # 取得に成功した場合はフレームを返し、失敗した場合はNoneを返す
        ret, frame = self.read()
        if not ret:
            return None
        return frame

    def get_frame_gray(self):
        # カメラから1フレームを取得し、グレースケールに変換する
        # 取得に成功した場合はグレースケールのフレームを返し、失敗した場合はNoneを返す
        frame = self.get_frame()
        if frame is None:
            return None
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    def get_frame_rgb(self):
        # カメラから1フレームを取得し、RGBに変換する
        # 取得に成功した場合はRGBのフレームを返し、失敗した場合はNoneを返す
        frame = self.get_frame()
        if frame is None:
            return None
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
