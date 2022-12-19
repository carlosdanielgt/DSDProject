import boto3
import pandas as pd
import botocore

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
    translation_string = "Key to success will be developing a sustainable partnership model for shared access, securing the rights for permanent access, storage, and delivery of information in digital format, and obtaining secure, ongoing funding."
    translation = get_translation_en_to_fr(translation_string)
    print(translation)
    translation_string = "Plusieurs intervenants ont exprimé l'avis que la condition sociale est un motif trop vague, qui n'est pas bien circonscrit, comme le sexe et la couleur."
    translation = get_translation_fr_to_en(translation_string)
    print(translation)
