# Overview
Contrail uses flows to implement following features (as of R3.0)
  - Network Policy
  - Security Group
  - ECMP
  - RPF Check
  - Different type of NAT used for
  - Floating-IP
  - Link-local services
  - Metadata services
  - BGP As a Service

# Flows in VRouter

Flows in VRouter have following fields,

## Flows in VRouter
A flow in vrouter is shown as below,

    Entries: Created 86315592 Added 86305583 Processed 86315016 Used Overflow entries 127
    (Created Flows/CPU: 2 2 0 0 3 0 0 1 0 6 0 0 4 0 0 0 0 0 0 34389347 51926223 0 0 0 4 0 0 0 0 0 0 0)(oflows 0)

    Action:F=Forward, D=Drop N=NAT(S=SNAT, D=DNAT, Ps=SPAT, Pd=DPAT, L=Link Local Port)
    Other:K(nh)=Key_Nexthop, S(nh)=RPF_Nexthop
    Flags:E=Evicted, Ec=Evict Candidate, N=New Flow, M=Modified
    TCP(r=reverse):S=SYN, F=FIN, R=RST, C=HalfClose, E=Established, D=Dead

    Index                Source:Port/Destination:Port                      Proto(V)
    -----------------------------------------------------------------------------------
    25<=>28140        1.1.1.3:63                                         17 (1)
                      8.0.75.57:63
    (Gen: 243, K(nh):12, Action:F, Flags:, S(nh):12,  Stats:1/88,  SPort 58395)

### Flow Index
The fields 25<=> 28140 indicate that the flow is allocated index 25 and its reverse flow is at index 28140.

### Flow Key
Flow key is made of <nh-id, src-ip, dst-ip, protocol, src-port, dst-port>
  - nh-id: This is nexthop-id for the flow. The nexthop-id value is based on the
         type of packet
         1. Packet from vm-interface:
            The interface next-hop created for vm-interface is used as key
         2. MPLSoGRE or MPLSoUDP packet from fabric:
            The next-hop pointed to by the MPLS Label is used as key
         3. VxLan packet from fabric
            Bridge lookup is done for DMAC in the table pointed by vxlan-id.
            The nexthop in bridge route is used as the key
  - src-ip, dst-ip, protocol, src-port and dst-port are the 5-tuple from packet

In the example above, key is <nh-id=17, src-ip=1.1.1.3, src-port=63, dst-ip=8.0.75.57, dst-port=63, protocol=17>

### Flow Data
Data part of the flow contains following fields

***Gen*** :

Represents generation-id for the flow. This is an 8-bit number representing generation-id for the flow. Every time a hash entry is reused for a flow, the gen-id is incremented.

***K(nh)*** :

Represents nh-id for the flow

***Action*** :

Action for the flow. Values can be Forward(F), Deny (D) or Nat

***Flags*** :

  - TCP Eviction flags
    Tracks the tcp-state flags. Used to evict TCP flows on connection closure


***S(nh)*** : 

This is nexthop used for RPF checks. When a flow is being setup, agent will do route lookup for the source-ip and sets up the rpf-nh in the flow. The type of NH used will depend on matched route for the source-ip,

    - source-ip is reachable on a local vm-interface
       The rpf-nh points to nexthop created for the interface
    - source-ip is reachable thru a remote compute node (non-ECMP route)
       The rpf-nh points to tunnel-nh for the remote compute node
       VRouter checks if the soruce-ip in tunnel-header meatches the IP address
       in the tunnel-nh
    - source-ip is reachable via ECMP nexthop
       If source-ip is in ECMP, the rpf-nh will point to ECMP-NH. VRouter
       should accept packet as long as it comes from any of the member NH in
       ECMP

***Stats*** :

Packet and Bytes counts for the flow. Updated when a packet hits the flow.

***SPort*** :

Specifies the source-port used when packet is encapsulated in MPLSoUDP or VxLAN tunnels.

***VRF*** :

Changes VRF for the packet to value configured. In the above example (1) specifies the VRF.

***ECMP Component Index*** :

Specifies the member to be picked in case of ECMP

Contrail does not use flow to make forwarding decisions in the flows. However,
flows can influence forwarding decision (NAT rewrites, VRF Translation and
choosing ECMP members)

### Summary fields
The first two lines of output give summary information for the flows

***_Entries: Created 86315592 Added 86305583 Processed 86315016 Used Overflow entries 127_***

This line give summary statistics for the flow.

***_(Created Flows/CPU: 2 2 0 0 3 0 0 1 0 6 0 0 4 0 0 0 0 0 0 34389347 51926223 0 0 0 4 0 0 0 0 0 0 0)(oflows 0)_***

This line give number of flow created on per-cpu basis and also number of overflow entries currently in use.

## Organisation of Flow-Table
Flow table is organised as a hash-table with 4 entries per-bucket. Hash collision are resolved by allocating entries from an overflow table. The overflow table acts as free-list that can be used when all entries in bucket are allocated. Once allocated, the overflow entries are freed when corresponding flow is deleted.


The default size of hash-table is 512K entries (128K buckets) and overflow table is 8K entries. The size of tables can be modified by setting the vrouter module parameters vr_flow_entries and vr_oflow_entries. It is recommended that overflow-table should be atleast twice the number of expected flows and the overflow entries must be atleast 20% of the flow-table size.

# AgentHdr format

All packets exchanged between agent and vrouter will have a proprietary header given below.
 
     0                        16                         31
     +--------------------------+--------------------------+
     |    ifindex               | vrf                      |
     +--------------------------+--------------------------+
     |    command               | prameter-1               |
     +--------------------------+--------------------------+
     |    parameter-1           | parameter-2              |
     +--------------------------+--------------------------+
     |    parameter-2           | parameter-3              |
     +--------------------------+--------------------------+
     |    parameter-3           | parameter-4              |
     +--------------------------+--------------------------+
     |    parameter-4           | parameter-5              |
     +--------------------------+--------------------------+
     |    parameter-5           | Unused                   |
     +--------------------------+--------------------------+

- ifindex : Interface index for the ingress interface. Can be fabric interface when packet is received on fabric or vm-interface.
- vrf : vrf-index for the packet
- parameter-1 : Flow-handle allocated by vrouter for the flow
- parameter-2 : 
- parameter-3 : 
- parameter-4 : 
- parameter-5 : Gen-Id for the flow

*NOTE: The contents of parameter-* fields vary based on command

## Dropstats counters
<TODO - Document dropstats relavent to flows>

#Flows in Agent

contrail-vrouter-agent is responsible to manage the flows in vrouter. Agent
applies policies rules and computes appropriate actions for the flows.

The diagram below gives summary of flow processing,

               +------------------+
               |                  |
               |     pkt0 Rx      |
               |                  |
               +--------+---------+
                        |
                        |
               +--------v---------+
               |                  |
               | Pkt Handler      |
               |                  |
               +--------+---------+
                        | 1:N (Choose partition based on hash of 5-tuple)
                        |
                        |   <-----------------------------------------------------------------+
                        |   |                                                                 ^
                        |   |      <-----------------------------------------------------+    |
                        |   |      |                                                     ^    |
        +---------------v---v------v----+                                                |    |
        |                               |                                                |    |
        |      +------------------+     |                                                |    |
        |      |                  |     |                                                |    |
        |      | Flow Setup       |     |                                                |    |
        |      |                  |     |                                                |    |
        |      +--------+---------+     |                                                |    |
        |               |               |                                                |    |
        |               |               |                                                |    |
        |               |               |                                                |    |
        |      +--------v---------+     |                                                |    |
        |      |                  |     |                                                |    |
        |      | Flow Table       +-----+------------+---------------------+             |    |
        |      |                  |     |            |                     |             |    |
        |      +--------+---------+     |            |                     |             |    |
        |               |               |            |                     |             |    |
        |               |               |            |                     |             |    |
        |               |               |            |                     |             |    |
        |      +--------v----------+    |  +---------v--------+   +--------v---------+   |    |
        |      |                   |    |  |                  |   |                  |   |    |
        |      | Index Management  |    |  |  Flow Management |   |  Flow Stats      |   |    |
        |      |                   |    |  |                  |   |  Collector       |   |    |
        |      +--------+----------+    |  +---------^---+----+   +--------+---------+   |    |
        |               |               |            |   |                 |             |    |
        |               |               |            |   |                 v------------>+    |
        |               |               |            |   v                                    |
        |               |               |            |   +----------------------------------->+
        |      +--------v----------+    |  +---------+---+----+
        |      |                   |    |  |                  |
        |      | Flow KSync        |    |  | DB Clients       |
        |      |                   |    |  |                  |
        |      +--------+----------+    |  +------------------+
        +---------------|---------------+
                        |
               +--------v----------+
               |                   |
               | KSync Socket      |
               |                   |
               +-------------------+
                        |
                        |
                        |
                        |
               +--------v----------+
               |                   |
               | VRouter           |
               |                   |
               +-------------------+



### Pkt0 Rx
VRouter creates a pkt0 interface to exchange packets between agent and vrouter. All packets exchanged over pkt0 interface will be prepended with a proprietary agent-header. The format of agent header is given above.

Agent opens a socket on pkt0 interface and registers with Boost ASIO library for I/O. Boost library notifies agent when a packet is received on the interface. On getting notification from Boost library, Agent reads the packet enqueues packet immediately to "Packet Handler" module without parsing the packet.

**Task Context** : ASIO notification happens in context of main thread of agent process. Since main thread runs outside of task library, the module should not access any databases managed in agent. On receiving a packet, its is immediately enqueued to "Packet Handler"

### Packet Handler
This module receives packet enqueued by "Pkt0 Rx" module. VRouter traps different type of packets to agent. Example, packet for flow setup, ping packets to gateway-ip, ARP response packets etc.

VRouter parses the agent-header and packet contents to classify packet to following module,
- Flow Request
- ARP
- ICMP
- DNS

Post classification, packet is enqueued to the right module.

An overview of packet parsing is given below,

    - Packet received from fabric-interface ?
        - Validate Outer Ethernet header
            - Dest-MAC should be that of fabric-interface
        - Validate outer IP header
            - Dest-IP should be that of vhost interface
        - Extract MPLS Label/VxLan-ID from the tunnel
        - Strip Tunnel header
        - Is tunnel-type MPLSoGRE or MPLSoUDP
            - If MPLS label points to layer3 next-hop
                - Do "IP Parsing"
            - Else
                - Do "Ethernet Parsing"
        - Is tunnel-type VxLAN
            - Do "Ethernet Parsing"
    - Packet received from a VM ?
        - Do "Ethernet Parsing"

    Ethernet Parsing:
    - Do lookup into bridge-table for dest-mac
        - If dest-mac hits route with receive-nh
            - Mark flow as L3-Flow
        - Else
            - Mark flow as L2-Flow
        - Parse VLAN header if present
    - Do "IP Parsing"

    IP Parsing:
    - If protocol is TCP/UDP/SCTP
        - Set source-port and dest-port based on L4 headers
    - If protocol is ICMP
        - If ICMP Echo packet
            - Set source-port = ICMP Identifier
        - If ICMP Destination Unreachable
            - Set 5-tuple from the inner payload of ICMP packet

### Flow Module
Flow module implements horizontal scaling to support high flow rates. By default, it there are 4 "partitions" which can run in parallel. Flows are distributed across partitions by hashing 5-tuple in the packet. Only the forward flow trapped by vrouter is hashed to a partition. A reverse flow will always use same partition as it corresponding forward flow.

Each flow partition runs following sub-module in sequence,
- Flow Handler
- Flow Table Management
- Index Management
- Flow KSync

#### Flow Handler
Flow Handler receives parsed packet from Packet Handler module.

This module computes the attributes for forward flow and the reverse flows. A flow can have different attributes,
- Floating-IP
- ECMP load-balancing
- RPF next-hop
- VRF Translations
- Metadata Flows
- Linklocal Flows

#### Flow Table
- Flow-table maintains a tree of all flow-entries for given partition.
- Identifies duplicate flows
- Do policy match by implementing lookup into network-policy and security-groups
- Mark flows in inconsistent state as Short-Flow
    - Ex. Transition from NAT to Non-NAT flow
- Notify Flow Management module of add/change/delete of flows  
- Invoke Index Manager of the new flow

#### Index Management
There is difference in key between VRouter module and Agent module. VRouter uses flow-handle as key for flows and Agent uses the 6-tuple as key. Due to this inconsistency, its possible that agent will see more than one flows using same index (as transitionary state).

The Index Manager module ensures that only one flow will actively use an index. It makes use of Gen-Id for this purpose. Flow with highest value of Gen-Id can own the index and do operations to the VRouter. Flows having older Gen-Id are treated as evicted flows and get deleted.

Once Index Manager gives ownership of an index to a flow, it will invoke "Flow KSync" module to send messages to VRouter.

#### Flow KSync
This module has 2 main functionality,

1. Ensure object dependencies

A flow can refer to next-hops and mirror-entries thru indexes. This module ensures that the nexthop and mirror index pointed by flow are programmed to VRouter before flow is programmed.

KSync provides a mechanism to ensure the dependencies listed above. But, KSync dependency tracking is not multi-thread safe and it expects that flow setup does not run when KSync messages are processed. As a result, the Flow KSync module supports simple retry mechanism to ensure dependencies instead of using KSync dependency tracking.

2. Encode of messages
This module is responsible to encode/decode Flow messages to VRouter. The messages are enqueued to KSync Socket after encode.

### KSync Socket

KSync Socket implements a queue. Any module wanting to send messages to VRouter enqueues message to the queue. The KSync Socket module will bunch the requests together and send message to VRouter.

### Flow DB Client
The "Flow Handler" module will setup based on the current contents of various DBTables. When configuration changes (ex. change in security-group, network-pocicy etc...), the flows need to be reevaluated to be consistent with latest configuration. The "Flow DB Client" and "Flow Management" modules keeps the flow action consistent with latest configuration.

The "Flow DB Client" registers with DBTables of interest - 
- Interface
- Virtual-Network
- NextHop
- Route
- ACL/Security-Group

It gets notification about add/delete/change of DBEntries. On receiving notification, it checks if fields of interest to flow are modified (ex: security-group changed in Interface notification). If so, it will enqueue a request to "Flow Management" module to handle the notification. Its not a good idea to do large computation in notification context, hence it only enqueues a message to "Flow Management" module.

### Flow Management

The "Flow Management" module gets different type of notifications,

- Flow add/change/delete from "Flow Table Management" module
- DB Entries add/change/delete from "DB Client" module

The Flow management module maintains following information to track dependency between flow and DBEntries,

- Flow to list of DBEntries it is dependent on (say Flow-to-DBEntry tree)
- DBEntry to list of flows dependent on the DBEntry (say DBEntry-to-Flow tree).

When it gets notification for add/change/delete of flow, it will update the Flow-to-DBEntry tree with latest dependency information.

The processing on notification for a DBEntry depends on the the type of DBEntry, <TODO>

### Flow Stats Collector

The Flow Stats collector is responsible for ageing of flows.

The ageing algorithm has following parameters,
- Ageing time. By default, ageing time is 180 seconds.
- Scan interval. This is time by which complete flow-table is scanned once. This is set to 25% of the ageing time. As a result, flow-ageing time can have tolerance of 25% of ageing time.

The ageing algorithm can be summarised as below. The algorithm is run every 50-msec

    - Compute number of flow-entries to visit
        - This is a function of timer (50 msec), scan-interval (25% of ageing time) and number of flow-entries managed by this timer.
    - Repeat for flows identified above
        - Query stats for the flow from memory mapped flow-table
            - If there is change in stats
                - Update active time in the flow
            - If there is no change in stats
                - If flow is inactive for > ageing-time
                    - Enqueue message to age the flow
    - Store the next-flow to visit in next-iteration

#### Flow Table memory mapped to agent
On bootup, agent maps the flow-table in VRouter onto its memory-space. The memory-mapped table are used by Flow Stats module to query for flow statistics.

# Flow setup events
The sequence of events that happen for setting-up a flow are given below,

Flow-Setup Phase-1 : This phase is executed in VRouter


    1 VRouter decides to trap flow-setup message
    2 Check hash-entry already allocated for the flow
    3 If hash-entry already allocated
        3.1 Check how many packets cached in flow
        3.2 If number of packets cached in flow > "Flow Cache Limit"
            Drop packet and increment "Flow Cache Limit Exceeded"
        3.3 Add packet to list of packets held on the flow
        3.4 Increment "Flow Cache Limit" counter
    4 Else /* hash-entry not allocated */
        4.1 Is "Hold Flow Count Limit" exceeded (see 5.3)
            Drop packet and increment "Flow Unusable" counter
        4.2 Allocate an hash-entry
            4.2.1 If hash-entry cannot be allocated
                  Drop packet and increment "Flow Table Full" counter
        4.3 Increment the "Hold Flow Count Limit"
        4.4 Cache packet against the flow-entry allocated
    5 Add AgentHdr and enqueue packet to pkt0 interface

Flow-Setup Phase-2: This phase is executed in Agent


    1  Pkt0 Rx module receives packet from pkt0 interface
    2  Enqueues packet to PacketHandler module
    3  PacketModule enqueues request to one of the partitions
       3.1 PacketHandler uses hash of 5-tuple to pick flow partition
    4  Flow Module in agent computes both forward-flow and reverse-flow
    5  Agent writes reverse flow first
        5.1 Agent requests VRouter to allocate hash-entry for reverse-flow
        5.2 Agent also links reverse-flow with the forward-flow
            Note: Only reverse flow is linked to forward-flow at this time
                  Forward flow is not linked to reverse flow yet
    6 Agent waits for VRouter to allocate an entry for reverse flow


Flow-Setup Phase-3: This phase is executed in VRouter


    1 VRouter decodes message for reverse-flow
    2 Check if hash-entry already allocated for the flow
    3 If hash-entry already-allocated
       3.1 If allocated-flow in HOLD state
           3.1.1 Decrement "Flow Hold Limit Count"
           3.1.2 Release packets cached against the flow
       3.2 Update flow with new parameters in request
       3.3 Return EEXIST error
    4 Else
       4.1 Allocate flow-entry
       4.2 If flow-entry cannot be allocated
           4.2.1 Return ENOSPACE
       4.3 Return flow-index allocated


Flow-Setup Phase-4: This phase is executed in Agent


    1 Agent decodes response from VRouter
    2 If VRouter returned error
        2.1 If error is EEXIST
            This is not really error. It says VRouter already has flow
            Goto 3.1
        2.2 If error is ENOSPACE
            Flow entry cannot be allocated for reverse flow
            Make both forward and reverse flow as Short-Flow
    3 Else /* VRouter returned success */
        3.1 Update flow-index for the reverse-flow
        3.2 Send message to VRouter to update forward-flow
        3.3 Wait for VRouter response for forward-flow message


Flow-Setup Phase-5: This phase is executed in VRouter


    1 VRouter decodes message for reverse-flow
    2 Flow message already has index in flow-table
    3 Validate index in the flow-message
       3.1 If no flow present at given index
           3.1.1 Return ENOENT
       3.2 If gen-id does not match for the flow
           3.2.1 Return EBADF
       3.3 If key in flow-entry and request do not match
           3.3.2 Return EFAULT
    4 If allocated-flow in HOLD state
           3.1.1 Decrement "Flow Hold Limit Count"
           3.1.2 Release packets cached against the flow
    5 Update flow with new parameters in request

Flow-Setup Phase-6: This phase is executed in Agent


    1 Agent decodes response from VRouter
    2 If VRouter returned error
        2.1 If error is ENOENT
            Make both forward and reverse flows as short-flow
        2.2 If error is EBADF
            Make both forward and reverse flows as short-flow
        2.2 If error is EFAULT
            Make both forward and reverse flows as short-flow
        2.3 Return
    3 Else /* VRouter returned success */
        3.1 Flow state is synchronized between VRouter and Agent

# Flow Audit
Agent and VRouter exchange flow setup messages on pkt0 interface.