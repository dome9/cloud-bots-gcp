import os
import json
from sendgrid import SendGridAPIClient
from flatten_dict import flatten, unflatten


def sendEvent(output_message):
    print(f'{__file__} - send event output_message : {output_message}')
    with open('email_message.json') as const_message_file:
        message = json.load(const_message_file)
        try:
            message = flatten(message)
            list(list(message.values())[0][0].values())[0][0]['email'] = os.getenv('OUTPUT_EMAIL')
            list(message.values())[2][0]['value'] = json.dumps(output_message)
            message = unflatten(message)
        except Exception as e:
            print(f'{__file__} - send event failed to parse message, error: : {e}')

    try:
        sg = SendGridAPIClient(os.getenv('SEND_GRID_API_CLIENT'))
        response = sg.send(message)
        print(f'{__file__} - send event respone status : {response.status_code}')

    except Exception as e:
        print(f'{__file__} - send event failed, error: : {e}')

