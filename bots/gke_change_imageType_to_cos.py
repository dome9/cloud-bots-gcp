# Permissions: container.clusters.update, gkemulticloud.awsNodePools.update

from typing import Dict, List
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import logging
import bots_utils

COS_IMAGE_TYPE = 'COS'
update_node_pool_request_body = {
    "imageType": COS_IMAGE_TYPE
}


def run_action(project_id: str, rule: str, entity: Dict, params: List) -> str:
    logging.info(f'{__file__} - run_action started')
    zone = entity['region']
    name = entity['name']
    logging.info(f'{__file__} - project_id : {project_id} - zone : {zone} kubernetes name : {name}')
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('container', 'v1', credentials=credentials)
    node_pools = entity.get('nodePools', [])

    output_msg = ''

    for node_pool in node_pools:
        if node_pool.get('config', {}).get('imageType') != COS_IMAGE_TYPE:
            node_pool_id = node_pool['name']
            gke_name = '/'.join(['projects', project_id, 'locations', zone, 'clusters', name, 'nodePools', node_pool_id])
            logging.info(f'{__file__} - node pool name to change: - {node_pool_id}')

            try:
                logging.info(f'{__file__} - updating imageType of node pool: {node_pool_id}')
                request = service.projects().locations().clusters().nodePools().update(name=gke_name,
                                                                                       body=update_node_pool_request_body)
                response = request.execute()
                if bots_utils.UtilsConstants.ERROR in response:  # on failure
                    error_msg = f'failed to update imageType of node pool: {node_pool_id}'
                    logging.error(f'{__file__} - {error_msg}')
                    output_msg += error_msg
                else: # on success
                    msg = f'successfully updated imageType of node pool: {node_pool_id}'
                    logging.info(f'{__file__} - {msg}')
                    output_msg += f'\n{msg}'
            except Exception as e:
                msg = f'Unexpected error occurred while working on node pool: {node_pool_id} - {e}'
                logging.error(f'{__file__} - {msg}')
                output_msg += f'\n{msg}'

    return output_msg
