import time
import boto3
import json
import base64
from requests_toolbelt.multipart import decoder

def handler(event, context):
    client = boto3.client('stepfunctions')
    s3_client = boto3.client('s3')

    state_machine_arn = 'arn:aws:states:ca-central-1:356847865132:stateMachine:obituary_state_machine'

    name = event['queryStringParameters']['name']
    identifier = event['headers']['id']
    died = event['queryStringParameters']['year_died']
    born = event['queryStringParameters']['year_born']
    body = event['body']

    if event['isBase64Encoded']:
        body = base64.b64decode(body)

    content_type = event['headers']['content-type']
    data = decoder.MultipartDecoder(body, content_type)

    input = {
        "input": {
            "name": name,
            "year_born": born,
            "year_died": died,
            "id": identifier
        }
    }
    inp = json.dumps(input)
    response = client.start_execution(
        stateMachineArn=state_machine_arn,
        input=inp
    )

    bucket = "s3-thelastshowproj"
    namefile = "picture.jpg"
    picture_s3 = data.parts[0].content

    execution = response['executionArn']
    s3_client.put_object(Bucket=bucket, Key=namefile, Body=picture_s3)

    while True:
        exec_res = client.describe_execution(executionArn=execution)
        stat = exec_res['status']

        if stat == 'FAILED':
            print("State machine execution failed")
            break

        elif stat == 'SUCCEEDED':
            output = json.loads(exec_res['output'])
            res = output['body']
            break

        else:
            time.sleep(1)

    return {
        "statusCode": 200, "body": json.dumps(res)
    }
