This document describes the details of SRIOV configuration, configuration knobs
in different components of Openstack modules, flow of data between those
components, Contrail provisioning/fab changes to achieve this configuration and
testbed changes.


##1. Enabling SRIOV on compute node

A) Enable ASPM (Active State Power Management) of PCI Devices in BIOS
   (If required, upgrade BIOS to see ASPM option)

B) Enable Intel IOMMU on linux, in passthrough mode

        B1) In /etc/default/grub, GRUB_CMDLINE_LINUX_DEFAULT="iommu=pt intel_iomAu=on"

        B2) updatA-grub

        B3) Reboot the compute node


C) Enable the required number of VF's on the required NIC
   echo '7' > /sys/class/net/eth0/device/sriov_numvfs
   
   This enables 7 VF's on 'eth0' interface, which can be observed on 'lspci -nn'
    or 'ip link'


##2) Config file changes

A) Nova compute config file changes
   
   A1) Configure the physical network names on physical interfaces in 
       /etc/nova/nova.conf.
       The physical interface must have VF's enabld as mentioned in 1.C

        [default]
        pci_passthrough_whitelist = 
          { "devname": "eth0", "physical_network": "physnet1"}

        The above configuration allows the VM's attached to "physnet1" to use 
        "eth0"s VF's.
        The pci_passthrough_whitelist can repeat multiple times for every 
        physical inteface of compute node in the configuration file. 

   A2) Reboot nova compute (service nova-compute restart)

B) Nova scheduler config file changes

   B1) Configure Nova Scheduler filter which choses compute nodes based on 
       above SRIOV config in /etc/nova/nova.conf

        [default]
        scheduler_default_filters = PciPassthroughFilter
        scheduler_available_filters = nova.scheduler.filters.all_filters
        scheduler_available_filters = 
           nova.scheduler.filters.pci_passthrough_filter.PciPassthroughFilter

   B2) Restart nova scheduler (service nova-scheduler restart)


##3) Fab provisioning support

The above configuration and provisiong can be achieved using the Contrail Fab
setup.

A) testbed.py changes

   A1)
        

        env.sriov = {
            host1 :[{'interface' : 'eth0', 'VF' : 7, 'physnets' : ['physnet1']},
                    {'interface' : 'eth1', 'VF' : 7, 'physnets' : ['physnet2']}],
            host2 :[{'interface' : 'eth0', 'VF' : 7, 'physnets' : ['physnet3']}]
        }

   A2) host1 and host2 need to have  compute node roles in the testbed

   A3) sriov stanza describes the configuration to be setup on two different
       compute nodes "host1" and "host2".
       "host1" to be setup with two physical interface "eth0" and "eth1" having 
       '7' VF's each belonging to "physnet1" and "physnet2" respectively.
       "host2" to be setup with "eth0" having '7' VF's belonging to physical
       network "physnet3"

B) Complete Cloud Setup

   B1) "fab setup_all" enables required linux iommu option as mentioned in 1.B,
        configures VF's as mentioned in 1.C, configures physical networks as
        mentioned in 2.A1

   B2) "openstack" role node also gets setup with scheduler options as
        mentioned in 2.B1

   B3) Enabling the BIOS, as in 1.A, needs to be setup manually before the
       fab provsioning starts

C) Provisioning a new SRIOV compute node independently
   
   C1) If a new compute node needs to be setup with SRIOV capability both compute node
       role and openstack role needs to be setup
   
   C2) fab add_vrouter_node:user@a.b.c.d sets up the new compute node with required
       configuration as in 1.C, 2.A1

   C3) fab setup_openstack_node:user@a.b.c.d sets up the openstack role as in 2.B1


##4) Launching VMs:

Once the provisioning is complete, the SRIOV VM's can be launched using the below
neutron commands.Alternatively, the configuration can be done using Contrail UI.
The openstack "Horizon" does not support booting of SRIOV VM's.

A) Create VN with above configured physical network and vlan id

   neutron net-create  --provider:physical_network=physnet1
                       --provider:segmentation_id=100 vn1

   This creates virtual network vn1 with belonging to physical network "physnet1"
    with the vlan id "100"

B) Crate a subnet in vn1

   neutron subnet-create vn1 a.b.c.d/netmask

C) neutron port-create --name <name of port> <vn1 uuid> --binding:vnic_type direct

   This creates an SRIOV port belonging to virtual network vn1

D) nova boot --flavor m1.large --image <image name> --nic port-id=<uuid of above port> <vm name>

   This boots a VM with SRIOV port on the permissible Compute node.

E) VM's "lspci" can be used to verify that the Ethernet controller is VF


##5) Internals

A) Neutron and API server

   The provider network configuration is supported by neutorn extension "provider".
   For the SRIOV support, neutron service is enabled with this extension and
   Contrail core plugin is modified to support this extension. The SRIOV port,
   requires new bindings, viz; "binding:profile", "binding:vif_details",
   "binding:vif_type", "binding:vnic_type" and "binding:host_id". Contrail's
   api-server persists this binding information in Cassandra and this binding
   information is available to different components of Openstack through
   "neutron GetPort" API.

   "binding:host_id" contains the compute node name on which the VM is (to be)
   launched, "binding:profile" contains the PCI vendor, slot and VF information
   for Libvirt to bind the VM's interface to VF, "binding:vnic_type" as "normal"
   for regular VM's and "direct" for SRIOV ports, "binding:vif_type" as
   "vrouter" for regular VM's and "hw_veb" for SRIOV VM's, "binding:vif_details"
   contains vlan id the VF needs to be configured with.

   For SRIOV port, the "binding:vnic_type" is set as "direct" and
   "binding:vif_type" as "hw_veb" by api-server at the time of port configuration.
   "binding:profile", "binding:host_id" is updated by nova-api once the
   nova-scheduler filters the compute and provides the profiling parameters.
   "binding:vif_details" are updated by api-server at the time of port
   configuration with vlan id from virtual-network the port is belonging to.

   For SRIOV port, currently "binding:vnic_type" is always 'direct' and 'macvtap'
   is not supported.

   api-server also sets up the link from VM to compute node's vrouter object so that
   the configuration data objects like VM, VMI etc are downloaded to compute node's
   agent.

B) Nova compute

   Resource tracker in nova-compute updates Disk information, Memory information
   and Virtual CPU infornation to Nova Scheduler. Once the nova-compute is setup
   with PCI and physical network information, as in 2.A, the resource tracker
   updates available free VF and physical network information for every configured
   physical interface to nova-scheduler. If any new SRIOV VM is booted on the
   compute node, resource tracker updates the free available VF's again to
   nova-scheduler. This way nova-scheduler always contains free VF's of every
   compute node along with physical network names for "PciPassThroughFlter" to
   decide which host can be chosen for VM to boot.

   The nova-compute libvirt plugin uses the above mentioned "binding:profile"
   information to generate the domxml file with PCI information (vendor, slot,
   address, VF number) and Vlan id when the "binding:vif_type" is "hw_veb".
   The nova-compute libvirt plugin communicates to libvirtd over unix domain
   socket and  libvirtd configures the physical interface with the required
   settings. As 'macvtap' mode is not supported, SRIOV port is directly connected
   to VF. 

C) Nova scheduler

   Due to changes in 2.B, nova-scheduler uses "PciPassthroughFilter" as default
   filter to decide on which host the VM should launch. "PciPassthroughFilter"
   fitlers the hosts based on "physical network" names and free available VF's
   on that compute.

   A custom filter can be written and attached to nova-scheduler to suit the
   requirements of the user

D) vrouter-agent

   Compute node's vrouter-agent receives the VM, VMI config objects when an SRIOV
   VM is launched on this compute node from control-node as IFMAP objects. vrouter
   uses this information to generate the UVE's (and if possible VF statistics)

##6) Configuration Flow

A) When a virtual network is created with provider information, the provider
   information is persisted by api-server in Cassandra. The VN  contains the
   name of physical network and vlan id to use.

B) When a neutron port is created with vnic_type as direct, api-server updates
   the "binding:vif_type" to "hw_veb", "binding:vnic_type" to "direct",
   "binding:vif_details" with vlan id from virtual network.

C) When nova-boot is command is issued with above SRIOV port, nova-api receives
   the REST API

D) nova-api identifies that VM is being booted with vnic_type direct and gets the
   port's physical network name from Neutron using GetPort API

E) nova-api does an RPC call to nova-scheduler to filter the compute to launch
   the VM

F) nova-scheduler filters the compute node in "PciPassthroughFilter" using
   physical network name that is passed from nova-api. Scheduler uses nova-compute
   resource tracker information to identify the compute that are having free VF's
   in given physical network name. Once the compute is filtered, the filter
   information is returned to nova-api

G) nova-api updates the "binding:host_id" and "binding:profile" data in port,
   as a result api-server updates  port binding information with new VMI bindings

H) nova-scheduler also RPC casts (one way request message) to chosen compute node
   to launch the VM

I) nova-compute plugin gets the port information using nova-conductor and retieves
   the required data like "vif_profile", "vif_type", "vif_details" and "vnic_type".
   Upon getting this required data, it invoked spawn() routine of the libvirt plugin

J) nova-compute's libvirt updates the domxml file corresponding to VM with the
   required information like PCI information and Vlan id and communicates the
   data to libivrtd

K) libvirtd launches the VM and sets up the required VF setting on physical
   interface

***
