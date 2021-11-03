# What it does: Enables flow logs in a given subnetwork
# Bot will enable flow logs
# Usage: AUTO: flow_logs_enable
# Example: Subnet where <condition> should have enableFlowLogs=true
# AUTO: flow_logs_enable
# Permissions: compute.subnetworks.get, compute.subnetworks.update
# Limitations: None

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import logging
import bots_utils


def run_action(project_id, rule, entity, params):
    logging.info(f'{__file__} - run_action started')
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)
    region = entity.get('region')
    fingerprint = entity.get('fingerPrint')
    subnetwork = entity.get('name')

    logging.info(f'{__file__} - project_id : {project_id} - region : {region} - subnetwork : {subnetwork} - fingerprint : {fingerprint}')

    subnetwork_body = {
        "enableFlowLogs": "true",
        "fingerprint": fingerprint
        }

    output_msg = ''

    try:
        logging.info(f'{__file__} - enabling flow logs on: {subnetwork}')
        request = service.subnetworks().patch(project=project_id, region=region, subnetwork=subnetwork, body=subnetwork_body)
        response = request.execute()
        if bots_utils.UtilsConstants.ERROR in response:  # on failure
            msg = f'Failed enabling flow logs on: {subnetwork}: {response[bots_utils.UtilsConstants.ERROR]}'
            logging.error(f'{__file__} - {msg}')
            output_msg += msg
        else:  # on success
            msg = f'flow logs successfully enabled on: {subnetwork}'
            logging.info(f'{__file__} - {msg}')
            output_msg += msg
    except Exception as e:
        msg = f'Unexpected error occurred - {e}'
        logging.error(f'{__file__} - {msg}')
        output_msg += msg

    return output_msg
