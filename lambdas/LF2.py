import json
import boto3
import os
from botocore.vendored import requests
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

TABLE_NAME = 'yelp-db'
SAMPLE_N = '5'
SEARCH_URL = 'https://search-chat-concierge-cloud-nyu-2xycurqltvlkdpsdtsbhu5uouy.us-east-1.es.amazonaws.com'

awsauth = AWS4Auth("", "", 'us-east-1', 'es',
                   os.getenv('AWS_SESSION_TOKEN'))

es = Elasticsearch(SEARCH_URL, http_auth=awsauth, connection_class=RequestsHttpConnection)


def send_sms(number, message):
    sns = boto3.client(
        'sns',
        aws_access_key_id=os.getenv('AWS_SERVER_PUBLIC_KEY'),
        aws_secret_access_key=os.getenv('AWS_SERVER_SECRET_KEY')
    )

    smsattrs = {
        'AWS.SNS.SMS.SenderID': {
            'DataType': 'String',
            'StringValue': 'TestSender'
        },
        'AWS.SNS.SMS.SMSType': {
            'DataType': 'String',
            'StringValue': 'Promotional'  # change to Transactional from Promotional for dev
        }
    }

    response = sns.publish(
        PhoneNumber=number,
        Message=message,
        MessageAttributes=smsattrs
    )
    print(number)
    print(response)
    print("The message is: ", message)


def search(cuisine):
    requestBody = {}
    requestBody['size'] = SAMPLE_N
    requestBody['query'] = {}
    requestBody['query']['bool'] = {}
    requestBody['query']['bool']['must'] = list([{
        'match': {
            'cuisine.title': cuisine
        }
    }])
    data = es.search(index="restaurants", body=requestBody)
    return data['hits']['hits']


def get_restaurant_data(ids):
    dynamodb = boto3.resource('dynamodb')
    payload = {}
    payload[TABLE_NAME] = {
        "Keys": [{'id': i} for i in ids]
    }
    response = dynamodb.batch_get_item(
        RequestItems=payload
    )

    res_data = response['Responses'][TABLE_NAME]
    ans = 'Hi! Here are your suggestions,\n '
    for i in range(0, len(res_data)):
        ans += "{}. {}, located at {}\n".format(i + 1, res_data[i]['name'], res_data[i]['address'])
    return ans


def lambda_handler(event, context):
    slotDetails = event['Records'][0]['messageAttributes'];
    slots = {
        'Cuisine': slotDetails['Cuisine']['stringValue'],
        'Phone': slotDetails['Phone']['stringValue'],
        'Time': slotDetails['Time']['stringValue'],
        'Location': slotDetails['Location']['stringValue'],
        'Number': slotDetails['Number']['stringValue']
    }
    ids = search(slots['Cuisine'])
    ids = list(map(lambda x: x['_id'], ids))
    message = get_restaurant_data(ids)
    send_sms("+1"+slots['Phone'], message)
    return {}
