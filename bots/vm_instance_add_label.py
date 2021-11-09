# Permissions: compute.instances.get, compute.instances.setLabels

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import logging
import bots_utils


def run_action(project_id, rule, entity, params):
    logging.info(f'{__file__} - run_action started')
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)
    zone = entity.get('zone')
    instance = entity.get('name')
    logging.info(f'{__file__} - project_id : {project_id} - zone : {zone} instance : {instance}')

    try:
        tag_key, tag_value = params
    except ValueError:
        error_msg = 'One or more params are missing'
        logging.error(f'{__file__} - {error_msg}')
        return error_msg

    # get instance labels and label fingerprint
    try:
        logging.info(f'{__file__} - getting instance labels and label fingerprint')
        request = service.instances().get(project=project_id, zone=zone, instance=instance)
        response = request.execute()

        if bots_utils.UtilsConstants.ERROR in response:  # on failure
            error_msg = f'failed to get instance labels and label fingerprint - ' \
                        f'{response[bots_utils.UtilsConstants.ERROR]}'
            logging.error(f'{__file__} - {error_msg}')
            return error_msg

        # on success
        labels = response.get('labels',{})
        labels[tag_key] = tag_value
        print(f'{__file__} - labels : {labels}')
        label_fingerprint = response.get('labelFingerprint')

    except Exception as e:
        error_msg = f'Unexpected error - {e}'
        logging.error(f'{__file__} - {error_msg}')
        return error_msg

    output_msg = ''

    # add the new label
    try:
        instances_set_labels_request_body = {
            'labels': labels,
            'labelFingerprint': label_fingerprint
        }
        logging.info(f'{__file__} - adding the new label')
        request = service.instances().setLabels(project=project_id, zone=zone, instance=instance,
                                                body=instances_set_labels_request_body)
        response = request.execute()
        if bots_utils.UtilsConstants.ERROR in response:  # on failure
            error_msg = f'failed to set instance labels - {response[bots_utils.UtilsConstants.ERROR]}'
            logging.error(f'{__file__} - {error_msg}')
            output_msg += error_msg
        else:  # on success
            msg = f'added label to instance: {instance}'
            logging.info(f'{__file__} - {msg}')
            output_msg += msg
    except Exception as e:
        error_msg = f'Unexpected error - {e}'
        logging.error(f'{__file__} - {error_msg}')
        output_msg += error_msg

    return output_msg
