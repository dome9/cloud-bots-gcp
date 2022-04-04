# What it does: Disables public IP for all the network interfaces of a VM Instance
# Usage: vm_instance_disable_public_ip
# Example: vm_instance_disable_public_ip
# Limitations: None
# Example GSL: VMInstance should not have isPublic=true
# Associated Rule: D9.GCP.NET.04
# Permissions: compute.instances.get, compute.instances.deleteAccessConfig

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import logging
import bots_utils


def run_action(project_id, rule, entity, params):
    logging.info(f'{__file__} - run_action started')
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)

    instance_name, zone = get_properties_from_entity(entity)

    output_msg = ''

    logging.info(f'{__file__} - Fetching VM instance: {instance_name}')
    instance = get_vm_instance(service, project_id, zone, instance_name)
    disabled_all = disable_public_ip_all_nics(service, project_id, instance, instance_name, zone)
    if not disabled_all:
        msg = f'Failed to disable public IP on vm instance: {instance_name}'
        logging.error(f'{__file__} - {msg}')
        raise Exception(msg)
    msg = f'Successfully disabled public IP on vm instance: {instance_name}'
    logging.info(f'{__file__} - {msg}')
    output_msg += msg
    return output_msg


def get_vm_instance(service, project_id, zone, instance_name):
    request = service.instances().get(project=project_id, zone=zone, instance=instance_name)
    instance = request.execute()
    return instance


def disable_public_ip_all_nics(service, project_id, instance, instance_name, zone):
    # disabled_all variable is for tracking if there was a network interface that the bot could not disable
    disabled_all = True
    for nic in instance['networkInterfaces']:
        if 'accessConfigs' not in nic:
            logging.info(f'Network interface: {nic["name"]} has no public IP. Moving forward')
            continue
        try:
            access_configs = nic['accessConfigs']
            nic_name = nic['name']
            for access_config in access_configs:
                is_disabled = disable_public_ip_for_single_nic(service, project_id, instance_name, zone,
                                                               access_config['name'], nic_name)
                if is_disabled:
                    logging.info(f'Successfully disabled public IP for network interface: {nic_name}')
                else:
                    disabled_all = False
        except KeyError as e:
            logging.info(f'Failed to extract network interface\'s property: {e} on network interface: {nic["name"]}')
            disabled_all = False
    return disabled_all


def disable_public_ip_for_single_nic(service, project_id, instance_name, zone, access_config_name, nic_name):
    try:
        request = service.instances().deleteAccessConfig(project=project_id, zone=zone, instance=instance_name,
                                                         accessConfig=access_config_name, networkInterface=nic_name)
        request.execute()
        return True
    except Exception as e:
        logging.info(f'Failed to disable public IP for network interface: {nic_name} - {e}')
        return False


def get_properties_from_entity(entity):
    try:
        instance_name = entity['name']
        zone = entity['zone']
    except KeyError as e:
        raise KeyError(f"Missing property from entity: {e}")
    zone = extract_zone_name(zone)
    return instance_name, zone


def extract_zone_name(zone):
    try:
        zone = zone[zone.rfind('/') + 1:]
    except Exception as e:
        raise Exception(f'Failed to extract zone name: {e}')
    return zone
