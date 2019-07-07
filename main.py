from handle_event import *
from send_events_and_errors import *
from send_logs import *


def main(req):
    print('GCP cloud bot function processed a request.')
    try:
        source_message = req.get_json()
    except Exception as e:
        print('Bad request.')
        return f'GCP cloud bot had an error'

    start_time = time.time()
    print(f'{__file__} - source message : {source_message}')
    output_message = {}
    if source_message:
        print(f'source message : {source_message}')
        output_message['ReportTime'] = source_message.get('reportTime', 'N.A')
        output_message['Account id'] = source_message['account'].get('id', 'N.A')
        output_message['Finding key'] = source_message.get('findingKey', 'N.A')
        try:
            export_results = handle_event(source_message, output_message)
        except Exception as e:
            export_results = True
            print(f'{__file__} - Handle event failed')
            output_message['Handle event failed'] = str(e)
        if export_results:
            if os.getenv('OUTPUT_EMAIL'):
                sendEvent(output_message)
        else:
            print(f'''{__file__} - Output didn't sent : {output_message}''')
        is_send_logs = os.getenv('SEND_LOGS', False)
        print(f'{__file__} - SEND_LOGS set to {str(is_send_logs)}')
        if is_send_logs:
            send_logs(output_message, start_time, source_message.get('account').get('vendor'))
    if output_message:
        return f'{output_message}'

    else:
        return f'GCP cloud bot had an error - {output_message}'
