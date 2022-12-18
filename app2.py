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
        
def populate_data():
    chunksize = 10000
    with pd.read_csv('./en-fr.csv', chunksize=chunksize) as reader:
        for chunk in reader:
            items_to_add = []
            for i in range(len(chunk)):
                items_to_add.append({"en": chunk.iloc[i, 0], "fr": chunk.iloc[i, 1]})

            # write the chunk to db 
            with table.batch_writer() as batch:
                for item in items_to_add:
                    try:
                        response = batch.put_item(Item={
                            "en": item["en"],
                            "fr": item["fr"]
                        })
                    except botocore.exceptions.ClientError as error:
                        pass
                    except TypeError as error:
                        pass

if __name__ == "__main__":
    translation = get_translation_en_to_fr("Market Summary Packaged food sales have been increasing since inflation started to decline in recent years.")
    print(translation)
    # translation = get_translation_fr_to_en("heys")
    # print(translation)
