import boto3
import os
import decimal
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ["TABLE"])

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
    print(main({}, {}))