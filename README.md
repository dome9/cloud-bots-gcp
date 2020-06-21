<p align="center">
    <a href="https://cloudbots.dome9.com">
      <img width="150" src="docs/pictures/cloudbotslogo.svg">
    </a>
</p>

<div align="center">
    <h1><a target="_blank" href="https://cloudbots.dome9.com">CloudBots</a> is an automatic remediation solution for public cloud platforms (GCP, <a href="https://github.com/Dome9/cloud-bots" target="_blank">AWS</a>, and <a href="https://github.com/Dome9/cloud-bots-azure" target="_blank">Azure</a>)</h1>
</div>

  - [What are Dome9 CloudBots?](#what-are-dome9-cloudbots)
  - [Flow Diagram](#flow-diagram)
      - [The Bots](#the-bots)
  - [Deploy the CloudBots](#deploy-the-cloudbots)
      - [Configure your GCP Projects for
        CloudBots](#configure-your-gcp-projects-for-cloudbots)
          - [Download the CloudBots zip
            file](#download-the-cloudbots-zip-file)
          - [Create GCP Service Account for
            cloudbots](#create-gcp-service-account-for-cloudbots)
          - [Configure SendGrid](#configure-sendgrid)
          - [Create a GCP Function with the
            CloudBots](#create-a-gcp-function-with-the-cloudbots)
          - [Webhook for Function](#webhook-for-function)
      - [Multiple GCP Accounts](#multiple-gcp-accounts)
      - [Configure your Dome9 account](#configure-your-dome9-account)
          - [Configure a Dome9 Compliance
            Ruleset](#configure-a-dome9-compliance-ruleset)
          - [Configure a Dome9 Continuous Compliance
            policy](#configure-a-dome9-continuous-compliance-policy)
  - [Log Collection for
    Troubleshooting](#log-collection-for-troubleshooting)
  - [What are Dome9 CloudBots?](#what-are-dome9-cloudbots)
      - [Flow Diagram](#flow-diagram)
          - [The Bots](#the-bots)
      - [Onboarding](#onboarding)
          - [Clone repo](#clone-repo)
          - [Create GCP Service Account for
            cloudbots](#create-gcp-service-account-for-cloudbots)
          - [Configure SendGrid](#configure-sendgrid)
          - [Create a GCP Function with the
            CloudBots](#create-a-gcp-function-with-the-cloudbots)
          - [Webhook for Function](#webhook-for-function)
          - [Multiple Accounts](#multiple-accounts)
      - [Configure Dome9](#configure-dome9)
          - [Configure a Ruleset](#configure-a-ruleset)
          - [Configure the Continuous Compliance
            policy](#configure-the-continuous-compliance-policy)
      - [Log Collection for
        Troubleshooting](#log-collection-for-troubleshooting)

## What are Dome9 CloudBots?

Dome9 CloudBots are an autoremediation solution for GCP, built on top of
the CloudGuard Dome9 Continuous Compliance capabilities.

They can also be used standalone, without Dome9, to remedy issues in AWS
and Azure accounts. Details are included how to configure and trigger
them.

# Flow Diagram

![Flow Diagram](docs/pictures/GCP-CloudBots-Flow-Diagram.png)

## The Bots

Refer to [this](dome9CloudBots/bots/bots.md) file for a list of the
bots, what each one does, and an example of a rule that could be used to
trigger it.

# Deploy the CloudBots

To use the CloudBots, you have to set up your GCP project, and your
Dome9 account.

## Configure your GCP Projects for CloudBots

Follow these steps to configure your GCP Projects:

  - download the CloudBots zip file
  - Create a GCP Service Account
  - Optionally, configure SendGrid to forward notifications by email
  - Create a GCP Function for the CloudBots

### Download the CloudBots zip file

1.  Download the CloudBots zip file from this repository (The GCP
    Function will require the content zipped).
2.  If you cloned the repository, zip the contents.

### Create GCP Service Account for cloudbots

1.  In the GCP console, navigate to IAM & admin, and then select Service
    accounts.
2.  Click CREATE SERVICE ACCOUNT to add a service account.
    ![](docs/pictures/Create-Service-Account.png)
3.  Enter a name (e.g., *Dome9-cloudbots*)
4.  In the Service Account ID field, the name of the service account
    will be used for the Cloud Function (in the previous step).
5.  Click *Create*.

### Configure SendGrid

SendGrid ([sendgrid.com](sendgrid.com)) is a third-party email service.
It has different tiers and pricing. It is used by GCP to distribute
emails. See
[here](https://cloud.google.com/compute/docs/tutorials/sending-mail/using-sendgrid)
for more info.

This step is optional.

1.  Navigate to sendgrid.com
2.  Create a new account, following the instructions on the site.
3.  Navigate to *Settings*, and then select *API Keys*.
4.  Click *Create API Key*.
5.  Enter a name for the key (e.g., *Dome9-cloudbots*, an select Full
    Access.
6.  Click *Create Key*, then copy the value of the key.
7.  Click *Done*.

### Create a GCP Function with the CloudBots

1.  Navigate to *Cloud Functions*.
2.  Click *CREATE FUNCTION*.
3.  Enter a name for the function (e.g., *Dome9-Cloudbot*).
4.  Make sure the Trigger is *HTTP*.
5.  In the Source Code section, select *ZIP upload*.
6.  In the Runtime section, select *Python 3.7*.
7.  In the ZIP file section, browse to the location of zip file created
    before.
8.  In the Stage bucket section, click *Browse*.
9.  Click *+*, enter a name for the bucket, and then click *CREATE*.
    ![](docs/pictures/Stage-bucket-new.png)
10. In the *Function to execute* section, enter *main*.
11. Click *Environment variables, networking, timeouts and more* at the
    bottom of the navigation menu, on the left.
12. In the Service account field, select the account created above.
13. In the Environment variables section, click Add variable, and add
    the following variables:
    1.  SEND\_GRID\_API\_CLIENT - enter to SendGrid API Key, created
        above.
    2.  OUPTPUT\_EMAIL - the email recipient (for notification emails,
        generated with SendGrid).
    3.  SEND\_LOGS - set to True to send log information to Dome9, for
        troubleshooting; False to disable this (default is True).
14. Click *CREATE* to create the function for the cloudbots.
    ![](docs/pictures/Create-Function.png)

### Webhook for Function

The cloudbot function in GCP is triggered from Dome9 using a webhook.
For this, the URL of the function is required.

1.  Click on the Cloud Function you created.
2.  Copy the URL for Dome9 Notification.

## Multiple GCP Accounts

You can use CloudBots for several GCP projects, but install it in only
one project. The other projects will be accessed from the first by
granting IAM permissions.

1.  Create a GCP Function in one of the GCP projects, following the
    steps above.
2.  For each of the other projects, navigate to IAM & admin, and select
    IAM.
    1.  Click ADD.  
        ![](docs/pictures/IAM-Add-members.png)
    2.  In the New members field, enter the service account created
        above.
    3.  Select the Project Editor role.
    4.  Click SAVE.

## Configure your Dome9 account

On Dome9 add remediation tags to rules in a Compliance ruleset.

See also

[CloudGuard Dome9
Compliance](https://sc1.checkpoint.com/documents/CloudGuard_Dome9/Documentation/Compliance-and-Governance/Compliance-and-Governance.html)

[Continuous
Compliance](https://sc1.checkpoint.com/documents/CloudGuard_Dome9/Documentation/Compliance-and-Governance/ContinuousCompliance.html)

[Notification
Policies](https://sc1.checkpoint.com/documents/CloudGuard_Dome9/Documentation/Alerts-Notifications/NotPolicy.html)

### Configure a Dome9 Compliance Ruleset

CloudBots are triggered by findings discovered by Dome9 Compliance
rulesets. You must configure a ruleset to trigger the CloudBots.

Follow these steps in your Dome9 account to tag the compliance rules &
rulesets to use bots as a remediation step.

1.  In the Dome9 web app, navigate to the Rulesets page in the
    Compliance & Governance menu.

2.  Select or create a ruleset that will be used for the cloudbots.

3.  Select the rules for which you want to add a remediation step.

4.  In the Compliance Section add a row with the following string:
    `AUTO: <bot-name> <params>` where *bot-name* is the name of the bot,
    and *params* is a list of arguments for the bot (if any).
    
    For example, `AUTO: vm_instance_stop` will run the bot to stop a VM
    instance.

### Configure a Dome9 Continuous Compliance policy

Once the rules in the ruleset have been tagged for remediation, set up a
Continuous Compliance policy to run the ruleset, and send findings the
GCP function webhook.

1.  Navigate to the **Policies** page in the Compliance & Governance
    menu.
2.  Click **ADD POLICY** (on the right).
3.  Select the account from the list, then click **NEXT**, this will be
    the one account in which the bots are deployed.
4.  Select the ruleset from the list, then click **NEXT**.
5.  Click **ADD NOTIFICATION**.
6.  Select *Send to HTTP Endpoint* and enter the URL for the Function, as described above  [Webhook for Function](#webhook-for-function), and then click **SAVE**.

**Note:** Dome9 will send event messages to the webhook for new
findings. To send events for previous findings, follow these steps:

1.  Navigate to the **Policies** page.
2.  Find the ruleset and account in the list, and hover over the right
    of the row, then click on the *Send All Alerts* icon.
3.  Select the *webhook* Notification Type option, and the Notification
    Policy (the one created above), then click **SEND**. Dome9 will send
    event messages to the GCP function webhook.

# Log Collection for Troubleshooting

The cloudbots send log information to Dome9, that is used for
troubleshooting. By default, this is enabled for all bots. You can
disable this in your GCP account. Select the function, and set the
environment variable SEND\_LOGS to False. This will apply to all bots in
the account. By default, this is set to True, enabling logs.

Each account is controlled by the variable for the function configured
in that account.
