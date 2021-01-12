Mapping VLAN Tags from a Physical NIC to a VMI (NIC-Assisted Mirroring)
=======================================================================

 

When mirroring is enabled, the vRouter throughput reduces because of the
additional packet handling overhead caused by cloning the packet to be
mirrored, encapsulating it in the required header, and forwarding it to
the mirror destination. Impact to throughput increases in proportion to
the amount of traffic that needs to be mirrored.

A solution to avoid impact on throughput due to mirroring is to use the
mirroring capabilities of an installed Network Interface Card (NIC).

Contrail Release 4.0 has the ability to mirror specific traffic to a
traffic analyzer or to a physical probe using the Network interface card
(NIC) instead of the vRouter to mirror packets. When NIC-assisted
mirroring is enabled, ingress packets to be mirrored sent from a VM are
routed to the NIC with a configured VLAN tag. The NIC is configured for
VLAN port-mirroring and mirrors any packet with the VLAN tag.

In this approach, the vRouter doesn’t mirror the packets. When
NIC-assisted mirroring is enabled, the ingress packets coming from the
VM that are to be mirrored are sent to the NIC with a configured VLAN
tag.

The NIC is programmed to do VLAN port mirroring, so that iany packet
with the configured VLAN is mirrored additionally by the NIC. This
change in vRouter is only for traffic coming from the VMs. Traffic
coming from the fabric is directly mirrored from the NIC itself and
there is no additional mirroring need in vRouter. The programming of the
NIC itself for appropriate mirroring is outside the scope of the current
activity. An example is the Niantic 82599 10G NIC, which supports VLAN
port mirroring options.

The following are cautions to observe when using NIC-assisted mirroring:

-  VM traffic sent to another VM running on the same compute node will
   not be mirrored when NIC-assisted mirroring is selected.

-  Traffic coming in from the fabric interface will not be mirrored.

-  When a VLAN interface is used as the fabric interface, traffic will
   be tagged first with the NIC-assisted mirroring VLAN, followed by the
   VLAN tag on the fabric interface. The NIC-assisted mirroring VLAN
   will be the inner tag and the fabric interface VLAN will be the outer
   tag.

The NIC must be programmed for VLAN port mirroring. While configuring
mirroring in Contrail, the user can indicate NIC-assisted mirroring with
the VLAN tag. The Contrail UI supports NIC-assisted mirroring
configuration in the Ports page and in the Policies page with an
additional flag for NIC-assisted mirroring and the VLAN tag to be used.

 
