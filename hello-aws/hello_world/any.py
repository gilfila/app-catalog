import json
import boto3

# Initialize AWS service clients
clients = {
    'Comprehend': boto3.client('comprehend'),
    'Rekognition': boto3.client('rekognition'),
    'Textract': boto3.client('textract'),
    'Translate': boto3.client('translate')
}

# supported aws methods
valid_methods = {
    'Comprehend': [
        'batch_detect_dominant_language',
        'batch_detect_entities',
        'batch_detect_key_phrases',
        'batch_detect_sentiment',
        'batch_detect_syntax',
        'batch_detect_targeted_sentiment',
        'contains_pii_entities',
        'describe_document_classification_job',
        'describe_dominant_language_detection_job',
        'describe_entities_detection_job',
        'describe_events_detection_job',
        'describe_key_phrases_detection_job',
        'describe_pii_entities_detection_job',
        'describe_resource_policy',
        'describe_sentiment_detection_job',
        'describe_targeted_sentiment_detection_job',
        'describe_topics_detection_job',
        'detect_dominant_language',
        'detect_entities',
        'detect_key_phrases',
        'detect_pii_entities',
        'detect_sentiment',
        'detect_syntax',
        'detect_targeted_sentiment',
        'list_document_classification_jobs',
        'list_dominant_language_detection_jobs',
        'list_entities_detection_jobs',
        'list_events_detection_jobs',
        'list_key_phrases_detection_jobs',
        'list_pii_entities_detection_jobs',
        'list_sentiment_detection_jobs',
        'list_tags_for_resource',
        'list_targeted_sentiment_detection_jobs',
        'list_topics_detection_jobs',
        'tag_resource',
        'untag_resource'
    ],
    'Rekognition': [ 
        'AssociateFaces',
        'CreateCollection',
        'CreateUser',
        'DeleteCollection',
        'DeleteFaces',
        'DeleteUser',
        'DescribeCollection',
        'DetectFaces',
        'DetectLabels',
        'DetectModerationLabels',
        'DetectProtectiveEquipment',
        'DetectText',
        'DisassociateFaces',
        'GetCelebrityInfo',
        'IndexFaces',
        'ListCollections',
        'ListFaces',
        'ListUsers',
        'RecognizeCelebrities',
        'SearchFacesByImage',
        'SearchUsers',
        'SearchUsersByImage',
        'GetCelebrityRecognition',
        'GetContentModeration',
        'GetFaceDetection',
        'GetFaceSearch',
        'GetLabelDetection',
        'GetPersonTracking',
        'GetSegmentDetection',
        'GetTextDetection',
        'StartCelebrityRecognition',
        'StartContentModeration',
        'StartFaceDetection',
        'StartFaceSearch',
        'StartLabelDetection',
        'StartPersonTracking',
        'StartSegmentDetection',
        'StartTextDetection'
    ],
    'Textract': [ 
        'AnalyzeDocument',
        'AnalyzeExpense',
        'AnalyzeID',
        'DetectDocumentText',
        'GetDocumentAnalysis',
        'GetDocumentTextDetection',
        'GetExpenseAnalysis',
        'GetLendingAnalysis',
        'GetLendingAnalysisSummary',
        'StartDocumentAnalysis',
        'StartDocumentTextDetection',
        'StartExpenseAnalysis',
        'StartLendingAnalysis'
    ],
    'Translate': [  
        'DeleteTerminology',
        'DescribeTextTranslationJob',
        'GetTerminology',
        'ImportTerminology',
        'ListLanguages',
        'ListTagsForResource',
        'ListTerminologies',
        'ListTextTranslationJobs',
        'StartTextTranslationJob',
        'StopTextTranslationJob',
        'TagResource',
        'TranslateDocument',
        'TranslateText',
        'UntagResource'
    ],
    'EventBridge': [ 
        'CreateApiDestination',
        'CreateConnection',
        'DeauthorizeConnection',
        'DeleteApiDestination',
        'DeleteConnection',
        'DeleteRule',
        'DisableRule',
        'EnableRule',
        'InvokeApiDestination',
        'PutEvents',
        'PutRule',
        'PutTargets',
        'RemoveTargets',
        'TagResource',
        'UntagResource',
        'UpdateApiDestination',
        'UpdateConnection'
    ]
}

def is_json_object(request):
    """
    Determines if the input is a JSON object (dictionary) or a string that needs to be parsed.
    
    Returns:
        bool: True if the input is a dictionary (JSON object), False if it is a string.
    """
    if isinstance(request, dict):
        return True
    elif isinstance(request, str):
        try:
            # Attempt to parse the string as JSON
            json.loads(request)
            return False  # If it successfully parses, it's a string that contains JSON
        except json.JSONDecodeError:
            return False  # If it fails to parse, it's just a regular string
    
    return False

def parse_request(request_str):
    """Parse the custom formatted request string into a dictionary."""
    request_dict = {}
    try:
        # Clean the request string and split by ',\n'

        request_str = request_str.replace("{", "").replace("}", "").replace("'", "")
        params = request_str.split(',\n')

        for param in params:
            if '=' in param:
                key, value = param.split('=', 1)
                request_dict[key.strip()] = value.strip().strip()

    except Exception as e:
        raise ValueError(f'Error processing request: {str(e)}')
    
    return request_dict

import json


def lambda_handler(event, context):
    try:
        # Extract the desired fields from the event
        method_name = event.get('awsMethod')
        api_name = event.get('awsAPI')
        request = event.get('request')

        print("method:" + str(method_name))
        print("api:" + str(api_name))
        print("request:" + str(request))

        if api_name not in clients:
            return {
                'statusCode': 400,
                'body': json.dumps('Invalid AWS API')
            }

        if method_name not in valid_methods.get(api_name, []):
            return {
                'statusCode': 400,
                'body': json.dumps('Invalid method for the specified API')
            }

        # Parse the request string to a dictionary
        if is_json_object(request): 
            request_dict = request
        else:
            request_dict = parse_request(request)
           
        # Get the appropriate client
        client = clients[api_name]
        
        # Dynamically call the API method
        method_to_call = getattr(client, method_name)
        
        # Call the method with the extracted parameters
        response = method_to_call(**request_dict)

        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
