import json
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

def run_action(project_id, rule, entity, params):
    print(f'{__file__} - run_action started')
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)
    
    region = entity.get('region')
    fingerprint = entity.get('fingerPrint')
    subnetwork = entity.get('name')

    print(f'{__file__} - project_id : {project_id} - region : {region} - subnetwork : {subnetwork} - fingerprint : {fingerprint}')
    print("hola")
    # Without fingerprint
    
    subnetwork_body = {
        "logConfig": {
        "enable": true
        }
    }
    
    print("La variable funciona")

    print(subnetwork_body)

    request = service.subnetworks().patch(project=project, region=region, subnetwork=subnetwork, body=subnetwork_body)
    response = request.execute()
    print(f'{__file__} - response - {response}')
    return f'{response}'
