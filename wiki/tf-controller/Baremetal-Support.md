From R2.1, OpenContrail supports extending a cluster to include baremetal servers and other virtual instances connected to a TOR switch supporting OVSDB protocol. The baremetal servers and other virtual instances can be configured to be part of any of the virtual networks configured in the contrail cluster, facilitating communication between them and the virtual instances running in the cluster. Contrail policy configurations can be used to control this communication.

The solution is achieved by using OVSDB protocol to configure the TOR switch and to import dynamically learnt addresses from it. VXLAN encapsulation will be used in the data plane communication with the TOR switch.

## TOR Services Node (TSN)

A node provisioned in a new role, called TOR Services Node (or TSN), is introduced. TSN will act as the multicast controller for the TOR switches and will also provide DHCP and DNS services to the baremetal servers or virtual instances running behind TOR ports.

TSN will receive all the broadcast packets from the TOR, which are then replicated to the required compute nodes in the cluster and to other EVPN nodes. Broadcast packets from the virtual machines in the cluster are sent from the respective compute nodes to the TOR switch directly.

TSN can act as the DHCP server for the baremetal servers or virtual instances, leasing them IP address along with other DHCP options configured in the system. It also provides a DNS service for the baremetal servers.

Multiple TSN nodes can be configured in the system based on the scaling needs of the cluster.

## Contrail TOR Agent

A TOR agent provisioned in the OpenContrail cluster acts as the OVSDB client for the TOR switch - all the OVSDB interactions with the TOR are done via the TOR agent. It programs the different OVSDB tables on the TOR switch and receives the local unicast table entries from it.

While TOR agents can be run on any node in the cluster, typical practice is to run it on the TSN node.

## Configuration Model

The following figure depicts the configuration model used in the system.

> 
        Physical Router
              |
              | 
        Physical Interface  -----  Logical Interface
                                          |
                                          |
                                   Virtual Machine Interface  -----  Virtual Network
> 

TOR Agent receives the configuration relevant to the TOR switch. It translates the OpenContrail configuration to OVSDB and populates the relevant OVSDB table entries in the TOR switch.  The following table maps the OpenContrail configuration objects to the OVSDB tables.

> 
        Contrail Objects                OVSDB Tables

        Physical Device	              Physical Switch
        Physical Interface	          Physical Port
        Virtual Networks	          Logical Switch
        Logical Interface	          <Vlan, Physical Port> binding to Logical Switch
        L2 Unicast Route table        Unicast Remote and Local Table
        -	                          Multicast Remote Table
        -	                          Multicast Local Table
        -	                          Physical Locator Table
        -	                          Physical Locator Set Table
> 

## Control Plane

The TOR Agent receives the EVPN entries (routes) for the virtual networks in which the TOR switch ports are members. These are added to the unicast remote table in the OVSDB. 

MAC addresses learnt in the TOR switch in different logical switches (entries from local table in OVSDB) are propagated to the TOR Agent. TOR Agent exports them to the control node in the corresponding EVPN tables, which are further distributed to other controllers and subsequently to compute nodes and other EVPN nodes in the cluster.

The TSN node receives the replication tree for each virtual network from the control node. The other compute nodes also receive the replication tree from the control node and this tree includes the TSN node.

## Data Plane

VXLAN is the data plane encapsulation used. The Virtual tunnel endpoint (VTEP) for the baremetal end will be on the TOR switch.

Unicast traffic from baremetal servers are VXLAN encapsulated by the TOR switch and forwarded, if the destination MAC is known within the virtual switch.

Unicast traffic from the virtual instances in the OpenContrail cluster are forwarded to the TOR switch, where VXLAN is terminated and the packet is forwarded to the baremetal server.

Broadcast traffic from baremetal servers are received by the TSN node. It uses the replication tree to flood the broadcast packets in the virtual network.

Broadcast traffic from the virtual instances in the OpenContrail cluster are sent to the TSN node, which replicates the packets to the TORs.

## Configuration

Contrail WebUI can be used to configure a TOR switch and interfaces on the switch.

In "Configure - Physical Devices - Physical Routers" page, create an entry for the TOR switch, providing the TOR's IP address, VTEP address. The TSN and TOR agent addresses for this TOR should also be configured here. The router name used should match the hostname on the TOR.

In "Configure - Physical Devices - Interfaces" page, add the logical interfaces to be configured on the TOR. Please note that the Name of the logical interface should match the name on the TOR (eg, ge-0/0/0.10). Other logical interface configurations like Vlan id, Mac address and IP address of the baremetal server and the virtual network it belongs to can be configured here.

# HA Solution for TOR Agent

When a TOR is managed through OVSDB via a TOR-Agent on Contrail, high availability of this solution would require support of TOR-Agent redundancy. If the TOR-Agent responsible for a TOR is unable to act as the TOR’s vRouter agent due to any failure condition in the network or the node then another TOR-Agent needs to take over and manage the TOR.

This is achieved using HA-proxy. HA-proxy is a reliable solution that offers high availability and proxy for TCP applications. An SSL connection is initiated from the TOR to the TOR-agent via HA Proxy. The TOR will be connected to exactly one active TOR-Agent at any given point.

The TOR connects to the HA Proxy, which is configured to use one of the TOR-Agents on the two TSNs. An SSL connection is established from the TOR to the TOR-Agent. The Active TOR-Agent (one having the SSL connection established with) will be responsible for advertising routes from the TOR using BGP EVPN to the Contrail Controller. The TOR-Agent also programs routes learnt via EVPN over XMPP southbound into OVSDB on the TOR. The Active TOR agent also advertises the multicast route (ff:ff:ff:ff:ff:ff) to the TOR. It ensures that there is only one multicast route in OVSDB, pointing to its TSN (this is programmed in OVSDB upon connection setup). 

Note that both the TOR Agents receive the same configuration from the control node. Also, the routes are synced via BGP.

Once the SSL connection is established, Keepalive messages are exchanged between the TOR and the TOR-Agent. Keepalive messages are sent from either end and are responded from the other end. When any message exchange is seen on the connection, keepalive message is skipped for that interval. When the TOR side sees that keepalive failed, it closes the current SSL session and tries to re-connect. When the TOR-Agent side sees that keepalive failed, it also closes the SSL session. Upon SSL session closure, the TOR Agent retracts the routes exported to control node.

## Failure Scenario

If the node on which the TOR-Agent is running goes down / fails or if the TOR-Agent crashes or when there is a network or other issue due to which the HA Proxy cannot communicate with the TOR-Agent, a new SSL connection from the TOR is established to the other TOR-Agent. 

Once connection is established to the new TOR Agent, TOR-Agent updates the multicast route in OVSDB to point its TSN, gets all the OVSDB entries, audits the data with the configuration available with it and updates the database. Entries from OVSDB local table are exported to control node from the TOR-Agent.

When SSL connection goes down, the TOR-Agent retracts the routes exported. Also, if the XMPP connection between TOR-Agent and Control node also goes down, control node immediately removes the routes exported by the TOR-Agent. In this scenario, the entries from OVSDB local table are retracted and then added back from the new TOR-Agent. In this scenario, we could see disruption in ongoing sessions.

As the configuration and routes from control node are already synced to the new TSN as well, it can act on the broadcast traffic from the TOR immediately. Service impact will be only for the time taken for SSL connection setup and programming of multicast and unicast routes in OVSDB.

## Redundancy for HA Proxy

In a high available configuration, multiple HA Proxy nodes will be configured, with VRRP running between them. The TORs will be configured to use the virtual IP address of these HA Proxy nodes, to make the SSL connection to its controller. The active TCP connections will go to the virtual IP Master node, which proxies them to the chosen TOR-Agents. A TOR-Agent among the two nodes is chosen based on lower number of connections from HA Proxy to that node and can be controlled through the configuration of the HA Proxy.

In case of a failure in the HA Proxy node, a standby node becomes the virtual IP Master and will setup the connections to the TOR-Agents. The SSL connections will be re-established and a similar scenario as explained in the previous section will be seen.

## Configuration for TOR-Agent HA

To get the required configuration downloaded from control node to the TSN Agent and to TOR Agent, prouter node has to be linked to the required vrouter nodes (representing the two TOR-Agents and the TSN) in the configuration. 

# Provisioning

TSN can be provisioned using Fab scripts. The following changes are required in the testbed.py:

1. In env.roledefs, hosts for 'tsn' and 'toragent' roles have to be added. The TSN node should also be configured in 'compute' role as well.

2. The TOR agent configuration should be added as below. The TOR Agent node should also be configured in 'compute' role as well.

3. Two TOR agents provisioned on different hosts are considered redundant to each other if the tor_name and tor_ovs_port in their respective configurations are the same. Note that this means the TOR agents will be listening on the same port for SSL connection on both the nodes.

    `

        env.tor_agent = {

                host2: [{

                        # IP address of the TOR
                        'tor_ip':'<ip address>',                                    

                        # Numeric value to uniquely identify the TOR
                        'tor_agent_id':'<id - a number>',                                                

                        # Unique name for TOR Agent. This is an optional field.
                        # If this is not specified, name used will be 
                        # <hostname>-<tor_agent_id>
                        'tor_agent_name':'nodexx-1',

                        # Always ovs
                        'tor_type':'ovs',                                     

                        # tcp or pssl (the latter from R2.2)
                        'tor_ovs_protocol':'tcp',                                     

                        # The TCP port to connect on the TOR (protocol = tcp);
                        # or ssl port on which TOR Agent listens, to which
                        # TOR connects (protocol = pssl) 
                        'tor_ovs_port':'<port>',                                   

                        # IP address of the TSN for this TOR
                        'tor_tsn_ip':'<ip address>',

                        # Name of the TSN node
                        'tor_tsn_name': '<name>' ,

                        # Name of the TOR switch, should match the hostname on the TOR
                        'tor_name':'<switch name>',  

                        # IP address for Data tunnel endpoint
                        'tor_tunnel_ip':'ip address',  
                
                        # HTTP server port
                        'tor_agent_http_server_port': <port number>, 
                                                    
                        # Vendor name for TOR Switch.       
                        'tor_vendor_name':'Juniper',

                        # Product name of TOR switch. This is an optional field.
                        'tor_product_name':'QFX5100',
                }]
        }

          # Path where the CA certificate file is stored on the node where fab is run.
          # Fab copies the file to node where TOR agent is run.
          # This is optional and is required only when tor_ovs_protocol is pssl.
          # The certificates on the TOR should be signed using this CA cert.
        env.ca_cert_file = '/root/file.pem'

    `

The following fab tasks can be used to provision the TSN and TOR Agents.

1. add_tsn : Provision all the TSNs given in the testbed.

2. add_tor_agent : Add all the tor-agents given in the testbed.

3. add_tor_agent_node : Add all tor-agents in specified node. 
   Eg. fab add_tor_agent_node:root@10.204.10.10

4. add_tor_agent_by_id : Add the specified tor-agent (identified by tor_agent_id).
   Eg. fab add_tor_agent_by_id:1,root@10.204.10.10

5. add_tor_agent_by_index : Add the specified tor-agent (identified by index/position in testbed).
   Eg. fab add_tor_agent_by_index:0,root@10.204.10.10

6. add_tor_agent_by_index_range : Add a group of tor-agents (identified by indices in testbed).
   Eg. fab add_tor_agent_by_index_range:0-2,root@10.204.10.10

7. delete_tor_agent : Remove all tor-agents in all nodes.

8. delete_tor_agent_node : Remove all tor-agents in specified node. 
   Eg. fab delete_tor_agent_node:root@10.204.10.10

9. delete_tor_agent_by_id : Remove the specified tor-agent (identified by tor-id).
   Eg. fab delete_tor_agent_by_id:2,root@10.204.10.10

10. delete_tor_agent_by_index : Remove the specified tor-agent (identified by index/position in testbed).
    Eg. fab delete_tor_agent_by_index:0,root@10.204.10.10

11. delete_tor_agent_by_index_range : Remove a group of tor-agents (identified by indices in testbed)
    Eg. fab delete_tor_agent_by_index_range:0-2,root@10.204.10.10

12. setup_haproxy_config : provision HA Proxy.

Note that fab setup_all would provision appropriately when run with the updated testbed. Also, nova-compute will not be installed on the tsn nodes. To be able to launch VMs, one needs to use additional compute nodes which are not tor-agents/TSNs. Both TSN and Toragent default "http_server_port" is 8085, if run Toragent on TSN node, one should change "tor_agent_http_server_port".

## Adding ToR agents or TSN node to an existing setup

On the new node, install contrail-install-packages and run /opt/contrail/contrail_packages/setup.sh  
Populate testbed.py to reflect this new node with tor-agent/tsn info  
From /opt/contrail/utils on config node, for each new node xyz :   

    fab upgrade_kernel_node:root@xyz
    Reboot the node so that it boots with the new kernel version
    fab setup_interface_node:root@xyz
    fab install_only_vrouter_node:no,root@xyz
    fab setup_only_vrouter_node:no,no,root@xyz
    fab add_tor_agent:False
    fab setup_haproxy_config
    (the above step of setup_haproxy_config is required only for HA mode)
    fab add_tsn:False

Then run /etc/contrail/compute_reboot on the new node which will initiate a reboot of the node  

## Regenerate Contrail SSL certificates
In case the SSL certificate used on the Contrail side needs to be regenerated, the following steps can be followed:
* Remove existing SSL certificates (rm /etc/contrail/ssl/certs/tor.<tor-id>.cert.pem /etc/contrail/ssl/private/tor.<tor-id>.privkey.pem) on the TSN node (both TSN nodes in case of HA configuration).
* fab add_tor_agent (this will re-generate the tor-agent configuration file as well as the SSL certificates - if the testbed.py is latest and no other changes were done in the tor-agent configuration file, this step would be fine. Otherwise, get new certificates using the below command. In case it is created using the command below, the generated files have to be copied to the second TSN node as well, in case of HA configuration.

`openssl req -new -x509 -days 3650 -text -sha256 -newkey rsa:4096 -nodes -subj "/C=US/ST=Global/O=juniper" -keyout /etc/contrail/ssl/private/tor.<tor-id>.privkey.pem -out /etc/contrail/ssl/certs/tor.<tor-id>.cert.pem`
* Restart contrail-tor-agent
* Remove the file /var/db/certs/ca-cert.pem file on the QFX.

## Prior Configuration required on QFX5100

The following configuration has to be done on a QFX5100 beforehand.

* Enable OVSDB
* Set the connection protocol 
* Indicate the interfaces that will be managed via OVSDB
* Configure switch options with VTEP source (in the example below, lo0.0 is used – ensure that this address is reachable from TSN node)
* In case of pssl, update the controller details. When HA proxy is used, use the address of the HA Proxy node and use the vIP when VRRP is used between multiple nodes running HA Proxy.

> 
* set interfaces lo0 unit 0 family inet address \<router-id-reachable-on-ip-fabric\>
* set switch-options ovsdb-managed
* set switch-options vtep-source-interface lo0.0
* set protocols ovsdb passive-connection protocol tcp port \<port-number\>
* set protocols ovsdb interfaces \<interfaces-to-be-managed-by-ovsdb\>
* set protocols ovsdb controller \<tor-agent-ip\> inactivity-probe-duration 10000 protocol ssl port \<tor-agent-port\>
> 

* When using SSL to connect, CA-signed certificates have to be copied to /var/db/certs directory in the QFX. One way to get these is using the following (run on any server). 

>
* apt-get install openvswitch-common
* ovs-pki init
* ovs-pki req+sign vtep
* scp vtep-cert.pem root@tor-ip:/var/db/certs
* scp vtep-privkey.pem root@tor-ip:/var/db/certs
* cacert.pem file will be available in /var/lib/openvswitch/pki/switchca, when the above are done. This is the file to be provided in the above testbed (for ca_cert_file).
>
 
## Caveats

It is not possible to configure both tagged and untagged logical ports on the same QFX physical port via OVSDB. So, this configuration should not be done.

## Debug

On the QFX, the following commands show the OVSDB configuration.

* 	show ovsdb logical-switch
* 	show ovsdb interface
* 	show ovsdb mac
* 	show ovsdb controller
* 	show vlans

Introspect on TOR agent and TSN nodes show the configuration and operational state of these modules.

The TSN module is like any other contrail-vrouter-agent on a compute node, with Introspect access available on port 8085 by default. Operational data like interfaces, VN and VRF information along with the routes can be checked here.

The port on which TOR agent Introspect access is available will be present in the config file provided to contrail-tor-agent. This provides the OVSDB data available through the client interface, apart from the other data available in a Contrail Agent.

## Debug FAQ

* TOR Agent is not coming up : Check the TOR Agent configuration file. In case pssl is specified, check that the certificate files are specified and are present on the node.

* SSL connection is not established : Check the controller configuration on the TOR. It should either point to the node where HA Proxy is run or directly to the node where TOR Agent is running.
If the connection is getting established and getting closed, check that the certificate files in TOR are correct, signed with the ca-cert file provided to the TOR-Agent. In case TOR-Agent is re-provisioned, it is possible that the certificates on the TOR-Agent are updated and the QFX is expecting the older one - remove /var/db/certs/ca-cert.pem on the QFX in such a case.

* OVSDB is not getting updated : Check that the router name specified in Contrail matches the hostname on the TOR. Note that in case of QFX VC configuration, all QFX nodes are expected to have the same hostname.

* Scale configuration : Check the limits configured on the TSN node using ``vrouter --info`` and verify that these limits are appropriate. If required, update them by having /etc/modprobe.d/vrouter.conf with the following and restarting the node:
``options vrouter vr_mpls_labels=131072 vr_nexthops=131072 vr_vrfs=65536 vr_bridge_entries=262144 ``

Calculate these as follows:
> * mpls_labels = (max number of VNs * 3) + 4000
> * nexthops = (max number of VNs * 4) + (number of VM interfaces on the compute node * 5) + number of TORs + (number of compute nodes * 2) + 100
> * vrfs = Max number of VNs
> * macs = Maximum number of MACs in a VN

* Scale configuration : With high MAC count on the TOR, if the SSL connection to the TOR-Agent is flapping, check if the keepalive timer requires tuning. In /etc/contrail/contrail-tor-agent-<xx>.conf file, option tor_keepalive_interval can be set to desired value. Check that inactivity-probe-duration is specified while configuring the controller on the QFX.

## Changes in the Configuration file to the Agent

In /etc/contrail/contrail-vrouter-agent.conf file for TSN, Agent mode option is now additionally available in DEBUG section to configure the agent in TSN mode.

> 
agent_mode = tsn
> 

The following are the typical configuration items in a Tor Agent config file.

> 
[DEFAULT]
> 
agent_name = noded2-1    # Name (formed with hostname and TOR id from below)
>
agent_mode = tor         # Agent mode 
>
http_server_port=9010    # Port on which Introspect access is available
>
[DISCOVERY]
>
server=<ip>              # IP address of discovery server
>
[TOR]
>
tor_ip=<ip>              # IP address of the TOR to manage
>
tor_id=1                 # Identifier for ToR. TOR Agent subscribes 
                         # to ifmap-configuration with this name
>
tor_type=ovs             # ToR management scheme - only “ovs” is supported
>
tor_ovs_protocol=tcp     # IP-Transport protocol used to connect to TOR
>
tor_ovs_port=port        # OVS server port number on the ToR
>
tsn_ip=<ip>              # IP address of the TSN
>
tor_keepalive_interval=10000 # keepalive timer in ms
>
ssl_cert=/etc/contrail/ssl/certs/tor.1.cert.pem # Path to ssl certificate for tor-agent, needed for pssl
>
ssl_privkey=/etc/contrail/ssl/private/tor.1.privkey.pem # Path to ssl private-key for tor-agent, needed for pssl
>
ssl_cacert=/etc/contrail/ssl/certs/cacert.pem # Path to ssl cacert for tor-agent, needed for pssl
>
## Contrail REST API

* Physical Router

    {
              u'physical-router': {
    u'physical_router_management_ip': u'100.100.100.100',
    u'virtual_router_refs': [],
    u'fq_name': [
      u'default-global-system-config',
      u'test-router'
    ],
    u'name': u'test-router',
    u'physical_router_vendor_name': u'juniper',
    u'parent_type': u'global-system-config',
    u'virtual_network_refs': [],
    'id_perms': {
      u'enable': True,
      u'uuid': None,
      u'creator': None,
      u'created': 0,
      u'user_visible': True,
      u'last_modified': 0,
      u'permissions': {
        u'owner': u'cloud-admin',
        u'owner_access': 7,
        u'other_access': 7,
        u'group': u'cloud-admin-group',
        u'group_access': 7
      },
      u'description': None
    },
    u'bgp_router_refs': [],
    u'physical_router_user_credentials': {
      u'username': u'',
      u'password': u''
    },
    'display_name': u'test-router',
    u'physical_router_dataplane_ip': u'101.1.1.1'
             }
    }

* Physical Interface

    {
      u'physical-interface': {
    u'parent_type': u'physical-router',
    'id_perms': {
      u'enable': True,
      u'uuid': None,
      u'creator': None,
      u'created': 0,
      u'user_visible': True,
      u'last_modified': 0,
      u'permissions': {
        u'owner': u'cloud-admin',
        u'owner_access': 7,
        u'other_access': 7,
        u'group': u'cloud-admin-group',
        u'group_access': 7
      },
      u'description': None
    },
    u'fq_name': [
      u'default-global-system-config',
      u'test-router',
      u'ge-0/0/1'
    ],
    u'name': u'ge-0/0/1',
    'display_name': u'ge-0/0/1'
      }
    }

* Logical Interface

    {
      u'logical-interface': {
    u'fq_name': [
      u'default-global-system-config',
      u'test-router',
      u'ge-0/0/1',
      u'ge-0/0/1.0'
    ],
    u'parent_uuid': u'6608b8ef-9704-489d-8cbc-fed4fb5677ca',
    u'logical_interface_vlan_tag': 0,
    u'parent_type': u'physical-interface',
    u'virtual_machine_interface_refs': [
      {
u'to': [
          u'default-domain',
          u'demo',
          u'4a2edbb8-b69e-48ce-96e3-7226c57e5241'
]
      }
    ],
    'id_perms': {
      u'enable': True,
      u'uuid': None,
      u'creator': None,
      u'created': 0,
      u'user_visible': True,
      u'last_modified': 0,
      u'permissions': {
        u'owner': u'cloud-admin',
        u'owner_access': 7,
        u'other_access': 7,
        u'group': u'cloud-admin-group',
        u'group_access': 7
      },
      u'description': None
    },
    u'logical_interface_type': u'l2',
    'display_name': u'ge-0/0/1.0',
    u'name': u'ge-0/0/1.0'
      }
    }