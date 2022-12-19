import boto3
import pandas as pd
import botocore

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
   
def get_translation_fr_to_en(string):
    response = table.query(
        IndexName= 'french',
        KeyConditionExpression= 'fr = :val', 
        ExpressionAttributeValues= {
            ':val' : string        
        }
    )
    items = response['Items']
    if len(items) > 0:
        item = items[0]
        eng = item['en']
        return eng

if __name__ == "__main__":
    translation_string = "AAFC Science and Innovation:"
    translation = get_translation_en_to_fr(translation_string)
    print(translation)
    # translation = get_translation_fr_to_en("heys")
    # print(translation)
