import cryptography
import json
import requests
import logging
import os
from dotenv import load_dotenv
from intersight_auth import IntersightAuth
from datetime import datetime, timedelta

def lambda_handler(event, context):
    load_dotenv()
        
    #Get Alarms Created Within the last X days/minutes/weeks of right now
    alarmdelta = datetime.utcnow() - timedelta(minutes=15)

    # Create an Intersight AUTH object using the API key and Secret Key from Intersight
    AUTH = IntersightAuth(
        secret_key_filename='SecretKey.txt',
        api_key_id=os.getenv('INTERSIGHT_API_KEY')
        )

    # Intersight REST API Base URL
    BURL = 'https://www.intersight.com/api/v1/'

    alarms_json_body = {
        "request_method": "GET",
        "resource_path": (
                'https://www.intersight.com/api/v1/cond/Alarms?' +
                '$filter=not(Severity eq %27Cleared%27) and (CreationTime gt ' + str(alarmdelta.strftime("%Y-%m-%dT%H:%M:%SZ")) + ')'
        )
    }

    RESPONSE = requests.request(
        method=alarms_json_body['request_method'],
        url=alarms_json_body['resource_path'],
        auth=AUTH
    )

    alarms = RESPONSE.json()["Results"]

    for r in alarms:        
        post_message(r["CreationTime"] + "\n" + r["Severity"] + "\n" + r["AffectedMoDisplayName"] + "\n" + r["Description"])
      
    return 1

def post_message(content):
    #Post a message to a specific room using Webex BOT API auth token and ROOM id
    
    WEBEX_ROOM = os.getenv('WEBEX_ROOM')
    WEBEX_TOKEN = os.getenv('WEBEX_TOKEN')

    url = "https://api.ciscospark.com/v1/messages"
    headers = {
        "Authorization": WEBEX_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {
       "roomId": WEBEX_ROOM,
        "text": content
    }

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)