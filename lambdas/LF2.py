import json
import boto3
import os
from botocore.vendored import requests

def send_sms(number, message):
    sns = boto3.client(
        'sns',
        aws_access_key_id=os.environ.get('AWS_SERVER_PUBLIC_KEY'),
        aws_secret_access_key=os.environ.get('AWS_SERVER_SECRET_KEY')
    )

    smsattrs = {
        'AWS.SNS.SMS.SenderID': {
            'DataType': 'String',
            'StringValue': 'TestSender'
        },
        'AWS.SNS.SMS.SMSType': {
            'DataType': 'String',
            'StringValue': 'Transactional'
        }
    }

    response = sns.publish(
        PhoneNumber=number,
        Message=message,
        MessageAttributes=smsattrs
    )

    print(response)


def search(cuisine):
    requestBody = {}
    requestBody['size'] = SAMPLE_N
    requestBody['query'] = {}
    requestBody['query']['match_phrase'] = {}
    requestBody['query']['match_phrase']['categories.title'] = cuisine
    headers = {'Content-type': 'application/json'}
    r = requests.get(url=SEARCH_URL, data=json.dumps(requestBody), headers=headers)
    data = r.json()
    return data['hits']['hits']


def get_restaurant_data(ids):
    print(ids)
    dynamodb = boto3.resource('dynamodb')
    payload = {}
    payload[TABLE_NAME] = {
        "Keys": [{'id': i} for i in ids]
    }
    response = dynamodb.batch_get_item(
        RequestItems=payload
    )
    
    print('--------------------', response)
    res_data = response['Responses'][TABLE_NAME]
    ans = ''
    for i in range(0, len(res_data)):
        ans += "{}. {}, located at {}\n".format(i + 1, res_data[i]['name'],
                                                ' '.join(res_data[i]['location']['display_address']))
    return ans



def lambda_handler(event, context):
    print(event)
    cuisine = event.Records[0].
    search(event.messageAt)
    return {}
