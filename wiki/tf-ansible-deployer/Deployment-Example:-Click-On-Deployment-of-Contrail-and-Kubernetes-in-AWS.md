## Introduction

This document contains instructions to deploy a Contrail cluster that interconnects PODs orchestrated by Kubernetes. The Contrail cluster is composed of one controller and two compute nodes that run as EC2 VMs.

## Requirements

New AWS individual users only have root access and they may optionally set up IAM. If you are connected as a root user, you only need to subscribe to the Centos 7 image. 

1. Once you have signed into the AWS console, go to the following URL: https://aws.amazon.com/marketplace/
2. Search for Centos and click on the "CentOS 7 (x86_64) - with Updates HVM" image. Continue to Subscribe. Accept Terms.

If you are connected as an IAM user, check the Appendix at the end of the document.

## Procedure

Just click on this button to create the stack:

<a href="https://console.aws.amazon.com/cloudformation/#/stacks/new?stackName=contrail-k8s&amp;templateURL=https://s3.eu-west-1.amazonaws.com/contrail-ansible-deployer/cloudformation_template.yaml" target="_blank"><img alt="Launch Stack" src="https://cdn.rawgit.com/buildkite/cloudformation-launch-stack-button-svg/master/launch-stack.svg"></a>

1. Click Next. Give a name to the stack.
2. Leave the AnsibleDeployerCommit to the default value: master
3. Set the AnsibleDeployerConfigURL to this URL: https://s3.eu-west-2.amazonaws.com/contrail-k8s-workshop/aws-k8s-config.yaml
4. Leave the AnsibleOrchestrator at its default value (kubernetes).
5. Set InstallContrail to Yes.
6. Remember - or - change the InstallPassword.
7. InstanceType: set it to t2.medium. This will only affect the ansible VM because the configuration referred by the AnsibleDeployerConfigURL already specifies the instance_type of all the other VMs.
8. Leave the SubnetCIDR and VpcCIDR at their default values. Click Next. Again, Click Next.
9. Check "I acknowledge that AWS CloudFormation might create IAM resources". Click Create.

This will trigger the creation, among other things, of one instance that runs the Ansible host. In turn, the Ansible host will create the cluster:

*IMPORTANT*: If you don’t want to spend a fortune, when you are done with the lab make sure you manually delete the 3 cluster VMs, then delete the stack, and verify no instances run and no volumes are left either.

## Accessing the cluster:

First, you need to SSH the Ansible host with user root and password contrail123 (or whatever password you set).

Next:

```
ssh centos@<ip>   # <ip> can be the public IP or the private IP of the VM, both work
sudo -s
```

## Appendix: IAM Users

If, instead of using a root account, you are signing with an IAM user, you need to grant additional privileges for the user.

- Log on to the AWS console.
- In the AWS services search at the top left of the console, look for IAM and select it.
- On the left navigation bar, click on the user whose privileges you need to change.
- At the right bottom, click Add inline policy.
- Go to the JSON tab, and replace the content with the following policy:

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "cloudformation:*",
                "aws-marketplace:*",
                "sns:*",
                "s3:*",
                "ec2:*",
                "elasticloadbalancing:*",
                "cloudwatch:*",
                "autoscaling:*",
                "iam:*"
            ],
            "Resource": "*"
        }
    ]
}

- Review policy. Add policy name. Create policy.
