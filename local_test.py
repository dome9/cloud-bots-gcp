from main import *

sns_event = {
	"account": {
		"id": "chkp-gcp-omerar-box",
         "vendor": "GCP",
	},
	"findingKey": "test",
	"entity": {
		"name": "instance-test",
		"zone": "us-central1-a"
	},
	"remediationActions": ["vm_instance_stop"],
	"rule": {"complianceTags": "", "name": "test"},
	"status": "failed",
    "logsHttpEndpoint": "https://03nlnc41gk.execute-api.us-east-1.amazonaws.com/remediation/feedback",
	"logsHttpEndpointKey": "V274YHPSVG9gr3BxsHoN6IwEQ06ZloS6lxOX2hc3",
	"logsHttpEndpointStreamName": "remediation_feedback",
	"logsHttpEndpointStreamPartitionKey": "1",
	"executionId": "2914b53f-f785-4a7a-b616-32fe9326d39b",
	"dome9AccountId": "39801"
}



context =""


main(sns_event);