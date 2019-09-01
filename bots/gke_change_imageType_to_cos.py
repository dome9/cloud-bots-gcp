from typing import Dict, List

from google.cloud import container_v1

COS_IMAGE_TYPE = 'COS'


def run_action(project_id: str, rule: str, entity: Dict, params: List) -> str:
    print(f'{__file__} - run_action started')
    zone = entity['region']
    name = entity['name']
    print(f'{__file__} - project_id : {project_id} - zone : {zone} kubernetes name : {name}')
    gke_client = container_v1.ClusterManagerClient()
    node_pools = entity.get('nodePools', [])

    for node_pool in node_pools:
        if node_pool.get('config', {}).get('imageType') != COS_IMAGE_TYPE:
            node_pool_id = node_pool['name']
            print(f'{__file__} - node pool name to change: - {node_pool_id}')
            response = gke_client.update_node_pool(project_id, zone, name, node_pool_id, node_pool['version'], COS_IMAGE_TYPE)
            print(f'{__file__} - response -{response}')

    return 'All node pools image type changed to COS successfully'
