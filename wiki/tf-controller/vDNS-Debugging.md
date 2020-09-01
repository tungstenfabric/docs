## Steps to debug virtual-DNS issues

If there is a specific host/VM not getting resolved,

* Find hypervisor on which requesting VM is running (via `nova show` or alternate)
* Access http://hypervisor-ip:8085/Snh_SandeshTraceRequest?x=DnsBind to get how vrouter-agent handled request for dns resolution
* Find hypervisor on which VM whose name is not resolving
* Access http://hypervisor-ip:8085/Snh_SandeshTraceRequest?x=XmppMessageTrace to see if vrouter-agent sent the VM details to the contrail-dns service, for example ([gist](https://gist.github.com/jsidhu/9e531b3e2f3300876354)):
  
> `2016-02-25 17:14:57.079 XmppTxStream: Sent xmpp message to: <CONTROLLER-IP> Port 8093 Size: 452 Packet: <?xml version="1.0"?> <iq type="set" from="<HYPERVISOR>/dns" to="network-dns@contrailsystems.com/dns-peer" id="10020"> <dns transid="10020"> <update> <virtual-dns>default-domain:project-name-virtual-DNS</virtual-dns> <zone>project- name.local</zone> <entry> <class>1</class>  <type>1</type> <name>vm-hostname</name> <data>192.168.1.10</data> <ttl>86400</ttl> <priority>0</priority> </entry> </update> </dns> </iq> $ controller/src/xmpp/xmpp_connection.cc 211`
  
* Access http://controller-ip:8092/Snh_SandeshTraceRequest?x=XmppMessageTrace to see if contrail-dns received message from vrouter-agent about VM presence
* Access http://controller-ip:8092/Snh_SandeshTraceRequest?x=DnsBind to see whether contrail-dns programmed bind entries correctly on every controller
* Access http://controller-ip:8092/Snh_ShowDnsConfig to see which records the controller is aware of for this virtual dns. The last column, installed, must be true which indicates the record was successfuly sent to bind/named
* grep <vm-name> in /etc/contrail/dns/* in every controller to check presence of entry. zone files are lazily created and thus do not indicate a problem if grep does not find anything. The opposite is true for jnl files, a positive match on the jnl file also does not indicate a that named is aware of such records.s


## How to dump the zone files' contents to see if the records are in bind

* contrail-rndc -c /etc/contrail/dns/contrail-rndc.conf sync - sync records from jnl to zones files

* contrail-rndc -c /etc/contrail/dns/contrail-rndc.conf dumpdb -zones

* The above command creates a file "named_dump.db" that has all records from all zones, which you can grep to look for records