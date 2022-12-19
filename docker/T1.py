import pandas as pd
import requests
import boto3

dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id='AKIAZYES2ALXHKRO7S3M',
                          aws_secret_access_key='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',
                          region_name='us-east-2'
                          )
table = dynamodb.Table('translations2')

def get_translation_en_to_fr(string):
    response = table.get_item(
        Key={
            'en': string
        }
    )
    if "Item" in response:
        item = response['Item']
        french = item['fr']
        return french
    else:
        return ''

def executeMpi(data):
    finalResult = get_translation_en_to_fr(data['sentence'])
    if finalResult=='':
        
        url = "https://deep-translator-api.azurewebsites.net/google/"

        querystring = {"source": "english",
        "target": "french",
        "text": data['sentence'],
        "proxies": []}
        
        response = requests.request("POST", url,  json=querystring)
        finalResult = response.json()['translation']
        # print("from api")
    return str(finalResult)
