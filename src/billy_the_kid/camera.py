import cv2
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class Camera:
    def __init__(self, camera_id):
        self.camera_id = camera_id
        self.cap = cv2.VideoCapture(camera_id)

        if not self.cap.isOpened():
            logger.error(f"Failed to open camera with ID {camera_id}")
            exit()
        logger.info(f"Camera with ID {camera_id} opened successfully")

    def read(self):
        ret, frame = self.cap.read()
        if not ret:
            logger.warning("Failed to read frame from camera")
        return ret, frame

    def release(self):
        self.cap.release()
        logger.info("Camera resources released")

    def get_frame(self):
        ret, frame = self.read()
        if not ret:
            logger.warning("Failed to get frame")
            return None
        return frame

    def get_frame_rgb(self):
        frame = self.get_frame()
        if frame is None:
            return None
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        logger.debug("Frame converted to RGB")
        return rgb_frame

    def process_frame(self, image_path):
        ret, frame = self.read()

        if ret:
            # 画像サイズを固定 (例: 960x540)
            fixed_size = (960, 540)
            resized_frame = cv2.resize(
                frame, fixed_size, fx=0, fy=0, interpolation=cv2.INTER_AREA
            )
            logger.debug(f"Frame resized to {fixed_size}")

            # 縮小画像をJPEGで圧縮し4MB以下に抑える
            quality = 80
            _, encoded_img = cv2.imencode(
                ".jpg", resized_frame, [cv2.IMWRITE_JPEG_QUALITY, quality]
            )

            # 画像のファイルサイズが4MBを超える場合に、JPEG圧縮の品質を下げて画像サイズを小さくする処理
            while len(encoded_img) > 4 * 1024 * 1024:
                quality -= 10
                logger.debug(f"Reducing JPEG quality to {quality}")
                _, encoded_img = cv2.imencode(
                    ".jpg", resized_frame, [cv2.IMWRITE_JPEG_QUALITY, quality]
                )

            # 画像をファイルに書き出し
            with open(image_path, "wb") as f:
                f.write(encoded_img)
            logger.info(f"Frame processed and saved to {image_path}")
        else:
            logger.warning("Failed to process frame")

    def run(self):
        logger.info("Starting camera loop")
        frame_count = 0
        while True:
            self.process_frame("output.jpg")
            frame_count += 1

            if frame_count % 100 == 0:  # 100フレームごとにログを出力
                logger.info(f"Processed {frame_count} frames")

            # 'q'を押して終了
            if cv2.waitKey(1) & 0xFF == ord("q"):
                logger.info("Quit signal received")
                break

        self.release()
        cv2.destroyAllWindows()
        logger.info("Camera loop ended")
