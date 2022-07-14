
=====================================
Release Notes: Tungsten Fabric R21.05
=====================================


Release Tag: R21.05

Available at hub.docker.com. 

Support for Red Hat OpenShift 4.6
----------------------------------

In the latest release of Tungsten Fabric you can enable Tungsten Fabric as the Container Network Interface (CNI) in environments using Red Hat OpenShift 4.6. Red Hat OpenShift is a platform.
`<https://docs.tungsten.io/en/latest/tungsten-fabric-cloud-native-user-guide/how-to-install-tungsten-fabric-openshift46.rst>`_


Ironic Support with Juju
------------------------

Tungsten Fabric now supports new charms for Ironic from OpenStack Train version 15.x.x.

Support for OpenStack Ussuri and Ubuntu Version 20.04
-----------------------------------------------------

In this release of Tungsten Fabric OpenStack Ussuri with Ubuntu version 18.04 (Bionic Beaver) and Ubuntu version 20.04 (Focal Fossa) are now supported. The installation process is the same as installing Tungsten Fabric with OpenStack by Using Juju Charms.

Support for Red Hat OpenStack Platform Director 16.1
----------------------------------------------------

Tungsten Fabric now supports integration with Red Hat OpenStack Platform Director (RHOSPd or OSPd) 16.1. Table 1 lists the OpenStack releases and the corresponding operating system and deployer versions supported by Tungsten Fabric.

.. _Table 1:

*Table 1* : Supported Release Versions

	+--------------------------------+------------------+-----------+----------+
	| Tungsten Fabric Release        | Operating System | OpenStack | Deployer |
	+================================+==================+===========+==========+
	| Tungsten Fabric Release R21.05 |     RHEL 8.2     | OSP16     |  OSPd16  |
	+--------------------------------+------------------+-----------+----------+


Support for 4 Byte AS Number
----------------------------

Tungsten Fabric now supports 4-byte or 32-bit Autonomous System (AS) numbers in BGP as specified in RFC 6793. The provision for 4-byte AS numbers is introduced to avoid exhaustion of AS numbers. You can now set an AS number in the range 1-4294967295. The default AS number is 64512. 

To start using AS value in the 4-byte range:

1. Navigate to Infrastructure > Cluster> Advanced Options page.

The Global Config tab is displayed, which lists all system configuration information.

2. Click the Edit icon. The Edit System Configuration dialog box is displayed.

3. Select Enabled option button under 4 Byte ASN field. To disable 4-byte ASN range, select Disabled.

You can now assign 2-byte or 16-bit AS number in the range 1-65535. To assign 4-byte value in Route Target(s) field:

1. Navigate to Overlay > Virtual Networks > Edit Virtual Network page to edit existing virtual network. Navigate to Overlay > Virtual Networks > Create Virtual Network page to create a new virtual network. 

2. Click Routing, Bridging and Policies.
Route Target(s) field is displayed.
Click +Add.

In the Route Target(s) section, you can now assign a 4-byte value in the range of 1-4,294,967,295 in the ASN field, when 4 Byte ASN is enabled in Global Config. If you assign the ASN field a 4-byte value, you must assign a 2-byte value in the range of 0-65,535 in the Target field. You can also assign a 2-byte value in the range of 1-65,535 in the ASN field, when 4 Byte ASN is disabled in Global Config. If you assign the ASN field a 2-byte value, you must assign a 4-byte value in the range of 0-4,294,967,295 in the Target field. You can also add suffix L or l (lower-case L) at the end of a value in the ASN field to assign the value in 4-byte range. Even if the value provided in the ASN field is in the range of 1-65,535, adding L or l (lower-case L) at the end of the value assigns it in 4-byte range. If you assign the ASN field a value in the 4-byte range, you must enter a value in the range of 0-65,535 in the Target field.


Encryption Support for Redis Traffic
------------------------------------

Tungsten Fabric now supports an SSL encrypted tunneling program called stunnel to secure Redis traffic. The stunnel is used to route traffic between Redis clients and servers. SSL encryption in the stunnel acts as a layer of security when Tungsten Fabric analytics client processes connect to a Redis instance server. In prior releases connection requests sent from tf-analytics clients to Redis server sometimes posed security threats since Redis did not support encryption. The stunnel feature is supported only when Tungsten Fabric is deployed with Red Hat OpenStack Platform (RHOSP).


Support for Tungsten Fabric Deployment with Kubernetes Using Juju Charms
------------------------------------------------------------------------

Starting in Release 21.05, you can deploy Tungsten Fabric with Kubernetes by using Juju Charms. Juju helps you deploy, configure, and efficiently manage applications on private clouds and public clouds. A Charm is a module containing a collection of scripts and metadata and is used with Juju to deploy Tungsten Fabric. Juju Charms helps reduce the complexity of deploying Tungsten Fabric by providing a simple way to deploy, configure, scale, and manage Tungsten Fabric operations. Tungsten Fabric now supports the following charms: 

• contrail-kubernetes-master
• contrail-kubernetes-node

`<https://docs.tungsten.io/en/latest/tungsten-fabric-installation-and-upgrade-guide/deploying-tf-using-juju-charms-kubernetes.html>`_


Support for Netronome SmartNIC vRouter
--------------------------------------

Tungsten Fabric now supports Netronome Agilio CX for Tungsten Fabric
deployment with Red Hat OpenStack Platform Director (RHOSPd) 13 environment. This
feature will enable increased packets per second (PPS) capacity of Tungsten Fabric vRouter
datapath allowing applications to reach their full processing capacity. Additionally, it allows to reclaim CPU cores from Tungsten Fabric vRouter off-loading permitting more VMs and
VNFs to be deployed per server.

`<https://docs.tungsten.io/en/latest/tungsten-fabric-installation-and-upgrade-guide/smartnic-vrouter-support.html>`_

Support for Tungsten Fabric with Kubernetes in Nested Mode by Using Juju Charms
-------------------------------------------------------------------------------

Tungsten Fabric now supports provisioning of a Kubernetes cluster inside an OpenStack cluster. Tungsten Fabric Networking offers a nested control and data plane where a single control plane and a single network stack can manage and service both the OpenStack and Kubernetes clusters. In nested mode, a Kubernetes cluster is provisioned in virtual machines of an OpenStack cluster. The CNI plugin and the Tungsten Fabric Kubernetes manager of the Kubernetes cluster interface directly with Tungsten Fabric components that manage the OpenStack cluster. All Kubernetes features, functions and specifications are supported in nested mode. For more information, see Installing Tungsten Fabric with Kubernetes in Nested Mode by Using Juju Charms.
`<https://docs.tungsten.io/en/latest/tungsten-fabric-installation-and-upgrade-guide/juju-charms-nested-kubernetes.html>`_


Encryption Support Between Analytics API Servers and Client Servers
-------------------------------------------------------------------

Tungsten Fabric now supports the connection between Analytics API servers and Client servers encrypted with SSL. The Clients servers connect to the Analytics API server through the REST API Port. In earlier releases, the connection between Analytics API server and the Clients servers was not encrypted, which could pose a security threat.

`<https://docs.tungsten.io/en/latest/tungsten-fabric-monitoring-and-troubleshooting-guide/encrypting-connection-analytics-server-and-client-server.html>`_

Enhanced Routing Policies to Support Modification of Secondary Routes in Virtual Networks
-----------------------------------------------------------------------------------------

Tungsten Fabric now supports virtual network routing policies automatically applied to secondary routes. This feature is especially useful as a mechanism to modify routes imported from MP-BGP, including routes that are imported from the MPLS network, using routing policies.

`<https://docs.tungsten.io/en/latest/tungsten-fabric-service-provider-focused-features-guide/tf-routing-policy-sp-features.html>`_

Support for Trunk Networking Between Tungsten Fabric Networking and Neutron
---------------------------------------------------------------------------

Tungsten Fabric now integrates with Neutron trunk port APIs, which enables trunk networking between Tungsten Fabric and Neutron instances. Trunk networking uses trunk extension that is used to multiplex incoming and outgoing packets from multiple Neutron logical networks using a single Neutron logical port. A trunk extension is integrated in Neutron as a collection of Neutron logical ports. In the trunk extension that is implemented, Tungsten Fabric introduces logical entities defined by OpenStack Trunk API to provide backend support for Neutron Trunk Port API. The Neutron Trunk Port object maps to Tungsten Fabric Virtual Port Group (VPG) object, which was designed for handling non-LCM BMS workflow and multi-VLAN support.


Support for Increased vRouter Next Hop Limit and Monitoring Next Hop and MPLS Labels Usage
------------------------------------------------------------------------------------------

Tungsten Fabric now supports an increased next hop value in the vRouter to 32 bits. By default, the vRouter creates 512K next hops and it supports up to 1 million next hops. You can also now configure a watermark limit in vRouter agent configuration file, which enables you to monitor the usage and availability of next hops and Multiprotocol Label Switching (MPLS) labels. In earlier releases, Tungsten Fabric vRouter supported 16 bits next hop value, which enabled it to create a maximum of only 65,536 next hops.

`<https://docs.tungsten.io/en/latest/tungsten-fabric-networking-and-security-user-guide/next-hop-limit-increase.html>`_

Enhanced DPDK vRouter Performance Through Full CPU Partitioning and Isolation
-----------------------------------------------------------------------------

Tungsten Fabric now supports full CPU partitioning. CPU isolation is an RHEL method to partition and isolate the CPU cores on a compute node from the symmetric multiprocessing (SMP) balancing and scheduler algorithms. The full CPU isolation feature optimizes the performance of DPDK vRouter when deployed with the DPDK settings recommended for RHOSP. To enable full CPU partitioning and isolation, you need to configure tuned and isolcpus.

`<https://docs.tungsten.io/en/latest/tungsten-fabric-service-provider-focused-features-guide/vrouter-isolcpu.html>`_

Inter Subcluster Route Filtering
--------------------------------

Tungsten Fabric now supports inter subcluster route filtering. With this release, a new extended community called origin-sub-cluster (similar to origin-vn) is added to all routes originating from a subcluster. The format of this new extended community is subcluster::. This new extended community is added by encoding the subcluster ID in the ID field within the extended community. The subcluster ID helps you determine the subcluster from which the route originated, and is unique for each subcluster.

`<https://docs.tungsten.io/en/latest/tungsten-fabric-service-provider-focused-features-guide/remote-compute-50.html>`_

Zero Impact Upgrade: Upgrading Tungsten Fabric Networking Software without Rebooting Compute Nodes with Kernel-mode vRouters
----------------------------------------------------------------------------------------------------------------------------

Tungsten Fabric now supports huge pages in environments where compute nodes are using kernel-mode vRouters and the environment is deployed using Red Hat Openstack or Juju. Huge page support for kernel-mode vRouters allows the Zero Impact Upgrade (ZIU) procedure to complete Tungsten Fabric software upgrades without rebooting compute nodes. 

`<https://docs.tungsten.io/en/latest/tungsten-fabric-installation-and-upgrade-guide/install-tf-rhosp-ziu.html>`_

`<https://docs.tungsten.io/en/latest/tungsten-fabric-installation-and-upgrade-guide/deploying-tf-using-juju-charms.html>`_

Zero Impact Upgrade: Tungsten Fabric Networking Software Upgrades in Environments Deployed using Ansible
--------------------------------------------------------------------------------------------------------

Tungsten Fabric now supports the Zero Impact Upgrade (ZIU) procedure to upgrade Tungsten Fabric Networking software in environments that are deployed using Ansible. For additional information, see How to Perform a Zero Impact Tungsten Fabric Networking Upgrade using Ansible.

`<https://docs.tungsten.io/en/latest/tungsten-fabric-installation-and-upgrade-guide/installing-tf-ansible-ziu.html>`_

Support for Octavia as LBaaS
----------------------------

Tungsten Fabric now supports Octavia as LBaaS. The Neutron LBaaS plugin is no longer available in OpenStack Train release. If you want to use legacy Tungsten Fabric load balancer, you can use VNC or the Tungsten Fabric Web UI. 

`<https://docs.tungsten.io/en/latest/tungsten-fabric-installation-and-upgrade-guide/canonical-octavia.html>`_

`<https://docs.tungsten.io/en/latest/tungsten-fabric-installation-and-upgrade-guide/rhosp-octavia.html>`_

Support for Fast Routing Convergence
------------------------------------

Tungsten Fabric now supports fast convergence of the network in case of failures in the overlay tunnel endpoints. With the fast convergence feature, Tungsten Fabric can detect and respond to failures in the gateway or vRouter and take corrective action faster, thereby reducing the convergence time. Convergence time is the time taken by the control plane to detect a failure and take corrective action. Faster convergence reduces the risk of silent packet drop in case of a failure in the network.

`<https://docs.tungsten.io/en/latest/tungsten-fabric-fabric-lifecycle-management-guide/fast-routing-convergence.html>`_

Configurable XMPP Timeout
-------------------------

Tungsten Fabric now allows you to configure the XMPP timer value in the range 1 through 90 seconds. Reducing the timer to a lower value facilitates faster convergence in the network. Though you can configure a value as low as one (1), the recommended value is nine (9). A lower value for the timer is recommended only for smaller clusters.

`<https://docs.tungsten.io/en/latest/tungsten-fabric-fabric-lifecycle-management-guide/fast-routing-convergence.html>`_

VLAN Forwarding Disabled for DPDK vRouters Deployed on VLAN Interfaces
----------------------------------------------------------------------

Tungsten Fabric now has VLAN forwarding on interfaces disabled by default on DPDK vRouters that are deployed in a cluster. This optimizes the performance of DPDK enabled vRouters.

In releases prior VLAN forwarding interface is enabled by default, enabling packet forwarding between the host and the fabric. This resulted in increased load on vRouters affecting their performance.

To enable VLAN forwarding interface on vRouter, set the value for DPDK_ENABLE_VLAN_FWRD to True in contrail-settings.yaml. If VLAN forwarding interface is enabled, the following message is logged in the contrail-vrouter-dpdk container logs:

VLAN forwarding is enabled and causing performance impact on the system

Support for Viewing Details of a DPDK Enabled vRouter
-----------------------------------------------------

Tungsten Fabric now supports the dpdkinfo command which enables you to see the details of the internal data structures of a DPDK enabled vRouter. The dpdkinfo command enables you to view information related to bond interfaces, Link Aggregation Control Protocol (LACP), memory pool (mempool), Logical core (lcore), network interface card (NIC) and application. The dpdkinfo command reads the internal data structures and unstructured data from a DPDK enabled vRouter and displays the data on the console.

`<https://docs.tungsten.io/en/latest/tungsten-fabric-monitoring-and-troubleshooting-guide/vrouter-cli-utilities-vnc.html#dpdkinfo-command>`_

Packet Latency Improvements in the vRouter
------------------------------------------

Tungsten Fabric now has significant vRouter packet latency improvements in DPDK deployments. The latency for 64B packets is measured to be around 120 microseconds (µs) in release 2008 as against 300-400 µs prior to release 2008. In historic DPDK deployments, the vRouter functions in a hybrid mode where it uses part pipelining mode and part run-to-completion mode for packet processing thereby ensuring good load balancing and also reasonable latency. However, from release 2008, you can switch the vRouter from hybrid to run-to-completion mode where the packets are processed in a single session with no load balancing thereby reducing latency overheads. To switch DPDK modes, you must set the DPDK_COMMAND_ADDTIONAL_ARGS+= "--vr_no_load_balance" parameter in the ifcfg-vhost0 file on the vRouter.

This feature has the following caveats:

The run-to-completion mode has inherent disadvantages such as if the virtual machine is unable to load balance, you might see bottlenecks using this mode.

The VNF must be enabled with multiqueue virtio. This is to ensure that the VNF performs load balancing in place of the vRouter.

Only MPLSoUDP and VXLAN encapsulation protocols are supported.


Support for Clearing vif Statistics Counters
--------------------------------------------

Tungsten Fabric now supports clearing of vif statistics counters for all interfaces by using the --clear command.

`<https://docs.tungsten.io/en/latest/tungsten-fabric-monitoring-and-troubleshooting-guide/vrouter-cli-utilities-vnc.html>`_

Contrail Tools Container
------------------------

Contrail-tools container provides a centralized location for all the available tools and CLI commands in one place. Tungsten Fabric now features the contrail-tools command which will be installed by default. contrail-tools command enables you to log in to the container and execute the tool. Additionally, the command will kill the container on exit.

`<https://docs.tungsten.io/en/latest/tungsten-fabric-monitoring-and-troubleshooting-guide/contrail-tools.html>`_

Support for DPDK Release 19.11
------------------------------

Tungsten Fabric vRouter now supports DPDK Release 19.11. To view the DPDK version, use the following commands:

.. code-block:: console

    [root@user ~]# contrail-tools
    (contrail-tools)[root@user /]$ dpdkinfo -v
    DPDK Version: DPDK 19.11.0
    vRouter version: {"build-info": [{"build-time": "2020-09-17 00:44:40.135183", "build-hostname": "contrail-build-r2008-centos-121-generic-20200916063600.novalocal", "build-user": "contrail-builder", "build-version": "2008"}]

Sandump Tool
------------
Tungsten Fabric now features the Sandump tool, available in contrail-tools container. Sandump tool captures the Sandesh messages from netlink connection between the Agent and the vRouter (only DPDK mode) and, provides detailed interpretation of all the captured bytes.​

`<https://docs.tungsten.io/en/latest/tungsten-fabric-monitoring-and-troubleshooting-guide/sandump-tool.html>`_

Enablement Changes to Optional Tungsten Fabric Analytics Modules
----------------------------------------------------------------

Starting with Tungsten Fabric Release 2011, the optional TF Analytics modules—analytics alarm, analytics SNMP, and analytics database—must be enabled in the OOO (TripleO) Heat templates. 

Support for Intel DDP in vRouter for Fortville NICS
---------------------------------------------------

The Tungsten Fabric vRouter now supports Intel dynamic device personalization (DDP) technology, which enables faster processing of packets with MPLSoGRE encapsulation. The Intel DDP technology is supported only in Intel Fortville Series NICs.

`<https://docs.tungsten.io/en/latest/tungsten-fabric-service-provider-focused-features-guide/support-for-ddp-in-intel-x710-ethernet.html>`_

Retaining the AS Path Attribute in a Service Chain
--------------------------------------------------

Starting with Tungsten Fabric Release 21.05, you can configure the AS path to be retained in the routes re-originated from the destination VN to the source VN in a service chain. You also have the ability to enable or disable the path retention for selected service chains. You can enable or disable the Retain AS Path option while configuring the network policy in the Overlay > Network Policies > Create Network Policy page.

`<https://docs.tungsten.io/en/latest/tungsten-fabric-fabric-lifecycle-management-guide/service-chaining-as-path-retain.html>`_

Support for vRouter Dynamic MAC Address/IP Address Learning and BFD Health Check for Workloads
Starting with Tungsten Fabric Release 2011, the Tungsten Fabric vRouter dynamically learns the MAC address/IP address binding of the workloads deployed on a Tungsten Fabric connected virtual machine (VM). The vRouter learns the MAC address/IP address binding of the pods to enable an efficient workload to workload communication. Also, Tungsten Fabric supports Bidirectional Forwarding and Detection (BFD) based health check to verify the liveliness of a workload.

`<https://docs.tungsten.io/en/latest/tungsten-fabric-service-provider-focused-features-guide/vrouter-mac-ip-learning-and-bfd-for-pods.html>`_


Support for Sandump Tool on Windows Machines
--------------------------------------------

Tungsten Fabric now supports the Sandump tool with Wireshark, available on Windows machines. Sandump tool captures the Sandesh messages from netlink connection between the Agent and the vRouter (only DPDK mode) and, provides detailed interpretation of all the captured bytes.​ 

`<https://docs.tungsten.io/en/latest/tungsten-fabric-monitoring-and-troubleshooting-guide/sandump-tool.html>`_

Support for agent_header.lua Wireshark Plugin in Windows OS Computers
---------------------------------------------------------------------

Tungsten Fabric now allows the use of the agent_header.lua Wireshark plugin in Windows OS computers, which enables you analyze the packets exchanged between vRouter data plane and vRouter agent on the pkt0 interface.

`<https://docs.tungsten.io/en/latest/tungsten-fabric-monitoring-and-troubleshooting-guide/adding-agent-header-using-wireshark-plugin.html>`_

Upgrade Tungsten Fabric Networking using Red Hat Fast Forward Upgrade Procedure
-------------------------------------------------------------------------------

Tungsten Fabric can now use a combined procedure to upgrade Red Hat OpenStack Platform (RHOSP) from RHOSP 13 to RHOSP 16.1 by leveraging Red Hat Fast Forward Upgrade (FFU) procedure while simultaneously upgrading Tungsten Fabric from Release 5.1 to Release 21.05. 

`<https://docs.tungsten.io/en/latest/tungsten-fabric-installation-and-upgrade-guide/ffu-ziu-rhosp16.1-cn.html>`_

Support for KubeVirt in Kubernetes Environments
-----------------------------------------------

Tungsten Fabric can now use KubeVirt in Kubernetes-orchestrated environments that use Tungsten Fabric as the Container Networking Interface (CNI). KubeVirt is a virtualization add-on to Kubernetes that allows virtual machines (VMs) to run alongside the application containers present in Kubernetes environments.

`<https://docs.tungsten.io/en/latest/tungsten-fabric-cloud-native-user-guide/how-to-enable-kubevirt-kubernetes.html>`_


Support for Keystone Authentication in Kubernetes Environments Using Juju
-------------------------------------------------------------------------

Tungsten Fabric can now use the Keystone authentication service in OpenStack for authentication in environments that contain cloud networks using both Openstack and Kubernetes orchestrators when the Kubernetes environment is running Juju. This capability simplifies authentication in mixed cloud environments and is available when the cloud networks are both using Tungsten Fabric.

`<https://docs.tungsten.io/en/latest/tungsten-fabric-cloud-native-user-guide/how-to-use-keystone-in-kubernetes.html>`_

Support for contrail-vrouter-utils package in the Contrail Tools Container
--------------------------------------------------------------------------

Starting with Contrail Networking Release 2011, the contrail-vrouter-utils package is available only in the contrail-tools container. You must use the contrail-tools container to execute tools like vif, nh, rt, and so on available in the contrail-vrouter-utils package. In previous releases, the contrail-vrouter-utils package is available in the contrail-vrouter-agent and contrail-vrouter-dpdk container. You can no longer use the contrail-vrouter-agent and contrail-vrouter-dpdk containers to execute the tools available in the contrail-vrouter-utils package.


Support for Netronome SmartNIC vRouter for Juju Charms Deployment
-----------------------------------------------------------------

Tungsten Fabric now supports Netronome Agilio CX for Tungsten Fabric deployment with Juju charms. This feature enables increased packets per second (PPS) capacity of Tungsten Fabric vRouter datapath allowing applications to reach their full processing capacity. Additionally, it allows to reclaim CPU cores from Tungsten Fabric vRouter off-loading permitting more VMs and VNFs to be deployed per server.

`<https://docs.tungsten.io/en/latest/tungsten-fabric-installation-and-upgrade-guide/smartnic-vrouter-juju-charms.html>`_

Support for Red Hat OpenShift 4.6
---------------------------------

In the latest release of Tungsten Fabric you can enable Tungsten Fabric as the Container Network Interface (CNI) in environments using Red Hat OpenShift 4.6. Red Hat OpenShift is a platform. 
For more information on Red Hat Openshift 4.6 in Tungsten Fabric, see How to Contrail Networking and Red Hat OpenShift 4.6.
