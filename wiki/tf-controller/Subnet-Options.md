
Subnets can be created and deleted in a Virtual Network, each having its own attributes. The attributes that can be defined for each subnet, along with the subnet prefix and prefix length are listed below. Subnets are configured in virtual-network-network-ipam under the network-ipam(s) associated with the virtual-network, with as many 'ipam-subnets' as desired within each associated network-ipam.

<br>
1.  Default Gateway

***
* A default gateway for the subnet can be set explicitly, can be left to be allocated by Contrail, or can be disabled.
* 'default-gateway' is the corresponding field in ipam-subnets.
* When default gateway is to be disabled, set this field to 0.0.0.0.
* When the field is not set, Contrail allocates an address from the subnet as the default gateway.
* Neutron commands <br>
`     neutron subnet-create test-vn 10.0.0.0/24 --gateway 10.0.0.1`<br>
`     neutron subnet-create test-vn 10.0.0.0/24 --no-gateway`

<br>
2. Allocation Pool

***
* Allocation pools with start and end addresses can be configured as 'allocation-pools'.
* VMs spawned are assigned addresses from within the allocation pool range.
* Neutron command <br>
`     neutron subnet-create test-vn 10.0.0.0/24 --allocation-pool start=10.0.0.100,end=10.0.0.200`

<br>
3. DHCP

***
* DHCP is enabled by default on each subnet.
* 'enable-dhcp' is the corresponding field in ipam-subnets (boolean).
* When enabled, the DHCP requests from the VMs are trapped to contrail-vrouter-agent, which responds with the IP address of the VM's interface along with other configured DHCP options.
* When disabled, the DHCP requests from the VMs are broadcast within the virtual network or are unicast for broadcast and unicast requests respectively.
* Neutron commands <br>
`     neutron subnet-create test-vn 10.0.0.0/24 —enable_dhcp` <br>
`     neutron subnet-create test-vn 10.0.0.0/24 —disable_dhcp`

<br>
4. DHCP options

***
* Contrail allows DHCP options to be configured at different levels - IPAM, Subnet, Interface
* Interface level has the highest precedence, followed by Subnet and IPAM in that order. Options defined at a higher precedence level override the options defined at lower precedence level. Thus, global DHCP options can be defined at IPAM or Subnet levels and specific options can be overridden at Subnet or Interface levels.
* In all these cases, dhcp-option-list can be configured, having a list of dhcp-optiontypes, each option having dhcp-option-name and dhcp-option-value. Complete list of options supported is here : https://github.com/Juniper/contrail-controller/wiki/Extra-DHCP-Options.
* Neutron command <br>
`     neutron port-create test-vn --extra-dhcp-opts list=true opt_name='dhcp_option_name',opt_value='value'`

<br>
5. Host Routes

***
* To update routes in the VM, host routes can be defined.
* Set of prefix and next-hop address for the prefix can be configured, which are then sent to the VM as classless static route option in DHCP response. 
* These can be configured as part of DHCP options (see above) or in host-routes field in ipam-subnets. 
* Neutron command <br>
`     neutron subnet-create test-vn 10.0.0.0/24 --host_routes type=dict list=true destination=10.0.1.0/24,nexthop=10.0.0.3`

<br>
6. Subnet name

***
* Name for the subnet, 'subnet-name' is the corresponding field in ipam-subnets.
* Neutron command
`     neutron subnet-create test-vn 10.0.0.0/24 --name subnet-name`

<br>
7. DNS name servers

***
* Name servers for the subnet can be explicitly set.
* These are set using the DHCP option 'domain-name-servers' to the required address list (see DHCP options above).
* To disable DNS name servers in the subnet, set the DHCP option 'domain-name-servers' to 0.0.0.0.
* If this option is not set, the VM receives the service address (see below) as the DNS name server and contrail-vrouter-agent provides the DNS service for the subnet.
* Neutron command <br>
`     neutron subnet-create test-vn 10.0.0.0/24 --dns_nameservers list=true 8.8.8.7 8.8.8.8` <br>
`     neutron subnet-create test-vn 10.0.0.0/24 --dns_nameservers list=true 0.0.0.0    # disable DNS` 

<br>
8. Service Address

***
* In every subnet, one address is reserved for Gateway (when enabled) and another is reserved for Services. This Services address is used as the DHCP server address and can be seen in all the DHCP responses.
* The same address is also used as the DNS server address for the subnet if DNS name server is not configured. In such a case, this address will be sent as domain-name-server in DHCP response to the VM.
* 'dns-server-address' is the corresponding field in ipam-subnets. If not set, this address will be auto-allocated from the subnet (typically .2 address from the subnet). When set to 0.0.0.0, no additional address is allocated and the gateway address of the subnet is used for this purpose as well. 


## Disabling Gateway
Gateway, DHCP service and DNS service can be enabled and disabled independently. When Gateway is disabled in the subnet, Contrail can still provide the DHCP and DNS service. If another VM will serve as the Gateway, configure that VMs address in the 'routers' DHCP option, with Gateway disabled in the subnet. VMs in the subnet will receive this address as the gateway address in their DHCP responses from contrail-vrouter-agent. The service address will be the DHCP server and DNS server address.

If host routes are also configured on the subnet, the default route is expected to be added as part of the host route configuration. The 'router' option will not be included in this case (RFC3442) and hence default route has to be part of host routes.


## Disabling DNS
If DNS is not disabled and not configured in the DHCP options, the service address of the subnet is used as the DNS server. The DNS requests to this address will be served by contrail-vrouter-agent. DNS configuration in the IPAM is explained here : https://github.com/Juniper/contrail-controller/wiki/DNS-and-IPAM.

To disable DNS, configure dhcp-option-list to have "0.0.0.0" against "domain-name-servers". In this case, the DHCP response from contrail-vrouter-agent will not contain the 'domain-name-servers' option.


## Disabling DHCP
If DHCP is disabled in the subnet, the broadcast DHCP requests will be flooded in the virtual-network. A DHCP server in the virtual network has to provide the DHCP service in this case. The virtual network may be configured in l2-only mode. L2 only mode is not a recommended mode of operation - the impact on other services needs to be understood completely.