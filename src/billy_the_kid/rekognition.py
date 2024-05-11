import boto3
from PIL import Image, ImageDraw, ImageFont


"""
Amazon Rekognition API
"""


class Rekognition:

    def __init__(self):
        self.client = boto3.client("rekognition")

    """
    modelを開始する
    """

    def start_model(
        self,
        project_arn: str,
        model_arn: str,
        version_name: str,
        min_inference_units: int,
    ) -> None:

        try:
            # モデルを開始する
            print("Starting model: " + model_arn)
            response = self.client.start_project_version(
                ProjectVersionArn=model_arn, MinInferenceUnits=min_inference_units
            )

            # モデルが実行状態になるまで待つ
            project_version_running_waiter = self.client.get_waiter(
                "project_version_running"
            )
            project_version_running_waiter.wait(
                ProjectArn=project_arn, VersionNames=[version_name]
            )

            # 実行ステータスを取得する
            describe_response = self.client.describe_project_versions(
                ProjectArn=project_arn, VersionNames=[version_name]
            )

            for model in describe_response["ProjectVersionDescriptions"]:
                print("Status: " + model["Status"])
                print("Message: " + model["StatusMessage"])
        except Exception as e:
            print(e)

        print("Done...")

    """
    modelを停止する
    """

    def stop_model(self, model_arn: str) -> None:
        print("Stopping model:" + model_arn)

        # モデルを停止する
        try:
            response = self.client.stop_project_version(ProjectVersionArn=model_arn)
            status = response["Status"]
            print("Status: " + status)
        except Exception as e:
            print(e)

        print("Done...")

    """
    画像を表示する
    """

    def display_image(image_path: str, response):
        image = Image.open(image_path)

        # Ready image to draw bounding boxes on it.
        imgWidth, imgHeight = image.size
        draw = ImageDraw.Draw(image)

        # calculate and display bounding boxes for each detected custom label
        print("Detected custom labels for " + image_path)
        for customLabel in response["CustomLabels"]:
            print("Label " + str(customLabel["Name"]))
            print("Confidence " + str(customLabel["Confidence"]))
            if "Geometry" in customLabel:
                box = customLabel["Geometry"]["BoundingBox"]
                left = imgWidth * box["Left"]
                top = imgHeight * box["Top"]
                width = imgWidth * box["Width"]
                height = imgHeight * box["Height"]

                fnt = ImageFont.truetype("/Library/Fonts/Arial.ttf", 50)
                draw.text((left, top), customLabel["Name"], fill="#00d400", font=fnt)

                print("Left: " + "{0:.0f}".format(left))
                print("Top: " + "{0:.0f}".format(top))
                print("Label Width: " + "{0:.0f}".format(width))
                print("Label Height: " + "{0:.0f}".format(height))

                points = (
                    (left, top),
                    (left + width, top),
                    (left + width, top + height),
                    (left, top + height),
                    (left, top),
                )
                draw.line(points, fill="#00d400", width=5)

        image.show()

    """
    カスタムラベルを表示する
    """

    def show_custom_labels(self, model, image_path: str, min_confidence: int) -> int:
        with open(image_path, "rb") as image:
            response = self.client.detect_custom_labels(
                Image={"Bytes": image.read()},
                MinConfidence=min_confidence,
                ProjectVersionArn=model,
            )

        print(response)

        self.display_image(image_path, response)

        return len(response["CustomLabels"])
