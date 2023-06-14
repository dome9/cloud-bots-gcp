# Permissions: compute.firewalls.delete, compute.networks.updatePolicy

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import logging
import bots_utils


def run_action(project_id, rule, entity, params):
    logging.info(f'{__file__} - run_action started')
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)
    firewall = entity.get('name')
    logging.info(f'{__file__} - project_id : {project_id} - firewall : {firewall}')

    output_msg = ''

    try:
        logging.info(f'{__file__} - deleting firewall rule: {firewall}')
        request = service.firewalls().delete(project=project_id, firewall=firewall)
        response = request.execute()
        if bots_utils.UtilsConstants.ERROR in response:  # on failure
            msg = f'Failed deleting firewall rule: {firewall} - {response[bots_utils.UtilsConstants.ERROR]}'
            logging.error(f'{__file__} - {msg}')
            raise Exception(msg)
        else:  # on success
            msg = f'firewall rule: {firewall} was successfully deleted'
            logging.info(f'{__file__} - {msg}')
            output_msg += msg
    except Exception as e:
        msg = f'Unexpected error occurred - {e}'
        logging.error(f'{__file__} - {msg}')
        raise e

    return output_msg

