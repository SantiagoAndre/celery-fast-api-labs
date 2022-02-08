import websocket
import time
import json
import os
import _thread as thread

import requests
from requests.auth import HTTPBasicAuth
import sys

def get_auth_token(username, password, client_id='', client_secret='', scope=''):
    # The URL for the auth endpoint
    url = 'http://localhost:8010/users/token/'

    # The payload with the grant type and user credentials
    payload = {
        'grant_type': 'password',  # This is usually the grant_type for username & password auth
        'username': username,
        'password': password,
        'scope': scope,
    }
    
    # If you need to authenticate with the client credentials, you can use HTTPBasicAuth
    auth = None
    if client_id and client_secret:
        auth = HTTPBasicAuth(client_id, client_secret)

    # The headers
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    # Making the POST request to the auth endpoint
    response = requests.post(url, data=payload, headers=headers, auth=auth)

    # Check if the request was successful
    if response.status_code == 200:
        # Return the JSON response which contains the access token
        return response.json()
    else:
        # In case of an error, print the response
        print(f"Failed to get token: {response.text}")
        return None



def on_message(ws, message):
    m = json.loads(message)
    print(f"\nroom {m['room']} -> {m['sender']['username']}:{m['message']}")

   

def on_error(ws, error):
    print('Error:', error)


def on_close(ws):
    print("### Connection Closed ###")


def on_open(ws):
    def run(*args):

        thread.start_new_thread(send_message, (ws,))

    thread.start_new_thread(run, ())


def send_message(ws):
    while True:
        room = input("Enter the room code: ").strip()
        message = input("Enter your message (type 'exit' to close): ")
        if message.strip().lower() == "exit":
            ws.close()
            break
        data_to_send = {
            "room": room,
            "message": message
            
        }
        ws.send(json.dumps(data_to_send))


if __name__ == "__main__":
    print('For running this script, ensure you have the following libraries:')
    print('websocket-client==0.58.0')
    print('asgiref==3.2.10')
    print('To execute this client run: "make websocket_client"')
    response = get_auth_token(sys.argv[1], sys.argv[2])
    if response is None:
        print("wrong user or password")
        exit(0)
    token = response['access_token']


    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(f"ws://localhost:8010/chatrooms/ws?token={token}",
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
    ws.run_forever()
