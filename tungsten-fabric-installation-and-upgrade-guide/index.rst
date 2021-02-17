:orphan:

Tungsten Fabric installation and upgrade guide
==============================================

Use this guide to install and upgrade Tungsten Fabric solution. This guide covers various installation scenarios including:

* Tungsten Fabric with VMware vCenter.
* Tungsten Fabric with Red Hat.
* Tungsten Fabric with Kolla/Ocata OpenStack.
* Tungsten Fabric with Juju Charms.


Documentation Structure
-----------------------

Understanding Tungsten Fabric
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* :doc:`understanding-tf` 
* :doc:`understanding-tf-components` 
* :doc:`summary-of-container-design`
* :doc:`intro-microservices-tf`  
  
Supported platforms and server requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* :doc:`hardware-reqs-vnc`
  
Upgrading Tungsten Fabric
~~~~~~~~~~~~~~~~~~~~~~~~~

* :doc:`installing-tf-ansible-ziu`
* :doc:`install-tf-rhosp-ziu`
* :doc:`update-canonical-openstack-juju`
* :doc:`upgrade-tf-ansible-deployer`
* :doc:`upgrade-in-place`

Backup and restore Tungsten Fabric
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* :doc:`backup-using-json-50`

Using Tungsten Fabric with VMware vCenter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* :doc:`vcenter-tf`
* :doc:`install-tf-vRO-plugin`
* :doc:`integrating-tf501-with-vRO`  
* :doc:`vcenter-as-orchestrator-deployment-scenarios-501`

Using Tungsten Fabric with OpenStack
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Setting Up Contrail with Red Hat OpenStack 16.1
***********************************************

* :doc:`setting-up-tf-rhosp16-introduction`
* :doc:`setting-up-tf-rhosp16-infrastructure`
* :doc:`setting-up-tf-rhosp16-undercloud`
* :doc:`setting-up-tf-rhosp16-overcloud`

Setting Up Contrail with Red Hat OpenStack 13
*********************************************

* :doc:`setting-up-tf-rhosp-introduction`
* :doc:`setting-up-tf-rhosp-infrastructure`
* :doc:`setting-up-tf-rhosp-undercloud`
* :doc:`setting-up-tf-rhosp-overcloud`
* :doc:`smartnic-vrouter-support`
* :doc:`rhosp-octavia`

Configuring Virtual Networks
****************************

* :doc:`creating-projects-vnc`
* :doc:`creating-virtual-network-vnc`
* :doc:`creating-image-vnc`
* :doc:`creating-security-groups`

Using Contrail Resources in Heat Templates
******************************************

* :doc:`heat-template-vnc`
   
QoS Support in Contrail Networking
**********************************

* :doc:`network-qos-vnc-3.1`
* :doc:`network-qos-configuring`

Load Balancers
**************

* :doc:`lbaas-tf3-F5`
* :doc:`lbaas-v2-vnc`
* :doc:`load-balance-as-service-vnc`

Optimizing Tungsten Fabric
**************************

* :doc:`multiqueue-virtio-vnc`

Tungsten Fabric OpenStack Analytics
***********************************

* :doc:`ceilometer-configuring`

TF OpenStack APIs
*****************

* :doc:`neutron-perform-improve-vnc`

Using Tungsten Fabric with Juju Charms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* :doc:`deploying-tf-using-juju-charms`
* :doc:`deploying-tf-using-juju-charms-kubernetes`
* :doc:`juju-charms-nested-kubernetes`
* :doc:`canonical-octavia`

Post Installation Tasks
~~~~~~~~~~~~~~~~~~~~~~~

* :doc:`role-resource-access-control-vmc`
* :doc:`rbac-analytics-api`
* :doc:`config-control-node-with-bgp`
* :doc:`md5-authentication-configuring`
* :doc:`config-TLS-vncDocument1`
* :doc:`graceful-restart-bgp-persist-vnc`
  
.. toctree::
   :maxdepth: 1
   :hidden:
   :titlesonly:
   
   backup-using-json-50
   canonical-octavia
   ceilometer-configuring
   config-TLS-vncDocument1
   config-control-node-with-bgp
   creating-image-vnc
   creating-projects-vnc
   creating-security-groups
   creating-virtual-network-vnc
   deploying-tf-using-juju-charms-kubernetes
   deploying-tf-using-juju-charms
   graceful-restart-bgp-persist-vnc
   hardware-reqs-vnc
   heat-template-vnc
   how-to-install-tf-networking-openshift4
   install-tf-rhosp-ziu
   install-tf-vRO-plugin
   install-nested-openshift-311-using-anible
   install-openshift-using-anible-311
   installing-tf-ansible-ziu
   install-tf-rhosp-ziu
   integrating-tf501-with-vRO
   intro-microservices-tf
   juju-charms-nested-kubernetes
   lbaas-tf3-F5
   lbaas-v2-vnc
   load-balance-as-service-vnc
   md5-authentication-configuring
   multiqueue-virtio-vnc
   network-qos-configuring
   network-qos-vnc-3.1
   neutron-perform-improve-vnc
   provisioning-k8s-cluster
   rbac-analytics-api
   rhosp-octavia
   role-resource-access-control-vmc
   setting-up-tf-rhosp-infrastructure
   setting-up-tf-rhosp-introduction
   setting-up-tf-rhosp-overcloud
   setting-up-tf-rhosp-undercloud
   setting-up-tf-rhosp16-infrastructure
   setting-up-tf-rhosp16-introduction
   setting-up-tf-rhosp16-overcloud
   setting-up-tf-rhosp16-undercloud
   smartnic-vrouter-support
   summary-of-container-design
   understanding-tf-components
   understanding-tf
   update-canonical-openstack-juju
   upgrade-tf-ansible-deployer
   upgrade-in-place
   vcenter-as-orchestrator-deployment-scenarios-501
   vcenter-tf