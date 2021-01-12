Support for Broadcast and Multicast
===================================

 

.. raw:: html

   <div id="intro">

.. raw:: html

   <div class="mini-toc-intro">

This section describes how the Contrail Controller supports broadcast
and multicast.

.. raw:: html

   </div>

.. raw:: html

   </div>

Subnet Broadcast
----------------

Multiple subnets can be attached to a virtual network when it is
spawned. Each of the subnets has one subnet broadcast route installed in
the unicast routing table assigned to that virtual network. The
recipient list for the subnet broadcast route includes all of the
virtual machines that belong to that subnet. Packets originating from
any VM in that subnet are replicated to all members of the recipient
list, except the originator. Because the next hop is the list of
recipients, it is called a composite next hop.

If there is no virtual machine spawned under a subnet, the subnet
routing entry discards the packets received. If all of the virtual
machines in a subnet are turned off, the routing entry points to
discard. If the IPAM is deleted, the subnet route corresponding to that
IPAM is deleted. If the virtual network is turned off, all of the subnet
routes associated with the virtual network are removed.

*Subnet Broadcast Example*

The following configuration is made:

-  Virtual network name – **vn1**

-  Unicast routing instance – ``vn1.uc.inet``

-  Subnets (IPAM) allocated – ``1.1.1.0/24; 2.2.0.0/16; 3.3.0.0/16``

-  Virtual machines spawned –
   ``vm1 (1.1.1.253); vm2 (1.1.1.252); vm3 (1.1.1.251); vm4 (3.3.1.253)``

The following subnet route additions are made to the routing instance
``vn1.uc.inet.0``:

-  ``1.1.1.255`` -> forward to NH1 (composite next hop)

-  ``2.2.255.255`` -> DROP

-  ``3.3.255.255`` -> forward to NH2

-  The following entries are made to the next-hop table:

-  NH1 – ``1.1.1.253; 1.1.1.252; 1.1.1.251``

-  NH2 – ``3.3.1.253``

If traffic originates for ``1.1.1.255`` from ``vm1 (1.1.1.253)``, it
will be forwarded to ``vm2 (1.1.1.252)`` and ``vm3 (1.1.1.251)``. The
originator ``vm1 (1.1.1.253)`` will not receive the traffic even though
it is listed as a recipient in the next hop.

All-Broadcast/Limited-Broadcast and Link-Local Multicast
--------------------------------------------------------

The address group ``255.255.255.255`` is used with all-broadcast
(limited-broadcast) and multicast traffic. The route is installed in the
multicast routing instance. The source address is recorded as ANY, so
the route is ``ANY/255.255.255.255 (*,G)``. It is unique per routing
instance, and is associated with its corresponding virtual network. When
a virtual network is spawned, it usually contains multiple subnets, in
which virtual machines are added. All of the virtual machines,
regardless of their subnets, are part of the recipient list for
``ANY/255.255.255.255``. The replication is sent to every recipient
except the originator.

Link-local multicast also uses the all-broadcast method for replication.
The route is deleted when all virtual machines in this virtual network
are turned off or the virtual network itself is deleted.

*All-Broadcast Example*

The following configuration is made:

-  Virtual network name – ``vn1``

-  Unicast routing instance – ``vn1.uc.inet``

-  Subnets (IPAM) allocated – ``1.1.1.0/24; 2.2.0.0/16; 3.3.0.0/16``

-  Virtual machines spawned –
   ``vm1 (1.1.1.253); vm2 (1.1.1.252); vm3 (1.1.1.251); vm4 (3.3.1.253)``

The following subnet route addition is made to the routing instance
``vn1.uc.inet.0``:

-  ``255.255.255.255/*`` -> NH1

The following entries are made to the next-hop table:

-  NH1 – ``1.1.1.253; 1.1.1.252; 1.1.1.251; 3.3.1.253``

If traffic originates for ``1.1.1.255`` from ``vm1 (1.1.1.253)``, the
traffic is forwarded to ``vm2 (1.1.1.252), vm3 (1.1.1.251)``, and
``vm4 (3.3.1.253)``. The originator ``vm1 (1.1.1.253)`` will not receive
the traffic even though it is listed as a recipient in the next hop.

Host Broadcast
--------------

The host broadcast route is present in the host routing instance so that
the host operating system can send a subnet broadcast/all-broadcast
(limited-broadcast). This type of broadcast is sent to the fabric by
means of a **vhost** interface. Additionally, any subnet
broadcast/all-broadcast received from the fabric will be handed over to
the host operating system.

 
