Multiqueue Virtio Interfaces in Virtual Machines
================================================

Tungsten Fabric 3.2 adds support for multiqueue for the DPDK-based vrouter.

Tungsten Fabric 3.1 supports multiqueue virtio interfaces for Ubuntu
kernel-based router, only.

Multiqueue Virtio Overview
--------------------------

OpenStack Liberty supports the ability to create VMs with multiple
queues on their virtio interfaces. Virtio is a Linux platform for I/O
virtualization, providing a common set of I/O virtualization drivers.
Multiqueue virtio is an approach that enables the processing of packet
sending and receiving to be scaled to the number of available virtual
CPUs (vCPUs) of a guest, through the use of multiple queues.

Requirements and Setup for Multiqueue Virtio Interfaces
-------------------------------------------------------

To use multiqueue virtio interfaces, ensure your system meets the
following requirements:

-  The OpenStack version must be Liberty or greater.

-  The maximum number of queues in the VM interface is set to the same
   value as the number of vCPUs in the guest.

-  The VM image metadata property is set to enable multiple queues
   inside the VM.

Setting Virtual Machine Metadata for Multiple Queues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the following command on the OpenStack node to enable multiple
queues on a VM:
::

   source /etc/contrail/openstackrc
   nova image-meta <image_name> set hw_vif_multiqueue_enabled="true"

After the VM is spawned, use the following command on the virtio
interface in the guest to enable multiple queues inside the VM:

``ethtool –L <interface_name> combined <#queues>``

Packets will now be forwarded on all queues in the VM to and from the
vRouter running on the host.

.. note::

   Multiple queues in the VM are only supported with the kernel mode
   vRouter in Tungsten Fabric 3.1.

Tungsten Fabric 3.2 adds support for multiple queues with the DPDK-based
vrouter, using OpenStack Mitaka. The DPDK vrouter has the same setup
requirements as the kernel mode vrouter. However, in the ``ethtool –L``
setup command, the number of queues cannot be higher than the number of
CPU cores assigned to vrouter in the testbed file.

 
