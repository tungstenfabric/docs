## Introduction

This document contains instructions to deploy a Contrail cluster that interconnects two types of workloads:

* VMs orchestrated by Openstack
* PODs orchestrated by Kubernetes

The scripts also deploy Openstack and Kubernetes functions from scratch.

## Requirements

The example setup consists of a single bare metal server with KVM. After deployment with the instructions in its page, the server ends up running three base VMs:

- 1 controller VM, with the following functions: Contrail controller, Openstack controller, and Kubernetes master.
- 2 compute VMs, each of which has the following functions: Contrail vRouter, Openstack compute, and Kubernetes node.

You don't need to create the VMs. Instead, the deployment scripts will do it for you.

Each VM has the following resources:

`vcpu: 4`
`vram: 16000`
`vdisk: 100G`

**NOTE**: This is just an example deployment for simple test purposes. It is NOT a sizing recommendation or specification.

***IMPORTANT***: It is not recommended to run nested virtualization, so a VM with openstack-compute role is a very bad idea. This role should run in _provider: bms_. We are showing openstack_compute on _provider: kvm_ as a poor (wo)man approach for someone who wants to see the solution from a functional perspective and only has one server.

A similar procedure exists for a setup where functions run directly on BMS, or on public cloud infrastructure (AWS, GCP, Azure). The corresponding examples will be added.

## Preparing the BMS

The server is installed with Centos 7.5. Here are some preparation steps:

```
yum install -y epel-release
yum install -y python-pip
pip install requests
yum install -y python-urllib3 libguestfs-tools libvirt-python virt-install libvirt git ansible python-pip
service libvirtd start
```

Next, clone the contrail-ansible-deployer repo and populate the configuration:

```
git clone https://github.com/Juniper/contrail-ansible-deployer
cd contrail-ansible-deployer
> config/instances.yaml
vi config/instances.yaml
```

Here is an instances.yaml example for a server with one NIC, whose IP address is 172.16.10.1:

```
provider_config:
  kvm:
    image: CentOS-7-x86_64-GenericCloud-1710.qcow2.xz
    image_url: https://cloud.centos.org/centos/7/images/
    ssh_pwd: c0ntrail123
    ssh_user: root
    ssh_public_key:
    ssh_private_key:
    vcpu: 12
    vram: 64000
    vdisk: 100G
    subnet_prefix: 192.168.122.0
    subnet_netmask: 255.255.255.0
    gateway: 192.168.122.1
    nameserver: 10.84.5.100
    ntpserver: 192.168.122.1
    domainsuffix: local
instances:
  kvm101:
    provider: kvm
    host: 10.87.64.23
    bridge: default
    ip: 192.168.122.100
    roles:
        config_database:
        config:
        control:
        analytics_database:
        analytics:
        webui:
        k8s_master:
        kubemanager:
        openstack:
  kvm102:
    provider: kvm
    host: 10.87.64.23
    bridge: default
    ip: 192.168.122.101
    roles:
        vrouter:
        k8s_node:
        openstack_compute:
  kvm103:
    provider: kvm
    host: 10.87.64.23
    bridge: default
    ip: 192.168.122.102
    roles:
        vrouter:
        k8s_node:
        openstack_compute:
global_configuration:
  CONTAINER_REGISTRY: opencontrailnightly
contrail_configuration:
  CONTRAIL_VERSION: latest
  UPGRADE_KERNEL: true
  AUTH_MODE: keystone
  KEYSTONE_AUTH_URL_VERSION: /v3
  KEYSTONE_AUTH_ADMIN_PASSWORD: contrail123
  CLOUD_ORCHESTRATOR: openstack

kolla_config:
  customize:
    nova.conf: |
      [libvirt]
      virt_type=qemu
      cpu_mode=none
  kolla_globals:
    network_interface: "eth0"     #Do not change – this is the VM interface and not the host interface
    kolla_internal_vip_address: "192.168.122.100"
    kolla_external_vip_address: "192.168.122.100"
    enable_haproxy: "no"
    enable_ironic: "no"
    enable_swift: "no"
```
For more information about the contents of this file, see [this page](https://www.juniper.net/documentation/en_US/contrail5.0/topics/concept/install-contrail-overview-ansible-50.html#jd0e124).

## Deploying the Cluster

The deployment takes just five steps:

```
ansible-playbook -i inventory/ playbooks/provision_instances.yml
ansible-playbook -i inventory/ -e orchestrator=openstack playbooks/configure_instances.yml
ansible-playbook -i inventory/ playbooks/install_openstack.yml
ansible-playbook -i inventory/ -e orchestrator=openstack playbooks/install_k8s.yml
ansible-playbook -i inventory/ -e orchestrator=openstack playbooks/install_contrail.yml
```
***TIP***: Empty the /root/.ssh/known_hosts if you need to redeploy.

After the first step completes you can SSH from the server to the three VMs 192.168.122.10x (x=0,1,2), with credentials root/c0ntrail123 .

At the end of the procedure you should also be able to connect to the Contrail webUI, in two steps:

1. From your computer terminal, create SSH forwarding tunnel. Assuming the IP addresses in the example:

`ssh -L 8143:192.168.122.100:8143 root@10.87.64.23`

2. At your web browser, connect to URL http://localhost:8143 , user admin , password c0ntrail123 . There is currently an issue by which you may need to refresh the browser after authentication.

### Working around a current provisioning issue (to be fixed):

* On the webUI, go to Configure > Networking > Ports > default-domain > default-project
* Edit the vhost0 interfaces and under Advanced Options uncheck Packet Mode.

## Launching & Interconnecting Tenant PODs and VMs

```
yum install -y gcc python-devel wget
pip install --upgrade setuptools
pip install python-openstackclient
wget http://download.cirros-cloud.net/0.4.0/cirros-0.4.0-x86_64-disk.img
source /etc/kolla/kolla-toolbox/admin-openrc.sh
openstack image create cirros --disk-format qcow2 --public --container-format bare --file cirros-0.4.0-x86_64-disk.img
nova flavor-create m1.tiny auto 512 1 1
openstack network create net1
openstack subnet create --subnet-range 10.1.1.0/24 --network net1 mysubnet1
nova boot --image cirros --flavor m1.tiny --nic net-id=<UUID> VM1
nova boot --image cirros --flavor m1.tiny --nic net-id=<UUID> VM2

yum install -y git
git clone https://github.com/virtualhops/k8s-demo
kubectl create -f k8s-demo/po-ubuntuapp.yml
kubectl create -f k8s-demo/rc-frontend.yml
kubectl expose rc/frontend
kubectl exec -it ubuntuapp curl frontend # many times
