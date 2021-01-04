Understanding Red Hat OpenStack Platform Director
=================================================

 

Red Hat OpenStack Platform Director
-----------------------------------

| Starting with Contrail Networking Release 2008, Contrail Networking
  supports using Contrail with Red Hat OpenStack Platform Director 16.1.
| This chapter explains how to integrate a Contrail Networking Release
  2008 (or higher) installation with Red Hat OpenStack Platform Director
  16.1.

Red Hat OpenStack Platform provides an installer called the Red Hat
OpenStack Platform director (RHOSPd or OSPd), which is a toolset based
on the OpenStack project TripleO (OOO, OpenStack on OpenStack). TripleO
is an open source project that uses features of OpenStack to deploy a
fully functional, tenant-facing OpenStack environment.

TripleO can be used to deploy an RDO-based OpenStack environment
integrated with Tungsten Fabric. Red Hat OpenStack Platform director can
be used to deploy an RHOSP-based OpenStack environment integrated with
Contrail Networking.

OSPd uses the concepts of undercloud and overcloud. OSPd sets up an
undercloud, a single server running an operator-facing deployment that
contains the OpenStack components needed to deploy and manage an
overcloud, a tenant-facing deployment that hosts user workloads.

The overcloud is the deployed solution that can represent a cloud for
any purpose, such as production, staging, test, and so on. The operator
can select to deploy to their environment any of the available overcloud
roles, such as controller, compute, and the like.

OSPd leverages existing core components of OpenStack including Nova,
Ironic, Neutron, Heat, Glance, and Ceilometer to deploy OpenStack on
bare metal hardware.

-  Nova and Ironic are used in the undercloud to manage the bare metal
   instances that comprise the infrastructure for the overcloud.

-  Neutron is used to provide a networking environment in which to
   deploy the overcloud.

-  Glance stores machine images.

-  Ceilometer collects metrics about the overcloud.

For more information about OSPd architecture, see `OSPd
documentation <https://docs.openstack.org/tripleo-docs/latest/install/introduction/architecture.html>`__.

Contrail Networking Roles
-------------------------

OSPd supports composable roles, which are groups of services that you
define through Heat templates. Composable roles allow you to integrate
Contrail Networking into the overcloud environment.

The following are the Contrail Networking roles used for integrating
into the overcloud:

-  Contrail Controller

-  Contrail Analytics

-  Contrail Analytics Database

-  Contrail-TSN

-  Contrail-DPDK

`Figure 1 <setting-up-contrail-rhosp16-introduction.html#rhosp1>`__
shows the relationship and components of an undercloud and overcloud
architecture for Contrail Networking.

|Figure 1: Undercloud and Overcloud with Roles|

Undercloud Requirements
-----------------------

The undercloud is a single server or VM that hosts the OpenStack
Platform director, which is an OpenStack installation used to provision
OpenStack on the overcloud.

See `Undercloud
Requirements <https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/16.1/html/director_installation_and_usage/planning-your-undercloud>`__
for the compute requirements of the undercloud.

Overcloud Requirements
----------------------

The overcloud roles can be deployed to bare metal servers or to virtual
machines (VMs), but the compute nodes must be deployed to bare metal
systems. Every overcloud node must support IPMI for booting up from the
undercloud using PXE.

Ensure the following requirements are met for the Contrail Networking
nodes per role.

-  Non-high availability: A minimum of 4 overcloud nodes are needed for
   control plane roles for a non-high availability deployment:

   -  1x contrail-config (includes Contrail control)

   -  1x contrail-analytics

   -  1x contrail-analytics-database

   -  1x OpenStack controller

-  High availability: A minimum of 12 overcloud nodes are needed for
   control plane roles for a high availability deployment:

   -  3x contrail-config (includes Contrail control)

   -  3x contrail-analytics

   -  3x contrail-analytics-database

   -  3x OpenStack controller

   If the control plane roles are deployed to VMs, use 3 separate
   physical servers and deploy one role of each kind to each physical
   server.

See `Overcloud
Requirements <https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/16.1/html/director_installation_and_usage/planning-your-overcloud>`__
for the compute requirements of the overcloud.

Networking Requirements
-----------------------

As a minimum, the installation requires two networks:

-  provisioning network - This is the private network that the
   undercloud uses to provision the overcloud.

-  external network - This is the externally-routable network you use to
   access the undercloud and overcloud nodes.

Ensure the following requirements are met for the provisioning network:

-  One NIC from every machine must be in the same broadcast domain of
   the provisioning network, and it should be the same NIC on each of
   the overcloud machines. For example, if you use the second NIC on the
   first overcloud machine, you should use the second NIC on each
   additional overcloud machine.

   During installation, these NICs will be referenced by a single name
   across all overcloud machines.

-  The provisioning network NIC should not be the same NIC that you are
   using for remote connectivity to the undercloud machine. During the
   undercloud installation, an Open vSwitch bridge will be created for
   Neutron, and the provisioning NIC will be bridged to the Open vSwitch
   bridge. Consequently, connectivity would be lost if the provisioning
   NIC was also used for remote connectivity to the undercloud machine.

-  The provisioning NIC on the overcloud nodes must be untagged.

-  You must have the MAC address of the NIC that will PXE boot the IPMI
   information for the machine on the provisioning network. The IPMI
   information will include such things as the IP address of the IPMI
   NIC and the IPMI username and password.

-  All of the networks must be available to all of the Contrail
   Networking roles and computes.

While the provisioning and external networks are sufficient for basic
applications, you should create additional networks in most overcloud
environments to provide isolation for the different traffic types by
assigning network traffic to specific network interfaces or bonds.

When isolated networks are configured, the OpenStack services are
configured to use the isolated networks. If no isolated networks are
configured, all services run on the provisioning network. If only some
isolated networks are configured, traffic belonging to a network not
configured runs on the provisioning network.

The following networks are typically deployed when using network
isolation topology:

-  Provisioning - used by the undercloud to provision the overcloud

-  Internal API - used by OpenStack services to communicate with each
   other

-  Tenant - used for tenant overlay data plane traffic (one network per
   tenant)

-  Storage - used for storage data traffic

-  Storage Management - used for storage control and management traffic

-  External - provides external access to the undercloud and overcloud,
   including external access to the web UIs and public APIs

-  Floating IP - provides floating IP access to the tenant network (can
   either be merged with external or can be a separate network)

-  Management - provides access for system administration

Compatibility Matrix
--------------------

The following combinations of Operating
System/OpenStack/Deployer/Contrail Networking are supported:

Table 1: Compatibility Matrix

================ ========= ======== ==================================
Operating System OpenStack Deployer Contrail Networking
================ ========= ======== ==================================
RHEL 8.2         OSP16     OSPd16   Contrail Networking 2008 or higher
================ ========= ======== ==================================

Installation Summary
--------------------

The general installation procedure is as follows:

-  Set up the infrastructure, which is the set of servers or VMs that
   host the undercloud and overcloud, including the provisioning network
   that connects them together.

-  Set up the undercloud, which is the OSPd application.

-  Set up the overcloud, which is the set of services in the
   tenant-facing network. Contrail Networking is part of the overcloud.

For more information on installing and using the RHOSPd, see `Red Hat
documentation <https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/16.1/html/director_installation_and_usage/index>`__.

.. raw:: html

   <div class="table">

.. raw:: html

   <div class="caption">

Release History Table

.. raw:: html

   </div>

.. raw:: html

   <div class="table-row table-head">

.. raw:: html

   <div class="table-cell">

Release

.. raw:: html

   </div>

.. raw:: html

   <div class="table-cell">

Description

.. raw:: html

   </div>

.. raw:: html

   </div>

.. raw:: html

   <div class="table-row">

.. raw:: html

   <div class="table-cell">

`2008 <#jd0e17>`__

.. raw:: html

   </div>

.. raw:: html

   <div class="table-cell">

Starting with Contrail Networking Release 2008, Contrail Networking
supports using Contrail with Red Hat OpenStack Platform Director 16.1.

.. raw:: html

   </div>

.. raw:: html

   </div>

.. raw:: html

   </div>

 

.. |Figure 1: Undercloud and Overcloud with Roles| image:: documentation/images/g300376.png
