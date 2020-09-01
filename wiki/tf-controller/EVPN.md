EVPN

EVPN is a flexible solution to interconnect multiple edges (virtual machines) within a data center using layer 2 overlays. Traditionally data center have been build as flat Layer 2 network with issues like flooding, limitations w.r.t. redundancy and provisioning, high volume of MAC learned which in turn causes a big churn during node failures. EVPN tries to address these issues without disturbing the traditional flat MAC connectivity. 

MAC Learning in EVPN

EVPN differs from traditional Layer 2 in mac learning. It is not data plane driven but via control plane. This provides a control on learned mac across virtual forwarders and avoids flooding in network. 
Forwarders are responsible for advertising the locally learned MAC to controllers. The communication between controllers happen via MP-BGP(Multi proto BGP). The peering of controllers using BGP for EVPN helps in better and faster convergence.  
Learning of MAC is confined to the virtual network to which concerned VM belongs to and hence isolating traffic between multiple virtual networks. Thus different VN can share same MAC without any traffic crossover. 

Unicast in EVPN

The forwarding is based on MAC addresses where traffic can terminate on local end-point or encapsulated to reach the remote end-point. Encapsulation can be MPLS/GRE or VXLAN. 

BUM traffic in EVPN

Multicast and Broadcast traffic is flooded within a virtual network. The replication tree is built by control plane based on the advertisements of end-nodes (VM) done by forwarders. There is one distribution tree for one virtual network. This helps in avoiding the maintenance of multicast states at fabric nodes or in other words fabric nodes are agnostic of multicast. The replication happens at edge/forwarders.
Per-group subscription is not provided. Broadcast, Unknown Unicast and Multicast gets same treatment and gets flooded in the VN, where VM belongs.  






VXLAN

VXLAN is an overlay technology that encapsulates MAC frames at layer 2 into a UDP header. Communication is established between two tunnel end points called Virtual Tunnel Endpoints or VTEPs. VTEPs encapsulate the virtual machine traffic in a VXLAN header as well as strip the encapsulation off. 
Only VM belonging to same VXLAN segment can communicate with each other. VNID(Virtual Network Identifier) is a 24-bit identifier used to uniquely identify the VXLAN segment. This helps in having same MAC across multiple VXLAN segments without cross over of traffic between them. 
Multicast in VXLAN is implemented via Layer 3 multicast where end points subscribe to groups. 


Design Details of EVPN and VXLAN               

EVPN is always enabled.
Release supports two kind of forwarding modes – 1) Fallback bridging, 2) Layer2 
Fallback Bridging – In this mode IPv4 traffic lookup is done via IP FIB and all non IPv4 traffic is directed to MAC FIB. 
Layer2 – All traffic goes via MAC FIB lookup.
Forwarding mode can be configured on per virtual-network basis. 

In both forwarding models EVPN is used to share MAC across different control planes. MAC lookup result is a nexthop, which like IP forwarding will point to local VM or a tunnel to reach the VM on remote server. The tunnel encapsulations supported for EVPN are MPLSoGRE, MPLSoUDP and VXLAN. The selection of encapsulation type is based on the priorities of mentioned encapsulation types. For more details on MPLS encapsulation please refer to IP forwarding section. 

In VXLAN VNID is assigned uniquely for every virtual network, which is carried in VXLAN header. Unlike MPLS label that can uniquely identify VM, VNID can be used to identify VN only. At the remote server when VXLAN is received from fabric the lookup of VNID will provide VN's VRF. This VRF will be used to do the lookup of MAC from inner header, which in turn will provide the destination VM. 

VXLAN assignment can be configured on per virtual-network basis.

Non-IP multicast traffic uses the same multicast tree as for IP multicast (255.255.255.255). The multicast will be matched against all-broadcast prefix in bridging table (FF:FF:FF:FF:FF:FF). VXLAN is not supported for IP/Non-IP multicast traffic.




Here is a brief summary of traffic type and encapsulation supported for it:

ENCAPSULATION
		MPLS-GRE	MPLS-UDP	VXLAN

TRAFFIC 
TYPE	IP-UNICAST	Y	Y	N
	IP-BUM	Y	Y	N
	NON-IP-UNICAST	Y	Y	Y
	NON-IP-BUM	Y	Y	N

Note: VXLAN priority and presence in encap.py is ignored for traffic not supporting it.

Forwarding Configuration

By default forwarding mode is enabled for both IP FIB and MAC FIB. To change the forwarding mode provisioning needs to be done.

Web UI

![](file:///Users/manishsingh/Documents/1.png)
 
In web UI the forwarding mode can be edited from respective VN configuration. In the snapshot virtual-network “vn” is being modified. 
Under Advanced options->Forwarding Mode, two options are available.
“L2 and L3” – Enable IP and MAC FIB (fallback)
“L2” – Enable only MAC FIB

This can also be achieved via provisioning script for forwarding mode as shown in command below.

python provisioning_forwarding_mode --project_fq_name 'default-domain:admin' --vn_name vn1 --forwarding_mode <l2_l3 | l2>

l2_l3 – Enable IP and MAC FIB (fallback)
l2 – Enable only MAC FIB

VXLAN Configuration
 
VXLAN identifier can only be set if the VXLAN network identifier mode has been set to configured. WebUI below shows the VXLAN identifier field.

![](file:///Users/manishsingh/Documents/2.png)

This can be achieved using provision script for forwarding mode as well as shown in command below.

python provisioning_forwarding_mode --project_fq_name 'default-domain:admin' --vn_name vn1 –vxlan_id <vxlan-id>

VXLAN mode configuration

This mode can be assigned to choose between auto generated VNID and user configured VXLAN. 

Through WebUI it can be configured from Forwarding options under Infrastructure as shown in picture below. 

Automatic – Vxlan Identifier is derived automatically for virtual-network.
Configured – Vxlan has to be provided by user for virtual-network. (In case user does not specify any value then VXLAN encapsulation is not used and falls back to MPLS)

 ![](file:///Users/manishsingh/Documents/3.png)

To enable it via script modify the script /opt/contrail/utils/encap.py
In the script change the value of vxlan-network-identifier-mode to “automatic” for picking VNID and to “configured” to pick user configured VXLANID.

python encap.py <add|update|delete> <username> <password> <tenant_name> <config_node_ip>










Encapsulation mode for EVPN

By default the encapsulation mode for EVPN is MPLSoGRE. All the packets going on fabric will be encapsulated with the label allocated for VM interface. 
The label encoding/decoding remains same as of IP forwarding.
Other than MPLSoGRE, two more encapsulation are supported for EVPN i.e. MPLSoUDP and VXLAN.
MPLSoUDP is different only in terms of tunnel header encapsulation from MPLSoGRE.
VXLAN has its own header. Please refer to VXLAN section for header details. VXLAN uses VNID as label to carry the traffic over fabric.
This VNID is assigned to every Virtual network and is shared by all VM in that virtual network. This VNID is mapped to VRF of the VN to which it belongs.
By default VXLAN is NOT enabled. To change the setting following steps need to be done either via webUI or script.

From webUI encapsulation priority can be added or deleted under configuration->infrastructure->forwarding options
The priority is the sequence in which they have been added. As show in snapshot below VXLAN is at highest priority and then come MPLSoGRE and at last MPLSoUDP. 

 ![](file:///Users/manishsingh/Documents/4.png)

This can also be achieved via scripts.
Modify /opt/contrail/utils/encap.py. Line in script stating evpn_status:

encap_obj=EncapsulationPrioritiesType(encapsulation=['MPLSoUDP','MPLSoGRE'])

This can be modified to 

encap_obj=EncapsulationPrioritiesType(encapsulation=['VXLAN', 'MPLSoUDP','MPLSoGRE'])

The config is applied globally for all virtual networks. Also the sequence determines the priority of encapsulation type.
Once the status is modified execute the script as shown:

python encap.py <add|update|delete> <username> <password> <tenant_name> <config_node_ip>

Note: VXLAN is currently supported ONLY for EVPN UNICAST and NOT IP traffic or multicast traffic.










