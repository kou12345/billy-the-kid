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
