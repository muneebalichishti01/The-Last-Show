import boto3
import requests
import json
client = boto3.client('ssm')

def handler(event, context):
    response = client.get_parameter(
        Name='gpt_4',
        WithDecryption=True,
    )

    identifier = event['id']
    name = event['name']
    born = event['year_born']
    died = event['year_died']
    api_key = response['Parameter']['Value']

    gpt_entry = f"write an obituary about a fictional character named {name} who was born on {born} and died on {died}."
    model_engine = "text-curie-001"

    head = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": model_engine,
        "prompt": gpt_entry,
        "max_tokens": 600,
        "temperature": 0.5
    }

    try:
        response = requests.post(
            "https://api.openai.com/v1/completions", headers=head, data=json.dumps(data))
        obit = response.json()['choices'][0]['text']
    except:
        obit = "ChatGPT error"

    resp = {
        "output": obit,
        "name": name,
        "year_born": born,
        "year_died": died,
        "id": identifier
    }

    return json.dumps(resp)
