from typing import Dict, List

from googleapiclient import discovery
COS_IMAGE_TYPE = 'COS'
from oauth2client.client import GoogleCredentials


def run_action(project_id: str, rule: str, entity: Dict, params: List) -> str:
    print(f'{__file__} - run_action started')
    zone = entity['region']
    name = entity['name']
    print(f'{__file__} - project_id : {project_id} - zone : {zone} kubernetes name : {name}')
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('container', 'v1', credentials=credentials)
    node_pools = entity.get('nodePools', [])

    for node_pool in node_pools:
        if node_pool.get('config', {}).get('imageType') != COS_IMAGE_TYPE:
            node_pool_id = node_pool['name']
            name = f'projects/{project_id}/locations/{zone}/clusters/{name}/nodePools/{node_pool_id}'
            update_node_pool_request_body = {
                "imageType": "COS"
            }
            print(f'{__file__} - node pool name to change: - {node_pool_id}')
            request = service.projects().locations().clusters().nodePools().update(name=name, body=update_node_pool_request_body)
            response = request.execute()

            print(f'{__file__} - response -{response}')

    return 'All node pools image type changed to COS successfully'


