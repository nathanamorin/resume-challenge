import boto3
import os
import decimal

if __name__ != "__main__":
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ["TABLE"])
else:
    dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:4566')

def main(event, context):
    try:
        re = table.update_item(                                                   
                    Key={
                        'id': "resume_site_count"
                    },
                    UpdateExpression="SET user_count = if_not_exists(user_count, :zero) + :val",
                    ExpressionAttributeValues={
                        ':val': decimal.Decimal(1),
                        ':zero': decimal.Decimal(0)
                    },
                    ReturnValues="UPDATED_NEW"
                )
        return str(re["Attributes"]["user_count"])
    except Exception as ex:
        print(ex)
        return 10^1000

if __name__ == "__main__":
    import uuid
    table_name = str(uuid.uuid4())
    table = dynamodb.Table(table_name)
    dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    # Manual test of api call given unit teseting is not possible without mocking the AWS API
    assert main({}, {}) == "1"

    for i in range(10):
        main({}, {})

    assert main({}, {}) == "12"