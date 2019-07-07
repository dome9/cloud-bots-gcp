import os
import json
from sendgrid import SendGridAPIClient


def sendEvent(output_message):
    print(f'{__file__} - send event output_message : {output_message}')
    with open('email_message.json') as const_message_file:
        message = const_message_file.read()
        message = json.loads(message)
        try:
            message.get('personalizations',[{}])[0].get('to')[0]['email'] = os.getenv('OUTPUT_EMAIL')
            message.get('content',[{}])[0]['value'] = json.dumps(output_message)
        except Exception as e:
            print(f'{__file__} - send event failed to parse message, error: : {e}')

    try:
        sg = SendGridAPIClient(os.getenv('SEND_GRID_API_CLIENT'))
        response = sg.send(message)
        print(f'{__file__} - send event respone status : {response.status_code}')

    except Exception as e:
        print(f'{__file__} - send event failed, error: : {e}')
