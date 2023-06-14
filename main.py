import time
from handle_event import *
from send_events_and_errors import *
from send_logs import *
from send_logs_api_gateway import *
from authenticate import authenticate
import logging

logging.basicConfig(level=logging.INFO)  # Set logging level to INFO

logger = logging.getLogger(__name__)

def main(req):
    logger.info('GCP cloud bot function processed a request.')
    source_message = req

    start_time = time.time()
    logger.info(f'{__file__} - source message : {source_message}')
    output_message = {}
    if source_message:
        logger.info(f'source message : {source_message}')
        output_message['ReportTime'] = source_message.get('reportTime', 'N.A')
        output_message['Account id'] = source_message['account'].get('id', 'N.A')
        output_message['findingKey'] = source_message.get('findingKey', 'N.A')
        output_message['logsHttpEndpoint'] = source_message.get('logsHttpEndpoint')
        output_message['logsHttpEndpointKey'] = source_message.get('logsHttpEndpointKey')
        output_message['logsHttpEndpointStreamName'] = source_message.get('logsHttpEndpointStreamName')
        output_message['logsHttpEndpointStreamPartitionKey'] = source_message.get('logsHttpEndpointStreamPartitionKey')
        output_message['dome9AccountId'] = source_message.get('dome9AccountId')
        output_message['executionId'] = source_message.get('executionId')
        output_message['vendor'] = source_message['account'].get('vendor')
        try:
            export_results = handle_event(source_message, output_message)
        except Exception as e:
            export_results = True
            logger.exception(f'{__file__} - Handle event failed: {str(e)}')
            output_message['Handle event failed'] = str(e)
        if export_results:
            if os.getenv('OUTPUT_EMAIL'):
                sendEvent(output_message)
        else:
            logger.info(f'{__file__} - Output was not sent: {output_message}')
        is_send_logs = os.getenv('SEND_LOGS', False)
        logger.info(f'{__file__} - SEND_LOGS set to {str(is_send_logs)}')
        send_logs_api_gateway(output_message)
        if is_send_logs:
            send_logs(output_message, start_time, source_message.get('account').get('vendor'))
    if output_message:
        return f'{output_message}'

    else:
        return f'GCP cloud bot had an error - {output_message}'


# Apply the authentication decorator to the main function
main = authenticate(main)
