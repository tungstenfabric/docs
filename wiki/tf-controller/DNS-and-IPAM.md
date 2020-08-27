
Four DNS modes are supported in the system, IPAM configuration can select the DNS mode required.

## 1. None
No DNS support for the VMs.

## 2. Default DNS server
DNS resolution for the VMs is done based on the name server configuration in the server infrastructure. When a VM gets a DHCP response, the subnet default gateway is configured as the DNS server for the VM. DNS requests that the VM sends to this default gateway are resolved via the (fabric) name servers configured on the respective compute nodes and the responses are sent back to the VM.

## 3. Tenant DNS server
Tenants can use their own DNS servers using this mode. A list of servers can be configured in the IPAM, which are then sent in the DHCP response to the VM as DNS server(s). DNS requests that the VM sends are routed as any other data packet based on the available routing information.

## 4. Virtual DNS server
In this mode, the system supports virtual DNS servers, providing DNS servers that resolve the DNS requests from the VMs. We can define multiple virtual domain name servers under each domain in the system. Each virtual domain name server is an authoritative server for the DNS domain configured. 

The following properties can be configured for each virtual DNS server:

1. Domain name (e.g. juniper.net)

2. Record order : when a name has multiple records matching, this determines the order in which the records are sent in the response. 
    * fixed - the records are sent in the order of creation
    * round-robin - the record order is cycled for each request to the record
    * random - the records are sent in random order

3. TTL in seconds : default time to live for the records in the domain

4. Next DNS server : indicates the next DNS server to send the request to when the request cannot be served in the context of the current virtual DNS server. 
    * When configured, the next DNS server can either be another virtual DNS server defined in the system or the IP address of an external DNS server which is reachable from the server infrastructure
    * Using the next DNS servers, we can configure a hierarchy of servers thru which the DNS requests are iterated
    * When a VDNS has no _Next DNS server_ configured, the DNS servers configured in _/etc/resolv.conf_ and used as forwarders (next DNS servers). In case the values in _/etc/resolv.conf_ are changed, a restart of contrail-dns is required for the change to take effect.

5. Flags to control the virtual DNS server behavior.
    * Enable or disable external access (from R2.21)
    * Enable or disable reverse resolution (from R2.21)
    * Enable or disable dynamic updates (whether VM spawning and delete should add and delete dynamic DNS records or not)
    
Each IPAM in the system can refer to one of the virtual DNS servers configured (when DNS mode is chosen as _Virtual DNS Server_). The virtual networks and virtual machines spawned will fall under the DNS domain of the virtual DNS server specified in the corresponding IPAM. The VMs will receive this domain in the DHCP DOMAIN-NAME option.

When a VM is spawned, an A record and a PTR record with the VM's name and IP address are added into the virtual DNS server associated with the corresponding virtual network's IPAM. DNS Records can also be added statically. A, CNAME, PTR and NS records are currently supported in the system. Each record takes the type (A / CNAME / PTR / NS), class (IN), name, data and TTL values.

**NS records** are used to delegate a sub-domain to another DNS server. The DNS server could be another virtual DNS server defined in the system or the IP address of an external DNS server reachable via the infrastructure. The sub-domain to be delegated (record name) and the name of the virtual DNS server or IP address of an external server (record data) can be configured in an NS record.

### External Access
The virtual DNS servers and records defined in them can be accessed from external DNS servers or clients by sending the DNS requests to any of the two control nodes. The external DNS servers can consider the sub-domains served by the virtual DNS servers as delegated zones and can add NS records in their respective servers pointing the delegated zones to the IP address of the control node. 

Similarly, virtual DNS servers can be configured to forward requests to external servers by using the "Next DNS Server" in the virtual DNS server configuration.

Here, it is assumed that any firewalls present between external servers and control nodes are appropriately configured to allow DNS traffic. 

In case the DNS domain names and subnets used across different projects / IPAMs are not unique, external access can be provided for only one such domain name (normal resolution), subnet (reverse resolution). This needs to be enhanced to configure which zone and which records can be externally accessed.

### Name resolution of link local services (R1.10 onwards)
Contrail provides access to services running on the fabric infrastructure to the virtual machine instances, through the link local service configuration. The instances can reach these services using the configured link local IP address and port. This link local address can be resolved from the virtual instance using the service name used in the link local configuration. The service_name or service_name.\<domain_name\> can be used to resolve the name. This resolution will work in either the default DNS mode or in virtual DNS mode (DNS mode configured in IPAM).

For example, when we have a "metadata" link local service configured, from the virtual instance metadata resolves to 169.254.169.254.

In case virtual DNS mode is configured, the domain configured for the virtual DNS server can also be appended to the name meant to be resolved. In the above example, if the virtual DNS domain name is juniper.net, then metadata.juniper.net also resolves to 169.245.169.254. Note that, metadata.\<any_other_domain_name\> will not resolve to this link local service.

### Floating IP name resolution (R1.10 onwards)
When running in the virtual DNS mode, floating IP addresses can be resolved in the virtual DNS server corresponding to the virtual network from which the floating IP is allocated.
Name resolution of the floating IP addresses will be possible while the floating IP address is associated to an active virtual machine instance.

The name to be used for the floating IP can be in one of the following formats
* IP address in dashed notation (example, 10-1-1-2)
* IP address in dashed notation appended with the tenant name (example, 10-1-1-2.public)
* Instance name (name used while starting the virtual instance, example vm1)
* Instance name appended with the tenant name (example, vm1.public)

The format to be used can be configured in the virtual DNS server configuration, with default being IP address in dashed notation appended with the tenant name.

### Configuration
Configuration can be done using the contrail webui as follows:

1. Create or delete virtual DNS servers here : Configure -> DNS -> Servers

2. Edit IPAMs DNS method and tenant DNS servers or virtual DNS servers here : Configure -> Networking -> IP Address Management

3. Add or delete static DNS records here : Configure -> DNS -> Records 
    * Remember that A and PTR records for VMs are added / deleted automatically in the corresponding virtual DNS servers

### Configure using scripts

* Create virtual DNS server

    `python /opt/contrail/utils/add_virtual_dns.py --name vdns1 --domain_name default-domain --dns_domain contrail.com --dyn_updates --record_order random --ttl 2000 --external_visible --reverse_resolution`

* Create virtual DNS server with next virtual dns server

    `python /opt/contrail/utils/add_virtual_dns.py --name vdns1 --domain_name default-domain --dns_domain contrail.com --dyn_updates --record_order random --ttl 2000 --next_vdns vdns2`

* Create dns record (A, PTR, CNAME, NS records can be created)

    `python /opt/contrail/utils/add_virtual_dns_record.py --name rec1 --vdns_fqname default-domain:vdns1 --rec_name host1 --rec_type A --rec_class IN --rec_data 1.2.3.4 --rec_ttl 1000`

* Associate an IPAM to a virtual dns server

    `python /opt/contrail/utils/associate_virtual_dns.py --ipam_fqname default-domain:admin:ipam1 --ipam_dns_method virtual-dns-server --vdns_fqname default-domain:vdns1`

* Change IPAM dns method to default

    `python /opt/contrail/utils/associate_virtual_dns.py --ipam_fqname default-domain:admin:ipam1 --ipam_dns_method default-dns-server`

* Disassociate IPAM from a virtual DNS server

    `python /opt/contrail/utils/disassociate_virtual_dns.py --ipam_fqname default-domain:admin:ipam1` 

    `python /opt/contrail/utils/disassociate_virtual_dns.py --ipam_fqname default-domain:admin:ipam1 --vdns_fqname default-domain:vdns1`

* Delete DNS record

    `python /opt/contrail/utils/del_virtual_dns_record.py --fq_name default-domain:vdns1:rec1`

* Delete virtual dns server

     `python /opt/contrail/utils/del_virtual_dns.py --fq_name default-domain:vdns1`

## Trouble Shooting

Operational virtual DNS servers and the configured DNS records on the control node can be seen at:

`http://<control node ip>:8092/Snh_ShowVirtualDnsServers?`

DNS query and response traces can be seen on the compute node at:

`http://<compute node ip>:8085/Snh_SandeshTraceRequest?x=DnsBind`

## Mapping to Neutron Resources and API

While the core network resource in Neutron maps to virtual-network in Contrail, network-ipam and virtual-DNS are resources introduced by Contrail. network-ipam is also defined as a Neutron extension and can be used via Neutron API as Horizon does it [here.](https://github.com/Juniper/contrail-horizon/blob/b79deaf9302673c01e1e6d01373b94808c15b2b0/openstack_dashboard/dashboards/project/networking/ipam/forms.py#L109). virtual-DNS will also be added as a Neutron extension in future.

virtual-DNS object has domain as parent and network-ipam has project as parent. So:

    virtual-network ==refers-to==> network-ipam ==refers-to==> virtual-DNS

The Contrail API server on first start creates a `default-network-ipam` object in the configuration database under the `default-domain` -> `default-project` hierarchy (referred further as global `default-network-ipam`). Using Contrail API hooks mechanism it is possible to also automatically create `default-network-ipam` object within a newly created project and `default-virtual-DNS` object within a newly created domain and link them to provide vDNS functionality.

Whenever a new virtual-network is created, the Contrail Neutron plugin will link it to the project specific `default-network-ipam` and if that doesn't exist it will link it to the global `default-network-ipam`.
