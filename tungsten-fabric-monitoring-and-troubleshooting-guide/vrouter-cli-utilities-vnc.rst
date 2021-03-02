vRouter Command Line Utilities
==============================

:date: 2020-12-07 

Overview
--------

vRouter is the component that takes packets from VMs and forwards them
to their destinations. In this effort, vRouter depends on the vRouter
agent to make sense of the overall topology, understand the various
policies that govern the communication between VMs, and program them in
vRouter in a way vRouter understands.

vRouter has a few fundamental data structures that abstracts out the
various communication paths. There is "interface," "flow," "route," and
"nexthop" that enables vRouter to push packets to their eventual
destinations. In addition, vRouter also has good statistics that can
help understand and debug packet paths. Various command line utilities
provided by the vRouter can be used to display these data structures and
better understand the behavior that one sees in a compute node.

This section describes the shell prompt utilities available for
examining the state of the vRouter kernel module in Contrail.

The most useful commands for inspecting the Contrail vRouter module are
summarized in the following table.

+---------------+-----------------------------------------------------+
| Command       | Description                                         |
+===============+=====================================================+
| ``vif``       | Inspect vRouter interfaces associated with the      |
|               | vRouter module.                                     |
+---------------+-----------------------------------------------------+
| ``flow``      | Display active flows in a system.                   |
+---------------+-----------------------------------------------------+
| ``vrfstats``  | Display next hop statistics for a particular VRF.   |
+---------------+-----------------------------------------------------+
| ``rt``        | Display routes in a VRF.                            |
+---------------+-----------------------------------------------------+
| ``dropstats`` | Inspect packet drop counters in the vRouter.        |
+---------------+-----------------------------------------------------+
| ``mpls``      | Display the input label map programmed into the     |
|               | vRouter.                                            |
+---------------+-----------------------------------------------------+
| ``mirror``    | Display the mirror table entries.                   |
+---------------+-----------------------------------------------------+
| ``vxlan``     | Display the VXLAN table entries.                    |
+---------------+-----------------------------------------------------+
| ``nh``        | Display the next hops that the vRouter knows.       |
+---------------+-----------------------------------------------------+
| ``--help``    | Display all command options available for the       |
|               | current command.                                    |
+---------------+-----------------------------------------------------+
| dpdkinfo      | Displays internal data structure details of a DPDK  |
|               | enabled vRouter.                                    |
+---------------+-----------------------------------------------------+
| dpdkconf      | Use this command to add or delete a DDP profile.    |
+---------------+-----------------------------------------------------+

The following sections describe each of the vRouter utilities in detail.

vif Command
-----------

The vRouter requires vRouter interfaces (``vif``) to forward traffic.
Use the ``vif`` command to see the interfaces that are known by the
vRouter.

.. note::

   Having interfaces only in the OS (Linux) is not sufficient for
   forwarding. The relevant interfaces must be added to vRouter. Typically,
   the set up of interfaces is handled by components like ``nova-compute``
   or vRouter agent.

   The ``vif`` command can be used to see the interfaces that the vRouter
   is aware of by including the ``--list`` option.

.. raw:: html

   <div id="jd0e162" class="sample" dir="ltr">

**Example: vif --list**

.. raw:: html

   <div class="output" dir="ltr">

::

   bash$ vif --list
   Vrouter Interface Table

   Flags: P=Policy, X=Cross Connect, S=Service Chain, Mr=Receive Mirror
          Mt=Transmit Mirror, Tc=Transmit Checksum Offload, L3=Layer 3, L2=Layer 2
          D=DHCP, Vp=Vhost Physical, Pr=Promiscuous, Vnt=Native Vlan Tagged
          Mnp=No MAC Proxy

   vif0/0      OS: eth0 (Speed 1000, Duplex 1)
               Type:Physical HWaddr:00:25:90:c3:08:68 IPaddr:0
               Vrf:0 Flags:L3L2Vp MTU:1514 Ref:22
               RX packets:2664341  bytes:702708970 errors:0
               TX packets:1141456  bytes:234609942 errors:0

   vif0/1      OS: vhost0
               Type:Host HWaddr:00:25:90:c3:08:68 IPaddr:0
               Vrf:0 Flags:L3L2 MTU:1514 Ref:3
               RX packets:716612  bytes:155442906 errors:0
               TX packets:2248399  bytes:552491888 errors:0

   vif0/2      OS: pkt0
               Type:Agent HWaddr:00:00:5e:00:01:00 IPaddr:0
               Vrf:65535 Flags:L3 MTU:1514 Ref:2
               RX packets:450524  bytes:94618532 errors:0
               TX packets:437968  bytes:66753290 errors:0

   vif0/3      OS: tap519615d8-a2
               Type:Virtual HWaddr:00:00:5e:00:01:00 IPaddr:0
               Vrf:1 Flags:PL3L2 MTU:9160 Ref:6
               RX packets:134  bytes:15697 errors:0
               TX packets:8568  bytes:945944 errors:0

.. raw:: html

   </div>

.. raw:: html

   </div>

Table 1: vif Fields

.. list-table:: 
      :header-rows: 1

      * - Release
        - Description
      * - vif Output Field
        - Description
      * - vif0/X
        - The vRouter assigned name, where 0 is the router ID and X is the index allocated to the interface within the vRouter.
      * - OS: pkt0
        - The pkt0 (in this case) is the name of the actual OS (Linux) visible interface name. For physical interfaces, the speed and the duplex settings are also displayed.
      * - ``Type:xxxxx``
        - ``Type:Virtual HWaddr:00:00:5e:00:01:00 IPaddr:0``

          The type of interface and its IP address, as defined by vRouter. The values can be different from what is seen in the OS. Types defined by vRouter include:

          * Virtual – Interface of a virtual machine (VM).
          * Physical – Physical interface (NIC) in the system.
          * Host – An interface toward the host.
          * Agent – An interface used to trap packets to the vRouter agent when decisions need to be made for the forwarding path.
      
      * - ``Vrf:xxxxx``
        - ```Vrf:65535 Flags:L3 MTU:1514 Ref:2```
          
          The identifier of the vrf to which the interface is assigned, the flags set on the interface, 
          the MTU as understood by vRouter, and a reference count of how many individual entities actually 
          hold reference to the interface (mainly of debugging value).

          Flag options identify that the following are enabled for the interface:
          
          * P - ​Policy. All traffic that comes to vRouter from this interface are subjected to policy.
          * L3 - ​Layer 3 forwarding.
          * L2 - ​Layer 2 bridging.
          * X - Cross connect mode, only set on physical and host interfaces, indicating that packets are moved between physical and host directly, with minimal intervention by vRouter. Typically set when the agent is not alive or not in good shape.
          * M - Mirroring transmit direction. All packets that egresses this interface are mirrored.
          * Mr - Mirroring receive direction​. All packets that ingresses this interface will be mirrored.
          * Tc - ​Checksum offload on the transmit side. Valid only on the physical interface.

      * - Rx
        - RX packets:60 bytes:4873 errors:0

          Packets received by vRouter from this interface.

      * - Tx
        - TX packets:21 bytes:2158 errors:0

          Packets transmitted out by vRouter on this interface.



vif Options
~~~~~~~~~~~

Use\ ``vif –-help`` to display all options available for the vif
command. Following is a brief description of each option.

.. note::

   It is not recommended to use the following options unless you are very
   experienced with the system utilities.

::

   # vif --help
   Usage: vif [--create <intf_name> --mac < --mac  <C>]
              [--add <C>> --mac <mac> --vrf <vrf>
                    --type [vhost|agent|physical|virtual|monitoring]
                    --transport [eth|pmd|virtual|socket]
                    --xconnect <physical interface name>
                    --policy, --vhost-phys, --dhcp-enable]
                    --vif <vif ID> --id <intf_id> --pmd --pci]
              [--delete <intf_id>|<intf_name>]
              [--get <intf_id>][--kernel]
              [--set <intf_id> --vlan <vlan_id> --vrf <vrf_id>]
              [--list][--core <core number>][--rate]
              [--sock-dir <sock dir>]
              [--clear][--id <intf_id>][--core <core_number>]
              [--help}

.. raw:: html

   </div>

+--------------+------------------------------------------------------+
| Option       | Description                                          |
+==============+======================================================+
| ``--create`` | Creates a “host” interface with name                 |
|              | ``<intf_name>``\ and mac ``<mac>``\ on the host      |
|              | kernel. The ``vhost0`` interface that you see on     |
|              | Linux is a typical example of invocation of this     |
|              | command.                                             |
+--------------+------------------------------------------------------+
| ``--add``    | Adds the existing interfaces in the host OS to       |
|              | vRouter, with type and flag options.                 |
+--------------+------------------------------------------------------+
| ``--delete`` | Deletes the interface from vRouter. The              |
|              | ``<intf_id> i`` is the vRouter interface ID as given |
|              | by ``vif0/X``, where ``X`` is the ID. So, in         |
|              | ``vif0/1``, ``1`` is the interface index of that vif |
|              | inside the vRouter module.                           |
+--------------+------------------------------------------------------+
| ``--get``    | Displays a specific interface. The ``<intf_id>``\ is |
|              | the vRouter interface ID, unless the command is      |
|              | appended by the ``—kernel`` option, in which case    |
|              | the ID is the kernel ID.                             |
+--------------+------------------------------------------------------+
| ``--set``    | Set working parameters of an interface. The ones     |
|              | supported are the ``vlan id`` and the ``vrf``. The   |
|              | ``vlan id`` as understood by vRouter differs from    |
|              | what one typically expects and is relevant for       |
|              | interfaces of service instances.                     |
+--------------+------------------------------------------------------+
| ``--list``   | Display all of the interfaces of which the vRouter   |
|              | is aware.                                            |
+--------------+------------------------------------------------------+
| ``--help``   | Display all options available for the current        |
|              | command.                                             |
+--------------+------------------------------------------------------+
| ``--clear``  | Clears statistics for all interfaces on all cores.   |
|              | For more information, see clear                      |
|              | Command                                              |
+--------------+------------------------------------------------------+

clear Command
-------------

Contrail Networking Release 2008 supports clearing of vif statistics
counters for all interfaces by using the ``--clear`` command. 
Table 2: clear Command Options

+----------------------------------+----------------------------------+
| Option                           | Description                      |
+==================================+==================================+
| ``--clear``                      | Clears statistics for all        |
|                                  | interfaces on all cores.         |
+----------------------------------+----------------------------------+
| ``--clear --id <vif-id>``        | Clears statistics for a specific |
|                                  | interface.                       |
+----------------------------------+----------------------------------+
| ``--clear --core <core-id>``     | Clears statistics on a specific  |
|                                  | core for all interfaces.         |
+----------------------------------+----------------------------------+
| ``--clear                        | Clears statistics for a specific |
| --id <vif-id> --core <core-id>`` | interface on a specific core.    |
+----------------------------------+----------------------------------+

flow Command
------------

Use the ``flow`` command to display all active flows in a system.

.. raw:: html

   <div id="jd0e495" class="example" dir="ltr">

Example: flow -l
~~~~~~~~~~~~~~~~

Use ``-l``\ to list everything in the flow table. The -1 is the only
relevant debugging option.

::

     # flow –l  
   Flow table
      Index        Source:Port                   Destination:Port   Proto(V)
     ------------------------------------------------------------------------------------------------- 
    263484          1.1.1.252:1203            1.1.1.253:0        1 (3)
                       (Action:F, S(nh):91,  Statistics:22/1848)
        379480          1.1.1.253:1203            1.1.1.252:0        1 (3) 
                       (Action:F, S(nh):75,  Statistics:22/1848)     

.. raw:: html

   </div>

​Each record in the flow table listing displays the index of the record,
the source IP: source port, the destination ip: destination port, the
inet protocol, and the source VRF (V) to which the flow belongs.

Each new flow has to be approved by the vRouter agent. The agent does
this by setting actions for each flow. There are three main actions
associated with a flow table entry: Forward (‘F’), Drop (‘D’), and Nat
(‘N’).

For NAT, there are additional flags indicating the type of NAT to which
the flow is subject, including: SNAT (S), DNAT (D), source port
translation (Ps), and destination port translation (Pd).

S(nh) indicates the source nexthop index used for the RPF check to
validate that the traffic is from a known source. If the packet must go
to an ECMP destination, E:X is also displayed, where ‘X’ indicates the
destination to be used through the index within the ECMP next hop.

The Statistics field indicates the Packets/Bytes that hit this flow
entry.

There is a Mirror Index field if the traffic is mirrored, listing the
indices into the mirror table (which can be dumped by using
``mirror –-dump``).

If there is an explicit association between the forward and the reverse
flows, as is the case with NAT, you will see a double arrow in each of
the records with either side of the arrow displaying the flow index for
that direction.

.. raw:: html

   <div id="jd0e523" class="example" dir="ltr">

Example: flow -r
~~~~~~~~~~~~~~~~

Use ``-r`` to view all of the flow setup rates.

::

   # flow –r  
   New =    2, Flow setup rate =    3 flows/sec, Flow rate =    3 flows/sec, for last  548 ms  
   New =    2, Flow setup rate =    3 flows/sec, Flow rate =    3 flows/sec, for last  543 ms  
   New =   -2, Flow setup rate =   -3 flows/sec, Flow rate =   -3 flows/sec, for last  541 ms  
   New =    2, Flow setup rate =    3 flows/sec, Flow rate =    3 flows/sec, for last  544 ms  
   New =   -2, Flow setup rate =   -3 flows/sec, Flow rate =   -3 flows/sec, for last  542 ms  

.. raw:: html

   </div>

.. raw:: html

   <div id="jd0e534" class="example" dir="ltr">

Example: flow --help
~~~~~~~~~~~~~~~~~~~~

Use ``--help`` to display all options available for the flow command.

::

   # flow –-help  
   Usage:flow [-f flow_index][-d flow_index][-i flow_index]
                           [--mirror=mirror table index]
                           [-l]
      -f <flow_index>    Set forward action for flow at flow_index <flow_index>
     -d <flow_index> Set drop action for flow at flow_index <flow_index>
     -i <flow_index>     Invalidate flow at flow_index <flow_index>
     --mirror                  mirror index to mirror to
     -l                            List  all flows
     -r                            Start dumping flow setup rate
     --help                    Print this help     

.. raw:: html

   </div>

vrfstats Command
----------------

Use ``vrfstats`` to display statistics per next hop for a ``vrf``. It is
typically used to determine if packets are hitting the expected next
hop.

.. raw:: html

   <div id="jd0e559" class="example" dir="ltr">

Example: vrfstats --dump
~~~~~~~~~~~~~~~~~~~~~~~~

The ``—dump`` option displays the statistics for all VRFs that have seen
traffic. In the following example, there was traffic only in
``Vrf 0``\ (the public VRF). ``Receives`` shows the number of packets
that came in the fabric destined to this location. ``Encaps`` shows the
number of packets destined to the fabric.

If there is VM traffic going out on the fabric, the respective tunnel
counters will increment. ​

::

    # vrfstats --dump
     Vrf: 0
     Discards 414, Resolves 3, Receives 165334
     Ecmp Composites 0, L3 Mcast Composites 0, L2 Mcast Composites 0, Fabric Composites 0, Multi Proto Composites 0
     Udp Tunnels 0, Udp Mpls Tunnels 0, Gre Mpls Tunnels 0
     L2 Encaps 0, Encaps 130955

.. raw:: html

   </div>

.. raw:: html

   <div id="jd0e581" class="example" dir="ltr">

Example: vrfstats --get 0​
~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ``--get 0`` to retrieve statistics for a particular ``vrf``.

::

    # vrfstats --get 0
     Vrf: 0
     Discards 418, Resolves 3, Receives 166929
     Ecmp Composites 0, L3 Mcast Composites 0, L2 Mcast Composites 0, Fabric Composites 0, Multi Proto Composites 0
     Udp Tunnels 0, Udp Mpls Tunnels 0, Gre Mpls Tunnels 0
     L2 Encaps 0, Encaps 132179 

.. raw:: html

   </div>

.. raw:: html

   <div id="jd0e595" class="example" dir="ltr">

​Example: ​vrfstats --help
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   Usage: vrfstats --get <vrf>
                                      --dump
                                      --help

   --get <vrf>           Displays packet statistics for the vrf <vrf>

   --dump          Displays packet statistics for all vrfs

   --help              Displays this help message

.. raw:: html

   </div>

rt Command
----------

Use the rt command to display all routes in a VRF.

.. raw:: html

   <div id="jd0e608" class="example" dir="ltr">

Example: rt --dump
~~~~~~~~~~~~~~~~~~

The following example displays ``inet`` family routes for ``vrf 0``.

::

   # rt --dump 0

   Kernel IP routing table 0/0/unicast

   Destination             PPL        Flags        Label        Nexthop

   0.0.0.0/8                0                        -              5

   1.0.0.0/8                0                        -              5

   2.0.0.0/8                0                        -              5

   3.0.0.0/8                0                        -              5

   4.0.0.0/8                0                        -              5

   5.0.0.0/8                0                        -              5

.. raw:: html

   </div>

In this example output, the first line displays the routing table that
is being dumped. In ``0/0/unicast``, the first 0 is for the router ID,
the next 0 is for the VRF ID, and unicast identifies the unicast table.
The vRouter maintains separate tables for unicast and multicast routes.
​ By default, if the ``—table``\ option is not specified, only the
unicast table is dumped.

Each record in the table output specifies the destination prefix length,
the parent route prefix length from which this route has been expanded,
the flags for the route, the MPLS label if the destination is a VM in
another location, and the next hop ID. To understand the second field
“PPL”, it is good to keep in mind that the unicast routing table is
internally implemented as an ‘mtrie’.

The ``Flags`` field can have two values. ``L`` indicates that the label
field is valid, and ``H`` indicates that ``vroute`` should proxy arp for
this IP.

The ``Nexthop`` field indicates the next hop ID to which the route
points.

.. raw:: html

   <div id="jd0e651" class="example" dir="ltr">

Example: rt --dump --table mcst
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To dump the multicast table, use the ``—table`` option with ``mcst`` as
the argument.

::

   # rt --dump 0 --table mcst

   Kernel IP routing table 0/0/multicast

   (Src,Group)                                  Nexthop

   0.0.0.0,255.255.255.255  

.. raw:: html

   </div>

dropstats Command
-----------------

Use the dropstats command to see packet drop counters in vRouter. Use
the dropstats --debug command to view the Cloned Original counters.

.. raw:: html

   <div id="jd0e682" class="example" dir="ltr">

Example: dropstats
~~~~~~~~~~~~~~~~~~

::

   (vrouter-agent-dpdk)[root@nodec56 /]$ dropstats
   Invalid IF                    0
   Trap No IF                    0
   IF TX Discard                 0
   IF Drop                       0
   IF RX Discard                 0

   Flow Unusable                 0
   Flow No Memory                0
   Flow Table Full               0
   Flow NAT no rflow             0
   Flow Action Drop              0
   Flow Action Invalid           0
   Flow Invalid Protocol         0
   Flow Queue Limit Exceeded     0
   New Flow Drops                0
   Flow Unusable (Eviction)      0

   Original Packet Trapped       0

   Discards                      0
   TTL Exceeded                  0
   Mcast Clone Fail              0

   Invalid NH                    2
   Invalid Label                 0
   Invalid Protocol              0
   Etree Leaf to Leaf            0
   Bmac/ISID Mismatch            0
   Rewrite Fail                  0
   Invalid Mcast Source          0
   Packet Loop                   0

   Push Fails                    0
   Pull Fails                    0
   Duplicated                    0
   Head Alloc Fails              0
   PCOW fails                    0
   Invalid Packets               0

   Misc                          0
   Nowhere to go                 0
   Checksum errors               0
   No Fmd                        0
   Invalid VNID                  0
   Fragment errors               0
   Invalid Source                0
   Jumbo Mcast Pkt with DF Bit   0
   No L2 Route                   0
   Memory Failures               0
   Fragment Queueing Failures    0
   No Encrypt Path Failures      0
   Invalid HBS received packet   0

   VLAN fwd intf failed TX       0
   VLAN fwd intf failed enq      0

   (vrouter-agent-dpdk)[root@nodec56 /]$ dropstats --debug
   Cloned Original               0

.. raw:: html

   </div>

.. note::

   Cloned Original drops are still included in the Drops section in the
   output of the vif --list command.

.. raw:: html

   <div id="jd0e698" class="example" dir="ltr">

dropstats ARP Block
~~~~~~~~~~~~~~~~~~~

GARP packets from VMs are dropped by vRouter, an expected behavior. In
the example output, the first counter GARP indicates how many packets
were dropped.

ARP requests that are not handled by vRouter are dropped, for example,
requests for a system that is not a host. These drops are counted
by\ ``ARP notme``\ counters.

The ``Invalid ARPs`` counter is incremented when the Ethernet protocol
is ARP, but the ARP operation was neither a request nor a response.

.. raw:: html

   </div>

.. raw:: html

   <div id="jd0e714" class="example" dir="ltr">

dropstats Interface Block
~~~~~~~~~~~~~~~~~~~~~~~~~

``Invalid IF`` counters are incremented normally during transient
conditions, and should not be a concern.

``Trap No IF`` counters are incremented when vRouter is not able to find
the interface to trap the packets to vRouter agent, and should not
happen in a working system.

``IF TX Discard`` and ``IF RX Discard`` counters are incremented when
vRouter is not in a state to transmit and receive packets, and typically
happens when vRouter goes through a reset state or when the module is
unloaded.

``IF Drop``\ counters indicate packets that are dropped in the interface
layer. The increase can typically happen when interface settings are
wrong.

.. raw:: html

   </div>

.. raw:: html

   <div id="jd0e737" class="example" dir="ltr">

dropstats Flow Block
~~~~~~~~~~~~~~~~~~~~

When packets go through flow processing, the first packet in a flow is
cached and the vRouter agent is notified so it can take actions on the
packet according to the policies configured. If more packets arrive
after the first packet but before the agent makes a decision on the
first packet, then those new packets are dropped. The dropped packets
are tracked by the Flow unusable counter.

The ``Flow No Memory`` counter increments when the flow block doesn't
have enough memory to perform internal operations.

The ``Flow Table Full`` counter increments when the vRouter cannot
install a new flow due to lack of available slots. A particular flow can
only go in certain slots, and if all those slots are occupied, packets
are dropped. It is possible that the flow table is not full, but the
counter might increment.

The ``Flow NAT no rflow`` counter tracks packets that are dropped when
there is no reverse flow associated with a forward flow that had action
set as NAT. For NAT, the vRouter needs both forward and reverse flows to
be set properly. If they are not set, packets are dropped.

The ``Flow Action Drop`` counter tracks packets that are dropped due to
policies that prohibit a flow.

The ``Flow Action Invalid`` counter usually does not increment in the
normal course of time, and can be ignored.

The ``Flow Invalid Protocol`` usually does not increment in the normal
course of time, and can be ignored.

The ``Flow Queue Limit Exceeded`` usually does not increment in the
normal course of time, and can be ignored.

.. raw:: html

   </div>

.. raw:: html

   <div id="jd0e778" class="example" dir="ltr">

dropstats Miscellaneous Operational Block
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``Discard`` counter tracks packets that hit a discard next hop. For
various reasons interpreted by the agent and during some transient
conditions, a route can point to a discard next hop. When packets hit
that route, they are dropped.

The ``TTL Exceeded`` counter increments when the MPLS time-to-live goes
to zero.

The ``Mcast Clone Fail`` happens when the vRouter is not able to
replicate a packet for flooding.

The ``Cloned Original``\ is an internal tracking counter. It is harmless
and can be ignored.

The ``Invalid NH``\ counter tracks the number of packets that hit a next
hop that was not in a state to be used (usually in transient conditions)
or a next hop that was not expected, or no next hops when there was a
next hop expected. Such increments happen rarely, and should not
continuously increment.

The ``Invalid Label``\ counter tracks packets with an MPLS label
unusable by vRouter because the value is not in the expected range.

The ``Invalid Protocol``\ ​typically increments when the IP header is
corrupt.

The ``Rewrite Fail``\ counter tracks the number of times vRouter was not
able to write next hop rewrite data to the packet.

The ``Invalid Mcast Source`` tracks the multicast packets that came from
an unknown or unexpected source and thus were dropped.

The ``Duplicated`` counter tracks the number of duplicate packets that
are created after dropping the original packets. An original packet is
duplicated when generic send offload (GSO) is enabled in the vRouter or
the original packet is unable to include the header information of the
vRouter agent.

The ``Invalid Source``\ counter tracks the number of packets that came
from an invalid or unexpected source and thus were dropped.

The remaining counters are of value only to developers.

.. raw:: html

   </div>

mpls Command
------------

The ``mpls`` utility command displays the input label map that has been
programmed in the vRouter.

.. raw:: html

   <div id="jd0e850" class="example" dir="ltr">

Example: mpls --dump
~~~~~~~~~~~~~~~~~~~~

The ``—dump`` command dumps the complete label map. The output is
divided into two columns. The first field is the label and the second is
the next hop corresponding to the label. When an MPLS packet with the
specified label arrives in the vRouter, it uses the next hop
corresponding to the label to forward the packet.

::

   # mpls –dump

   MPLS Input Label Map



      Label    NextHop

     ----------------------

       16          9

       17          11

.. raw:: html

   </div>

.. raw:: html

   <div id="jd0e861" class="example" dir="ltr">

You can inspect the operation on ``nh 9``\ as follows:

::

   # nh --get 9

   Id:009  Type:Encap     Fmly: AF_INET  Flags:Valid, Policy,   Rid:0  Ref_cnt:4

           EncapFmly:0806 Oif:3 Len:14 Data:02 d0 60 aa 50 57 00 25 90 c3 08 69 08 00

.. raw:: html

   </div>

.. raw:: html

   <div id="jd0e870" class="example" dir="ltr">

The nh output shows that the next hop directs the packet to go out on
the interface with index 3 (``Oif:3``) with the given rewrite data.

To check the index of 3, use the following:

::

   # vif –get 3

   vif0/3  OS: tapd060aa50-57

           Type:Virtual HWaddr:00:00:5e:00:01:00 IPaddr:0

           Vrf:1 Flags:PL3L2 MTU:9160 Ref:6

           RX packets:1056  bytes:103471 errors:0

           TX packets:1041  bytes:102372 errors:0

.. raw:: html

   </div>

.. raw:: html

   <div id="jd0e881" class="example" dir="ltr">

The\ ``-get 3`` output shows that the index of 3 corresponds to a tap
interface that goes to a VM.

You can also dump individual entries in the map using the ``—get``
option, as follows:

::

   # mpls –get 16

   MPLS Input Label Map



      Label    NextHop

   -----------------------

        16         9

.. raw:: html

   </div>

.. raw:: html

   <div id="jd0e895" class="example" dir="ltr">

Example: mpls -help
~~~~~~~~~~~~~~~~~~~

::

   # mpls –help

   Usage: mpls --dump

              mpls --get <label>

              mpls --help


   --dump  Dumps the mpls incoming label map

   --get       Dumps the entry corresponding to label <label>
                 in the label map

   --help     Prints this help message

.. raw:: html

   </div>

mirror Command
--------------

Use the ``mirror`` command to dump the mirror table entries.

.. raw:: html

   <div id="jd0e911" class="example" dir="ltr">

Example: Inspect Mirroring
~~~~~~~~~~~~~~~~~~~~~~~~~~

The following example inspects a mirror configuration where traffic is
mirrored from network\ ``vn1 (1.1.1.0/24)``\ to network
``vn2 (2.2.2.0/24)``. A ping is run from 1.1.1.253 to 2.2.2.253, where
both IPs are valid VM IPs, then the flow table is listed:

::

   # flow -l

   Flow table

   Index              Source:Port        Destination:Port    Proto(V)

   -------------------------------------------------------------------------

   135024               2.2.2.253:1208            1.1.1.253:0        1 (1)

                    (Action:F, S(nh):17,  Statistics:208/17472 Mirror Index : 0)



   387324               1.1.1.253:1208            2.2.2.253:0        1 (1)

                     (Action:F, S(nh):8,  Statistics:208/17472 Mirror Index : 0)

.. raw:: html

   </div>

In the example output, ``Mirror Index:0`` is listed, it is the index to
the mirror table. The mirror table can be dumped with the\ ``—dump``
option, as follows:

.. raw:: html

   <div id="jd0e933" class="example" dir="ltr">

::

   # mirror --dump

   Mirror Table

   Index    NextHop    Flags    References

   ------------------------------------------------

      0            18                     3

.. raw:: html

   </div>

The mirror table entries point to next hops. In the example, the index 0
points to next hop 18. The ``References`` indicate the number of flow
entries that point to this entry.

A next hop get operation on ID 18 is performed as follows:

.. raw:: html

   <div id="jd0e943" class="example" dir="ltr">

::

   # nh --get 18

   Id:018  Type:Tunnel    Fmly: AF_INET  Flags:Valid, Udp,   Rid:0  Ref_cnt:2

           Oif:0 Len:14 Flags Valid, Udp,  Data:00 00 00 00 00 00 00 25 90 c3 08 69 08 00

           Vrf:-1  Sip:192.168.1.10  Dip:250.250.2.253

           Sport:58818 Dport:8099

.. raw:: html

   </div>

The ``nh --get`` output shows that mirrored packets go to a system with
IP 250.250.2.253. The packets are tunneled as a UDP datagram and sent to
the destination. ``Vrf:-1`` indicates that a lookup has to be done in
the source ``Vrf`` for the destination.

You can also get an individual mirror table entry using the ``—get``
option, as follows:

.. raw:: html

   <div id="jd0e962" class="example" dir="ltr">

::

   # mirror --get 10

   Mirror Table

   Index    NextHop    Flags    References

   -----------------------------------------------

    10         1                           1

.. raw:: html

   </div>

.. raw:: html

   <div id="jd0e965" class="example" dir="ltr">

Example: mirror --help
~~~~~~~~~~~~~~~~~~~~~~

::

   # mirror --help

   Usage:  mirror --dump

           mirror --get <index>

           mirror --help

   --dump  Dumps the mirror table

   --get       Dumps the mirror entry corresponding to index <index>

   --help     Prints this help message

.. raw:: html

   </div>

vxlan Command
-------------

The vxlan command can be used to dump the VXLAN table. The vxlan table
maps a network ID to a next hop, similar to an MPLS table.

If a packet comes with a VXLAN header and if the VNID is one of those in
the table, the vRouter will use the next hop identified to forward the
packet.

.. raw:: html

   <div id="jd0e980" class="example" dir="ltr">

Example: vxlan --dump​
~~~~~~~~~~~~~~~~~~~~~~

::

   # vxlan --dump

   VXLAN Table

   VNID    NextHop

   ---------------------

     4         16

     5         16

.. raw:: html

   </div>

.. raw:: html

   <div id="jd0e985" class="example" dir="ltr">

Example: vxlan --get
~~~~~~~~~~~~~~~~~~~~

You can use the ``—get`` option to dump a specific entry, as follows:

::

   # vxlan --get 4

   VXLAN Table

    VNID    NextHop

   ----------------------

     4         16

.. raw:: html

   </div>

.. raw:: html

   <div id="jd0e996" class="example" dir="ltr">

Example: vxlan --help
~~~~~~~~~~~~~~~~~~~~~

::

   # vxlan --help

   Usage:  vxlan --dump

           vxlan --get <vnid>

           vxlan --help

   --dump  Dumps the vxlan table

   --get   Dumps the entry corresponding to <vnid>

   --help  Prints this help message

.. raw:: html

   </div>

nh Command
----------

The ``nh`` command enables you to inspect the next hops that are known
by the vRouter. Next hops tell the vRouter the next location to send a
packet in the path to its final destination. The processing of the
packet differs based on the type of the next hop. The next hop types are
described in the following table.

+-----------------------+---------------------------------------------+
| Next Hop Type         | Description                                 |
+=======================+=============================================+
| ``Receive``           | Indicates that the packet is destined for   |
|                       | itself and the vRouter should perform Layer |
|                       | 4 protocol processing. As an example, all   |
|                       | packets destined to the host IP will hit    |
|                       | the receive next hop in the default VRF.    |
|                       | Similarly, all traffic destined to the VMs  |
|                       | hosted by the server and tunneled inside a  |
|                       | GRE will hit the receive next hop in the    |
|                       | default VRF first, because the outer packet |
|                       | that carries the traffic to the VM is that  |
|                       | of the server.                              |
+-----------------------+---------------------------------------------+
| ``Encap (Interface)`` | Used only to determine the outgoing         |
|                       | interface and the Layer 2 information. As   |
|                       | an example, when two VMs on the same server |
|                       | communicate with each other, the routes for |
|                       | each of them point to an encap next hop,    |
|                       | because the only information needed is the  |
|                       | Layer 2 information to send the packet to   |
|                       | the tap interface of the destination VM. A  |
|                       | packet destined to a VM hosted on one       |
|                       | server from a VM on a different server will |
|                       | also hit an encap next hop, after tunnel    |
|                       | processing.                                 |
+-----------------------+---------------------------------------------+
| ``Tunnel``            | Encapsulates VM traffic in a tunnel and     |
|                       | sends it to the server that hosts the       |
|                       | destination VM. There are different types   |
|                       | of tunnel next hops, based on the type of   |
|                       | tunnels used. vRouter supports two main     |
|                       | tunnel types for Layer 3 traffic: MPLSoGRE  |
|                       | and MPLSoUDP. For Layer 2 traffic, a VXLAN  |
|                       | tunnel is used. A typical tunnel next hop   |
|                       | indicates the kind of tunnel, the rewrite   |
|                       | information, the outgoing interface, and    |
|                       | the source and destination server IPs.      |
+-----------------------+---------------------------------------------+
| ``Discard``           | A catch-all next hop. If there is no route  |
|                       | for a destination, the packet hits the      |
|                       | discard next hop, which drops the packet.   |
+-----------------------+---------------------------------------------+
| ``Resolve``           | Used by the agent to lazy install Layer 2   |
|                       | rewrite information.                        |
+-----------------------+---------------------------------------------+
| ``Composite``         | Groups a set of next hops, called component |
|                       | next hops or sub next hops. Typically used  |
|                       | when multi-destination distribution is      |
|                       | needed, for example for multicast, ECMP,    |
|                       | and so on.                                  |
+-----------------------+---------------------------------------------+
| ``Vxlan``             | A VXLAN tunnel is used for Layer 2 traffic. |
|                       | A typical tunnel next hop indicates the     |
|                       | kind of tunnel, the rewrite information,    |
|                       | the outgoing interface, and the source and  |
|                       | destination server IPs.                     |
+-----------------------+---------------------------------------------+

.. raw:: html

   <div id="jd0e1081" class="example" dir="ltr">

Example: nh --list
~~~~~~~~~~~~~~~~~~

::

   Id:000  Type:Drop      Fmly: AF_INET  Flags:Valid,   Rid:0  Ref_cnt:1781

   Id:001  Type:Resolve   Fmly: AF_INET  Flags:Valid,   Rid:0  Ref_cnt:244

   Id:004  Type:Receive  Fmly: AF_INET  Flags:Valid, Policy,   Rid:0

                  Ref_cnt:2 Oif:1

   Id:007  Type:Encap     Fmly: AF_INET  Flags:Valid, Multicast,   Rid:0  Ref_cnt:3

           EncapFmly:0806 Oif:3 Len:14 Data:ff ff ff ff ff ff 00 25 90 c4 82 2c 08 00

   Id:010  Type:Encap     Fmly:AF_BRIDGE  Flags:Valid, L2,   Rid:0  Ref_cnt:3

           EncapFmly:0000 Oif:3 Len:0 Data:

   Id:012  Type:Vxlan Vrf  Fmly: AF_INET  Flags:Valid,   Rid:0  Ref_cnt:2

           Vrf:1

   Id:013  Type:Composite  Fmly: AF_INET  Flags:Valid, Fabric,   Rid:0  Ref_cnt:3

           Sub NH(label): 19(1027)

   Id:014  Type:Composite  Fmly: AF_INET  Flags:Valid, Multicast, L3,   Rid:0  Ref_cnt:3

           Sub NH(label): 13(0) 7(0)

   Id:015  Type:Composite  Fmly:AF_BRIDGE  Flags:Valid, Multicast, L2,   Rid:0  Ref_cnt:3

           Sub NH(label): 13(0) 10(0)

   Id:016  Type:Tunnel    Fmly: AF_INET  Flags:Valid, MPLSoGRE,   Rid:0  Ref_cnt:1

           Oif:2 Len:14 Flags Valid, MPLSoGRE,  Data:00 25 90 aa 09 a6 00 25 90 c4 82 2c 08 00

           Vrf:0  Sip:10.204.216.72  Dip:10.204.216.21

   Id:019  Type:Tunnel    Fmly: AF_INET  Flags:Valid, MPLSoUDP,   Rid:0  Ref_cnt:7

           Oif:2 Len:14 Flags Valid, MPLSoUDP,  Data:00 25 90 aa 09 a6 00 25 90 c4 82 2c 08 00

           Vrf:0  Sip:10.204.216.72  Dip:10.204.216.21

   Id:020  Type:Composite  Fmly:AF_UNSPEC  Flags:Valid, Multi Proto,   Rid:0  Ref_cnt:2

           Sub NH(label): 14(0) 15(0)

.. raw:: html

   </div>

.. raw:: html

   <div id="jd0e1086" class="example" dir="ltr">

Example: nh --get
~~~~~~~~~~~~~~~~~

Use the\ ``--get``\ option to display information for a single next hop.

::

   # nh –get 9

   Id:009  Type:Encap     Fmly:AF_BRIDGE  Flags:Valid, L2,   Rid:0  Ref_cnt:4

           EncapFmly:0000 Oif:3 Len:0 Data:

.. raw:: html

   </div>

.. raw:: html

   <div id="jd0e1097" class="example" dir="ltr">

Example: nh --help
~~~~~~~~~~~~~~~~~~

::

   # nh –help

   Usage: nh --list

          nh --get <nh_id>

          nh --help

   --list  Lists All Nexthops

   --get   <nh_id> Displays nexthop corresponding to <nh_id>

   --help  Displays this help message

.. raw:: html

   </div>

dpdkinfo Command
----------------

In Contrail Networking Release 2008, the ``dpdkinfo`` command enables
you to see the details of the internal data structures of a DPDK enabled
vRouter.

.. raw:: html

   <div id="jd0e1114" class="example" dir="ltr">

dpdkinfo Options
~~~~~~~~~~~~~~~~

Use\ ``dpdkinfo –-help`` to display all options available for the
dpdkinfo command. The dpdkinfo command options are described in the
following table:

.. raw:: html

   </div>

+------------------------------+--------------------------------------+
| Option                       | Description                          |
+==============================+======================================+
| ``--bond``                   | Displays the bond interface          |
|                              | information for primary and backup   |
|                              | devices in a bond interface.         |
+------------------------------+--------------------------------------+
| ``--lacp all``               | Displays the Link Aggregation        |
|                              | Control Protocol (LACP)              |
|                              | configuration for Slow and Fast LACP |
|                              | timers along with port details of    |
|                              | actor and partner interfaces in a    |
|                              | LACP exchange.                       |
+------------------------------+--------------------------------------+
| ``--mempool all``            | Displays summary of used and         |
|                              | available memory buffers from all    |
|                              | memory pools.                        |
+------------------------------+--------------------------------------+
| ``--mempool <mempool_name>`` | Displays information about the       |
|                              | specified memory pool.               |
+------------------------------+--------------------------------------+
| ``--stats eth``              | Displays NIC statistics information  |
|                              | for the packets received (Rx) and    |
|                              | transmitted (Tx) by the vRouter.     |
+------------------------------+--------------------------------------+
| ``--xstats all``             | Displays extended NIC statistics     |
|                              | information from NIC cards.          |
+------------------------------+--------------------------------------+
| ``--xstats=<interface-id>``  | Displays extended NIC information of |
|                              | the primary and backup devices for   |
|                              | the given interface-id ( Primary->0, |
|                              | Slave_0->1, Slave_1 ->2 ).           |
+------------------------------+--------------------------------------+
| ``--lcore``                  | Displays the Rx queue mapped         |
|                              | interfaces along with Queue ID.      |
+------------------------------+--------------------------------------+
| ``--app``                    | Displays the overall application     |
|                              | information like actual physical     |
|                              | interface name, number of cores,     |
|                              | VLAN, queues, and so on.             |
+------------------------------+--------------------------------------+
| dpdkinfo --ddp list          | Displays the list of DDP profiles    |
|                              | added in the vRouter.                |
+------------------------------+--------------------------------------+

.. raw:: html

   <div id="jd0e1223" class="example" dir="ltr">

Example: dpdkinfo --bond
~~~~~~~~~~~~~~~~~~~~~~~~

The dpdkinfo --bond displays the following information for primary and
backup devices: actor/partner status, actor/partner key, actor/partner
system priority, actor/partner MAC address, actor/partner port priority,
actor/partner port number, and so on.

::

   dpdkinfo --bond
   No. of bond slaves: 2
   Bonding Mode: 802.3AD Dynamic Link Aggregation
   Transmit Hash Policy: Layer 3+4 (IP Addresses + UDP Ports) transmit load balancing
   MII status: UP
   MII Link Speed: 1000 Mbps
   MII Polling Interval (ms): 10
   Up Delay (ms): 0
   Down Delay (ms): 0
   Driver: net_bonding

   802.3ad info :
   LACP Rate: slow
   Aggregator selection policy (ad_select): Stable
   System priority: 32512
   System MAC address:00:50:00:00:00:00
   Active Aggregator Info: 
           Aggregator ID: 0
           Number of ports: 2 
           Actor Key: 4096
           Partner Key: 0
           Partner Mac Address: 00:00:80:7a:9b:05

   Slave Interface(0): 0000:02:00.0 
   Slave Interface Driver: net_ixgbe
   MII status: DOWN
   MII Link Speed: 0 Mbps
   Permanent HW addr:00:aa:7b:93:00:00
   Aggregator ID: 13215
   Duplex: half
   Bond MAC addr:ac:1f:6b:a5:0f:de
   Details actor lacp pdu: 
           system priority: 0
           system mac address:00:aa:7b:93:00:00
           port key: 0
           port priority: 0
           port number: 63368
           port state: 0 () 

   Details partner lacp pdu: 
           system priority: 15743
           system mac address:00:00:80:01:9c:05
           port key: 0
           port priority: 0
           port number: 28836
           port state: 117 (ACT AGG COL DIST DEF ) 

   Slave Interface(1): 0000:02:00.1 
   Slave Interface Driver: net_ixgbe
   MII status: UP
   MII Link Speed: 1000 Mbps
   Permanent HW addr:ac:1f:6b:a5:0f:df
   Aggregator ID: 1
   Duplex: full
   Bond MAC addr:ac:1f:6b:a5:0f:df
   Details actor lacp pdu: 
           system priority: 65535
           system mac address:ac:1f:6b:a5:0f:df
           port key: 17
           port priority: 255
           port number: 2
           port state: 61 (ACT AGG SYNC COL DIST ) 

   Details partner lacp pdu: 
           system priority: 127
           system mac address:ec:3e:f7:5f:f0:40
           port key: 3
           port priority: 127
           port number: 10
           port state: 63 (ACT TIMEOUT AGG SYNC COL DIST )

.. raw:: html

   </div>

.. raw:: html

   <div id="jd0e1235" class="example" dir="ltr">

Example: dpdkinfo --lacp all
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The dpdkinfo --lacp all command displays the following information for
primary devices: LACP rate and LACP configuration details, which include
Fast periodic (ms), Slow periodic (ms), Short timeout (ms), Long timeout
(ms), LACP packet statistics for Tx and Rx counters, and so on. Also,
dpdkinfo --lacp all displays actor and partner port status details of
all the backup devices.

::

   dpdkinfo --lacp all
   LACP Rate: fast

   Fast periodic (ms): 900
   Slow periodic (ms): 29000
   Short timeout (ms): 3000
   Long timeout (ms): 90000
   Aggregate wait timeout (ms): 2000
   Tx period (ms): 500
   Update timeout (ms): 100
   Rx marker period (ms): 2000

   Slave Interface(0): 0000:04:00.0 
   Details actor lacp pdu: 
          port state: 63 (ACT TIMEOUT AGG SYNC COL DIST ) 

   Details partner lacp pdu: 
          port state: 61 (ACT AGG SYNC COL DIST ) 

   Slave Interface(1): 0000:04:00.1 
   Details actor lacp pdu: 
          port state: 63 (ACT TIMEOUT AGG SYNC COL DIST ) 

   Details partner lacp pdu: 
          port state: 61 (ACT AGG SYNC COL DIST ) 

   LACP Packet Statistics:
                 Tx     Rx
   0000:04:00.0  6      28
   0000:04:00.1  7      30

.. raw:: html

   </div>

.. raw:: html

   <div id="jd0e1249" class="example" dir="ltr">

Example: dpdkinfo --mempool all and dpdk --mempool <mempool-name>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The dpdkinfo --mempool all displays a summary of the memory pool
information of the primary and backup devices, which include number of
available memory pools, size of the memory pool, and so on.

The dpdk --mempool <mempool-name> displays detailed information of the
memory pool you have specified in the command.

::

   dpdkinfo --mempool all

   ---------------------------------------------------
   Name                 Size       Used     Available
   ---------------------------------------------------
   rss_mempool          16384       620       15765
   frag_direct_mempool   4096        0         4096
   frag_indirect_mempool 4096        0         4096
   slave_port0_pool      8193        0         8193
   packet_mbuf_pool      8192        4         8188
   slave_port1_pool      8193       125        8068

    dpdkinfo --mempool rss_mempool
   rss_mempool
   flags = 10
   nb_mem_chunks = 77
   size = 16384
   populated_size = 16384
   header_size = 64
   elt_size = 9648
   trailer_size = 80
   total_obj_size = 9792
   private_data_size = 64
   avg bytes/object = 9856.000000
   Internal cache infos:
           cache_size=256
           cache_count[0]=65
           cache_count[8]=219
           cache_count[9]=2
           cache_count[10]=156
           cache_count[11]=195
   total_cache_count=637
   common_pool_count=15137

.. raw:: html

   </div>

.. raw:: html

   <div id="jd0e1268" class="example" dir="ltr">

Example: dpdkinfo --stats eth
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The dpdkinfo --stats eth command reads Rx and Tx packets statistics from
the NIC card and displays the information.

::

   dpdkinfo --stats eth
   Master Info: 
   RX Device Packets:1289, Bytes:148651, Errors:0, Nombufs:0
   Dropped RX Packets:0
   TX Device Packets:2051, Bytes:237989, Errors:0
   Queue Rx: [0]1289 
         Tx: [0]2051 
         Rx Bytes: [0]148651 
         Tx Bytes: [0]234429 
         Errors:
   ---------------------------------------------------------------------

   Slave Info(0000:02:00.0): 
   RX Device Packets:0, Bytes:0, Errors:0, Nombufs:0
   Dropped RX Packets:0
   TX Device Packets:0, Bytes:0, Errors:0
   Queue Rx:
         Tx:
         Rx Bytes:
         Tx Bytes:
         Errors:
   ---------------------------------------------------------------------

   Slave Info(0000:02:00.1): 
   RX Device Packets:1289, Bytes:148651, Errors:0, Nombufs:0
   Dropped RX Packets:0
   TX Device Packets:2051, Bytes:237989, Errors:0
   Queue Rx: [0]1289 
         Tx: [0]2051 
         Rx Bytes: [0]148651 
         Tx Bytes: [0]234429 
         Errors:

.. raw:: html

   </div>

.. raw:: html

   <div id="jd0e1279" class="example" dir="ltr">

Example: dpdkinfo --xstats
~~~~~~~~~~~~~~~~~~~~~~~~~~

The dpdkinfo --xstats command reads the Rx and Tx from the NIC cards and
displays the packet statistics in detail.

::

   dpdkinfo --xstats
   Master Info: 
   Rx Packets: 
           rx_good_packets: 1459
           rx_q0packets: 1459
   Tx Packets: 
           tx_good_packets: 2316
           tx_q0packets: 2316
   Rx Bytes: 
           rx_good_bytes: 161175
           rx_q0bytes: 161175
   Tx Bytes: 
           tx_good_bytes: 265755
           tx_q0bytes: 261915
   Errors: 
   Others: 
   ---------------------------------------------------------------------

   Slave Info(0):0000:02:00.0 
   Rx Packets: 
   Tx Packets: 
   Rx Bytes: 
   Tx Bytes: 
   Errors: 
           mac_local_errors: 2
   Others: 
   ---------------------------------------------------------------------

   Slave Info(1):0000:02:00.1 
   Rx Packets: 
           rx_good_packets: 1459
           rx_q0packets: 1459
           rx_size_64_packets: 677
           rx_size_65_to_127_packets: 641
           rx_size_128_to_255_packets: 54
           rx_size_256_to_511_packets: 48
           rx_size_512_to_1023_packets: 3
           rx_size_1024_to_max_packets: 36
           rx_broadcast_packets: 3 
           rx_multicast_packets: 772
           rx_total_packets: 1461
   Tx Packets: 
           tx_good_packets: 2316
           tx_q0packets: 2316
           tx_total_packets: 2316
           tx_size_64_packets: 276
           tx_size_65_to_127_packets: 582
           tx_size_128_to_255_packets: 1433  
           tx_size_256_to_511_packets: 4
           tx_size_512_to_1023_packets: 3 
           tx_size_1024_to_max_packets: 18
           tx_multicast_packets: 1431
           tx_broadcast_packets: 9
   Rx Bytes: 
           rx_good_bytes: 161175
           rx_q0bytes: 161175
           rx_total_bytes: 161567
   Tx Bytes: 
           tx_good_bytes: 265755
           tx_q0bytes: 261915
   Errors: 
           mac_local_errors: 2
   Others: 
           out_pkts_untagged: 2316

.. raw:: html

   </div>

.. raw:: html

   <div id="jd0e1290" class="example" dir="ltr">

Example: dpdkinfo --lcore
~~~~~~~~~~~~~~~~~~~~~~~~~

The dpdkinfo --lcore displays Logical core (lcore) information, which
includes number of forwarding lcores, the interfaces mapped to the
lcore, and queue-ID of the interfaces.

::

   dpdkinfo --lcore
   No. of forwarding lcores: 2 
   No. of interfaces: 4 
   Lcore 0: 
           Interface: bond0.102           Queue ID: 0 
           Interface: vhost0              Queue ID: 0 

   Lcore 1: 
           Interface: bond0.102           Queue ID: 1 
           Interface: tapd1b53efb-9e      Queue ID: 0

.. raw:: html

   </div>

.. raw:: html

   <div id="jd0e1302" class="example" dir="ltr">

dpdkinfo --app
~~~~~~~~~~~~~~

The dpdkinfo --app command displays the following information:

-  Application related information about number of lcores, the names of
   the existing​ backup interfaces, and so on.

-  For VLAN configured devices the command displays VLAN​ name, tag, and
   vlan_vif name.

-  For bond interfaces the command displays ethdev information, which
   include Max rx queues, Max tx queues, Reta size, Port id, number of
   ethdev slaves, Tapdev information, and so on.

-  Monitoring interface names (if available) and SR-IOV information,
   which includes logical core, ethdev port ID, and driver name.

.. raw:: html

   <!-- -->

::

   dpdkinfo --app
   No. of lcores: 12 
   No. of forwarding lcores: 2 
   Fabric interface: bond0.102
   Slave interface(0): enp2s0f0 
   Slave interface(1): enp2s0f1 
   Vlan name: bond0 
   Vlan tag: 102 
   Vlan vif: bond0 
   Ethdev (Master):
           Max rx queues: 128
           Max tx queues: 64
           Ethdev nb rx queues: 2
           Ethdev nb tx queues: 64
           Ethdev nb rss queues: 2 
           Ethdev reta size: 128
           Ethdev port id: 2
           Ethdev nb slaves: 2 
           Ethdev slaves: 0 1 0 0 0 0 

   Ethdev (Slave 0): 0000:02:00.0
           Nb rx queues: 2
           Nb tx queues: 64
           Ethdev reta size: 128

   Ethdev (Slave 1): 0000:02:00.1
           Nb rx queues: 2
           Nb tx queues: 64
           Ethdev reta size: 128

   Tapdev:
           fd: 39 vif name: bond0 
           fd: 48 vif name: vhost0

.. raw:: html

   </div>

.. raw:: html

   <div id="jd0e1326" class="example" dir="ltr">

Example: dpdkinfo --ddp list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In Contrail Networking Release 2011, you can use the dpdkinfo --ddp list
command to display the list of DDP profiles added in the vRouter.

The dpdkinfo --ddp list displays a summary of the DDP profile added in
the vRouter. The summary of the profile information includes tracking ID
of the profile, version number, and profile name.

::

   (contrail-tools)[root@cs-scale-02 /]$ dpdkinfo --ddp list
   Profile count is: 1
    
   Profile 0:
   Track id:     0x8000000c
   Version:      1.0.0.0
   Profile name: L2/L3 over MPLSoGRE/MPLSoUDP

.. raw:: html

   </div>

dpdkconf Command
----------------

In Contrail Networking Release 2011, the ``dpdkconf`` command enables
you to configure a DPDK enabled vRouter. In release 2011, you can use
the ``dpdkconf`` command to enable or delete a DDP profile in vRouter.

.. raw:: html

   <div id="jd0e1357" class="example" dir="ltr">

Example: dpdkconf --ddp add
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the dpdkconf --ddp add command during runtime to enable a DDP
profile in a DPDK enabled vRouter.

::

   (contrail-tools)[root@cs-scale-02 /]$ dpdkconf --ddp add
   Programming DDP image mplsogreudp - success

.. raw:: html

   </div>

.. raw:: html

   <div id="jd0e1368" class="example" dir="ltr">

Example: dpdkconf --ddp delete
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the dpdkconf --ddp delete command to delete a DDP profile, which is
already loaded in the vRouter.

::

   (contrail-tools)[root@cs-scale-02 /]$ dpdkconf --ddp delete
   vr_dpdk_ddp_del: Removed DDP image mplsogreudp - success

.. raw:: html

   </div>

.. raw:: html

   <div class="table">

.. raw:: html

   <div class="caption">


.. list-table:: Release History Table
      :header-rows: 1

      * - Release
        - Description
      * - 2011
        - In Contrail Networking Release 2011, you can use the dpdkinfo --ddp list command to display the list of DDP profiles added in the vRouter.
      * - 2011	
        - In Contrail Networking Release 2011, the dpdkconf command enables you to configure a DPDK enabled vRouter. In release 2011, you can use the dpdkconf command to enable or delete a DDP profile in vRouter.
      * - 2011
        - Contrail Networking Release 2008 supports clearing of vif statistics counters for all interfaces by using the --clear command.
      * - 2011	
        - In Contrail Networking Release 2008, the dpdkinfo command enables you to see the details of the internal data structures of a DPDK enabled vRouter.




Release History Table

.. raw:: html

   </div>

.. raw:: html

   <div class="table-row table-head">

.. raw:: html

   <div class="table-cell">

Release

.. raw:: html

   </div>

.. raw:: html

   <div class="table-cell">

Description

.. raw:: html

   </div>

.. raw:: html

   </div>

.. raw:: html

   <div class="table-row">

.. raw:: html

   <div class="table-cell">

`2011 <#jd0e1331>`__

.. raw:: html

   </div>

.. raw:: html

   <div class="table-cell">

In Contrail Networking Release 2011, you can use the dpdkinfo --ddp list
command to display the list of DDP profiles added in the vRouter.

.. raw:: html

   </div>

.. raw:: html

   </div>

.. raw:: html

   <div class="table-row">

.. raw:: html

   <div class="table-cell">

`2011 <#jd0e1349>`__

.. raw:: html

   </div>

.. raw:: html

   <div class="table-cell">

In Contrail Networking Release 2011, the ``dpdkconf`` command enables
you to configure a DPDK enabled vRouter. In release 2011, you can use
the ``dpdkconf`` command to enable or delete a DDP profile in vRouter.

.. raw:: html

   </div>

.. raw:: html

   </div>

.. raw:: html

   <div class="table-row">

.. raw:: html

   <div class="table-cell">

`2008 <#jd0e427>`__

.. raw:: html

   </div>

.. raw:: html

   <div class="table-cell">

Contrail Networking Release 2008 supports clearing of vif statistics
counters for all interfaces by using the ``--clear`` command.

.. raw:: html

   </div>

.. raw:: html

   </div>

.. raw:: html

   <div class="table-row">

.. raw:: html

   <div class="table-cell">

`2008 <#jd0e1109>`__

.. raw:: html

   </div>

.. raw:: html

   <div class="table-cell">

In Contrail Networking Release 2008, the ``dpdkinfo`` command enables
you to see the details of the internal data structures of a DPDK enabled
vRouter.

.. raw:: html

   </div>

.. raw:: html

   </div>

.. raw:: html

   </div>

 
