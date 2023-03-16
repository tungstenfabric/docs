
=====================================
Release Notes: Tungsten Fabric R22.06
=====================================


Release Tag: 22.06-RC

Available at hub.docker.com. 


Supported Platforms and Versions
--------------------------------


.. _Table 1:

*Table 1* : Supported Release Versions

+-------------------------------------------+---------------------+--------------------------------------------------------------------+
| Orchestrator Release                      | Deployment Tool     | Operating System, Kernel and Key Components Version                |                                                                               
+===========================================+=====================+====================================================================+
| Kubernetes 1.22.4                         | Juju Charms         | Ubuntu 20.04.3—Linux Kernel Version 5.4.0-120-generic              |
|                                           |                     | MaaS Version: 2.6.2                                                |                                                                                                                                                                                                                                                       
+-------------------------------------------+---------------------+--------------------------------------------------------------------+
| Kubernetes 1.22.4                         | Ansible             | CentOS 7.9—Linux Kernel Version 3.10.0-1160.25.1.el7.x86_64        |
|                                           |                     | Ansible version : 2.7.11                                           |
|                                           |                     | Docker version: 18.03.1-ce                                         |                                                                                                                                                          
+-------------------------------------------+---------------------+--------------------------------------------------------------------+
| OpenShift 4.8.x                           | Operator Framework  | RHEL CoreOS 4.8.x                                                  |                                                                                                                                                                                                                                                                                                  
+-------------------------------------------+---------------------+--------------------------------------------------------------------+
| Openstack Train                           | Ansible             | CentOS 7.9—Linux Kernel Version 3.10.0-1160.25.1.el7.x86_64        |
|                                           |                     | Ansible version: 2.7.11                                            |
|                                           |                     | Docker version: 18.03.1-ce                                         |                                                                                                                                                                                    
+-------------------------------------------+---------------------+--------------------------------------------------------------------+
| Openstack Queens                          | Ansible             | CentOS 7.9—Linux Kernel Version 3.10.0-1160.25.1.el7.x86_64        |
|                                           |                     | Ansible version: 2.7.11                                            |
|                                           |                     | Docker version: 18.03.1-ce                                         | 
+-------------------------------------------+---------------------+--------------------------------------------------------------------+
| Openstack Rocky                           | Ansible             | CentOS 7.9—Linux Kernel Version 3.10.0-1160.25.1.el7.x86_64        |
|                                           |                     | Ansible version: 2.7.11                                            |
|                                           |                     | Docker version: 18.03.1-ce                                         |                                                                                                                                                                                    
+-------------------------------------------+---------------------+--------------------------------------------------------------------+
| Openstack Queens                          | Ansible             | CentOS 7.9—Linux Kernel Version 3.10.0-1160.25.1.el7.x86_64        |
|                                           |                     | Ansible version: 2.7.11                                            |
|                                           |                     | Docker version: 18.03.1-ce                                         |                                                       
+-------------------------------------------+---------------------+--------------------------------------------------------------------+
| Canonical OpenStack Train                 | Juju Charms         |   Ubuntu 18.04.5—Linux Kernel Version 4.15.0-166-generic           |
|                                           |                     |   MaaS Version: 2.6.2                                              |                                                                                                                                                                                                                                        
+-------------------------------------------+---------------------+--------------------------------------------------------------------+
| Canonical OpenStack Ussuri                | Juju Charms         | Ubuntu 20.04.3—Linux Kernel Version 5.4.0-120-generic              |
|                                           |                     |  MaaS Version: 2.4.2                                               |                                                                                                                                                                                                                                     
+-------------------------------------------+---------------------+--------------------------------------------------------------------+
| Red Hat OpenStack Platform 16.2           | RHOSP 16 Director   | RHEL 8.4—Linux Kernel Version 4.18.0-305.12.1.el8_4.x86_64         |
|                                           |                     | Director Image: rhosp-director-images-16.2-20210902.2.el8ost.noarch|
|                                           |                     | Red Hat Content Sync Date : October 06, 2021, 05:21 PM PST         |
|                                           |                     |                                                                    |
+-------------------------------------------+---------------------+--------------------------------------------------------------------+


Support for Automatically Deploying Remote Compute Using RHOSP/TripleO
----------------------------------------------------------------------
Starting in Tungsen Fabric 22.06, you can deploy remote compute automatically using RHOSP/TripleO for edge compute use cases.

For more information see: `Remote Compute`_


Centos 8 Support for Tungsten Fabric Container Images
---------------------------------------------------
Starting in Tungsten Fabric Release 22.06, the Centos 8 Base Image version 8 is used as the base for Tungsten Fabric container images.

Graceful Restart or Long-Lived Graceful Restart Support for a EVPN Type 2 Route
--------------------------------------------------------------------------------
Starting in Tungsten Fabric Release 22.06, the graceful restart or long-lived graceful restart features supports EVPN Type 2 prefixes, reducing overall network impact to controller restarts.

For more information see: `Long-lived Graceful Restart`_ 

.. _Remote Compute: ../../../tungsten-fabric-service-provider-focused-features-guide/remote-compute-50.html
.. _Long-lived Graceful Restart: ../../../tungsten-fabric-installation-and-upgrade-guide/graceful-restart-bgp-persist-vnc.html
.. _OpenShift Operator Upgrade: ../../../tungsten-fabric-cloud-native-user-guide/tf-operator-upgrade-ocp4.html

