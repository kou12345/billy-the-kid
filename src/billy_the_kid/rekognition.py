import boto3
from PIL import Image

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

    # 認識したカスタムラベルの座標を返す
    def get_custom_labels(self, model, image_path: str, min_confidence: int) -> list:
        with open(image_path, "rb") as image:
            response = self.client.detect_custom_labels(
                Image={"Bytes": image.read()},
                MinConfidence=min_confidence,
                ProjectVersionArn=model,
            )

        image = Image.open(image_path)

        output = []

        # Ready image to draw bounding boxes on it.
        imgWidth, imgHeight = image.size

        for customLabel in response["CustomLabels"]:
            if "Geometry" in customLabel:
                box = customLabel["Geometry"]["BoundingBox"]
                left = imgWidth * box["Left"]
                top = imgHeight * box["Top"]
                width = imgWidth * box["Width"]
                height = imgHeight * box["Height"]

                output.append(
                    {
                        "Name": customLabel["Name"],
                        "Confidence": customLabel["Confidence"],
                        "Width": width,
                        "Height": height,
                        "Left": left,
                        "Top": top,
                        "ImageWidth": imgWidth,
                        "ImageHeight": imgHeight,
                    }
                )

        return output


"""
{
    "CustomLabels":[
        {
            "Name":"yellow target",
            "Confidence":86.44400024414062,
            "Geometry":{
                "BoundingBox":{
                    "Width":0.20201000571250916,
                    "Height":0.2780799865722656,
                    "Left":0.47442999482154846,
                    "Top":0.6149200201034546
                }
            }
        },
        {
            "Name":"yellow target",
            "Confidence":80.99800109863281,
            "Geometry":{
                "BoundingBox":{
                    "Width":0.18456999957561493,
                    "Height":0.23803000152111053,
                    "Left":0.410970002412796,
                    "Top":0.33625999093055725
                }
            }
        }
    ],
    "ResponseMetadata":{
        "RequestId":"2e3934c4-6282-4b5b-8d50-40f8b68eca20",
        "HTTPStatusCode":200,
        "HTTPHeaders":{
            "x-amzn-requestid":"2e3934c4-6282-4b5b-8d50-40f8b68eca20",
            "content-type":"application/x-amz-json-1.1",
            "content-length":"404",
            "date":"Wed, 15 May 2024 03:45:43 GMT"
        },
        "RetryAttempts":0
    }
}
"""
