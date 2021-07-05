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

.. toctree::
   :maxdepth: 1
   :titlesonly:
   
   understanding-tf
   understanding-tf-components 
   summary-of-container-design
   intro-microservices-tf  
  
Supported platforms and server requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 1
   :titlesonly:

   hardware-reqs-vnc
  
Upgrading Tungsten Fabric
~~~~~~~~~~~~~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 1
   :titlesonly:

   installing-tf-ansible-ziu
   install-tf-rhosp-ziu
   update-canonical-openstack-juju
   upgrade-tf-ansible-deployer
   upgrade-in-place
   ffu-ziu-rhosp16.1-cn

Backup and restore Tungsten Fabric
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 1
   :titlesonly:

   backup-using-json-50

Using Tungsten Fabric with VMware vCenter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 1
   :titlesonly:

   vcenter-tf
   install-tf-vRO-plugin
   integrating-tf501-with-vRO
   vcenter-as-orchestrator-deployment-scenarios-501

Using Tungsten Fabric with OpenStack
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Setting Up Contrail with Red Hat OpenStack 16.1
***********************************************

.. toctree::
   :maxdepth: 1
   :titlesonly:

   setting-up-tf-rhosp16-introduction
   setting-up-tf-rhosp16-infrastructure
   setting-up-tf-rhosp16-undercloud
   setting-up-tf-rhosp16-overcloud

Setting Up Contrail with Red Hat OpenStack 13
*********************************************

.. toctree::
   :maxdepth: 1
   :titlesonly:

   setting-up-tf-rhosp-introduction
   setting-up-tf-rhosp-infrastructure
   setting-up-tf-rhosp-undercloud
   setting-up-tf-rhosp-overcloud
   smartnic-vrouter-support
   rhosp-octavia

Configuring Virtual Networks
****************************

.. toctree::
   :maxdepth: 1
   :titlesonly:

   creating-projects-vnc
   creating-virtual-network-vnc
   creating-image-vnc
   creating-security-groups

Using Contrail Resources in Heat Templates
******************************************

.. toctree::
   :maxdepth: 1
   :titlesonly:

   heat-template-vnc
   
QoS Support in Contrail Networking
**********************************

.. toctree::
   :maxdepth: 1
   :titlesonly:

   network-qos-vnc-3.1
   network-qos-configuring

Load Balancers
**************

.. toctree::
   :maxdepth: 1
   :titlesonly:

   lbaas-tf3-F5
   lbaas-v2-vnc
   load-balance-as-service-vnc

Optimizing Tungsten Fabric
**************************

.. toctree::
   :maxdepth: 1
   :titlesonly:

   multiqueue-virtio-vnc

Tungsten Fabric OpenStack Analytics
***********************************

.. toctree::
   :maxdepth: 1
   :titlesonly:

   ceilometer-configuring

TF OpenStack APIs
*****************

.. toctree::
   :maxdepth: 1
   :titlesonly:

   neutron-perform-improve-vnc

Using Tungsten Fabric with Juju Charms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 1
   :titlesonly:

   deploying-tf-using-juju-charms
   deploying-tf-using-juju-charms-kubernetes
   juju-charms-nested-kubernetes
   canonical-octavia
   smartnic-vrouter-juju-charms

Post Installation Tasks
~~~~~~~~~~~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 1
   :titlesonly:

   role-resource-access-control-vmc
   rbac-analytics-api
   config-control-node-with-bgp
   md5-authentication-configuring
   config-TLS-vncDocument1
   graceful-restart-bgp-persist-vnc
  
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