# Bots

## firewall_rules_delete

What it does: deletes the GCP firewall rule(s)in the finding

Usage: AUTO: firewall_rules_delete

Sample GSL:    NetworkSecurityGroup should have networkAssetsStatslength()>0 

Limitations: None

Permissions: compute.firewalls.delete, compute.networks.updatePolicy

## flow_logs_enable

What it does: Enable flow logs in the subnetwork

Usage:  flow_logs_enable

Sample GSL:   Subnet should have enableFlowLogs=true

Limitations: None

Permissions: compute.subnetworks.get, compute.subnetworks.update

## gke_change_imageType_to_cos

What it does: Change Google Kubernetes image type to COS

Usage:  gke_change_imageType_to_cos

Sample GSL:    GkeCluster should have nodePools contain-all [config.imageType='COS']

Limitations: The cluster should be updated

Permissions: container.clusters.update, gkemulticloud.awsNodePools.update

## gke_enable_master_authorized_networks

What it does: Enables 'master authorized networks' on a gke cluster

Usage:  gke_enable_master_authorized_networks <cidr_blocks>
        cidr_blocks is an optional parameter (leave empty if needed)
        cidr_block has two properties - name and cidr range.
        Each cidr_block should be passed this way: name-cidr_range
        User can pass multiple cidr_blocks by separating them with a comma (see example)

Examples: gke_enable_master_authorized_networks 
         gke_enable_master_authorized_networks net1-10.0.0.0/24,net2-192.168.0.0/16

Limitations: None

Example GSL: GkeCluster should have masterAuthorizedNetworksConfig.enabled=true

Associated Rule: D9.GCP.NET.10

Permissions: container.clusters.update

## subnet_set_private_google_access_on

What it does: Enables subnet 'private google access'

Usage: subnet_set_private_google_access_on

Example: subnet_set_private_google_access_on

Limitations: None

Sample GSL:     Subnet should have privateIpGoogleAccess=true

Associated Rule: D9.GCP.NET.14

Permissions: compute.subnetworks.setPrivateIpGoogleAccess

## vm_instance_add_label

What it does: tags the VM in the finding 

Usage:  vm_instance_add_label tag-name tag-value  

Sample GSL:   VirtualMachine should have tags contain [ ( key like ‘Prod' ) ]

Limitations: None

Permissions: compute.instances.get, compute.instances.setLabels

## vm_instance_stop

What it does: stops the  VM in the finding

Usage:  vm_instance_stop

Sample GSL:   VirtualMachine should have tags contain [ ( key like ‘Prod' ) ]

Limitations: None

Permissions: compute.instances.stop