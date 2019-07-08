from googleapiclient import discovery
from oauth2client.client import GoogleCredentials


def run_action(project_id, rule, entity, params):
    print(f'{__file__} - run_action started')
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)
    firewall = entity.get('name')
    print(f'{__file__} - project_id : {project_id} - firewall : {firewall}')

    request = service.firewalls().delete(project=project_id, firewall=firewall)
    response = request.execute()
    print(f'{__file__} - response -{response}')
    return f'{response}'
