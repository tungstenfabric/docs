# Agent Modules in Contrail Networking

 

The VNsw Agent (also called Agent) in Contrail Networking is responsible
for managing the data plane component. It is similar to any datapath
agent that runs on the line cards of a network node. Agent
responsibilities include:

-   Interface with `contrail-controller` to get the configuration. Agent
    receives the configuration and translates it into a form that the
    datapath can understand.

-   Interface with `contrail-controller` to manage routes.

-   Collect and export statistics from datapath.

-   Translate the data model from IF-MAP to the data model used by
    datapath.

Agent contains the following modules:

-   Config

-   Oper-DB

-   Controller

-   UVE

-   Pkt

-   Services

-   KSync

Agent by itself is not a program or daemon. Based on the platform,
daemons are built using the modules listed above. The
`contrail-vxlan-agent` is the port of `contrail-vrouter-agent` on
platforms supporting VXLAN bridges.
[Figure 1](vrouter-agent-modules.html#agent-modules) provides an
overview of the different modules involved.

![Figure 1: Overview of Agent Modules](images/g301126.png)

## Config

Config module implements the northbound interface for Agent. Agent gets
two types of configurations, virtual machine ports and IF-MAP.

### Virtual-Machine Ports

Agent opens a thrift service (name InstanceService) to listen for
Port-Add/Port-Delete message. Port-Add informs agent about a virtual
machine (VM) interface created on the compute node. The Port-Add message
also contains the following information:

-   Name of virtual machine port.

-   Virtual machine for the port.

-   Mac and IP address for the port.

-   Virtual network for the port.

Once agent knows about the creation of a port, it will send a subscribe
message to `contrail-controller` for `virtual-machine`. When
`contrail-controller` receives the subscribe message for a
`virtual-machine`, it walks through the IF-MAP graph and sends all
configuration relevant for the `virtual-machine` to the Agent. The
module invoking port add message is platform dependent. In the case of
OpenStack, `nova-compute` service invokes the message.

### IF-MAP

All of the Contrail Virtual Network Controller (VNC) configuration is
stored as a Metadata Access Point (MAP) database. The MAP database is
accessed using IF-MAP protocol.

Agent does not access the MAP database directly. Instead, Agent opens an
XMPP connection to `contrail-controller` to get the MAP configuration.
The `contrail-controller` works on a subscription model. Agent must
subscribe to the virtual machines of interest and `contrail-controller`
will download all of the configuration relevant to the
`virtual-machine`. As a result, Agent receives only the minimal
configuration needed. Agent subscribes to a `virtual-machine` when it
receives a port add message for a `virtual-machine-interface`.

Agent uses the `ifmap-agent-client` library to parse the IF-MAP messages
from the XMPP channel to the `contrail-controller`. The
`ifmap-agent-client` defines a `DBTable` for every IF-MAP node type. A
special `DBTable` is defined to store the IF-MAP links. The
`ifmap-agent-client` also creates a graph for ease of navigating the
IF-MAP configuration. An IF-MAP node is vertex in the graph and links
form the edges in the graph.

### Configuration Management

Config module registers `DBTables` of interest from the
`ifmap-agent-client` library. Any add, delete, or update of the
configuration results in a callback to the Config module. The Config
module then does basic validation on the config nodes and then triggers
the operational module to process the configuration.

### Redundancy

Agent connects to two different control nodes for redundancy. When the
XMPP connection for one of the control node fails, it will subscribe to
the other control node for configuration. When connecting to the new
control node, Config module audits the configuration to remove stale
configuration.

## Oper-DB

The Oper-DB module holds the operational state of the different objects
in Agent. The operational state processes the configuration and creates
different tables appropriate for Agent.

Following are the principal tables in Oper-DB:

### Virtual Network

Table of all `virtual-networks` with UUID as the key. It contains the
following information:

Table 1: Virtual Network Table

| Item               | Description                                                                                                                                                |
|:-------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| VRF                | The `routing-instance` for the `virtual-network`.                                                                                                          |
| IPAM Data          | The IP Address Management (IPAM) configured for the `virtual-network`. It includes DHCP configuration, DNS configuration, subnet configuration, and so on. |
| Network Policy     | Network policy access control list (ACL) for the `virtual-network`.                                                                                        |
| Mirroring          | Mirroring ACL for the `virtual-network`.                                                                                                                   |
| VXLAN-ID           | Virtual Extensible Local Area Network ID (VXLAN-ID) to be used when VXLAN encapsulation is used.                                                           |
| Layer 3 Forwarding | Specifies if `layer3_forwarding` is enabled for IPv4 and IPv6 packets.                                                                                     |
| Bridging           | Specifies if bridge forwarding is enabled. Even if `layer3_forwarding` is disabled, IPv4 and IPv6 packets are bridge forwarded.                            |

### VRF

The virtual routing and forwarding (VRF) table represents a
`routing-instance` in configuration. Each `virtual-network` has a
"native" VRF. Other than the per `virtual-network` VRF, there can be
other internal VRFs. The internal VRFs are used in features, such as
service chaining.

Each VRF has a set of routing tables as its members.

Table 2: VRF Routing Tables

Table

Description

Inet4 Unicast Table

Table containing inet4 unicast routes.

Inet4 Multicast Table

Table containing inet4 multicast routes.

EVPN Table

Table containing EVPN routes keyed with MAC address, IP address, and
`vxlan/ethernet_tag`.

Bridge Table

Table containing MAC addresses. The bridge table is currently used only
in the case of a "native" VRF for a `virtual-network`.

Based the platform used, Agent creates some VRFs implicitly:

OpenStack

Agent implicitly creates a VRF for `fabric-network` with the name
`default-domain:default-project:ip-fabric:__default__`.

Xen

Agent implicitly creates a VRF for `fabric-network` with the name
`default-domain:default-project:__link_local__`.

### Virtual Machine

The virtual machine table stores all `virtual-machines` created on the
compute node.

### Interface

The interface table contains all of the interfaces in Agent. Based on
the type of interface, the trigger to create an interface can vary.
Also, the key fields used to uniquely identify the interface and the
data fields in an interface can vary based on the type of interface.

Agent supports the following different types of interfaces:

Table 3: Interface Types Supported by Agent

<table data-cellspacing="0" style="border-top:thin solid black;" width="99%">
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="header">
<th style="text-align: left;"><p>Item</p></th>
<th style="text-align: left;"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Physical Interface</p></td>
<td style="text-align: left;"><p>Represents physical ports on the compute node. Physical interfaces are created based on the <code class="inline" data-v-pre="">config-file</code> for Agent.</p>
<p>Key for physical interface is <code class="inline" data-v-pre="">&lt;interface-name&gt;</code>.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>Packet Interface</p></td>
<td style="text-align: left;"><p>Interface used to exchange packets between vRouter and Agent. Typically named <code class="inline" data-v-pre="">pkt0</code>, this interface is automatically created in Agent.</p>
<p>Key for packet interface is <code class="inline" data-v-pre="">&lt;interface-name&gt;</code>.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>Inet interface</p></td>
<td style="text-align: left;"><p>he layer 3 inet interfaces are managed by Agent. Agent can have one or more inet interfaces based on the platform used.</p>
<ul>
<li><p>OpenStack: In the case of OpenStack, Agent creates the <code class="inline" data-v-pre="">vhost0</code> inet-interface. <code class="inline" data-v-pre="">vhost0</code> is a layer 3 interface in <code class="inline" data-v-pre="">host-os</code>. Agent uses this layer 3 interface for tunnel encapsulation and decapsulation. The interface is added into the fabric VRF.</p></li>
<li><p>Xen: In the case of Xen, Agent creates the <code class="inline" data-v-pre="">xapi0</code> interface. The <code class="inline" data-v-pre="">xapi0</code> interface is added into the Xen <code class="inline" data-v-pre="">link-local</code> VRF.</p></li>
<li><p>vGW: Every vGW Virtual Gateway instance has a vGW interface created. The vGW interface is an unnumbered interface and does not have an IP address.</p>
<p>Key for inet interface is <code class="inline" data-v-pre="">&lt;interface-name&gt;</code>.</p></li>
</ul></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>VM Interface</p></td>
<td style="text-align: left;"><p>This interface represents a <code class="inline" data-v-pre="">virtual-machine-interface</code>. The interface is created when Agent receives an <code class="inline" data-v-pre="">AddPort</code> message from the Apache Thrift service <code class="inline" data-v-pre="">InstanceService</code>.</p>
<p>Key for VM interface is UUID for the interface.</p></td>
</tr>
</tbody>
</table>

An interface is in **Active** state if all of the necessary
configuration for the interface is available and it can be made
operational.

An interface is in **Inactive** state if it cannot be made operational.
The reason can be missing configuration, the `link-state` down, and so
on.

### Routes

Every VRF has a set of routing tables for inet4 unicast routes, inet4
mulitcast routes, EVPN routes, and bridge MAC entries.

Every route specifies the forwarding action for a destination. Agent has
multiple modules that can have different views of forwarding action for
a destination. Each forwarding action is specified in the form of a
path. Each module that adds a path is identified by a peer in the path.

Route keeps the list of paths sorted. The head of this list is treated
as the **Active** path for the route.

Every path contains next hop that describes forwarding action.

The unicast routing table also maintains route entries in the Patricia
tree form to support longest prefix match (LPM) on the tree.

### Next Hop

Next hop describes the forwarding action for routes pointing to it. When
route lookup for an address hits the route, the forwarding action for
the packet is defined by the next hop.

The different types of next hop supported in Agent are:

Table 4: Next Hop Types Supported by Agent

<table data-cellspacing="0" style="border-top:thin solid black;" width="99%">
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="header">
<th style="text-align: left;"><p>Type</p></th>
<th style="text-align: left;"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Discard</p></td>
<td style="text-align: left;"><p>Packets hitting <code class="inline" data-v-pre="">Discard</code> next hop must be dropped.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>Receive</p></td>
<td style="text-align: left;"><p>Packets hitting <code class="inline" data-v-pre="">Receive</code> next hop are destined to the <code class="inline" data-v-pre="">host-os</code>. The next hop has an interface on which packets must be transmited.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>Resolve</p></td>
<td style="text-align: left;"><p>Packets hitting <code class="inline" data-v-pre="">Resolve</code> next hop need ARP resolution. For example, if IP address 10.1.1.1/24 is assigned to interface <code class="inline" data-v-pre="">vhost0</code>, the following routes and next hop are generated.</p>
<ul>
<li><p>Route 10.1.1.1/32 is added with <code class="inline" data-v-pre="">Receive</code> next hop pointing to <code class="inline" data-v-pre="">vhost0</code>.</p></li>
<li><p>Route 10.1.1.0/24 is added with <code class="inline" data-v-pre="">Resolve</code> next hop. Any packet hitting this route triggers ARP resolution.</p></li>
</ul></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>ARP</p></td>
<td style="text-align: left;"><p>Routes created as a result of ARP resolution, that point to ARP next hop. In the example above, you can have routes 10.1.1.1.2/32, 10.1.1.3/32, and so on pointing to ARP next hop.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>Interface</p></td>
<td style="text-align: left;"><p>Specifies that packets hitting this next hop must be transmitted on the interface.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>Tunnel</p></td>
<td style="text-align: left;"><p>Specifies that packets hitting this next hop must be encapsulated in a tunnel. The tunnel next hop specifies tunnel destination IP address. The packet post tunneling is routed on the fabric network.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>Multicast Composite</p></td>
<td style="text-align: left;"><p>Mulitcast composite next hop contains a list of component next hops. Packets hitting the multicast composite next hop are replicated and transmitted on all the component next hops.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>ECMP Composite</p></td>
<td style="text-align: left;"><p>Equal Cost Multi-Path (ECMP) composite next hop contains a list of component next hops. Packets hitting the ECMP composite next hop must be sent out on one of the component next hops. Packet forwarding component must ensure that packets for a connection are always transmitted on the same component next hop of a ECMP composite next hop.</p>
<p>ECMP composite next hop is used to load balance traffic across multiple next hops.</p></td>
</tr>
</tbody>
</table>

### MPLS

The MPLS label defines the forwarding action for MPLS tunneled packets
received on the fabric network.

Agent assigns the following labels:

-   Two labels are allocated for every VM interface.

    -   A label for layer 3 packets.

    -   A label for bridge packets.

-   A label for every ECMP composite next hop.

-   A label for every multicast composite next hop.

The `label-range` for multicast composite next hop is preallocated and
does not overlap with other labels.

### Multicast

Multicast module is responsible for managing multicast routes.

### VXLAN

The VXLAN table contains an entry for every VXLAN ID created.

## Controller

This module manages the communication between Agent and
`contrail-controller`. Agent connects to two Contrail controllers for
redundancy. Two XMPP channels are opened with each of the Contrail
controllers.

### Configuration Channel

The Contrail controller uses this channel to send IF-MAP configuration
to Agent. Agent subscribes to configuration from only one of the XMPP
channels at a time. If the subscribed channel fails, it will switch
subscription to the other channel.

### Route Channel

This channel is used to exchange routes between Agent and Contrail
controller. Agent connects to two Contrail controllers at a time and
routes are exchanged between both of the channels. Routes from each of
the channels is added with a different "Route Peer." When one of the
channels fails, it only deletes "Route Path" from the channel that
failed.

#### Route Export

Agent exports routes for `virtual-machines` created on the local compute
node. Agent exports the route with the following information:

-   Routing instance for the route.

-   Destination network for the route (also called a `route-prefix`).

-   Next hop information:

    -   MPLS label for route if MPLSoGRE or MPLSoUDP encapsulation is
        used.

    -   VXLAN ID for route if VXLAN encapsulation is used.

    -   Gateway for the route. This is implicitly derived from the XMPP
        channel.

    -   Security group membership for the routes.

The control node implicitly derives the `virtual-network` name for the
route from the `routing-instance`.

#### Route Import

Agent subscribes to all `routing-instances` in the VRF table. The
`contrail-controller` collects routes from all Agents. Controller
synchronizes routes in a `routing-instance` if Agent is subscribed to
the `routing-instance`.

Routes are exchanged between Agent and `contrail-controller` over the
XMPP channel in XML format.

Controller module decodes the XMPP messages and adds or deletes "Route
Paths" into the routing tables. The `contrail-controller` provides the
following information for every route:

-   Routing instance for the route.

-   Destination network for the route.

-   MPLS label for the route if MPLSoGRE or MPLSoUDP encapsulation is
    being used.

-   VXLAN ID for route if VXLAN encapsulation is used.

-   Gateway for the route. This is implicitly derived from the XMPP
    channel.

-   Security group membership for the routes.

-   Virtual network for the route.

The `contrail-controller` also reflects back the routes added by Agent
itself. When the route is received, Agent looks at the gateway IP
address to identify if the route is hosted on a local compute node or a
remote compute node. If the route is hosted on a remote compute node,
the Controller module creates a next hop tunnel to be used in route. If
the route is hosted on a local compute node, a route pointing to the
next hop interface is added.

### Headless Mode

When the XMPP channel from Agent to the Contrail controller fails, Agent
flushes all of the "Route Paths" added by the controller. If the
connection to both of the Contrail controllers fail, this can result in
deleting routes distributed by the controller.

Connections to Contrail controllers can fail for many reasons including
network failure, Contrail controller node failing, and so on. Deleting
paths can result in connectivity loss between virtual machines.

Headless mode is introduced as a resilient mode of operation for Agent.
When running in headless mode, Agent retains the last "Route Path" from
Contrail controller. The "Route Paths" are held until a new stable
connection is established to one of the Contrail controllers. Once the
XMPP connection is up and is stable for a predefined duration, the
"Route Paths" from the old XMPP connection are flushed.

## Agent KSync

Oper-DB in Agent contains different tables and defines the data model
used in the Agent. While the Agent data model was initially developed
for Contrail vRouter agent, it is mostly independent of the underlying
forwarding platform.

The data model used by datapath can vary based on the platform being
ports. Agent KSync module is responsible to do the translation between
the data model used by Agent and the datapath.

The functionality of Agent KSync includes:

-   Provide translation between the data model of Agent and the
    forwarding plane.

    -   KSync will be aware of the data model used in the data plane.

    -   Oper-DB defines the data module for Agent.

-   Keeps the operational state of Agent in sync with the forwarding
    plane.

-   Keep Agent platform independent.

    Ex: KSync in Contrail vRouter agent is the only module that knows
    which flow table is memory mapped into the Contrail vRouter Agent
    memory.

## UVE

UVE module is responsible for generating UVE messages to the collector.
UVE module registers with Oper-DB and also polls the flows/vrouter to
generate the UVE messages to the collector.

## Services

This module is responsible to run the following services in Agent:

-   ARP

-   DHCP

-   DNS

-   Ping

-   ICMP error generation

 
