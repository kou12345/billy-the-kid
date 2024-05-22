import boto3
from PIL import Image
from typing import TypedDict, List
import logging
import botocore.exceptions

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class CustomLabelResponse(TypedDict):
    Name: str
    Confidence: float
    Width: float
    Height: float
    Left: float
    Top: float
    ImageWidth: int
    ImageHeight: int


class Rekognition:
    def __init__(self):
        self.client = boto3.client("rekognition")

    def start_model(
        self,
        project_arn: str,
        model_arn: str,
        version_name: str,
        min_inference_units: int,
    ):
        """Start the Rekognition model."""
        try:
            # Check if the model is already running
            describe_response = self.client.describe_project_versions(
                ProjectArn=project_arn, VersionNames=[version_name]
            )
            model_status = describe_response["ProjectVersionDescriptions"][0]["Status"]

            if model_status == "RUNNING":
                logger.info(f"Model {model_arn} is already running.")
                return

            logger.info(f"Starting model: {model_arn}")
            response = self.client.start_project_version(
                ProjectVersionArn=model_arn, MinInferenceUnits=min_inference_units
            )

            project_version_running_waiter = self.client.get_waiter(
                "project_version_running"
            )
            project_version_running_waiter.wait(
                ProjectArn=project_arn, VersionNames=[version_name]
            )

            describe_response = self.client.describe_project_versions(
                ProjectArn=project_arn, VersionNames=[version_name]
            )

            for model in describe_response["ProjectVersionDescriptions"]:
                logger.info(f"Status: {model['Status']}")
                logger.info(f"Message: {model['StatusMessage']}")
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "ResourceInUseException":
                logger.warning(f"Model {model_arn} is already running.")
            else:
                logger.error(f"Error starting model: {e}")
                raise

        logger.info("Model started successfully.")

    def stop_model(self, model_arn: str):
        """Stop the Rekognition model."""
        logger.info(f"Stopping model: {model_arn}")

        try:
            response = self.client.stop_project_version(ProjectVersionArn=model_arn)
            status = response["Status"]
            logger.info(f"Status: {status}")
        except botocore.exceptions.ClientError as e:
            logger.error(f"Error stopping model: {e}")
            raise

        logger.info("Model stopped successfully.")

    def get_custom_labels(
        self, model, image_path: str, min_confidence: int
    ) -> List[CustomLabelResponse]:
        """Get the custom labels and their coordinates from the image."""
        with open(image_path, "rb") as image_file:
            response = self.client.detect_custom_labels(
                Image={"Bytes": image_file.read()},
                MinConfidence=min_confidence,
                ProjectVersionArn=model,
            )

        with Image.open(image_path) as image:
            image_width, image_height = image.size

        custom_labels = []

        for custom_label in response["CustomLabels"]:
            if "Geometry" in custom_label:
                box = custom_label["Geometry"]["BoundingBox"]
                left = image_width * box["Left"]
                top = image_height * box["Top"]
                width = image_width * box["Width"]
                height = image_height * box["Height"]

                custom_labels.append(
                    {
                        "Name": custom_label["Name"],
                        "Confidence": custom_label["Confidence"],
                        "Width": width,
                        "Height": height,
                        "Left": left,
                        "Top": top,
                        "ImageWidth": image_width,
                        "ImageHeight": image_height,
                    }
                )

        return custom_labels
