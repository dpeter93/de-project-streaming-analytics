import requests
from dotenv import load_dotenv
import os
import json
from urllib.parse import urlencode

load_dotenv()

# OAuth authorization for my application in the CRM system
client_id = f'{os.getenv("client_id")}'
client_secret = f'{os.getenv("client_secret")}'
scope = 'read write'
authorization_url = 'https://api.capsulecrm.com/oauth/authorise'
token_url = 'https://api.capsulecrm.com/oauth/token'

auth_params = {
    'response_type': 'code',
    'client_id': client_id,
    'scope': scope
}

auth_url = authorization_url + '?' + urlencode(auth_params)

print(f"Visit the following URL in your browser to authorize the application:\n{auth_url}")

authorization_code = input("Enter the authorization code from the callback URL: ")

token_params = {
    'code': authorization_code,
    'client_id': client_id,
    'client_secret': client_secret,
    'grant_type': 'authorization_code'
}

token_response = requests.post(token_url, data=token_params)
token_data = token_response.json()

access_token = token_data.get('access_token')

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}

events = ["opportunity/created", "opportunity/updated", "opportunity/deleted", "opportunity/closed"]

# Post Rest hooks for the events list
def post_resthook():
    capsule_api_endpoint = 'https://api.capsulecrm.com/api/v2/resthooks'
    for event in events:
        data = {
            "restHook": {
                "targetUrl": f"https://apt-doberman-7724-eu2-rest-kafka.upstash.io/webhook?topic=events&user={os.getenv('sasl_plain_username')}&pass={os.getenv('sasl_plain_password')}",
                "event": event
            }
        }

        json_data = json.dumps(data)

        try:
            response = requests.post(capsule_api_endpoint, data=json_data, headers=headers)
            response.raise_for_status()
            print("Webhook request successful")
        except requests.exceptions.RequestException as e:
            print(f"Error making webhook request: {e}")


# Delete Rest hooks for given rest hook ID
def delete_resthook():
    resthook_id = input('ResthookID: ')
    capsule_api_endpoint = f'https://api.capsulecrm.com/api/v2/resthooks/{resthook_id}'
    try:
        response = requests.delete(capsule_api_endpoint, headers=headers)
        response.raise_for_status()
        print("Webhook delete successful")
    except requests.exceptions.RequestException as e:
        print(f"Error making webhook request: {e}")

if __name__ == '__main__':
    post_resthook()