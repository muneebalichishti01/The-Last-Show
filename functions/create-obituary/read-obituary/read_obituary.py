import boto3
import json


def handler(event, context):

    s3_client = boto3.client('s3')
    polly_client = boto3.client('polly')

    event_json = json.loads(event)
    gpt = event_json['output']

    response = polly_client.synthesize_speech(
        Text=gpt, OutputFormat='mp3', VoiceId='Ivy')

    namefile = "voice.mp3"
    bucket = "s3-thelastshowproj"
    aud = response['AudioStream'].read()

    s3_client.put_object(Bucket=bucket, Key=namefile, Body=aud)
