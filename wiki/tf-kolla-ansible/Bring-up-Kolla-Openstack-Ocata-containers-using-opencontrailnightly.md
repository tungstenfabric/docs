This page describes the steps involved in bringing up the Kolla Openstack Containers packaged with Contrail in an effort to bring up a cluster based on Contrail micro services (using contrail-ansible-deployer). 

# Pre-requisites for the base host

The steps given below assume a **Centos 7.4** base host. 

1. `yum install -y epel-release `

3. Install Ansible 2.3 (centos by default will install 2.4 which does not work with kolla playbooks). Also the kolla playbooks require version 2.8 or greater of the jinja2 library.
```shell
    yum -y install centos-release-openstack-ocata
    yum -y install ansible-2.3.1.0
    yum -y install python-oslo-config
    yum -y install git
```
4. This is required for "keepalived" to work:
```shell
    modprobe ip_vs
```
5. `git clone https://github.com/Juniper/contrail-kolla-ansible.git`

6. `cd contrail-kolla-ansible && git checkout contrail/pike`

# Setting required parameters in the inventory
1. Ensure the following parameters are set in contrail-kolla-ansible/etc/kolla/globals.yml:
```yaml
    openstack_release: ocata

    # Refer to https://github.com/Juniper/contrail-kolla-ansible/blob/stable/ocata/ansible/group_vars/all.yml for explanations of each variable. Following parameters might need customization
  
    kolla_base_distro: "centos"
    kolla_install_type: "binary"
    kolla_internal_vip_address: 192.168.1.150 <- This has to be a virtual IP
    network_interface: eth1
    neutron_external_interface: "eth2"
    kolla_external_vip_address: 192.168.1.150 <- This has to be a virtual IP and can be different from the one above. In that case the external_vip_interface also needs to be different.
    kolla_external_vip_interface: eth1
    neutron_plugin_agent: opencontrail

    opencontrail_release: "5.0.0-1"
    opencontrail_api_server_ip: "192.168.1.50"
    opencontrail_api_server_port: "8082"
    enable_openvswitch: "no"
    enable_neutron_bgp_dragent: "no"
    enable_neutron_dvr: "no"
    enable_neutron_lbaas: "no"
    enable_neutron_fwaas: "no"
    enable_neutron_qos: "no"
    enable_neutron_agent_ha: "no"
    enable_neutron_vpnaas: "no"
    enable_neutron_sfc: "no"
    enable_host_ntp: "no"
    neutron_opencontrail_init_image_full: "opencontrailnightly/contrail-openstack-neutron-init"
    nova_compute_opencontrail_init_image_full: "opencontrailnightly/contrail-openstack-compute-init"

```

# Setting required passwords
1. Ensure the following parameters are set in contrail-kolla-ansible/etc/kolla/passwords.yml
   Refer to the contrail/ocata branch of contrail-kolla-ansible repo for an example [here].(https://github.com/Juniper/contrail-kolla-ansible/blob/contrail/ocata/etc/kolla/passwords.yml)

   Generate the keys using ssh-keygen and make sure you copy your public key in the public key sections
   of 'nova_ssh_key','kolla_ssh_key', 'keystone_ssh_key','bifrost_ssh_key'
   

# Running the playbooks
1. Run the bootstrap playbook to setup the host with the required packages etc. to launch the open stack containers
```shell
    cd contrail-kolla-ansible/ansible
    ansible-playbook -i inventory/all-in-one -e@../etc/kolla/globals.yml -e@../etc/kolla/passwords.yml -e action=bootstrap-servers kolla-host.yml

   After this step, please pull in the neutron-init and compute-init images from the opencontrailnightly
   docker pull opencontrailnightly/contrail-openstack-neutron-init
   docker pull opencontrailnightly/contrail-openstack-compute-init
```

2. Deploying the containers
```shell
     ansible-playbook -i inventory/all-in-one -e@../etc/kolla/globals.yml -e@../etc/kolla/passwords.yml -e action=deploy site.yml
```
3. Create the /etc/kolla/admin-openrc.sh file to setup the environment parameters if you want to run open stack cli client commands
```shell
     ansible-playbook -i inventory/all-in-one -e@../etc/kolla/globals.yml -e@../etc/kolla/passwords.yml -e action=deploy post-deploy.yml
```

#Install the python openstack client on the host:

```
yum install -y python-openstackclient
```