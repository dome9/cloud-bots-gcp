import os
import json
from sendgrid import SendGridAPIClient


def sendEvent(output_message):
    print(f'{__file__} - send event output_message : {output_message}')
    message = {
        'personalizations': [
            {
                'to': [
                    {
                        'email': os.getenv('OUTPUT_EMAIL')
                    }
                ],
                'subject': 'GCP Remediation Output'
            }
        ],
        'from': {
            'email': 'GCP@cloudBots.com'
        },
        'content': [
            {
                'type': 'text/plain',
                'value': json.dumps(output_message)
            }
        ]
    }

    try:
        sg = SendGridAPIClient(os.getenv('SEND_GRID_API_CLIENT'))
        response = sg.send(message)
        print(f'{__file__} - send event respone status : {response.status_code}')

    except Exception as e:
        print(f'{__file__} - send event failed, error: : {e}')
