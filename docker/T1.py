import pandas as pd
import requests
import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
table = dynamodb.Table('translations')

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
        finalResult = [str(response.json()['translation'])]
    return str(finalResult)
