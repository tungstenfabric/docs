ARP plays a critical role in IP networks. This page describes ARP processing VRouter from Release 2.1 onwards

# Overview
ARP uses broadcast MAC address (ARP requests, Gratuitous ARP) to flood
packet in a broadcast domain. In virtualized networks, any form of broadcast
can be expensive operation and its preferrable to avoid broadcasts.

Contrail solution minimizes ARP flooding by implementing ARP proxy. Contrail
VRouter builds IP to ARP binding table based on different techniques given'
below. When VRouter receives ARP request for an IP and Contrail Vrouter knows
IP to ARP binding, it will proxy for the ARP request.

If Contrail VRouter identifies that packets must be routed, it will respond
with VRouter MAC address. When VRouter receives data packets with ARP
destination same as VRouter MAC address, it will subject the packet to
Layer-3 Routing.

# IP to MAC Binding
Contrail VRouter builds IP to MAC address binding using techniques given below.

## Configuration based Learning
Configuration for a virtual-machine-interface contains both IP address and MAC
address for the interface. For virtual-machines spawned on a compute node, the
vrouter will learn IP to MAC address binding from the configuration. The MAC
binding information is exported in EVPN Routes to the Control Node.

## E-VPN Route
All E-VPN route updates originated by Contrail compute nodes will contain both
IP and MAC information. The control-node will in turn redistribute the E-VPN
routes with both IP and MAC binding information. As a result, the IP to ARP
binding can be built for every host routes that are originated in the Contrail
domain.

Control nodes can have EVPN peering with gateway devices. If the EVPN routes by
gateway devices have IP to MAC binding information, VRouter can learn IP to MAC
binding from EVPN routes originated by gateway devices also.

If the EVPN route update by gateway devices does not contain IP information,
then VRouter will only learn the Layer2 forwarding information from the route
update.

## DHCP Snooping
As of R2.1, Contrail VRouter does not learn IP to MAC binding by DHCP Snooping.

## ARP Snooping
As of R2.1, Contrail VRouter does not learn IP to MAC binding by ARP Snooping.

# ARP Proxy
Contrail Vrouter tries to minimize the ARP flooding by proxying when it is
aware of IP to ARP binding.

All ARP packets are handled by the VRouter kernel module. When VRouter
receives ARP packet, it does a Inet Route lookup for the destination. The action
taken on ARP packet is based on following information,

* **Inet Route**
   
   Each unicast route contains following information to support ARP processing

  *    **Proxy Flag** Flag specifies if VRouter must do ARP proxy for

  *    **Flood Flag** Flag specifies if ARP packet is to be flooded

  *    **Stitched MAC** The stitched MAC for the route

* **NextHop**

  ARP processing can change based on the NH as given below

The following algorithm explains VRouter behavior on receiving an ARP Request
from one of the local VMs or one of the ToR node it manages
```
    Do Inet route lookup for the IP Destination
    If Route found for the IP Destination
        If Proxy Flag set in the route
            If MAC Stitching information present in the route
                Send ARP Respone with the MAC present in stitching information
            Else // MAC Stitching not found
                If Flood Flag set in the route
                    Flood the ARP packet
                Else // PROXY set, No-Flood, No-MAC Stitching
                    Send ARP response with VRouter MAC address
        Else // Proxy Flag not set
            If Flood flag set in the Route
                Flood the ARP packet
            Else // Proxy Not set, Flood not set
                Drop the packet
    Else // Route not found
        Flood the ARP
```

The following algorithm explains VRouter behavior on receiving an ARP Request
from fabric network.
```
Do Inet route lookup for the IP Destination
If Route found for the IP Destination
    If Proxy Flag set in the route
        If Route points to a local interface
            If MAC Stitching information present
                Send ARP Response with the stitched MAC
            Else
                If Flood flag set
                    Forward the ARP packet
                Else
                    Send ARP response with VRouter MAC address
        Else // Route does not point to local interface
            Forward the ARP packet
    Else // Proxy Flag not set
        Forward the ARP packet
```
Note, there is a difference between ARP Flooding and ARP Forwarding

<h2>ARP Flooding</h2>
ARP Flooding is initiated only when ARP packet is received from one of the local
interfaces on a compute node. ARP flooding initiates flooding the pacekt on
the virtual-network. ARP flooding is done by the VRouter using Layer-2 route
for broadcast MAC.

The Layer2 route for broadcast MAC will points to Composite-NH. The
Composite-NH in turn will contain following sub-Composite NH

* **Local Interface Composite NH**

  List of interfaces local to the compute node
* **Edge Replication Composite NH**

  Packet replication is Contrail domain is done in a distributed manner using
  Edge Replication Tree. The list contains list of Compute nodes for which
  packet must be replicated in the Edge Replication tree.
* **Source Replication Composite NH**

  Contains list of devices that do not participate in Edge Replication. All
  multicast/broadcast packets to such devices are replicated from the originator
  of multicast packets.
* **ToR Composite NH**

  A compute node can act as TSN for one or more ToR devices. ToR Composite NH
  contains list of ToR managed by this TSN.

<H2>ARP Forwarding</H2>
ARP Forwarding is initiated only when ARP packet is received on fabric interface.
An ARP packet is received on Fabric as a result of ARP Flooding initiated from
one of the compute nodes. In ARP Forwarding, the compute node is one of the
intermediate nodes in the broadcast tree for virtual network.

The forwarding rules in ARP Forwarding is given below,
* Replicate packet on Local Interfaces Composite NH

  Packet is replicated on Local Interfaces Composite NH
* ToR Composite NH

  Packet is replicated on ToR Composite NH
* If packet is received from one of the members in Source Replication Tree

  Packets are forwarded to Source Replication Tree only if it is received from
  another node in the Source Replication Tree
* Edge Replication Composite NH

    Packets are never forwarded on Edge Replication Composite NH

<H2>VRouter MAC Address</H2>
VRouter generates ARP response with its own MAC address in following scenario,

- ARP request is for gateway address
- VRouter identifes that packet must be routed

Based on who originated the packet, the MAC used for response will be,
- VRRP MAC :
  If the ARP request is from VM, VRouter responds with VRRP Mac.
- VHost MAC :
  If the ARP is received on fabric, VRouter responds with VHOST MAC address.
  ARP response for Baremetals will also with the VHOST Mac address

<H2>ARP and Gateway Address</H2>
In Contrail solution, Gateway Address is a special address. The Gateway address
is treated as Virtual-IP and can be owned by,

1. VRouter :
   VRouter on each compute node acts as default gateway for the VMs launched on
   the compute node. VRouter supports Ping and DHCP services on the Gateway
   address. VRouter also responds to ARP requests for Gateway IP with VRRP MAC
   address.

2. Gateway Device:
   The Gateway Address can also be asigned to a Gateway Device for external
   connectivity. The Gateway Device acts as default router for Baremetals

It is important that Virtual Machines uses VRouter as default gateway. For
VRouter to act as default-gateway, the ARP for default gateway should be the
VRRP address. VRouter also ensures that ARP request/responses from Gateway
Device do not reach Virtual Macines.

If ARP packet from Gateway Device is received on fabric inteface, VRouter will
not forward the packet to Virtual Machines.

<H1>ARP Flags management in a Route</H1>
The ARP flags in Inet Route entry is managed by Contrial VRouter Agent. The
design followed in Agent to set the flags is given below,

<H3>Flood Flag</H3>
All routes that are part of the IPAM for a virtual-network will have the ARP
flag set.

Gateway interfaces are an exception to this. Flood flag is not added for the
routes on Gateway interfaces.

<H3>Proxy Flag</H3>
Proxy Flag is set if,
- MAC stitching is available for a route
- Agent decides that the packet must be routed.

The table below gives values of Proxy and Flood flag in different scenarios

```
Scenario                                Proxy   Flood   MAC
-----------------------------------------------------------
VM spawned in same VN
    MAC Stitching present               T       T       N
    MAC Stitching not present           T       T       VM-MAC
Inter-VN Routes                         T       F       N
Service Chain routes                    T       F       N
ECMP Routes                             T       F       N
Fabric VRF Routes                       F       F       N
Gateway Interfaces
    Route on local compute              T       F       N
    Route on remote compute             T       T       N
Routes from Gateway Device
    Route within IPAM                   T       T
        MAC stitching present           T       T       MAC from EVPN route
        MAC stitching not-present       T       F       N
    Routes outside IPAM                 T       F       N
```

<H2>Virtual Networks with overlapping IPAM</H2>
Contrail supports use-case where two or more virtual-networks can have
overlapping IPAM address space. If the allocation pool in the two
virtual-network are different, the virtual-networks can be connected thru
network-policies. In this case, packets across the virtual-network must be
routed.

Contrail-Vrouter-Agent will treat this case as inter-vn traffic set.

<H2>Baremetal Servers (BMS)</H2>
All ARP broadcast packets from BMSs are received by the TSN node first.
The TSN node treats BMSs as a Virtual-Machine connected locally.