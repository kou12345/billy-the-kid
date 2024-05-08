# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3
import os
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

# .envファイルの内容を読み込見込む
load_dotenv()


def display_image(photo, response):
    image = Image.open(photo)

    # Ready image to draw bounding boxes on it.
    imgWidth, imgHeight = image.size
    draw = ImageDraw.Draw(image)

    # calculate and display bounding boxes for each detected custom label
    print("Detected custom labels for " + photo)
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


def show_custom_labels(model, photo, min_confidence):
    client = boto3.client("rekognition")

    with open(photo, "rb") as image:
        response = client.detect_custom_labels(
            Image={"Bytes": image.read()},
            MinConfidence=min_confidence,
            ProjectVersionArn=model,
        )

    # responseの中身を表示
    print(response)

    """
    {
        'CustomLabels': [], 
        'ResponseMetadata': {'RequestId': '844b2bf9-3426-4aab-9b81-68f03249557d', 
        'HTTPStatusCode': 200, 
        'HTTPHeaders': {'x-amzn-requestid': '844b2bf9-3426-4aab-9b81-68f03249557d', 'content-type': 'application/x-amz-json-1.1', 'content-length': '19', 'date': 'Wed, 08 May 2024 06:04:34 GMT'}, 
        'RetryAttempts': 0}
    }
    """

    display_image(photo, response)

    return len(response["CustomLabels"])


def start_model(project_arn, model_arn, version_name, min_inference_units):
    client = boto3.client("rekognition")

    try:
        # Start the model
        print("Starting model: " + model_arn)
        response = client.start_project_version(
            ProjectVersionArn=model_arn, MinInferenceUnits=min_inference_units
        )
        # Wait for the model to be in the running state
        project_version_running_waiter = client.get_waiter("project_version_running")
        project_version_running_waiter.wait(
            ProjectArn=project_arn, VersionNames=[version_name]
        )

        # Get the running status
        describe_response = client.describe_project_versions(
            ProjectArn=project_arn, VersionNames=[version_name]
        )
        for model in describe_response["ProjectVersionDescriptions"]:
            print("Status: " + model["Status"])
            print("Message: " + model["StatusMessage"])
    except Exception as e:
        print(e)

    print("Done...")


def main():
    project_arn = os.environ["PROJECT_ARN"]
    model_arn = os.environ["MODEL_ARN"]
    version_name = os.environ["VERSION_NAME"]
    min_inference_units = int(os.environ["MIN_INFERENCE_UNITS"])

    photo = ""
    min_confidence = 95

    start_model(project_arn, model_arn, version_name, min_inference_units)
    label_count = show_custom_labels(model_arn, photo, min_confidence)
    print("Custom labels detected: " + str(label_count))


if __name__ == "__main__":
    main()
