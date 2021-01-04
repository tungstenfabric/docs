Route Reflector Support in Contrail Control Node
================================================

 

Contrail Networking supports Route Reflector (RR) functionality in the
Control node for Internal Border Gateway Protocol (iBGP) peers. Route
reflection is a BGP feature that enables BGP routers to acquire route
information from one iBGP router and reflect or advertise the
information to other iBGP peers in the same autonomous system (AS).

In a large scale AS, deploying BGP routers peering with the Control Node
in a full-mesh topology affects scalability and leads to maintenance and
configurational issues. The issues are caused while exchanging large
volumes of routing information and maintaining connectivity among a
large number of devices in the AS. A Route Reflector provides a scalable
alternative to full-mesh internal BGP peering. See
`Figure 1 <contrail-route-reflectors.html#route-reflector-contrail>`__.

|Figure 1: Advantage of BGP Route Reflector over Full-mesh Topology|

You can create any number of RRs in the network. Each RR must have a
unique cluster ID to prevent looping among the RRs.

Contrail nodes support Edge Reflection Multicasting Virtual Private
Networking (ERMVPN) of the BGP Address Family. As non-Contrail nodes do
not support ERMVPN, RR is configured separately for Contrail nodes, and
external BGP speakers. If a single RR is deployed between Contrail nodes
and non-Contrail nodes, the RR cannot advertise ERMVPN routes to the
Contrail nodes. Contrail deploys a separate RR peering session among
Contrail nodes that supports ERMVPN and helps in propagating routes
among all Contrail nodes.

Benefits of RRs in Contrail
---------------------------

-  RRs can be deployed at multiple locations in the network, which helps
   to scale the BGP network at lower cost.

-  The RR feature conserves data center rack space by replacing physical
   route reflectors.

 

.. |Figure 1: Advantage of BGP Route Reflector over Full-mesh Topology| image:: documentation/images/g300492.png
