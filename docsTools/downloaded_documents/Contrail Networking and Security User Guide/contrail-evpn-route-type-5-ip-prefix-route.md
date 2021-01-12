# Support for EVPN Route Type 5

 

Contrail Release 5.0.1 and later supports EVPN Route Type 5 messages as
defined in the IETF specification *IP Prefix Advertisement in EVPN*.
EVPN Route Type 5 is an extension of EVPN Route Type 2, which carries
MAC addresses along with their associated IP addresses. EVPN Route Type
5 facilitates in inter-subnet routing.

Type 5 network layer reachability information (NLRI) contains
information in the following format:

<div id="jd0e17" class="sample" dir="ltr">

<div class="output" dir="ltr">

    +---------------------------------------+
    |      RD   (8 octets)                  |
    +---------------------------------------+
    |Ethernet Segment Identifier (10 octets)|
    +---------------------------------------+
    |  Ethernet Tag ID (4 octets)           |
    +---------------------------------------+
    |  IP Prefix Length (1 octet)           |
    +---------------------------------------+
    |  IP Prefix (4 or 16 octets)           |
    +---------------------------------------+
    |  GW IP Address (4 or 16 octets)       |
    +---------------------------------------+
    |  MPLS Label (3 octets)                |
    +---------------------------------------+

</div>

</div>

When Type-5 EVPN prefix is received from a BGP peer, it is first
installed into bgp.evpn.0 like all other routes. From here, based on
matching route targets, the route gets replicated into all \*.evpn.0
tables as applicable. From there, the routes are advertised over
Extensible messaging and presence protocol (XMPP) to all interested
agents.

**Note**

In Release 5.0.1, policy based route-leaking among different L3VRFs is
not supported. Hence, service chaining for Type 5 L3VRFs is also not
supported.

 
