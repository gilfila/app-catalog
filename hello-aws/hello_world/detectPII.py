"""
Purpose
HEY TONY
An AWS lambda function that analyzes documents with Amazon Textract.
"""
import json
import base64
import logging
import boto3

from botocore.exceptions import ClientError

# Set up logging.
logger = logging.getLogger(__name__)


def lambda_handler(event, context):

    # logging of arguments
    print("event:" + str(event))
    print("context:" + str(context))

    # Access the 'textDetections' array from the parsed JSON
    text_detections = event['textDetections']
    print("textDetections:" + str(text_detections))

    # Amazon translate client
    comprehend = boto3.client('comprehend')

    #Solution
    #Combine the list of strings into a single string
    combined_text = ' '.join(text_detections)

    # Call Amazon translate
    response = comprehend.detect_pii_entities(
        Text=combined_text,  # Use the combined text
        LanguageCode='en'
    )

    return response