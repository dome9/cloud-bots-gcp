"""
What it does: Deletes IAM rules of a Storage Bucket that allow public access
Usage: storage_bucket_remove_allow_public_access_rules
Example: storage_bucket_remove_allow_public_access_rules
Limitations: None
Example GSL: StorageBucket should not have iamPolicy with [ bindings contain [ members contain-any [ $ in ( 'allUsers', 'allAuthenticatedUsers' ) ] ] ]
Associated Rule: D9.GCP.IAM.09
Permissions: storage.buckets.getIamPolicy, storage.buckets.setIamPolicy
"""

from googleapiclient import discovery
from google.cloud.storage import Client, Bucket
from oauth2client.client import GoogleCredentials
import logging
import bots_utils

ALL_USERS = 'allUsers'
ALL_AUTHENTICATED_USERS = 'allAuthenticatedUsers'


def run_action(project_id, rule, entity, params):
    logging.info(f'{__file__} - run_action started')
    client = Client(project_id)

    bucket_name = get_properties_from_entity(entity)

    output_msg = ''

    logging.info(f'{__file__} - Fetching IAM policy of bucket: {bucket_name}')
    bucket = Bucket(client, name=bucket_name)
    iam_policy = get_bucket_iam_policy(bucket)
    is_deleted = delete_allow_public_access_rules(bucket, iam_policy)
    if is_deleted:
        msg = f'Successfully deleted IAM rules that allow public access to bucket: {bucket_name}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg
    else:
        msg = f'Failed to delete IAM rules that allow public access to bucket: {bucket_name} - ' \
              f'Bucket have no rules that allow public access'
        logging.error(f'{__file__} - {msg}')
        raise Exception(msg)
    return output_msg


def get_bucket_iam_policy(bucket):
    try:
        return bucket.get_iam_policy()
    except Exception as e:
        msg = f'Failed to get IAM policy - {e}'
        logging.error(f'{__file__} - {msg}')
        raise Exception(msg)


def delete_allow_public_access_rules(bucket, iam_policy):
    current_iam_policy_bindings = iam_policy.bindings
    new_iam_policy_bindings = []
    is_deleted = False
    for binding in current_iam_policy_bindings:
        if ALL_USERS in binding['members'] or ALL_AUTHENTICATED_USERS in binding['members']:
            is_deleted = True
            continue
        new_iam_policy_bindings.append(binding)
    iam_policy.bindings = new_iam_policy_bindings
    try:
        bucket.set_iam_policy(iam_policy)
    except Exception as e:
        msg = f'Failed to delete IAM rules that allow public access - {e}'
        logging.error(f'{__file__} - {msg}')
        raise Exception(msg)
    return is_deleted


def get_properties_from_entity(entity):
    try:
        bucket_name = entity['name']
    except KeyError as e:
        raise KeyError(f"Missing property from entity: {e}")
    return bucket_name
