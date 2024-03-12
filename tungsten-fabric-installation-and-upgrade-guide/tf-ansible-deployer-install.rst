.. This work is licensed under the Creative Commons Attribution 4.0 International License.
   To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

===============================================================
Installing Tungsten Fabric with Ansible Deployer
===============================================================

Prerequisites
-------------

The deployment instructions presented in this document install and configure Tungsten Fabric SDN solution in a 3 node environment (1 OpenStack/Tungsten Fabric Controller, 2 OpenStack/Tungsten Fabric Computes) using OpenStack as the orchestrator. We will further refer to the 3 nodes we are installing onto as the 'target nodes'.

A node can be either a virtual machine or a bare-metal server -- by using the bms provider ansible-deployer uses SSH to connect to the target nodes.

The Tungsten Fabric solution is provisioned via the `Ansible` automation tool. In order to deploy Tungsten Fabric solution we also need another node from which we will run the `ansible-playbook` commands. This node can be a container, virtual machine, or a bare-metal server. We will refer to this node as 'deployer node'. The deployer node is required in addition to the target nodes that will make up the OpenStack/Tungsten Fabric cluster.

Supported Operating Systems for the Target nodes and the Deploy node are `RedHat7` based or greater and `CentOS7` or greater.


Hardware and Software Requirements
----------------------------------

Before deploying ensure the hardware on which we will deploy matches the minimum requirements. Below are specified the minimum hardware and software requirements that need to be met for a smooth Tungsten Fabric experience.

Hardware:

   * Control Nodes:
         * At least 4 CPU cores
         * At least 64 GB RAM
         * At least 300 GB storage
         * At least one Ethernet port
   * Compute Nodes:
         * At least 2 CPU cores
         * At least 8 GB RAM
         * At least 64 GB storage
         * At least one Ethernet port
   * Deploy Node:
         * At least 1 CPU core
         * At least 4 GB RAM
         * At least 16 GB storage
         * At least one Ethernet port
     
Software -- For details around the supported software versions for each version of Tungsten Fabric consult the release notes.

For more information see: `Tugnsten Fabirc Releases`_ 


Steps on All Target Nodes
-------------------------

Ansible Deployer will use SSH to connect to each target node and perform the steps required for the installation SSH Keys or password configuration is required.

#. Generate SSH public key:

   ``# ssh-keygen -t rsa``

#. Copy SSH public key (from each Target node) to the Deploy node:

   ``# ssh-copy-id root@<Deploy_Node_IP_Address>``

Steps on the Deploy Node
---------------------------

Please note that all commands, on the Deploy node, have been run as **root**.

#. Install prerequisites:

   ``# yum install -y yum-plugin-priorities yum-utils vim net-tools git ansible``

#. Generate SSH public key:

   ``# ssh-keygen -t rsa``

#. Copy SSH public key from the Deploy node to the 3 Target nodes:

   ``# ssh-copy-id root@<Target_Node_IP_Addresses>``

#. Clone the `contrail-ansible-deployer` repo with the desired branch:

   ``# git clone https://github.com/Juniper/contrail-ansible-deployer.git -b R21.05``

#. Replace the content of `contrail-ansible-deployer/config/instances.yaml` with the following and fill in placeholders - marked as ``<...>`` - with info from your setup:

   The target nodes for both control and compute can have one or more network interface. Where multiple network interfaces are used, for example in deployments with dedicated management interfaces, it is possible to specify which interface should be used for Tungsten Fabric. 

   The information regarding the dataplane interface configuration is set in the following lines in ``instances.yaml``:

   ``PHYSICAL_INTERFACE: <Iface_Name_That_vhost0_Will_Use>``

   ``VROUTER_GATEWAY: <Gateway_IP_Address_for_Dataplane_Network>``

   Therefore, if we have a 2nd Ethernet port for the dataplane traffic, we will fill in the placeholders from the lines above with info associated to the 2nd Ethernet port.
   Otherwise, if only 1 Ethernet port is used, we will fill in all the placeholders with info associated to this Ethernet port.

::

       global_configuration:
         CONTAINER_REGISTRY: hub.docker.com/tungstenfabric
       provider_config:
         bms:
           ssh_pwd: <ssh_root_password>
           ssh_user: root
           ntpserver: pool.ntp.org
           domainsuffix: local
       instances:
         bms1:
           provider: bms
           ip: &tungsten_fabric_ip_address <Tungsten_Fabric_Controller_Mgmt_IP_Address>
           roles:
               config_database:
               config:
               control:
               analytics:
               analytics_database:
               analytics_alarm:
               analytics_snmp:
               webui:
               openstack:
         bms2:
           provider: bms
           ip: <Tungsten_Fabric_Compute1_Mgmt_IP_Address>
           roles:
               vrouter:
                 PHYSICAL_INTERFACE: <optional dataplane interface parameter>
                 VROUTER_GATEWAY: <optional dataplane gateway parameter>
               openstack_compute:
         bms3:
           provider: bms
           ip: <Tungsten_Fabric_Compute2_Mgmt_IP_Address>
           roles:
               vrouter:
                 PHYSICAL_INTERFACE: <optional dataplane interface parameter>
                 VROUTER_GATEWAY: <optional dataplane gateway parameter>
               openstack_compute:
       contrail_configuration:
         CONTRAIL_VERSION: R21.05
         CONTRAIL_CONTAINER_TAG: R21.05
         CLOUD_ORCHESTRATOR: openstack
         RABBITMQ_NODE_PORT: 5673
         VROUTER_GATEWAY: <Gateway_IP_Address_for_Dataplane_Network>
         PHYSICAL_INTERFACE: <Iface_Name_That_vhost0_Will_Use>
         AUTH_MODE: keystone
         KEYSTONE_AUTH_URL_VERSION: /v3
         KEYSTONE_AUTH_ADMIN_USER: admin
         KEYSTONE_AUTH_ADMIN_PASSWORD: <KeyStone_Admin_Password>
         ENCAP_PRIORITY: VXLAN,MPLSoUDP,MPLSoGRE
       kolla_config:
         kolla_globals:
           openstack_release: rocky
           enable_haproxy: no
           enable_ironic: no
           enable_swift: no
         kolla_passwords:
           keystone_admin_password: *keystone_passwd

6. Go to `contrail-ansible-deployer` folder and run the following `ansible-playbook` commands:

   ``# cd contrail-ansible-deployer``

   ``# ansible-playbook -i inventory/ -e orchestrator=openstack playbooks/configure_instances.yml``

   ``# ansible-playbook -i inventory/ playbooks/install_openstack.yml``

   ``# ansible-playbook -i inventory/ -e orchestrator=openstack playbooks/install_contrail.yml``

#. After the Tungsten Fabric deployment, we can run ``contrail-status`` command on both Tungsten Fabric Controller node and Tungsten Fabric Compute Node(s) to check whether Tungsten Fabric Docker containers are up and running. A successful installation should display all Tungsten Fabric containers as `active`.

   Below it is displayed the output of ``# contrail-status`` command run on Tungsten Fabric Controller node and on Tungsten Fabric Compute node, respectively:

   ``# contrail-status``

::

   == Contrail control ==
   control: active
   nodemgr: active
   named: active
   dns: active

   == Contrail config-database ==
   nodemgr: active
   zookeeper: active
   rabbitmq: active
   cassandra: active

   == Contrail database ==
   kafka: active
   nodemgr: active
   zookeeper: active
   cassandra: active

   == Contrail analytics ==
   snmp-collector: active
   query-engine: active
   api: active
   alarm-gen: active
   nodemgr: active
   collector: active
   topology: active

   == Contrail webui ==
   web: active
   job: active

   == Contrail config ==
   api: active
   zookeeper: active
   svc-monitor: backup
   nodemgr: active
   device-manager: active
   cassandra: active
   rabbitmq: active
   schema: active

   # contrail-status

::

   vrouter kernel module is PRESENT
   == Contrail vrouter ==
   nodemgr: active
   agent: active


Manage Tungsten Fabric
----------------------

Next, the user can login via Tungsten Fabric Web UI, by accessing:

``https://<Tungsten_Fabric_Controller_Mgmt_IP_Address>:8143``

with the following credentials:

Username: ``admin``

Password: ``<KeyStone_Admin_Password>``



.. _Tugnsten Fabirc Releases: ../release/index.html



