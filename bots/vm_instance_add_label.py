from googleapiclient import discovery
from oauth2client.client import GoogleCredentials


def run_action(project_id, rule, entity, params):
    print(f'{__file__} - run_action started')
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)
    zone = entity.get('zone')
    instance = entity.get('name')
    print(f'{__file__} - project_id : {project_id} - zone : {zone} instance : {instance}')

    tag_key, tag_value = params
    print(f'{__file__} - tag_key : {tag_key} - tag_value : {tag_value}')

    ## get instance labels and label fingerprint ##
    request = service.instances().get(project=project_id, zone=zone, instance=instance)
    response = request.execute()
    labels = response.get('labels',{})
    labels[tag_key] = tag_value
    print(f'{__file__} - labels : {labels}')
    label_fingerPrint = response.get('labelFingerprint')

    instances_set_labels_request_body = {
        'labels': labels,
        'labelFingerprint': label_fingerPrint
    }
    request = service.instances().setLabels(project=project_id, zone=zone, instance=instance,
                                            body=instances_set_labels_request_body)
    response = request.execute()
    print(f'{__file__} - response -{response}')
    return f'{response}'
