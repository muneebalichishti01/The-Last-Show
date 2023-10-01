import boto3
import json

dynamodb_resouce = boto3.resource('dynamodb')
table = dynamodb_resouce.Table('the-last-show-30142452')

def handler(event, context):

    store_content = event['store']
    generate_content = json.loads(event['generate'])

    aud_url = store_content['audio_url']
    pic_url = store_content['picture_url']
    born = generate_content['year_born']
    died = generate_content['year_died']
    identifier = generate_content['id']
    obit = generate_content['output']
    name = generate_content['name']

    body = {
        "id": identifier,
        "name": name,
        "year_born": born,
        "year_died": died,
        "obituary": obit,
        "audio_url": aud_url,
        "picture_url": pic_url
    }

    try:
        table.put_item(Item=body)
        return {
            "isBase64Encoded": "false",
            'statusCode': 200,
            'body': json.dumps(body)
        }
    
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
