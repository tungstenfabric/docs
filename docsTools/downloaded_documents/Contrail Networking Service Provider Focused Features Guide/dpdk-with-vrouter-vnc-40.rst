Configuring the Data Plane Development Kit (DPDK) Integrated with Contrail vRouter
==================================================================================

 

DPDK Support in Contrail​
-------------------------

Contrail Networking supports the Data Plane Development Kit (DPDK). DPDK
is an open source set of libraries and drivers for fast packet
processing. DPDK enables fast packet processing by allowing network
interface cards (NICs) to send direct memory access (DMA) packets
directly into an application’s address space, allowing the application
to poll for packets, and thereby avoiding the overhead of interrupts
from the NIC.

Integrating with DPDK allows a Contrail vRouter to process more packets
per second than is possible when running as a kernel module.

In Contrail Networking, before you use DPDK the DPDK configuration
should be defined in \ ``instances.yaml``\  for ansible based provision,
or in \ ``host.yaml``\  for helm-based provision. The AGENT_MODE
configuration specifies whether the hypervisor is provisioned in the
DPDK mode of operation.

When a Contrail compute node is provisioned with DPDK, the corresponding
yaml file specifies the number of CPU cores to use for forwarding
packets, the number of huge pages to allocate for DPDK, and the UIO
driver to use for DPDK.

Preparing the Environment File for Provisioning a Cluster Node with DPDK
------------------------------------------------------------------------

The environment file is used at provisioning to specify all of the
options necessary for the installation of a Contrail cluster, including
whether any node should be configured to use DPDK.

Each node to be configured with the DPDK vRouter must be listed in the
provisioning file with a dictionary entry, along with the percentage of
memory for DPDK huge pages and the CPUs to be used.

The following are descriptions of the required entries for the server
configuration. :

-  ``HUGE_PAGES``—Specify the percentage of host memory to be reserved
   for the DPDK huge pages. The reserved memory will be used by the
   vRouter and the Quick Emulator (QEMU) for allocating memory resources
   for the virtual machines (VMs) spawned on that host.

   **Note**

   The percentage allocated to ``HUGE_PAGES`` should not be too high,
   because the host Linux kernel also requires memory.

-  ``CPU_CORE_MASK``—Specify a CPU affinity mask with which vRouter will
   run. vRouter will use only the CPUs specified for its threads of
   execution. These CPU cores will be constantly polling for packets,
   and they will be displayed as 100% busy in the output of “top”.

   The supported format is hexadecimal (for example, 0xf).

-  ``DPDK_UIO_DRIVER``—Specify the UIO driver to be used with DPDK.

   The supported values include:

   -  ``vfio-pci``—Specify that the vfio module in the Linux kernel
      should be used instead of uio. The vfio module protects memory
      access using the IOMMU when a SR-IOV virtual function is used as
      the physical interface of vrouter.

   -  ``uio_pci_generic``—Specify that the UIO driver built into the
      Linux kernel should be used. This option does not support the use
      of SR-IOV VFs. This is the default option if DPDK_UIO_DRIVER is
      not specified.

   -  ``mlnx`` – For Mellanox ConnectX-4 and Mellanox ConnectX-5 NICs.

**Note**

For RHEL and Intel x710 Fortville-based NIC, use ``vfio-pci`` instead of
the default uio_pci_generic.

Use the standard Ansible or helm-based provision procedure. Upon
completion, your cluster, with specified nodes using the DPDK vRouter
implementation, is ready to use.

.. raw:: html

   <div id="jd0e98" class="sample" dir="ltr">

**Sample configuration in instances.yml for ansible-based provision**

.. raw:: html

   <div class="output" dir="ltr">

::

   Bms1:
       provider: bms
       ip: ip-address
       roles:
         vrouter:
                   AGENT_MODE: dpdk
                   CPU_CORE_MASK: “0xff”
                   DPDK_UIO_DRIVER: uio_pci_generic
                   HUGE_PAGES: 32000

.. raw:: html

   </div>

.. raw:: html

   </div>

.. raw:: html

   <div id="jd0e106" class="sample" dir="ltr">

**Sample configuration in host.yml for helm-based provision**

.. raw:: html

   <div class="output" dir="ltr">

::

   ...
   AGENT_MODE: dpdk
   CPU_CORE_MASK: “0xff”
   DPDK_UIO_DRIVER: uio_pci_generic
   HUGE_PAGES: 32000

.. raw:: html

   </div>

.. raw:: html

   </div>

Creating a Flavor for DPDK
--------------------------

To launch a VM in a DPDK-enabled vRouter hypervisor, the flavor for the
VM should be set to use huge pages. The use of huge pages is a
requirement for using a DPDK vRouter.

Use the following command to add the flavor, where ``m1.large`` is the
name of the flavor. When a VM is created using this flavor, OpenStack
ensures that the VM will only be spawned on a compute node that has huge
pages enabled.

.. raw:: html

   <div id="jd0e121" class="sample" dir="ltr">

.. raw:: html

   <div id="jd0e122" dir="ltr">

``# openstack flavor set m1.large --property hw:mem_page_size=large``

.. raw:: html

   </div>

.. raw:: html

   </div>

Huge pages are enabled for compute nodes where vRouter is provisioned
with DPDK.

If a VM is spawned with a flavor that does not have huge pages enabled,
the VM should not be created on a compute node on which vRouter is
provisioned with DPDK.

You can use OpenStack availability zones or host aggregates to exclude
the hosts where vRouter is provisioned with DPDK.

**Note**

Note: By default, 2MB huge pages are provisioned. If 1GB huge page is
required, it must be done by the Administrator.

Configuring and Verifying MTU for DPDK vRouter
----------------------------------------------

This section describes how you configure the maximum transmission unit
(MTU) for DPDK vRouter. To set MTU, you need to specify the desired
value for mtu in the ``contrail_vrouter_dpdk_bond.yaml`` file.

.. raw:: html

   <div id="jd0e144" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   network_config:
     -
       type: contrail_vrouter_dpdk
       name: vhost0
       members:
         -
           type: interface
           name: em3
         -
           type: interface
           name: em1
       mtu: 9100
       bond_mode: 2
       bond_policy: 802.3ad

.. raw:: html

   </div>

.. raw:: html

   </div>

You can verify the configured value from hypervisor by running the
following command:

.. raw:: html

   <div id="jd0e149" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   $ ip link list vhost0
   39: vhost0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 9100 qdisc pfifo_fast state UNKNOWN mode DEFAULT group default qlen 1000
       link/ether 98:03:9b:a7:3b:a0 brd ff:ff:ff:ff:ff:ff

.. raw:: html

   </div>

.. raw:: html

   </div>

You can use the vif -g or vif --get command to view the status of the
bond interfaces in a DPDK vRouter.

For example,

.. raw:: html

   <div id="jd0e162" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   # vif --get 0
   Vrouter Interface Table

   [...]
   vif0/0      PCI: 0000:00:00.0 (Speed 20000, Duplex 1) NH: 4
               Type:Physical HWaddr:00:1b:21:bb:f9:48 IPaddr:0.0.0.0
               Vrf:0 Mcast Vrf:65535 Flags:TcL3L2VpEr QOS:-1 Ref:26
               RX device packets:668852  bytes:110173140 errors:0
               RX port   packets:207344 errors:0
               RX queue errors to lcore 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
               Fabric Interface: eth_bond_bond0  Status: UP  Driver: net_bonding
               Slave Interface(o): 0000:02:00.0  Status: UP  Driver: net_ixgbe
               Slave Interface(1): 0000:02:00.1  Status: UP  Driver: net_ixgbe
               Vlan Id: 101  VLAN fwd Interface: bond
               RX packets:207344  bytes:45239337 errors:0
               TX packets:326159  bytes:237905360 errors:4
               Drops:0
               TX port   packets:326145 errors:10
               TX device packets:915402  bytes:511551768 errors:0

.. raw:: html

   </div>

.. raw:: html

   </div>

See `vRouter Command Line
Utilities <../task/configuration/vrouter-cli-utilities-vnc.html>`__ for
a list of vRouter command line utilities.

 
