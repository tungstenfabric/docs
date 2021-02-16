.. _installing-a-standalone-red-hat-openshift-container-platform-311-cluster-with-tf-using-tf-openshift-deployer:

Installing a Standalone Red Hat OpenShift Container Platform 3.11 Cluster with TF Using TF OpenShift Deployer
=============================================================================================================

:date: 2020-10-21

You can install Tungsten Fabric together with a standalone Red Hat
OpenShift Container Platform 3.11 cluster using TF OpenShift
deployer. Consider the topology illustrated here.

|Figure 1: Sample installation topology|

Prerequisites

The recommended system requirements are:

.. list-table:: 
   :header-rows: 1

   * - System Requirements
     - Master Node
     - Infrastructure Node
     - Compute Node
   * - CPU/RAM
     - 8 vCPU, 16 GB RAM
     - 16 vCPU, 64 GB RAM
     - As per OpenShift recommendations.
   * - Disk
     - 100 GB
     - 250 GB
     - 

.. note::

   If you use NFS mount volumes, check disk capacity and mounts. Also,
   openshift-logging with NFS is not recommended.

Perform the following steps to install a standalone OpenShift 3.11
cluster along with Tungsten Fabric using
contrail-openshift-deployer.

1. 

   .. raw:: html

      <div id="jd0e78">

   Set up environment nodes for RHEL OpenShift enterprise installations:

   1. Subscribe to RHEL.

      ``(all-nodes)# subscription-manager register --username <> --password <> --force``

   2. From the list of available subscriptions, find and attach the pool
      ID for the OpenShift Container Platform subscription.

      ``(all-nodes)# subscription-manager attach --pool=pool-ID``

   3. Disable all yum repositories.

      ``(all-nodes)# subscription-manager repos --disable="*"``

   4. Enable only the required repositories.

      ::

          (all-nodes)# subscription-manager repos \
             --enable="rhel-7-server-rpms" \
             --enable="rhel-7-server-extras-rpms" \
             --enable="rhel-7-server-ose-3.11-rpms" \
             --enable=rhel-7-fast-datapath-rpms \
             --enable="rhel-7-server-ansible-2.6-rpms"

   5. Install required packages, such as python-netaddr,
      iptables-services, and so on.

      ``(all-nodes)# yum install -y tcpdump wget git net-tools bind-utils yum-utils iptables-services bridge-utils bash-completion kexec-tools sos psacct python-netaddr openshift-ansible``

   .. note::
      CentOS OpenShift Origin installations are not supported.
2. Get the files from the latest tar ball. Download the OpenShift
   Container Platform install package from Juniper software download
   site and modify the contents of the ``openshift-ansible`` inventory
   file.

   1. Download the Openshift Deployer
      (``contrail-openshift-deployer-release-tag.tgz``) installer from
      the Juniper software download site,
      https://www.juniper.net/support/downloads/?p=contrail#sw. See
      `README Access for Tungsten Fabric Registry
      19xx <https://www.juniper.net/documentation/en_US/contrail19/information-products/topic-collections/release-notes/readme-contrail-19.pdf>`__  
      for appropriate release tags.

   2. Copy the install package to the node from where Ansible is
      deployed. Ensure that the node has password-free access to the
      OpenShift primary and slave nodes.

      ``scp contrail-openshift-deployer-release-tag.tgz openshift-ansible-node:/root/``

   3. Log in to the Ansible node and untar the
      contrail-openshift-deployer-``release-tag``.tgz package.

      ``tar -xzvf  contrail-openshift-deployer-release-tag.tgz -C /root/``

   4. Verify the contents of the ``openshift-ansible`` directory.

      ``cd /root/openshift-ansible/``

   5. Modify the ``inventory/ose-install`` file to match your OpenShift
      environment.

      Populate the ``inventory/ose-install`` file with TF
      configuration parameters specific to your system. The following
      mandatory parameters must be set. For example:

      ::

         contrail_version=5.1
         contrail_container_tag=<>
         contrail_registry="hub.juniper.net/contrail-nightly"
         contrail_registry_username=<>
         contrail_registry_password=<>
         openshift_use_openshift_sdn=false
         os_sdn_network_plugin_name='cni'
         openshift_use_contrail=true

      .. note::

         The ``contrail_container_tag`` value for this release can be found
         in the `README Access to Contrail Registry
         19XX </documentation/en_US/contrail19/information-products/topic-collections/release-notes/readme-contrail-19.pdf>`__  
         file.

         Juniper Networks recommends that you obtain the Ansible source
         files from the latest release.

   This procedure assumes that there is one primary node, one
   infrastructure node, and one compute node.

   ::

      master : server1 (1x.xx.xx.11)
      infrastructure : server2 (1x.xx.xx.22)
      compute : server3 (1x.xx.xx.33)

3. Edit ``/etc/hosts`` to include all the nodes information.

   ::

      [root@server1]# cat /etc/hosts
      127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
      ::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
      1x.xx.xx.100 puppet
      1x.xx.xx.11 server1.contrail.juniper.net server1
      1x.xx.xx.22 server2.contrail.juniper.net server2
      1x.xx.xx.33 server3.contrail.juniper.net server3

4. Set up password-free SSH access to the Ansible node and all the
   nodes.

   ::

      ssh-keygen -t rsa
      ssh-copy-id root@1x.xx.xx.11
      ssh-copy-id root@1x.xx.xx.22
      ssh-copy-id root@1x.xx.xx.33

5. Run Ansible playbook to install OpenShift Container Platform with
   TF. Before you run Ansible playbook, ensure that you have
   edited ``inventory/ose-install`` file.

   ::

      (ansible-node)# cd /root/openshift-ansible
      (ansible-node)# ansible-playbook -i inventory/ose-install playbooks/prerequisites.yml
      (ansible-node)# ansible-playbook -i inventory/ose-install playbooks/deploy_cluster.yml

   For a sample ``inventory/ose-install`` file, see `Sample
   inventory/ose-install
   File <install-openshift-using-anible-311.html#sample_ose_install>`__.

6. Create a password for the admin user to log in to the UI from the
   primary node.

   ::

      (master-node)# htpasswd /etc/origin/master/htpasswd admin

   .. note::

      If you are using a load balancer, you must manually copy the htpasswd
      file into all your primary nodes.

7. Assign cluster-admin role to admin user.

   ::

      (master-node)# oc adm policy add-cluster-role-to-user cluster-admin admin
      (master-node)# oc login -u admin

8. Open a Web browser and type the entire fqdn name of your primary node
   or load balancer node, followed by :8443/console.

   ::

      https://<your host name from your ose-install inventory>:8443/console

   Use the user name and password created in step
   `6 <install-openshift-using-anible-311.html#loginpass>`__ to log in
   to the Web console.

   Your DNS should resolve the host name for access. If the host name is
   not resolved, modify the /etc/hosts file to route to the above host.

.. note::

   OpenShift 3.11 cluster upgrades are not supported.

**Sample inventory/ose-install File**

::

   [OSEv3:vars]

   ###########################################################################
   ### OpenShift Basic Vars
   ###########################################################################
   openshift_deployment_type=openshift-enterprise
   deployment_type=openshift-enterprise
   containerized=false
   openshift_disable_check=docker_image_availability,memory_availability,package_availability,disk_availability,package_version,docker_storage

   # Default node selectors
   openshift_hosted_infra_selector="node-role.kubernetes.io/infra=true"

   oreg_auth_user=<>
   oreg_auth_password=<>

   ###########################################################################
   ### OpenShift Master Vars
   ###########################################################################

   openshift_master_api_port=8443
   openshift_master_console_port=8443
   openshift_master_cluster_method=native

   # Set this line to enable NFS
   openshift_enable_unsupported_configurations=True


   ###########################################################################
   ### OpenShift Network Vars
   ###########################################################################

   openshift_use_openshift_sdn=false
   os_sdn_network_plugin_name='cni'
   openshift_use_contrail=true

   ###########################################################################
   ### OpenShift Authentication Vars
   ###########################################################################

   # htpasswd Authentication
   openshift_master_identity_providers=[{'name': 'htpasswd_auth', 'login': 'true', 'challenge': 'true', 'kind': 'HTPasswdPasswordIdentityProvider'}]

   ###########################################################################
   ### OpenShift Router and Registry Vars
   ###########################################################################

   openshift_hosted_router_replicas=1
   openshift_hosted_registry_replicas=1

   openshift_hosted_registry_storage_kind=nfs
   openshift_hosted_registry_storage_access_modes=['ReadWriteMany']
   openshift_hosted_registry_storage_nfs_directory=/export
   openshift_hosted_registry_storage_nfs_options='*(rw,root_squash)'
   openshift_hosted_registry_storage_volume_name=registry
   openshift_hosted_registry_storage_volume_size=10Gi
   openshift_hosted_registry_pullthrough=true
   openshift_hosted_registry_acceptschema2=true
   openshift_hosted_registry_enforcequota=true
   openshift_hosted_router_selector="node-role.kubernetes.io/infra=true"
   openshift_hosted_registry_selector="node-role.kubernetes.io/infra=true"

   ###########################################################################
   ### OpenShift Service Catalog Vars
   ###########################################################################

   openshift_enable_service_catalog=True

   template_service_broker_install=True
   openshift_template_service_broker_namespaces=['openshift']

   ansible_service_broker_install=True

   openshift_hosted_etcd_storage_kind=nfs
   openshift_hosted_etcd_storage_nfs_options="*(rw,root_squash,sync,no_wdelay)"
   openshift_hosted_etcd_storage_nfs_directory=/export
   openshift_hosted_etcd_storage_labels={'storage': 'etcd-asb'}
   openshift_hosted_etcd_storage_volume_name=etcd-asb
   openshift_hosted_etcd_storage_access_modes=['ReadWriteOnce']
   openshift_hosted_etcd_storage_volume_size=2G

   ###########################################################################
   ### OpenShift Metrics and Logging Vars
   ###########################################################################
   # Enable cluster metrics
   openshift_metrics_install_metrics=True

   openshift_metrics_storage_kind=nfs
   openshift_metrics_storage_access_modes=['ReadWriteOnce']
   openshift_metrics_storage_nfs_directory=/export
   openshift_metrics_storage_nfs_options='*(rw,root_squash)'
   openshift_metrics_storage_volume_name=metrics
   openshift_metrics_storage_volume_size=2Gi
   openshift_metrics_storage_labels={'storage': 'metrics'}

   openshift_metrics_cassandra_nodeselector={"node-role.kubernetes.io/infra":"true"}
   openshift_metrics_hawkular_nodeselector={"node-role.kubernetes.io/infra":"true"}
   openshift_metrics_heapster_nodeselector={"node-role.kubernetes.io/infra":"true"}

   # Enable cluster logging. (( 
   ####openshift_logging_install_logging=True
   openshift_logging_install_logging=False
   #openshift_logging_storage_kind=nfs
   #openshift_logging_storage_access_modes=['ReadWriteOnce']
   #openshift_logging_storage_nfs_directory=/export
   #openshift_logging_storage_nfs_options='*(rw,root_squash)'
   #openshift_logging_storage_volume_name=logging
   #openshift_logging_storage_volume_size=5Gi
   #openshift_logging_storage_labels={'storage': 'logging'}
   #openshift_logging_es_cluster_size=1
   #openshift_logging_es_nodeselector={"node-role.kubernetes.io/infra":"true"}
   #openshift_logging_kibana_nodeselector={"node-role.kubernetes.io/infra":"true"}
   #openshift_logging_curator_nodeselector={"node-role.kubernetes.io/infra":"true"}

   ###########################################################################
   ### OpenShift Prometheus Vars
   ###########################################################################

   ## Add Prometheus Metrics:
   openshift_hosted_prometheus_deploy=True
   openshift_prometheus_node_selector={"node-role.kubernetes.io/infra":"true"}
   openshift_prometheus_namespace=openshift-metrics

   # Prometheus
   openshift_prometheus_storage_kind=nfs
   openshift_prometheus_storage_access_modes=['ReadWriteOnce']
   openshift_prometheus_storage_nfs_directory=/export
   openshift_prometheus_storage_nfs_options='*(rw,root_squash)'
   openshift_prometheus_storage_volume_name=prometheus
   openshift_prometheus_storage_volume_size=1Gi
   openshift_prometheus_storage_labels={'storage': 'prometheus'}
   openshift_prometheus_storage_type='pvc'

   # For prometheus-alertmanager
   openshift_prometheus_alertmanager_storage_kind=nfs
   openshift_prometheus_alertmanager_storage_access_modes=['ReadWriteOnce']
   openshift_prometheus_alertmanager_storage_nfs_directory=/export
   openshift_prometheus_alertmanager_storage_nfs_options='*(rw,root_squash)'
   openshift_prometheus_alertmanager_storage_volume_name=prometheus-alertmanager
   openshift_prometheus_alertmanager_storage_volume_size=1Gi
   openshift_prometheus_alertmanager_storage_labels={'storage': 'prometheus-alertmanager'}
   openshift_prometheus_alertmanager_storage_type='pvc'

   # For prometheus-alertbuffer
   openshift_prometheus_alertbuffer_storage_kind=nfs
   openshift_prometheus_alertbuffer_storage_access_modes=['ReadWriteOnce']
   openshift_prometheus_alertbuffer_storage_nfs_directory=/export
   openshift_prometheus_alertbuffer_storage_nfs_options='*(rw,root_squash)'
   openshift_prometheus_alertbuffer_storage_volume_name=prometheus-alertbuffer
   openshift_prometheus_alertbuffer_storage_volume_size=1Gi
   openshift_prometheus_alertbuffer_storage_labels={'storage': 'prometheus-alertbuffer'}
   openshift_prometheus_alertbuffer_storage_type='pvc'


   #########################################################################
   ### Openshift HA
   #########################################################################

   # Openshift HA
   openshift_master_cluster_hostname=load-balancer-0-3eba0c20dc494dfc93d5d50d06bbde89
   openshift_master_cluster_public_hostname=load-balancer-0-3eba0c20dc494dfc93d5d50d06bbde89


   #########################################################################
   ### TF Variables
   ########################################################################

   service_subnets="172.30.0.0/16"
   pod_subnets="10.128.0.0/14"

   # Below are TF variables. Comment them out if you don't want to install Contrail through ansible-playbook
   contrail_version=5.1
   contrail_container_tag=<>
   contrail_registry=hub.juniper.net/contrail
   contrail_registry_username=<>
   contrail_registry_password=<>
   openshift_docker_insecure_registries=hub.juniper.net/contrail
   contrail_nodes=[10.0.0.5,10.0.0.3,10.0.0.4]
   vrouter_physical_interface=eth0


   ###########################################################################
   ### OpenShift Hosts
   ###########################################################################
   [OSEv3:children]
   masters
   etcd
   nodes
   lb
   nfs
   openshift_ca

   [masters]
   kube-master-2-3eba0c20dc494dfc93d5d50d06bbde89
   kube-master-1-3eba0c20dc494dfc93d5d50d06bbde89
   kube-master-0-3eba0c20dc494dfc93d5d50d06bbde89

   [etcd]
   kube-master-2-3eba0c20dc494dfc93d5d50d06bbde89
   kube-master-1-3eba0c20dc494dfc93d5d50d06bbde89
   kube-master-0-3eba0c20dc494dfc93d5d50d06bbde89

   [lb]
   load-balancer-0-3eba0c20dc494dfc93d5d50d06bbde89

   [nodes]
   kube-master-2-3eba0c20dc494dfc93d5d50d06bbde89 openshift_node_group_name='node-config-master'
   controller-0-3eba0c20dc494dfc93d5d50d06bbde89 openshift_node_group_name='node-config-infra'
   compute-1-3eba0c20dc494dfc93d5d50d06bbde89 openshift_node_group_name='node-config-compute'
   controller-2-3eba0c20dc494dfc93d5d50d06bbde89 openshift_node_group_name='node-config-infra'
   kube-master-1-3eba0c20dc494dfc93d5d50d06bbde89 openshift_node_group_name='node-config-master'
   kube-master-0-3eba0c20dc494dfc93d5d50d06bbde89 openshift_node_group_name='node-config-master'
   compute-0-3eba0c20dc494dfc93d5d50d06bbde89 openshift_node_group_name='node-config-compute'
   controller-1-3eba0c20dc494dfc93d5d50d06bbde89 openshift_node_group_name='node-config-infra'

   [nfs]
   load-balancer-0-3eba0c20dc494dfc93d5d50d06bbde89

   [openshift_ca]
   kube-master-2-3eba0c20dc494dfc93d5d50d06bbde89
   kube-master-1-3eba0c20dc494dfc93d5d50d06bbde89
   kube-master-0-3eba0c20dc494dfc93d5d50d06bbde89

.. note::

   The /etc/resolv.conf must have write permissions.

Caveats and Troubleshooting Instructions

-  If a Java error occurs, install the
   ``yum install java-1.8.0-openjdk-devel.x86_64`` package and rerun
   ``deploy_cluster``.

-  If the service_catalog parameter does not pass but the cluster is
   operational, check whether the ``/etc/resolv.conf`` has cluster.local
   in its search line, and the nameserver as host IP address.

-  NTP is installed by OpenShift and must be synchronized by the user.
   This does not affect any TF functionality but is displayed in
   the contrail-status output.

-  If the ansible_service_broker component of OpenShift is not up and
   its ansible_service_broker_deploy displays an error, it means that
   the ansible_service_broker pod did not come up properly. The most
   likely reason is that the ansible_service_broker pod failed its
   liveliness and readiness checks. Modify the liveliness and readiness
   checks of this pod when it’s brought online to make it operational.
   Also, verify that the ansible_service_broker pod uses the correct URL
   from Red Hat.

 

.. |Figure 1: Sample installation topology| image:: images/g300780.png
