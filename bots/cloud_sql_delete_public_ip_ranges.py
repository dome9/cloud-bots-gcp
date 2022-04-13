"""
What it does: Deletes public IP ranges (0.0.0.0/0) from Cloud SQL authorized networks
Usage: cloud_sql_delete_public_ip_ranges
Example: cloud_sql_delete_public_ip_ranges
Limitations: None
Example GSL: CloudSql where ipAddresses contain [ ipAddress isPublic() ] and
             settings.ipConfiguration.ipv4Enabled=true should not have
             settings.ipConfiguration.authorizedNetworks contain [value like '0.0.0.0/0']
Associated Rule: D9.GCP.NET.23
Permissions: cloudsql.instances.get, cloudsql.instances.update
"""

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import logging
import bots_utils


PUBLIC_RANGE = '0.0.0.0/0'


def run_action(project_id, rule, entity, params):
    logging.info(f'{__file__} - run_action started')
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('sqladmin', 'v1beta4', credentials=credentials)
    
    instance_name = get_properties_from_entity(entity)

    output_msg = ''
    try:
        logging.info(f'{__file__} - Fetching Cloud SQL instance: {instance_name}')
        instance = get_cloud_sql_instance(service, project_id, instance_name)
        logging.info(f'{__file__} - Deleting public IP ranges for Cloud SQL instance: {instance_name}')
        is_deleted = delete_public_ip_ranges(service, project_id, instance_name, instance)
    except Exception as e:
        msg = f'Failed to delete public IP ranges from Cloud SQL instance: {instance_name} - {e}'
        logging.error(f'{__file__} - {msg}')
        raise Exception(msg)
    if is_deleted:
        msg = f'Successfully deleted public IP ranges from Cloud SQL instance: {instance_name}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg
    else:
        msg = f'Failed to delete public IP ranges from Cloud SQL instance: {instance_name} - No public IP ranges found'
        logging.error(f'{__file__} - {msg}')
        raise Exception(msg)
    return output_msg


def get_cloud_sql_instance(service, project_id, instance_name):
    request = service.instances().get(project=project_id, instance=instance_name)
    response = request.execute()
    return response


def delete_public_ip_ranges(service, project_id, instance_name, instance):
    authorized_networks = instance['settings']['ipConfiguration']['authorizedNetworks']
    non_public_authorized_networks = []
    is_deleted = False
    for i in range(len(authorized_networks)):
        if authorized_networks[i]['value'] == PUBLIC_RANGE:
            is_deleted = True
            continue
        non_public_authorized_networks.append(authorized_networks[i])
    instance['settings']['ipConfiguration']['authorizedNetworks'] = non_public_authorized_networks
    request = service.instances().patch(project=project_id, instance=instance_name, body=instance)
    request.execute()
    return is_deleted


def get_properties_from_entity(entity):
    try:
        instance_name = entity['name']
    except KeyError as e:
        raise KeyError(f"Missing property from entity: {e}")
    return instance_name
