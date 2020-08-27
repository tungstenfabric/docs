This page describes the steps involved in bringing up the Openstack Containers packaged with Contrail in an effort to bring up a cluster based on Contrail micro services (using contrail-ansible-deployer). 

# Pre-requisites for the base host

The steps given below assume a **Centos 7.4** base host. 

1. `yum install -y epel-release `

3. Install Ansible 2.3 (centos by default will install 2.4 which does not work with kolla playbooks). Also the kolla playbooks require version 2.8 or greater of the jinja2 library. So make sure ansible and jinja2 are installed from the centos-release-openstack-ocata repositories.
```shell
    yum -y remove python-jinja2
    yum -y install centos-release-openstack-ocata
    yum -y install ansible-2.3.1.0
    yum -y install python-oslo-config
```
4. This is required for "keepalived" to work:
```shell
    modprobe ip_vs
```
5. `git clone https://github.com/Juniper/contrail-kolla-ansible.git`

6. `cd contrail-kolla-ansible && git checkout contrail/ocata`

# Setting required parameters in the inventory
1. Ensure the following parameters are set in contrail-kolla-ansible/etc/kolla/globals.yml:
```yaml
    # This is the IP address where contrail services are running - will be used to configure the contrail neutron plugin
    contrail_api_interface_address: 192.168.1.50

    # The kolla containers from stable/ocata use tag 4.0.0 in the dockerhub. For latest(nightly?) containers, this can be changed to "ocata", but it might not be stable.
    docker_namespace: kolla
    kolla_base_distro: centos
    kolla_install_type: binary    
    openstack_release: 4.0.0

    # Retain the following - these are workarounds to make kolla openstack talk keystone v2
    enable_keystone_v3: 'no'
    keystone_admin_url: '{{ admin_protocol }}://{{ kolla_internal_fqdn }}:{{ keystone_admin_port }}'
    keystone_admin_user: admin
    keystone_internal_url: '{{ internal_protocol }}://{{ kolla_internal_fqdn }}:{{ keystone_public_port }}'
    keystone_public_url: '{{ public_protocol }}://{{ kolla_external_fqdn }}:{{ keystone_public_port }}'

    # Refer to https://github.com/Juniper/contrail-kolla-ansible/blob/stable/ocata/ansible/group_vars/all.yml for explanations of each variable. Following parameters might need customization

    kolla_external_vip_address: 192.168.1.50
    kolla_external_vip_interface: eth1
    kolla_internal_vip_address: 192.168.1.50
    network_interface: eth1
    neutron_plugin_agent: opencontrail
    enable_haproxy: "no"   <--- This is required if a virtual IP is not required for the kolla_internal_vip_address and you have specified an interface IP.
    rabbitmq_user: openstack

    #Override the following variables to point to the latest build of the neutron-init and compute-init containers. These containers provide the required binaries and the contrail neutron plugin and compute packages.
    neutron_opencontrail_init_image_full: "opencontrailnightly/contrail-openstack-neutron-init:master-20180131150536-centos7-ocata"
    nova_compute_opencontrail_init_image_full: "opencontrailnightly/contrail-openstack-compute-init:master-20180131150536-centos7-ocata"
```
# Setting up the inventory
1. Refer to the official kolla documentation [here to setup the inventory](https://docs.openstack.org/kolla-ansible/ocata/user/quickstart.html#deploy-kolla).

2. In case of nested VMS, the following is required on compute hosts to spawn VMs:
```shell
    mkdir -p /etc/kolla/config/nova/
    vi /etc/kolla/config/nova/nova-compute.conf
    ....
    cat /etc/kolla/config/nova/nova-compute.conf
    [libvirt]
    virt_type=qemu
```

# Running the playbooks
1. Run the top-level playbook as below which will run all the required playbooks. 
```shell
    cd contrail-kolla-ansible/ansible && ansible-playbook -i inventory/all-in-one all.yml
```
   
   **NOTE**: In case of a multi-node installation, the inventory will be "multi-node" so substitute all-in-one with multi-node in the above command. Refer to the [Ocata deployment guide to setup appropriate inventory files](https://docs.openstack.org/kolla-ansible/ocata/user/quickstart.html#deploy-kolla)

## Or if you want more control by running each playbook sequentially as given below: 
1. Run the bootstrap playbook to setup the host with the required packages etc. to launch the open stack containers
```shell
    cd contrail-kolla-ansible/ansible
    ansible-playbook -i inventory/all-in-one -e@../etc/kolla/globals.yml -e@../etc/kolla/passwords.yml -e action=bootstrap-servers kolla-host.yml
```

2. Deploying the containers
```shell
     ansible-playbook -i inventory/all-in-one -e@../etc/kolla/globals.yml -e@../etc/kolla/passwords.yml -e action=deploy site.yml
```
3. Create the /etc/kolla/admin-openrc.sh file to setup the environment parameters if you want to run open stack cli client commands
```shell
     ansible-playbook -i inventory/all-in-one -e@../etc/kolla/globals.yml -e@../etc/kolla/passwords.yml -e action=deploy post-deploy.yml
```

4. Run this playbook to install the open stack client packages.
```shell
    ansible-playbook -i inventory/all-in-one -e@../etc/kolla/globals.yml -e@../etc/kolla/passwords.yml -e action=deploy post-deploy-contrail.yml
```

# Deploying the Contrail Micro Services
Finally, to deploy the contrail microservices, refer to this [README from the contrail-ansible-deployer git repository.](https://github.com/Juniper/contrail-ansible-deployer/blob/master/README.md).