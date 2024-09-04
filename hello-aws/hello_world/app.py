
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Purpose
An AWS lambda function that analyzes documents with Amazon Textract.
"""
import json
import base64
import logging
import boto3

from botocore.exceptions import ClientError

# Set up logging.
logger = logging.getLogger(__name__)

# Get the boto3 client.
translate_client = boto3.client('translate')


# end of episode 1
def lambda_handler(event,context):
    
    #logging of arguements
    print("event:" + str(event))
    print("context:" + str(context))

    # Amazon translate client
    translate = boto3.client('translate')


    # Call Amazon translate
    response = translate.translate_text(
        SourceLanguageCode= event['translateFrom'],
        TargetLanguageCode= event['translateTo'],
        Text= event['text']
    )
    
    return response['TranslatedText']