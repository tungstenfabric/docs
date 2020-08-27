This page describes the steps involved in bringing up the Openstack Containers packaged with Contrail in an effort to bring up a cluster based on Contrail micro services (using contrail-ansible-deployer). 

# Pre-requisites for the base host

The steps given below assume a **Centos 7.4** base host. 

1. `yum install -y epel-release `

3. Install Ansible 2.3 (centos by default will install 2.4 which does not work with kolla playbooks). Also the kolla playbooks require version 2.8 or greater of the jinja2 library.
```shell
    yum install centos-release-openstack-ocata
    yum -y install ansible-2.3.1.0
    yum -y install python-oslo-config
```
4. This is required for "keepalived" to work:
```shell
    modprobe ip_vs
```
5. `git clone https://github.com/Juniper/contrail-kolla-ansible.git`

# Setting required parameters in the inventory
1. Create the passwords.yml and the globals.yml file as below:
```shell
    cd contrail-ansible/kolla-ansible/etc/kolla
    cp passwords.yml.original passwords.yml
    cp globals.yml.original globals.yml
```
2. Ensure the following parameters are set in globals.yml:
```yaml
    # This is the IP address where contrail services are running - will be used to configure the contrail neutron plugin
    contrail_api_interface_address: 192.168.10.110
    # The kolla containers from 4.1 build 8 are pushed into the following registry with the following image tag format - 10.84.22.43:5000/kolla/ubuntu-binary-<service>:contrail_4_1_8 So retain the following 5 parameters
    docker_registry: 10.84.22.43:5000
    docker_namespace: kolla
    kolla_base_distro: ubuntu
    kolla_install_type: binary    
    openstack_release: contrail_4_1_8

    # Retain the following - these are workarounds to make kolla openstack talk keystone v2
    enable_keystone_v3: 'no'
    keystone_admin_url: '{{ admin_protocol }}://{{ kolla_internal_fqdn }}:{{ keystone_admin_port }}'
    keystone_admin_user: admin
    keystone_internal_url: '{{ internal_protocol }}://{{ kolla_internal_fqdn }}:{{ keystone_public_port }}'
    keystone_public_url: '{{ public_protocol }}://{{ kolla_external_fqdn }}:{{ keystone_public_port }}'

    # Refer to https://github.com/Juniper/contrail-ansible/blob/master/kolla-ansible/ansible/group_vars/all.yml for explanations of each variable. Following parameters might need customization

    enable_nova_compute: 'no'
    kolla_external_vip_address: 192.168.1.100
    kolla_external_vip_interface: eth1
    kolla_internal_vip_address: 192.168.10.100
    network_interface: eth2
    neutron_plugin_agent: opencontrail
    rabbitmq_user: openstack
```
# Setting up the inventory
1. Refer to the official kolla documentation [here to setup the inventory](https://docs.openstack.org/kolla-ansible/ocata/quickstart.html).

# Running the playbooks
1. Run the bootstrap playbook to setup the host with the required packages etc. to launch the open stack containers
```shell
    cd contrail-ansible/kolla-ansible/ansible
    ansible-playbook -i inventory/all-in-one -e@../etc/kolla/globals.yml -e@../etc/kolla/passwords.yml -e action=bootstrap-servers kolla-host.yml
```

2. Deploying the containers
```shell
     ansible-playbook -i inventory/all-in-one -e@../etc/kolla/globals.yml -e@../etc/kolla/passwords.yml -e action=deploy site.yml
```
3. Create the /etc/kolla/admin-openrc.sh file to setup the environment parameters if you want to run open stack cli client commands
```shell
     ansible-playbook -v -i inventory/all-in-one -e@../etc/kolla/globals.yml -e@../etc/kolla/passwords.yml -e action=deploy post-deploy.yml
```

4. **After** deploying the contrail services (**not before**), run this playbook to install the open stack client packages and to disable the nova-compute service on the open stack node in the case of open stack node being different from the contrail compute node.
```shell
    ansible-playbook -vvv -i inventory/two-node-kolla.inv -e@../etc/kolla/globals.yml -e@../etc/kolla/passwords.yml -e action=deploy post-deploy-contrail.yml
```