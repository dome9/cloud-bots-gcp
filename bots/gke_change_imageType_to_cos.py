from google.cloud import container_v1
from oauth2client.client import GoogleCredentials

import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/ravid/Raviddeebcccba08f.json"

COS_IMAGE_TYPE = 'COS'


def run_action(project_id, rule, entity, params):
    print(f'{__file__} - run_action started')
    zone = entity['region']
    name = entity['name']
    print(f'{__file__} - project_id : {project_id} - zone : {zone} kubernetes name : {name}')
    credentials = GoogleCredentials.get_application_default()
    gke_client = container_v1.ClusterManagerClient(credentials=credentials)
    node_pools = entity.get('nodePools', [])
    try:
        for node_pool in node_pools:
            if node_pool.get('config', {}).get('imageType') != COS_IMAGE_TYPE:
                node_pool_id = node_pool.get('name')
                print(f'{__file__} - node pool name to change: - {node_pool_id}')
                gke_client.update_node_pool(project_id, zone, name, node_pool_id, node_pool.get('version'), 'COS')
        response = 'All node pools image type changed to COS successfully'
    except Exception as e:
        response = 'Error while changing imageType to COS'
    print(f'{__file__} - response -{response}')
    return f'{response}'
