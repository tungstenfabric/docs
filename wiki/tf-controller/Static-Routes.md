Routes can be statically configured in a virtual-network to direct traffic to go via a service virtual machine. The configured static routes are distributed to other nodes via BGP, thus directing traffic through required virtual machine.  These routes are configured on a virtual machine’s interface.

For example in a virtual-network with subnet 10.0.0.0/24, all the traffic
originating from a VM in virtual-network, destined to subnet 11.1.1.0/24 can be configured to go via a service appliance, using static route configured on a service VM interface.

     VM2 (10.1.1.252)  <------>  VM1 (10.1.1.251)  <------>  Service VM (10.1.1.253) 
      compute node 2              compute node 1               compute node 3

In the above diagram service VM interface has a static route configured to receive all traffic destined to subnet 11.1.1.0/24.  

Route table of virtual-network.

`Route/prefix	   NextHop`

`10.1.1.251/32	Compute Node1, Label A`

``10.1.1.252/32	Compute Node2, Label B``

``10.1.1.253/32	Compute Node3, Label C``

``11.1.1.0/24   Compute Node3, Label C``

## Configuration

### Configure using Contrail UI
Enable static route option in service template
* Choose service template image and type
* Enable static route option for interfaces of interest

Adding static routes on service instance interface
* Choose virtual network for interfaces
* Configure static routes for interface, in the drop down menu of static routes
* If auto scaling option is chosen, then traffic destined to static route subnet would be load balanced across service instances 

### Configure using Scripts
The below command adds a static route to forward traffic destined to 11.1.1.0/24 to be routed to the service VM interface of the VM with interface UUID '4cf8bc4d-21e6-4555-9fe3-eaec454e9c3e' into a route-table with name my_route_table2. 

On the cfgm node, 

`cd /opt/contrail/utils`

`python provision_static_route.py --prefix 11.1.1.0/24 --virtual_machine_interface_id '4cf8bc4d-21e6-4555-9fe3-eaec454e9c3e' --route_table_name my_route_table2 --api_server_ip 10.204.217.7 --api_server_port 8082 --oper add --user admin --password contrail123 --tenant_name admin`

You can add more than one route in the same route-table.

To delete a static route, 

`python provision_static_route.py --prefix 11.1.1.0/24 --virtual_machine_interface_id '4cf8bc4d-21e6-4555-9fe3-eaec454e9c3e' --route_table_name my_route_table2 --api_server_ip 10.204.217.7 --api_server_port 8082 --oper del --user admin --password contrail123 --tenant_name admin`

Note : 
The VM interface UUID can be obtained from Agent Introspect (http://\<compute\>:8085/Snh_ItfReq?name=) 

# Host Routes
Support is also added for host routes to be configured in the VM, via the classless static routes option in the DHCP server response sent to the VM. The routes to be sent in the DHCP response to the VM can be configured for each virtual network.

Host Routes can be added while creating the network in the “Create Network” page (configure -> Network -> Networks). Click on the “Host Routes” option and add the host routes that have to be sent to the virtual machines.