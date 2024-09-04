
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# # SPDX-License-Identifier: Apache-2.0

# """
# Purpose
# An AWS lambda function that analyzes documents with Amazon Textract.
# """
# import json
# import base64
# import logging
# import boto3

# from botocore.exceptions import ClientError

# # Set up logging.
# logger = logging.getLogger(__name__)


# def lambda_handler(event,context):
    
#     #logging of arguements
#     print("event:" + str(event))
#     print("context:" + str(context))

#     s3BucketName = event["bucket"]
#     documentName = event["filepath"]

#     # Amazon translate client
#     client = boto3.client('rekognition')

#     response = client.detect_text(
#     Image={
#         'S3Object': {
#             'Bucket': s3BucketName,
#             'Name': documentName
#             }
#     }
# )
    
#     return response['TextDetections']



# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Purpose:
An AWS Lambda function that analyzes documents with Amazon Rekognition.
"""

import json
import base64
import logging
import boto3
from botocore.exceptions import ClientError

# Set up logging.
logger = logging.getLogger(__name__)

def lambda_handler(event, context):
    print("event:" + str(event))  
    print("context:" + str(context))

    s3_bucket_name = event["bucket"]
    document_name = event["filepath"]

    rekognition_client = boto3.client('rekognition')

    try:
        response = rekognition_client.detect_text(
            Image={
                'S3Object': {
                    'Bucket': s3_bucket_name,
                    'Name': document_name
                }
            }
        )

        # Extract and return all text detections
        all_text_detections = []
        for detection in response['TextDetections']:
            if detection['Type'] == 'LINE':  # Filter for lines of text
                all_text_detections.append(detection['DetectedText'])

        return {
            'statusCode': 200,  
            'body': json.dumps({
                'textDetections': all_text_detections
            })
        }

    except ClientError as error:
        logger.error("Error calling Rekognition: %s", error)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(error)})
        }
