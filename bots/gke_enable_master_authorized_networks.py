# What it does: Enables 'master authorized networks' on a gke cluster
# Usage: gke_enable_master_authorized_networks <cidr_blocks>
#        cidr_blocks is an optional parameter (leave empty if needed)
#        cidr_block has two properties - name and cidr range.
#        Each cidr_block should be passed this way: <name>-<cidr_range>
#        User can pass multiple cidr_blocks by separating them with a comma (see example)
# Examples:  gke_enable_master_authorized_networks
#           gke_enable_master_authorized_networks net1-10.0.0.0/24,net2-192.168.0.0/16
# Limitations: None
# Example GSL: GkeCluster should have masterAuthorizedNetworksConfig.enabled=true
# Associated Rule: D9.GCP.NET.10
# Permissions: container.clusters.update

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import logging
import bots_utils

CIDR_BLOCKS_SEPARATOR = ","
CIDR_BLOCK_PROPERTIES_SEPARATOR = "-"


def run_action(project_id, rule, entity, params):
    logging.info(f'{__file__} - run_action started')
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('container', 'v1', credentials=credentials)

    cluster_name, region = get_properties_from_entity(entity)
    output_msg = ''

    logging.info(f'{__file__} - Enabling master authorized networks on cluster \'{cluster_name}\'')

    try:
        enable_master_authorized_networks(service, project_id, region, cluster_name, params)
    except Exception as e:  # on failure
        msg = f'Failed to enable \'master authorized networks\' for cluster \'{cluster_name}\': ' \
              f'{e}'
        logging.error(f'{__file__} - {msg}')
        raise Exception(msg)

    msg = f'Successfully enabled \'master authorized networks\' for cluster \'{cluster_name}\''
    logging.info(f'{__file__} - {msg}')
    output_msg += msg

    return output_msg


def enable_master_authorized_networks(service, project_id, region, cluster_name, params):
    cidr_blocks = get_cidr_blocks(params)
    update_cluster_parameters = {"desiredMasterAuthorizedNetworksConfig": {}}
    update_cluster_parameters["desiredMasterAuthorizedNetworksConfig"]["enabled"] = True
    update_cluster_parameters["desiredMasterAuthorizedNetworksConfig"]["cidrBlocks"] = cidr_blocks
    update_cluster_request_body = {
        "update": update_cluster_parameters
    }

    cluster_path = f'projects/{project_id}/locations/{region}/clusters/{cluster_name}'
    request = service.projects().locations().clusters().update(name=cluster_path, body=update_cluster_request_body)
    request.execute()


def get_properties_from_entity(entity):
    try:
        cluster_name = entity['name']
        region = entity['region']
    except KeyError as e:
        raise KeyError(f"Missing property from entity: {e}")
    return cluster_name, region


def get_cidr_blocks(params):
    if len(params) > 1:
        raise Exception("Too many parameters! "
                        "Expected: gke_enable_master_authorized_networks <cidr_blocks>, "
                        "where each cidr_block: <name>-<cidr_range>. "
                        "Example: gke_enable_master_authorized_networks net1-10.0.0.0/24,net2-192.168.0.0/16")
    if len(params) == 0:
        return []
    try:
        cidr_blocks = []
        cidr_blocks_strings = params[0].split(CIDR_BLOCKS_SEPARATOR)
        for cidr_block_string in cidr_blocks_strings:
            cidr_block_properties = cidr_block_string.split(CIDR_BLOCK_PROPERTIES_SEPARATOR)
            cidr_blocks.append({
                "displayName": cidr_block_properties[0],
                "cidrBlock": cidr_block_properties[1]
            })
        return cidr_blocks
    except Exception as e:
        raise Exception(f"Failed to extract cidr_blocks from parameters. Error message - {e}"
                        "Expected: gke_enable_master_authorized_networks <cidr_blocks>, "
                        "where each cidr_block: <name>-<cidr_range>. "
                        "Example: gke_enable_master_authorized_networks net1-10.0.0.0/24,net2-192.168.0.0/16")
