import json
import boto3
import os
from botocore.vendored import requests

TABLE_NAME='yelp-restaurants'
SAMPLE_N='5'
SEARCH_URL='https://search-chat-concierge-cloud-anq6myrjo7reh4vgcawtoq3v6u.us-east-1.es.amazonaws.com'


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
    requestBody['query']['match_phrase']['cuisine.title'] = cuisine
    headers = {'Content-type': 'application/json'}
    r = requests.get(url=SEARCH_URL, data=json.dumps(requestBody), headers=headers)
    data = r.json()
    print('##############', data)
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
                                                ' '.join(res_data[i]['address']))
    return ans



def lambda_handler(event, context):
    print(event)
    slotDetails = event['Records'][0]['messageAttributes'];
    slots = {
        'Cuisine': slotDetails['Cuisine']['stringValue'],
        'Phone': slotDetails['Phone']['stringValue'],
        'Time': slotDetails['Time']['stringValue'],
        'Location': slotDetails['Location']['stringValue'],
        'Number': slotDetails['Number']['stringValue']
    }
    print(slots)
    ids = search(slots['Cuisine'])
    print(ids)
    message = get_restaurant_data(ids)
    print(message)
    send_sms(number, message)
    return {}
