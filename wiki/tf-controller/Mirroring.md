# Mirroring

Specific traffic can be mirrored to a traffic analyzer in Contrail by configuring rules to identify required flows to be mirrored and by specifying the analyzer where the traffic is mirrored to. In addition, mirroring can be configured on VM interfaces to get all the traffic to and from the interface to the specified analyzer. 

When a packet is mirrored, a Juniper header is added to provide additional information in the analyzer and then the packet is appropriately encapsulated and sent to the destination.

In R3.x, Mirroring function will be enhanced with the following options:

1. Knob to control addition of Juniper header in the mirrored packet. When disabled, the Juniper header is not added to the mirrored packet.
2. Knob to control if the Nexthop used is dynamic or static.

    * When dynamic is chosen, nexthop based on the destination is used. Packets are forwarded to the destination based on the encapsulation priority.
    * When static is chosen, nexthop created for the specified destination with VxLAN encapsulation using the configured VNI, destination VTEP, MAC is used to transmit the mirrored packets.

The following are the combinations required:

1. Dynamic Nexthop with Juniper header added (this is the default combination and is the only supported case upto R3.0.2)
2. Dynamic Nexthop, without Juniper header
3. Static Nexthop, without Juniper header, with the original L2 packet

### Implementation

Contrail-vrouter-agent adds a mirror entry in the vrouter and points to the nexthop to be used. The data for Juniper header is taken from the flow entry. In case of interface mirroring, the Juniper header will have a new TLV in the metadata to have interface name and use that instead of providing destination VN.

* Mirror entry will now have flags to indicate whether to add Juniper header or not and whether to add L2 header or not.
* When dynamic nexthop is used, nexthop is chosen as is done currently and the mirror entry points to it.
* When static nexthop is used, a new nexthop is created with the configured values and mirror entry points to it.

Dynamic without Juniper header
* Agent will change this to static NH while programming vrouter
* Agent will have destination VRF name from mirror configuration, sends subscribe to control-node (L2); get NH for the destination and program it as static in the kernel.
* The destination VN is special, with a flag indicating that it is meant for mirroring destination VMs. Based on this flag, vrouter sends the original packet to the VMs spawned in this destination virtual network.
* This mode is incompatible with existing analyzer instance.

Static without Juniper header
* Static never adds Juniper header and will always be VxLAN
* Same as dynamic without Juniper header, except that configuration gives VxLAN info.

Config required for 
* Dynamic without Juniper Header - Analyser VM mac & destination Mirror VRF, mode- dynamic, Juniper header - false 
* Static without Juniper Header -  VTEP IP , VNI(Vxlan_id), mode-static JuniperHeader -false 
