Contrail Vrouter Agent Introspect on a compute node can be accessed via HTTP on port 8085. Various links accessible from here can be used to see the current operational data in the vrouter.

* agent.xml shows agent operational data. In this, we can see the list of interfaces, VMs, VNs, VRFs, Next hops, MPLS labels, Security groups, ACLs, Mirror configurations.

* controller.xml shows the current XMPP connections with the control node (XMPP server), the status and stats on these connections.

* cpuinfo.xml gives the CPU load and memory usage on the compute node.

* ifmap_agent.xml shows the current configuration data received from ifmap.

* kstate.xml gives data configured in the vrouter (kernel) module

* pkt.xml gives the current flow data in the agent

* sandesh_trace.xml give the module traces

* services.xml provides stats and packet dumps for control packets like DHCP, DNS, ARP, ICMP.

Below is a brief description of various next-hop types contrail vrouter agent uses.

* **Interface** - Destination VM is reachable locally on the compute node, tap interface on which packet has to sent for given destination address is also printed along with this next hop.

* **Tunnel** - Destination address is reachable on a remote compute node, hence packet would be encapsulated and sent to remote compute node where given destination VM is present

* **Resolve** - Destination route pointing such a nexthop, would result in ARP. For example lets assume IP address of compute node is 1.1.1.1/24, then a route 1.1.1.0/24 would be added pointing to a resolve NH, and any packet hitting this route would result in ARP.

* **Receive** - Destination route pointing to such a next-hop would be consumed by host. If compute node IP address is 1.1.1.1/24, then a 1.1.1.1/32 route would installed pointing to receive NH, and so that packets would be accepted and processed by host.

* **Composite** - Usually multicast route points to such a next-hop, composite next hop would in turn consist of multiple tunnel and interface next hop to which packet would be replicated to.
