import boto3
import pandas as pd
import botocore

dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id='AKIAZYES2ALXHKRO7S3M',
                          aws_secret_access_key='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',
                          region_name='us-east-2'
                          )
table = dynamodb.Table('translations')

def populate_data():
    chunksize = 10000
    with pd.read_csv('./en-fr.csv', chunksize=chunksize) as reader:
        for chunk in reader:
            items_to_add = []
            for i in range(len(chunk)):
                items_to_add.append(
                    {"en": chunk.iloc[i, 0], "fr": chunk.iloc[i, 1]})

            # print(items_to_add)

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
    populate_data()
