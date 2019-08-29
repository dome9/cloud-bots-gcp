from typing import Dict, List

from google.cloud import container_v1
from oauth2client.client import GoogleCredentials

COS_IMAGE_TYPE = 'COS'


def run_action(project_id: str, rule: str, entity: Dict, params: List) -> str:
    print(f'{__file__} - run_action started')
    zone = entity['region']
    name = entity['name']
    print(f'{__file__} - project_id : {project_id} - zone : {zone} kubernetes name : {name}')
    credentials = GoogleCredentials.get_application_default()
    gke_client = container_v1.ClusterManagerClient(credentials=credentials)
    node_pools = entity.get('nodePools', [])

    for node_pool in node_pools:
        if node_pool.get('config', {}).get('imageType') != COS_IMAGE_TYPE:
            node_pool_id = node_pool['name']
            print(f'{__file__} - node pool name to change: - {node_pool_id}')
            response = gke_client.update_node_pool(project_id, zone, name, node_pool_id, node_pool['version'], COS_IMAGE_TYPE)
            print(f'{__file__} - response -{response}')

    return response
