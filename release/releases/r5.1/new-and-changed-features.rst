.. This work is licensed under the Creative Commons Attribution 4.0 International License.
   To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

========================
New and Changed Features
========================

The features listed in this section are new or changed as of Tungsten Fabric Release 5.1. A brief description of each new feature is included.

-  `New and Changed Features in Tungsten Fabric Release 5.1`_

New and Changed Features in Tungsten Fabric Release 5.1
-------------------------------------------------------

The features listed in this section are new as of Tungsten Fabric Release 5.1.

BGPaaS Peer Zone Collection
---------------------------

Starting with Tungsten Fabric Release 5.1, to better support high availability (HA) architectures, BGPaaS supports control node zone selection, with options available to configure BGPaaS control node zone peers. This capability enables you to set up primary and secondary control node zones, which can have one or more control nodes.

For more information, see `BGP as a Service`_  .

Installing Tungsten Fabric with Mesos
-------------------------------------

Starting with Tungsten Fabric Release 5.1, Tungsten Fabric supports Mesosphere DC/OS. Tungsten Fabric overlay and non-overlay network virtualization features are available in Apache Mesos environment.

For more information, see `Installing Tungsten Fabric with Mesos`_  .

Adding a New Compute Node to an Existing Containerized Tungsten Fabric Cluster
------------------------------------------------------------------------------

Starting with Tungsten Fabric Release 5.1, Tungsten Fabric supports the adding of a new compute node to the existing OpenStack cluster by configuring the instances.yaml file.

For more information, see `Adding a New Compute Node to Existing Containerized Tungsten Fabric Cluster`_  .

Support for Edge Routed Bridging
--------------------------------

Starting with Tungsten Fabric Release 5.1, the edge-routed bridging (ERB) for QFX series switches feature configures the inter-VN unicast traffic routing to occur at the leaf (ToR) switches in an IP CLOS with underlay connectivity topology. The ERB feature introduces the ERB-UCAST-Gateway and CRB-MCAST-Gateway roles in release 5.1. ERB is supported on the following devices running only Junos OS release 18.1R3:

- QFX5110-48S
- QFX5110-32Q
- QFX10002-36Q
- QFX10002-72Q
- QFX10008
- QFX10016

For more information, see `Edge Routed Bridging for QFX Series Switches`_ .

Routing Policies Match on Extended Communities
----------------------------------------------

Tungsten Fabric Release 5.1 supports extended communities on the import routing policy function. Release 5.1 allows import routing policy terms to match on extended communities and import routing policy actions to add, set, and remove extended communities. Filtering routes based on extended communities prevent advertising unnecessary service interface and static routes from the control node.

For more information, see `Creating a Routing Policy With External Communities in Contrail Command`_ .

Support for OpenShift 3.11
--------------------------

Tungsten Fabric Release 5.1 supports the installation of a standalone Red Hat OpenShift Container Platform version 3.11 cluster using ansible-openshift as the deployment tool.

For more information, see `Installing a Standalone Red Hat OpenShift Container Platform 3.11 Cluster Using OpenShift Ansible Deployer`_ .

Support for Kubernetes 1.12
---------------------------

Tungsten Fabric Release 5.1 supports the following Kubernetes release 1.12 network policy features:

- Egress support for network policy
- Classless Interdomain Routing (CIDR) selector support for egress and ingress network policies
- contrail-ansible-deployer provisioning

For more information, see `Kubernetes Updates_` .

Auto-provisioning of IPtable Filtering Rules on Tungsten Fabric Nodes
---------------------------------------------------------------------

Tungsten Fabric nodes are automatically configured with locally enforced firewall rules allowing access only to Tungsten Fabric services.

Certificate Lifecycle Management Using Red Hat Identity Management
------------------------------------------------------------------

Tungsten Fabric Release 5.1 supports using Transport Layer Security (TLS) with RHOSP to perform lifecycle management, including renewal, expiration, and revocation, of certificates using Red Hat Identity Management (IdM). Because IdM uses fully qualified domain names (FQDNs) to manage endpoints instead of IP addresses, Tungsten Fabric services are also enhanced to use FQDNs.

Support for Controlling the Maximum Flow Scale Supported on a Virtual Machine Interface
---------------------------------------------------------------------------------------

Tungsten Fabric Release 5.1 supports the following Kubernetes release 1.12 network policy features:

Starting in Tungsten Fabric Release 5.1, you can configure the maximum number of flows (max-flows) on a virtual machine interface (VMI) and in a virtual network. In releases prior to Tungsten Fabricv Release 5.1, you can control the number of flows only at the virtual machine-level.

When you configure max-flows at the virtual network-level, the configuration is applied to every VMI within the virtual network. When you configure max-flows at the virtual machine interface-level, the configuration applies only to that VMI.

Support for Multiple Network Interfaces in Kubernetes
-----------------------------------------------------

Starting in Tungsten Fabric Release 5.1, you can allocate multiple network interfaces (multi-net) to a container managed by Kubernetes to enable the container to connect to multiple networks. You can specify the networks the container can connect to. This capability can be leveraged to apply service chaining to containerized network functions.

For more information, see `Multiple Network Interfaces for Containers_` .

Support for Prefix-Based Fat Flow
---------------------------------

Starting in Tungsten Fabric Release 5.1, fat flows has been extended to prefix length. With the introduction of prefix-based fat flow, Tungsten Fabric supports mask processing where you can create flows based on a group of subscribers. This provides a higher level of flow aggregation than single IP address-based fat flow by grouping all the flows for all the end devices sharing the same subnet into a common fat flow.

For more information, see `Fat Flows_` .

Enable TLS Communication Between Analytics and Kafka
----------------------------------------------------

Starting with Tungsten Fabric Release 5.1, Transport Layer Security (TLS) communication is enabled between Kafka brokers and Tungsten Fabric analytics processes. contrail-collector and contrail-alarm-gen connects to Kafka for UVE processing. The User-Visible Entity (UVE) mechanism is used to aggregate and send the status information.

Support for Route Reflectors
----------------------------

Tungsten Fabric Release 5.1 supports Route Reflector (RR) functionality in the Control node for for Internal Border Gateway Protocol (iBGP) peers. Route reflection is a BGP feature that enables BGP routers to acquire route information from one iBGP router and reflect or advertise the information to other iBGP peers in the same autonomous system (AS).

For more information, see `Route Reflector Support in Tungsten Fabric Control Node_` .

Support for Tungsten Fabric on Windows Operating System
-------------------------------------------------------

Starting in release 5.1, Tungsten Fabric supports overlay network virtualization for Windows Docker containers. Windows server 2016 supports containerization using Docker containers and Tungsten Fabric components such as vRouter agent and the vRouter kernel module have been ported and qualified to run on Windows Server 2016. A Docker CNM plugin is added to process requests from the Docker daemon when a user creates or removes a network or an endpoint.

To install Tungsten Fabric for Windows, you must have Windows Server 2016 and Docker EE 17.06.

For more information, see `Understanding Tungsten Fabric Deployment on Windows_` .

Support for EVPN Multicast Type 6 Selective Multicast Ethernet Tag Routes
-------------------------------------------------------------------------

Tungsten Fabric Release 5.1 supports EVPN Type 6 selective multicast Ethernet tag (SMET) route to selectively send or receive traffic based on the presence or absence of active receivers on a compute node. The EVPN Type-6 SMET route helps build and use multicast trees selectively on a per `<*, G>` basis.

Currently, all broadcast, unknown unicast, multicast (BUM) traffic is carried over the inclusive multicast ethernet tag (IMET) routes. This results in flooding all compute nodes irrespective of whether an active receiver is present or not on each of those compute-nodes.

For more information, see `Support for EVPN Type 6 Selective Multicast Ethernet Tag Route_` .

Support for MPLS L3VPN InterAS Option C
---------------------------------------

Tungsten Fabric Release 5.1 supports L3VPN inter AS Option C, which is used to interconnect multi-AS backbones as described in RFC 4364.

For more information, see `Support for L3VPN Inter AS Option C_` .

.. _BGP as a Service: https://www.juniper.net/documentation/en_US/contrail5.1/information-products/topic-collections/release-notes/jd0e36.html

.. _Installing Tungsten Fabric with Mesos: https://www.juniper.net/documentation/en_US/contrail5.1/topics/task/installation/installing-contrail-mesos.html

.. _Adding a New Compute Node to Existing Containerized Tungsten Fabric Cluster: https://www.juniper.net/documentation/en_US/contrail5.1/topics/task/configuration/adding-new-cluster.html

.. _Edge Routed Bridging for QFX Series Switches: https://www.juniper.net/documentation/en_US/release-independent/solutions/topics/task/configuration/edge-routed-overlay-cloud-dc-configuring.html

.. _Creating a Routing Policy With External Communities in Contrail Command: https://www.juniper.net/documentation/en_US/contrail5.1/topics/task/configuration/create-external-community-routing-policy.html

.. _Installing a Standalone Red Hat OpenShift Container Platform 3.11 Cluster Using OpenShift Ansible Deployer: https://www.juniper.net/documentation/en_US/contrail5.1/topics/task/configuration/install-openshift-using-anible-311.html

.. _Kubernetes Updates: https://www.juniper.net/documentation/en_US/contrail5.1/topics/concept/k8s-ip-fabric.html

.. _Multiple Network Interfaces for Containers: https://www.juniper.net/documentation/en_US/contrail5.1/topics/task/configuration/multi-network-interfaces-containers.html

.. _Fat Flows: https://www.juniper.net/documentation/en_US/contrail5.1/topics/topic-map/contrail-fat-flows.html

.. _Route Reflector Support in Tungsten Fabric Control Node: https://www.juniper.net/documentation/en_US/contrail5.1/topics/concept/contrail-route-reflectors.html

.. _Understanding Tungsten Fabric Deployment on Windows: https://www.juniper.net/documentation/en_US/contrail5.1/topics/concept/understanding-windows-contrail.html

.. _Support for EVPN Type 6 Selective Multicast Ethernet Tag Route: https://www.juniper.net/documentation/en_US/contrail5.1/topics/reference/evpn-type-6-selective-multicast-ethernet-tag-route.html

.. _Support for L3VPN Inter AS Option C: https://www.juniper.net/documentation/en_US/contrail5.1/topics/concept/contrail-inter-as-option-c.html
