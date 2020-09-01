Neutron API support
-------------------


The Opencontrail Neutron plugin provides an implementation for the following core resources:
   
* Network
* Subnet
* Port
    
It also implements the following standard/upstreamed Neutron extensions:

* Security Group
* Router/Floating IP/Source-NAT(router-gateway-set)
* Per-tenant Quota
* Allowed Address Pair
* Load Balancer As a Service

The following Contrail specific extensions are implemented:

* Network Ipam
* Network Policy
* VPC/Route Table
* Floating IP Pools

For more information about using OpenStack Networking API v2.0 (Neutron), refer to [Official document ](http://docs.openstack.org/api/openstack-network/2.0/content/). and the [Neutron Wiki](http://wiki.openstack.org/wiki/Neutron).

Note that the plugin does not implement native Bulk/Pagination/Sort operations and relies on emulation provided by neutron common code. 

## Known Bugs in R1.10 ##

* \#1352281 Status of resource doesn't reflect if resource is being actually used (eg. port status is ACTIVE upon creation). 
* \#1349448 When gateway of subnet is in middle of subnet's cidr, the allocation pool attribute doesn't report 2 list elements (start-gw, gw+1,end). However, the gateway-ip will not be allocated to any VM port
* \#1352822,#1352281 Disabling admin state of resource is not supported on all resources.
* \#1323204 Doing a interface-detach shuts down the VM
* \#1351979 Updating allowed_address_pairs without any value or with action clear throws internal server
* \#1349375 if allocation-pool range is outside of cidr, internal server error is seen
* \#1352148 allowed_address_pair MAC Address is not used in vrouter
* \#1352278 Disabling a subnet gateway is not supported
* \#1355560 Multiple IP Addresses for a port is not supported
* \#1358212 Update on a port with fixed_ips attribute (subnet_id, ip_address) failed with internal server error
* \#1352657 Quota limits of max_dns_nameservers, max_subnet_host_routes, max_fixed_ips_per_port, max_routes are not supported
* \#1354792 quota-list showing quota for "default-project" also
* \#1352221 For a port, port-binding extended attributes are not supported
* \#1364740 For SG, ICMP rule type and code is not respected
* \#1350460 neutron l3 router, extra route not supported
* \#1365322 Assigning floating IP on VMs behind SNAT is not supported.

Current list of known bugs in Contrail neutron API support can be found [here](http://bit.ly/1lHXzAf).
## Caveats ##

External Gateway on a router is only of beta-quality in R1.10

In the Contrail architecture these are the known incompatibilities with Neutron API.

* Filtering based on any arbitrary key in resource is not supported - only by id, name and tenant_id are supported
* To use a Floating IP it is not necessary to connect the 'public' subnet and 'private' subnet to a Neutron Router. The fact that a 'public' network is marked 'router:external' is sufficient for a Floating IP to be created/associated and packet forwarding to it will work.
* For networks with multiple subnets, when one of the subnets in network is attached to a router, all subnets on the network will be treated as having been attached to the router. 
* The default values for quotas are sourced from /etc/contrail/contrail-api.conf instead of /etc/neutron/neutron.conf


## Tests ##

Refer to 

https://github.com/Juniper/contrail-test/wiki/Running-Neutron-API-Tests

https://github.com/Juniper/contrail-test/wiki/Running-Neutron-Tempest-Tests