# Remote Instances

Extending virtual instances running in non Openstack clusters or extending baremetal servers into Contrail virtual networks can be achieved using [OVSDB protocol](https://github.com/Juniper/contrail-controller/wiki/Baremetal-Support) or by configuring a contrail compute node to run in gateway mode to support remote instances. The latter is supported from R3.1 and this wiki summarizes this feature.

Traffic from each external virtual instance is tagged with a unique VLAN, which is then mapped to a virtual machine interface in the contrail cluster. A contrail compute node can be configured to map VLAN tagged traffic coming on a physical port (other than the cluster's underlay IP fabric port) to a virtual machine interface configured in the contrail cluster. The virtual machine interface corresponds to the interface of the remote instance. For the vrouter on the gateway compute node, it works similar to a local virtual machine interface, with the traffic being subjected to the similar forwarding decisions and policies.

Note that one VLAN is mapped to one virtual machine interface.

## Provisioning

In /etc/contrail/contrail-vrouter-agent.conf, add the following in DEFAULT section and restart contrail-vrouter-agent.

`gateway_mode = server`

## Configuration

1. Configure a physical router with the hostname of the compute node that acts as the gateway.
2. Create a physical interface on the physical router, with the name of the interface on the compute node that will be used for this traffic.
3. Create a logical interface on the physical interface, with a unique VLAN id and type set to L2.
4. Create a virtual machine interface in the required virtual network along with the MAC address of the remote instance and IP address and link it to the logical interface.

## External configuration

The traffic from the remote instance should come with the required VLAN tag to the gateway port.

# Gateway HA

Multiple gateway nodes can be configured to have high availability.

In the initial version, the selection of active gateway node is expected to be handled by using (R)STP from the switches connecting the gateway node. For this, a special virtual network is configured in Contrail that will flood the STP BPDUs. On the gateway compute nodes, create logical interfaces with VLAN 0. Create a dummy virtual machine interface belonging to the special virtual network (following the same procedure as above). Link the virtual machine interface to the VLAN 0 logical interfaces on the gateway nodes that are to form a HA group. With this configuration, STP would allow traffic to one of the gateway ports while blocking others.

For each remote instance, create a logical interface on the gateway nodes in the HA group. Link the logical interface to the virtual machine interface created for the remote instance (corresponding instance IP should have active-backup mode set, which is the default mode). After this, contrail will handle switchover of the traffic to a different gateway node.