NOTE: Refer [this](https://github.com/Juniper/contrail-ansible-deployer/wiki/%5B-Container-Workflow%5D-Deploying-Contrail-with-OpenStack) documentation to use contrail-kolla-ansible-deployer **container** to deploy Contrail with OpenStack Kolla.

Deploying Kolla containers using contrail-kolla-ansible and contrail containers using contrail-ansible-deployer involves the following broad steps:

```
1. Setup base host
2. Deploy Openstack (kolla) and Contrail containers
```

# 1. Setup base host

The steps given below assume a **Centos 7.5** base host with kernel 3.10.0-862.3.2.el7.x86_64. vRouter has [dependency](https://github.com/Juniper/contrail-ansible-deployer/wiki/Provisioning-F.A.Q#5-vrouter-module-is-not-getting-installed-on-the-computes-vrouter-container-in-error-state-and-docker-logs-show-the-error-like-this) with host kernel.

#### 1.0 Install pre-requisite packages

```
yum -y install epel-release 
yum install -y python-pip
pip install requests
```

#### 1.1 Install Ansible 

```
yum -y install git
pip install ansible==2.5.2.0
```

#### 1.2 Clone contrail-ansible-deployer

```
git clone http://github.com/Juniper/contrail-ansible-deployer
cd contrail-ansible-deployer
```

#### 1.3 Configure necessary parameters config/instances.yaml under appropriate parameters

Here's the bare minimal configuration for single node, single interface all-in-one cluster.

For a multi-interface setup, refer here for [recommended configurations](https://github.com/Juniper/contrail-ansible-deployer/wiki/Contrail's-multi-interface-setup-in-general): 

```
provider_config:
  bms:
    ssh_pwd: <Pwd>
    ssh_user: root
    ntpserver: <NTP Server>
    domainsuffix: local
instances:
  <Server Hostname>:
    provider: bms
    ip: <BMS IP>
    roles:
      config_database:
      config:
      control:
      analytics_database:
      analytics:
      webui:
      vrouter:
      openstack:
      openstack_compute:  
contrail_configuration:
  AUTH_MODE: keystone
  KEYSTONE_AUTH_URL_VERSION: /v3
kolla_config:
  kolla_globals:
    enable_haproxy: no
    enable_ironic: "no"
    enable_swift: "no"
  kolla_passwords:
    keystone_admin_password: <Keystone Admin Password>
```

And here is a slightly more elaborate file for a similar single node All-in-one for explaining purpose

```

provider_config:
  bms:
    ssh_pwd: <Pwd>
    ssh_user: root
    ntpserver: <NTP Server>
    domainsuffix: local
instances:
 <Server Hostname>:
    provider: bms
    ip: <BMS IP>
    roles:
      config_database:
      config:
      control:
      analytics_database:
      analytics:
      webui:
      vrouter:
      openstack:
      openstack_compute:
global_configuration:
  CONTAINER_REGISTRY: <Registry FQDN/IP>:<Registry Port>
  REGISTRY_PRIVATE_INSECURE: True
  CONTAINER_REGISTRY_USERNAME: <RegistryUserName>
  CONTAINER_REGISTRY_PASSWORD: <Password>
contrail_configuration:
  CLOUD_ORCHESTRATOR: openstack
  # Default value for OPENSTACK_VERSION is 'queens'
  OPENSTACK_VERSION: ocata
  # Default value for CONTRAIL_VERSION is 'latest'. The version must be available in
  # registry specified in CONTAINER_REGISTRY
  CONTRAIL_VERSION: 5.0-198
  # Set UPGRADE_KERNEL to True to automatically install the latest kernel version
  UPGRADE_KERNEL: True
  CONTRAIL_VERSION: <container-tag>  # Ex: latest or any private-repo containers tag.
  VROUTER_GATEWAY: <Gateway IP>
  AUTH_MODE: keystone
  KEYSTONE_AUTH_URL_VERSION: /v3
kolla_config:
  kolla_globals:
    enable_haproxy: no
    enable_ironic: no
    enable_swift: no
  kolla_passwords:
    keystone_admin_password: <Keystone Admin Password>
```


**Notes:**
1. Provider configuration refers to the cloud provider where the contrail cluster is going to be hosted. For bare metal servers, the provider will be "bms".
2. Refer [here fore more details about fields in this file](https://github.com/Juniper/contrail-ansible-deployer/blob/master/README.md#configuration)
3. Refer to the following files to know about what fields can be customized under the "kolla_globals" section for the open stack services and "contrail_configuration" section for contrail services:
*    [Kolla Globals File](https://github.com/Juniper/contrail-kolla-ansible/blob/contrail/ocata/etc/kolla/globals.yml.original)
*    [More Kolla Configs](https://github.com/Juniper/contrail-kolla-ansible/blob/contrail/ocata/ansible/group_vars/all.yml)
*    [Contrail Configuration Parameters](https://github.com/Juniper/contrail-container-builder/blob/master/containers/base/common.sh)

4. CONTAINER_REGISTRY can be set to your local docker registry if you are building your own containers. If not specified, it will try to pull the containers from docker hub.
   If a custom registry is specified, please note that you will have to specify the same registry under kolla_globals as "contrail_docker_registry". This is not automatically derived for now and will be done in a later code change.
5. CONTRAIL_VERSION, if not specified, will default to the "latest" tag. If you like a specific version from nightly builds, you can specify one of the tags found [here](https://hub.docker.com/r/opencontrailnightly/contrail-nodemgr/tags/)
6. Sample configurations for some other scenarios
* [Click here for multi-node multi-interface configuration](https://github.com/Juniper/contrail-ansible-deployer/wiki/Configuration-Sample-for-Multi-Node-Openstack-HA-and-Contrail-(multi-interface))
* [Click here for multi-node single-interface configuration](https://github.com/Juniper/contrail-ansible-deployer/wiki/Configuration-Sample-for-Multi-Node-Openstack-HA-and-Contrail-(single-interface))
7. If there are host specific values that need to be given per host (for example, if the names of the interfaces used for "network_interface" are different on the servers in your cluster), then refer to the [example here](https://github.com/Juniper/contrail-ansible-deployer/wiki/Configuration-Sample-for-Multi-Node-Openstack-HA-and-Contrail-(multi-interface)) to know about how to specify this.
8. Many of the parameters are automatically derived to sane defaults which is how the first configuration works. Users can explicitly specify variables to override the derived values if required. Please look into the code if you want to know the derivation logic.
9. If you wish to provision Contrail + Openstack on an All-In-One node with all services listening on a private subnet IP address (non-mgmt), please configure openstack as below:
```
openstack:
  kolla_internal_address: 192.168.10.10
  network_interface: eth2
```

   If there is no need to restrict access to only this subnet, it is sufficient to set "enable_haproxy" as "yes" under kolla_globals section.

#### 1.4 Install Contrail and Kolla requirements    

The following playbook installs packages on the deployer host as well as the target host required to bring up the kolla and contrail containers. 
    
```
ansible-playbook -i inventory/ -e orchestrator=openstack playbooks/configure_instances.yml
```


# 2. Deploy contrail and kolla containers

```
ansible-playbook -i inventory/ playbooks/install_openstack.yml
ansible-playbook -i inventory/ -e orchestrator=openstack playbooks/install_contrail.yml
```

# 3 Run openstack commands

#### 3.1 Install open stack clients

The openstack clients need not be installed as the kolla_toolbox container already has the clients installed. Refer [here to use the kolla_toolbox.](https://github.com/Juniper/contrail-ansible-deployer/wiki/Provisioning-F.A.Q#how-to-use-the-kolla_toolbox-container-to-run-openstack-cli-commands). Or if you prefer to run the commands from the base host, follow the instructions below.

The open stack clients were previously being automatically installed as part of the playbook run. But some dependent python libraries brought in as part of installing python docker compose libraries which now conflict with installing the python-openstackclients from Yum repos. The other option to get the python-openstackclient packages is installing through "pip" repos. But installing these pip packages can cause Ansible executable to crash because libraries being used by Ansible will also get changed. So the clients need to be installed manually using pip.

```
yum install -y gcc python-devel
pip install python-openstackclient
pip install python-ironicclient
```

#### 3.2 Test your setup with VM to VM ping
```
source /etc/kolla/kolla-toolbox/admin-openrc.sh
wget http://download.cirros-cloud.net/0.4.0/cirros-0.4.0-x86_64-disk.img
openstack image create cirros2 --disk-format qcow2 --public --container-format bare --file cirros-0.4.0-x86_64-disk.img                                      
openstack network create testvn
openstack subnet create --subnet-range 192.168.100.0/24 --network testvn subnet1
openstack flavor create --ram 512 --disk 1 --vcpus 1 m1.tiny
NET_ID=`openstack network list | grep testvn | awk -F '|' '{print $2}' | tr -d ' '`
openstack server create --flavor m1.tiny --image cirros2 --nic net-id=${NET_ID} test_vm1
openstack server create --flavor m1.tiny --image cirros2 --nic net-id=${NET_ID} test_vm2
```
# F.A.Q
Please check here for common issues with provisioning and the fixes/workarounds:

[Provisioning F.A.Q](https://github.com/Juniper/contrail-ansible-deployer/wiki/Provisioning-F.A.Q)

# Known Limitations