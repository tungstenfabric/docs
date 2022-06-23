
=====================================
Release Notes: Tungsten Fabric R21.12
=====================================


Release Tag: TF21.12

Available at hub.docker.com. 


Supported Platforms and Versions
--------------------------------


.. _Table 1:

*Table 1* : Supported Release Versions

+-------------------------------------------+---------------------+--------------------------------------------------------------------+
| Orchestrator Release                      | Deployment Tool     | Operating System, Kernel and Key Components Version                |                                                                               
+===========================================+=====================+====================================================================+
| Kubernetes 1.21.4                         | Juju Charms         | Ubuntu 20.04.3—Linux Kernel Version 5.4.0-92-generic               |
|                                           |                     | MaaS Version: 2.6.2                                                |                                                                                                                                                                                                                                                       
+-------------------------------------------+---------------------+--------------------------------------------------------------------+
| Kubernetes 1.21.4                         | Ansible             | CentOS 7.9—Linux Kernel Version 3.10.0-1160.25.1.el7.x86_64        |
|                                           |                     | Ansible version : 2.7.11                                           |
|                                           |                     | Docker version: 18.03.1-ce                                         |                                                                                                                                                          
+-------------------------------------------+---------------------+--------------------------------------------------------------------+
| OpenShift 4.8.x                           | Operator Framework  | RHEL CoreOS 4.8.x                                                  |                                                                                                                                                                                                                                                                                                  
+-------------------------------------------+---------------------+--------------------------------------------------------------------+
| Openstack Rocky                           | Ansible             | CentOS 7.9—Linux Kernel Version 3.10.0-1160.25.1.el7.x86_64        |
|                                           |                     | Ansible version: 2.7.11                                            |
|                                           |                     | Docker version: 18.03.1-ce                                         |                                                                                                                                                                                    
+-------------------------------------------+---------------------+--------------------------------------------------------------------+
| Openstack Queens                          | Ansible             | CentOS 7.9—Linux Kernel Version 3.10.0-1160.25.1.el7.x86_64        |
|                                           |                     | Ansible version: 2.7.11                                            |
|                                           |                     | Docker version: 18.03.1-ce"                                        |                                                       
+-------------------------------------------+---------------------+--------------------------------------------------------------------+
| Canonical OpenStack Train                 | Juju Charms         |   Ubuntu 18.04.5—Linux Kernel Version 4.15.0-166-generic           |
|                                           |                     |   MaaS Version: 2.6.2                                              |                                                                                                                                                                                                                                        
+-------------------------------------------+---------------------+--------------------------------------------------------------------+
| Canonical OpenStack Ussuri                | Juju Charms         | Ubuntu 20.04.3—Linux Kernel Version 5.4.0-92-generic               |
|                                           |                     |  MaaS Version: 2.4.2                                               |                                                                                                                                                                                                                                     
+-------------------------------------------+---------------------+--------------------------------------------------------------------+
| Red Hat OpenStack Platform 16.1.3/16.1.6  | RHOSP 16 Director   | RHEL 8.2—Linux Kernel Version 4.18.0-193.29.1                      |
|                                           |                     | Director Image: rhosp-director-images-16.1-20201202.1.el8ost.noarch|
|                                           |                     | Red Hat Content Sync Date : 2021-20-09  (10:16:53)                 |
|                                           |                     |                                                                    |
|                                           |                     | RHEL 8.4—Linux Kernel Version 4.18.0-305.19.1.el8_4.x86_64         |
|                                           |                     | Director Image: rhosp-director-images-16.2-20210902.2.el8ost.noarch|
|                                           |                     | Red Hat Content Sync Date : October 06, 2021, 05:21 PM PST"        |
+-------------------------------------------+---------------------+--------------------------------------------------------------------+



Support for Dynamic Address Learning with IPVLAN Networking
------------------------------------------------------------

In the latest release of Tungsten Fabric a vRouter can learn multiple MAC-IP address bindings for a single MAC address when Dynamic Address Learning is enabled in a virtual network.

For more information see: :ref:`Dynamic MAC/IP Learning <DynamicMacIP>`.



Support for Layer 3 Multihoming
-------------------------------

It is now possible to provide high availability to vRouters with Layer 3 multihoming, without the need for MC-LAG or bond interfaces.

For more information see: `Layer 3 Multihoming`_

Support for Flow Stickiness in a Load-Balanced System
------------------------------------------------------

Improved flow stickiness is a feature that helps to minimize flow remapping across equal cost multipath (ECMP) groups in a load-balanced system. Flow stickiness reduces such flow being remapped and retains the flow with the original path when the ECMP group's member change. When a flow is affected by a member change, vRouter reprograms flow table and rebalances the flow.

For more information see: LINK MISSING

Support for User-Defined Tags in Security Policy
----------------------------------------------------

In this latest release security policy allows optional user-defined tags which enables you to define tag IDs along with tag names. You can also create a predefined tag type with user-defined tag value ID.


Upgrade Tungsten Fabric Through Kubernetes and/or Red Hat OpenShift
------------------------------------------------------------------------

Starting in Tungsten Fabric Release R21.12, you can update Tungsten Fabric through Kubernetes and/or Red Hat OpenShift. You can use this procedure to update Tungsten Fabric deployed by the Tungsten Fabric (TF) Operator.

For more information see: LINK MISSING


Configure MTU For Virtual Networks
------------------------------------

Starting in Tungsten Fabric Release R21.12, you can configure Maximum Transmission Unit (MTU) for virtual networks(VN) in the Contrail Command UI. To configure MTU, select Overlay>Virtual Networks>Create Virtual Network. In the Advanced option, you can configure the MTU value in the MTU field. The available range is 0-9216. The Dynamic Host Configuration Protocol (DHCP) will not use the MTU value and it will not be inherited by VMIs attached to the VN.


.. _Layer 3 Multihoming: ../../../tungsten-fabric-service-provider-focused-features-guide/layer-3-multihoming.html
