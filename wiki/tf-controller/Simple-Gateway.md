# Introduction

Every virtual-network has a routing-instance associated with it. The routing-instance defines network connectivity for the virtual-machines spawned in the corresponding virtual-network. By default, the routing-instance contains routes only for virtual-machines spawned in the virtual-network. Connectivity between virtual-networks can be achieved by defining Network policies. 

Virtual-Networks do not have access to "public" network. "public" network here can be the IP Fabric or external networks across the IP Fabric. A Gateway must be used to provide connectivity to "public" network from a virtual-network. In traditional deployments, a routing device such as Juniper MX can act as a gateway.
 
Simple Gateway is a restricted implementation of gateway which can be used for experimental purposes. Simple gateway provides access to "public" network to virtual-networks.

# Working of Simple Gateway Work

Working of Simple Gateway is explained by an example.

## Setup without Simple Gateway
The diagram below shows a setup when Simple Gateway is not configured

1. A Virtual-Network default-domain:admin:net1 is configured with subnet 192.168.1.0/24
1. Routing instance default-domain:admin:net1:net1 is associated with virtual-network default-domain:admin:net1
1. There is a virtual-machine with IP 192.168.1.253 spawned in net1
1. Virtual machine is spawned on compute server-1
1. Interface vhost0 is in host-os of server-1 and is assigned IP 10.1.1.1/24
1. Interface vhost0 is added to vrouter in routing-instance FABRIC
1. Simple Gateway is not configured

> 
    +-------------------------------------------------------------------+
    |                  Host-OS Networking Stack                         |
    |                  0.0.0.0/24 => 10.1.1.254                         |
    |                                                                   |
    |                                              10.1.1.1/24          |
    +--------------------------------------------------+----------------+
                                                       |vhost0
                                                       |
                                                       |
    +--------------------------------------------------+-----------------+
    |                                                  |                 |
    |   VRF:default-domain:admin:net1:net1             | VRF : Fabric    |
    |+-------------------------------+      +----------+--------------+  |
    ||                               |      |                         |  |
    || 192.168.1.253/32 => tap0      |      | 10.1.1.1/32 => vhost0   |  |
    || 192.168.1.0/24 => drop        |      |                         |  |
    |+-------+- ---------------------+      +----------+--------------+  |
    |        |                    VROUTER              |                 |
    +--------+-----------------------------------------+-----------------+
             | tap0                                    |eth0
             |                                         |
    +--------+------------+                            |
    |  192.168.1.253/24   |                 -----------+------------            
    |                     |                             Fabric-Network 
    |   VM-1              |
    +---------------------+
    

## Setup with Simple Gateway

The diagram below shows a setup with Simple Gateway configured for Virtual-Network default-domain:admin:net1.

Simple Gateway make use of Gateway Interface (**vgw** below) to provides connectivity between routing-instances FABRIC and default-domain:admin:net1:net1.

Packets between the FABRIC and default-domain:admin:net1:net1 

>
    +-------------------------------------------------------------------+
    |                  Host-OS Networking Stack                         |
    |                  0.0.0.0/24 => 10.1.1.254                         |
    |                  192.168.1.253/24 => vgw*                         |
    |                                              10.1.1.1/24          |
    +----+---------------------------------------------+----------------+
         |vgw                                          |vhost0
         |                                             |
         |                                             |
    +----+---------------------------------------------+----------------+
    |    | VRF: default-domain:admin:net1:net1         | VRF: FABRIC    |
    |+---+--------------------------+       +----------+-------------+  |
    || 192.168.1.253/32 => tap0     |       |10.1.1.1/32 => vhost0   |  |
    || 192.168.1.0/24 => drop       |       |192.168.1.0/24 => vhost0|  |
    || 0.0.0.0/0 => vgw             |       |                        |  |
    ||                              |       |                        |  |
    |+---------+--------------------+       +------------------------+  |
    |          |                  VROUTER                               |
    +----------+---------------------------------------+----------------+
               |tap0                                   |eth0
    +---+------+----------+                            |
    |  192.168.1.253/24   |                 -----------+------------            
    |                     |                             Fabric-Network 
    |   VM-1              |
    +---------------------+
    Routes marked with (*) are added by Simple Gateway feature.    

1. Simple Gateway is configured for Virtual-Network default-domain:admin:net1
1. Gateway interface **vgw** provides connectivity between routing instance default-domain:admin:net1:net1 and FABRIC.
   1. IP address is not configured for Gateway interface **vgw**
1. Host-OS is configured with following,
   1. Two INET interfaces are added to host-os - **vgw** and **vhost0**
   1. Host-os is not aware of routing-instances, so **vgw** and **vhost0** are part of same routing-instance in host-os
   1. Simple Gateway adds route 192.168.1.0/24 pointing to vgw interface is added to host-os. This route will ensure any packet destined to VM is sent to Vrouter on **vgw** interface.

1. vrouter is configured with following,
   1. Routing-instance FABRIC is created for Fabric Network.
       1. Interface vhost0 is added to routing-instance FABRIC
       1. Interface eth0 (connected to Fabric Network) is added to routing-instance FABRIC.
       1. Simple Gateway adds route 192.168.1.0/24 => vhost0 is added so that packets destined to virtual-network default-domain:admin:net1 are sent to host-os
   1. Routing-instance default-domain:admin:net1:net1 is created for virtual-network default-domain:admin:net1.
      1. Interface vgw is added to routing-instance default-domain:admin:net1:net1
      1. Simple Gateway adds a default route 0.0.0.0/0 pointing to interface vgw.
         Packets in routing-instance default-domain:admin:net1:net hitting this route are sent to host-os on **vgw** interface. The host-os will route packets to FABRIC network over vhost0 interface.

## Restrictions
1. A single compute node can have Simple Gateway for multiple virtual-networks
1. If multiple Virtual Networks have Simple Gateway on same compute node, they cannot have overlapping subnets. The host-os does not support routing-instances hence, all Gateway Interfaces in host-os are in same routing-instance. As a result, the subnets in Virtual Networks must not overlap. 
1. Each Virtual-Network can have single Simple Gateway interface. ECMP is not yet supported.

# Packet flow

## Packet from virtual-network (net1) to public network

1. Packet with source-ip=192.168.1.253 and destination-ip=10.1.1.253 from virtual-machine is received by vrouter on interface tap0
1. Interface tap0 is in routing-instance default-domain:admin:net1:net1
1. Route lookup for 10.1.1.253 in routing-instance default-domain:admin:net1:net1 hits default-route pointing to tap interface 'vgw'
1. vrouter transmits packet on 'vgw' and is received by networking-stack of host-os
1. Host-os does forwarding based on its routing table and forwards packet on vhost0 interface
1. Packets transmitted on vhost0 are received by vrouter
1. vhost0 interface is added in routing-instance FABRIC
1. Routing for 10.1.1.253 in routing-instance FABRIC will result in packet being transmitted on eth0 interface
1. vrouter transmits packet on eth0 interface
1. Host 10.1.1.253 on fabric receives the packet

## Packet from public network to virtual-network (net1)

1. Packet with source-ip=10.1.1.253 and destination-ip=192.168.1.253 from public network is received on interface eth0
1. vrouter has routing-instance FABRIC configured for fabric-network. Interface eth0 is added to routing-instance FABRIC
1. vrouter receives packet from eth0 in routing-instance FABRIC
1. Route lookup for 192.168.1.253 in FABRIC points to interface 'vhost0'
1. vrouter transmits packet on 'vhost0' and is received by networking-stack of host-os
1. Host-os does forwarding based on its routing table and forwards packet on 'vgw' interface
1. vrouter receives pacekt on 'vgw' interfcace into routing-instance default-domain:admin:net1:net1
1. Route lookup for 192.168.1.253 in routing-instance default-domain:admin:net1:net1 points to 'tap0' interface
1. vrouter transmits packet on tap0 interface
1. virtual-machine receives packet destined to 192.168.1.253

# Configuration

Simple Gateway can be configured with 4 different options.

## Option 1. Configuring VGW during provisioning using fab.
While provisioning setup using fab, we can provision virtual gateway by enabling the knob in testbed file.
We can select some or all of the compute node to be configured as vgw. To do so in env.roledefs along with other role definition we need add vgw roles. We can select a subset or complete set of compute node to become vgw. 

**Sample**:

    env.roledefs = {

        'all': [host1, host2, host3, host4, host5, host6],

        'cfgm': [host1, host2, host3],

        'openstack': [host2],

        'webui': [host3],

        'control': [host1, host3],

        'compute': [host4, host5, host6],

        'vgw': [host4, host5], >>>>>>>>>Add section VGW in one or multiple compute node

        'collector': [host1, host3],

        'database': [host1],

        'build': [host_build],
    }

    env.vgw = {

          host4: {

                 'vgw1': {

                             'vn':'default-domain:admin:public:public', 

                             'ipam-subnets': ['10.204.220.128/29', '10.204.220.136/29']

                             'gateway-routes': ['8.8.8.0/24', '1.1.1.0/24']

                          },

                 'vgw2':{

                              'vn':'default-domain:admin:public1:public1', 

                              'ipam-subnets': ['10.204.220.144/29']}},
          host5: {

                 'vgw2':{

                              'vn':'default-domain:admin:public1:public1', 

                              ipam-subnets': ['10.204.220.144/29']

                        }

                 }
          } 
    }

**Definition for the Key used**

**vgw<number>**: This is the interface name is going to get configured on the server.
 
**vn**: Virtual Network fully qualified name. This particular VN will be used by VGW .

**ipam-subnets**: Subnets used by vn. It can be single or multiple

**gateway-routes**: If any route is present then only those routes will be published by VGW or Default route (0.0.0.0) will be published

As per the above configuration, from the list of 3 compute nodes (host4,host5 and host6), 2 of them (host4 and host5) picked up for configuring VGW. 
In host4, Two VGW interface is configured with named vgw1 and vgw2. They are associated with virtual network public and public1 respectively.
Key 'ipam-subnets' represent the subnets used by each virtual network. 
Same VGW interface   can be configured in different compute node. But they need to be associated with same virtual network. In the above example vgw2 is configured in 2 host, host4 and host5. In both the cases they are associated with same virtual network.  
Key 'gateway-routes' is an optional parameter. If 'gateway-routes' is configured, corresponding vgw will only publish list of routes mentioned in the list. 


Once this above configuration is present, while executing fab setup_all, this will provision VGW.

## Option 2. Static Gateway using contrail-vrouter-agent.conf file

One or more Gateway Interfaces can be configured in contrail-vrouter-agent.conf file. Each Gateway Interface can take following parameters,

* **interface=vgw** : Gateway Interface name
* **routing_instance=default-domain:admin:public:public** : Name of the routing_instance for which gateway is being configured
* **ip_block=1.1.1.0/24** : List of subnet addresses allocated for the virtual-network. Route with this subnet are added to both host-os and routing-instance for FABRIC. Multiple subnets are represented by separating each with a space
* **routes=10.10.10.1/24 11.11.11.1/24** : List of subnets in public network that are reachable from virtual-network. Routes with this subnet are added to routing-instance configured above. Multiple routes are represented by separating each with a space

Any change in gateway configuration will be effective on next restart of agent.

## Option 3. Dynamic Simple Gateway
From R1.1, Virtual Gateway can be created & deleted dynamically by sending thrift messages to the vrouter agent. The following thrift messages are defined:

 1. AddVirtualGateway to add a virtual gateway
 2. DeleteVirtualGateway to delete a virtual gateway
 3. ConnectForVirtualGateway can be used by stateful clients, which allows audit of virtual gateway configuration. Upon a new ConnectForVirtualGateway request, one minute is given for the configuration to be redone. Any older virtual gateway configuration remaining after this time is deleted.

### To create a virtual gateway
Run the following script on the compute node where the virtual gateway will be created. This script enables forwarding on the node, creates the required interface, adds it to vrouter, adds required routes in the host OS and sends thrift message to the vrouter agent to create the virtual gateway.

    For example, to create interface vgw1 with subnets 20.30.40.0/24 and 30.40.50.0/24 in vrf default-domain:admin:vn1:vn1, run

    # set PYTHONPATH appropriately (where InstanceService.py and ttypes.py are present). For example,
    # For python 2.7
    export PYTHONPATH=/usr/lib/python2.7/dist-packages/contrail_vrouter_api/gen_py/instance_service
    
    # For python 2.6
    export PYTHONPATH=/usr/lib/python2.6/site-packages/contrail_vrouter_api/gen_py/instance_service

    python /opt/contrail/utils/provision_vgw_interface.py --oper create --interface vgw1 --subnets 20.30.40.0/24 30.40.50.0/24 --routes 8.8.8.0/24 9.9.9.0/24 --vrf default-domain:admin:vn1:vn1

   * Option --subnets specifies list of subnets defined in virtual-network vn1
   * Option --routes specifies routes in public-network injected into vn1. In example above, the Virtual machines in vn1 can access subnets 8.8.8.0/24 and 9.9.9.0/24 in public network

### To delete a virtual gateway
Run the following script on the compute node where the virtual gateway was created. This sends the DeleteVirtualGateway thrift message to the vrouter agent to delete the virtual gateway, deletes the interface from vrouter and deletes the routes added in the host OS.

    # set PYTHONPATH appropriately (where InstanceService.py and ttypes.py are present). For example,
    # For python 2.7
    export PYTHONPATH=/usr/lib/python2.7/dist-packages/contrail_vrouter_api/gen_py/instance_service
    
    # For python 2.6
    export PYTHONPATH=/usr/lib/python2.6/site-packages/contrail_vrouter_api/gen_py/instance_service

    `python /opt/contrail/utils/provision_vgw_interface.py --oper delete --interface vgw1 --subnets 20.30.40.0/24 30.40.50.0/24`

If using a stateful client, send the ConnectForVirtualGateway thrift message to the vrouter agent when the client starts.

**Note:**
If the vrouter agent restarts or if  the compute node reboots, it is expected that the client will reconfigure again

## Option 4. Static Gateway in devstack

Simple Gateway uses following configuration parameters in the devstack "localrc" file. The routes given below in example are derived from the configuration parameters given below.
 
**CONTRAIL_VGW_PUBLIC_NETWORK** : Name of the routing_instance for which gateway is being configured.

**CONTRAIL_VGW_PUBLIC_SUBNET** :  List of subnet addresses allocated for the virtual-network. Route with this subnet are added to both host-os and routing-instance for FABRIC. Multiple subnets are represented by separating each with a space
 
**CONTRAIL_VGW_INTERFACE** : List of subnets in public network that are reachable from virtual-network. Routes with this subnet are added to routing-instance configured above. Multiple routes are represented by separating each with a space

This method can only add default route 0.0.0.0/0 into routing-instance specified in CONTRAIL_VGW_PUBLIC_NETWORK.

# Example Scenario

Example configuration :

1. Virtual Network default-domain:admin:net1 needs Simple Gateway
1. Subnet 192.168.1.0/24 is configured for Virtual Network default-domain:admin:net1
1. Virtual Network net1 needs access to subnets 8.8.8.0/24 and 9.9.9.0/24 in public network

## contrail-vrouter-agent.conf Configuration
interface=vgw

routing_instance=default-domain:admin:net1:net1

ip_blocks=192.168.1.0/24

routes=8.8.8.0/24 9.9.9.0/24

## Dynamic Simple Gateway Configuration

Run following command

# set PYTHONPATH appropriately (where InstanceService.py and ttypes.py are present). For example,

`export PYTHONPATH=/usr/lib/python2.7/dist-packages/nova_contrail_vif/gen_py/instance_service`

`export PYTHONPATH=/usr/lib/python2.6/site-packages/contrail_vrouter_api/gen_py/instance_service`

`python /opt/contrail/utils/provision_vgw_interface.py --oper create --interface vgw1 --subnets 192.168.1.0/24  --routes 8.8.8.0/24 9.9.9.0/24 --vrf default-domain:admin:net1:net1`

## Devstack Configuration
Add following lines in the "localrc" file for stack.sh

CONTRAIL_VGW_INTERFACE=vgw

CONTRAIL_VGW_PUBLIC_SUBNET=192.168.1.0/24

CONTRAIL_VGW_PUBLIC_NETWORK=default-domain:admin:net1:net1

**NOTE** : This method can only add default route 0.0.0.0/0 into routing-instance specified in CONTRAIL_VGW_PUBLIC_NETWORK.

# FAQ's

### Packets from external network are not reaching the compute node.

The devices in fabric network must be configured with static routes for 192.168.1.0/24 to reach the compute node running as simple gateway.
 
### Packets are reaching compute node, but are not routed from host-os to VM.

Check if the firewall_driver in /etc/nova/nova.conf file is set to nova.virt.libvirt.firewall.IptablesFirewallDriver. This will enable IPTables which can discard packet. Either disable IPTables during runtime or alternatively set firewall_driver to nova.virt.firewall.NoopFirewallDriver by setting LIBVIRT_FIREWALL_DRIVER=nova.virt.firewall.NoopFirewallDriver in localrc
***

***