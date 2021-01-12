Mirroring Enhancements
======================

 

Mirroring Specified Traffic
---------------------------

Specific traffic can be mirrored to a traffic analyzer in Contrail by:

-  Configuring rules to identify the flows to be mirrored, and

-  Specifying the analyzer to which the traffic is mirrored

Additionally, mirroring can be configured on virtual machine (VM)
interfaces to send all the traffic to and from the interface to the
specified analyzer.

Configuring Headers and Next Hops
---------------------------------

When a packet is mirrored, a Juniper header is added to provide
additional information in the analyzer, then the packet is encapsulated
and sent to the destination.

Starting with Contrail 3.x releases, mirroring is enhanced with the
following options:

-  Option to control addition of the Juniper header in the mirrored
   packet.

   -  When disabled, the Juniper header is not added to the mirrored
      packet.

-  Option to control whether the next hop used is dynamic or static.

   -  If dynamic is selected, the next hop based on the destination is
      used. Packets are forwarded to the destination based on the
      encapsulation priority.

   -  If static is chosen, the next hop is created for the specified
      destination with VxLAN encapsulation using the configured VNI,
      destination VTEP, and MAC to transmit the mirrored packets.

      The following combinations are supported:

      -  Dynamic next hop with Juniper header added

         The default combination and the only supported case up to
         Release 3.0.2

      -  Dynamic next hop, without Juniper header

      -  Static next hop, without Juniper header, with the original
         Layer 2 packet

How Mirroring is Implemented
----------------------------

The Contrail vrouter agent adds a mirror entry in the vrouter and points
to the next hop to be used. The data for the Juniper header is taken
from the flow entry. For interface mirroring, the Juniper header has a
TLV in the metadata to use the interface name instead of providing a
destination VN.

For more information about implementation details, see
https://github.com/Juniper/contrail-controller/wiki/Mirroring.

 
