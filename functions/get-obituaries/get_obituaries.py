import boto3
import json

dynamodb_resource = boto3.resource("dynamodb")
table = dynamodb_resource.Table("the-last-show-30142452")

def handler(event, context):

    try:
        table_resp = table.scan()

        if table_resp["Count"] == 0:
            resp = {
                "statusCode": 200, "body": json.dumps({"message": "empty table", "data": []})
            }
            return resp

        resp = {
            "statusCode": 200,
            "body": json.dumps({"message": "items in table", "data": table_resp['Items']})
        }
        return resp

    except Exception as e:
        resp = {
            "statusCode": 404,
            "body": json.dumps({"message": str(e)})
        }
        return resp
