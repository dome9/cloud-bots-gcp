# Bots

## firewall_rules_delete

What it does: deletes the GCP firewall rule(s)in the finding

Usage: AUTO: firewall_rules_delete

Sample GSL:    NetworkSecurityGroup should have networkAssetsStatslength()>0 

Limitations: None

## vm_instance_add_label

What it does: tags the VM in the finding 

Usage: AUTO: vm_instance_add_label tag-name tag-value  

Sample GSL:   VirtualMachine should have tags contain [ ( key like ‘Prod' ) ]

Limitations: None

## vm_instance_stop

What it does: stops the  VM in the finding

Usage: AUTO: vm_instance_stop

Sample GSL:   VirtualMachine should have tags contain [ ( key like ‘Prod' ) ]

Limitations: None



## gke_change_imageType_to_cos

What it does: Change Google Kubernetes image type to COS

Usage: AUTO: gke_change_imageType_to_cos

Limitations: None
