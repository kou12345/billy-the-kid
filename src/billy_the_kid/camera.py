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

    def process_frame(self):
        ret, frame = self.read()

        if ret:
            # 画像サイズを縮小 (例: 50%)
            resized_frame = cv2.resize(frame, None, fx=0.5, fy=0.5)

            # 縮小画像をJPEGで圧縮し4MB以下に抑える
            _, encoded_img = cv2.imencode(
                ".jpg", resized_frame, [cv2.IMWRITE_JPEG_QUALITY, 80]
            )

            # 画像のファイルサイズが4MBを超える場合に、JPEG圧縮の品質を下げて画像サイズを小さくする処理
            while len(encoded_img) > 4 * 1024 * 1024:
                _, encoded_img = cv2.imencode(
                    ".jpg", resized_frame, [cv2.IMWRITE_JPEG_QUALITY, 70]
                )

            # 画像をファイルに書き出し
            with open("camera.jpg", "wb") as f:
                f.write(encoded_img)

    def run(self):
        while True:
            self.process_frame()

            # 'q'を押して終了
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        self.release()
        cv2.destroyAllWindows()
