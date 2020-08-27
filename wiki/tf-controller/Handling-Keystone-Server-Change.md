# Steps to reconfigure a cluster to use a new Keystone IP

The projects in API Server are synced from keystone, to configure a new keystone server would mean that all the existing Contrail data(projects/vns/vms/policy etc.) would be invalid and would be cleaned up. 

Delete all VMs on nova and any SIs

Stop all contrail services on nodes: <br>
service supervisor-config stop ; service supervisor-control stop ; service supervisor-analytics stop ; service supervisor-webui stop ; service supervisor-database stop ; service zookeeper stop ; service supervisor-support-service stop ; service supervisor-openstack stop ;service neutron-server stop

On the database nodes:<br>
Remove all contrail data : <br>

    cd /var/lib/cassandra 
    mkdir bkup
    mv * bkup
    
    cd /var/lib/zookeeper
    mkdir bkup
    mv version-2 bkup


On the Contrail-controller/openstack-services  nodes : <br>

Edit /etc/contrail/openstackrc with new keystone ip

Set the admin_token in the new server’s keystone.conf in these files  <br>
* In  /etc/contrail, these files : contrail-keystone-auth.conf, contrail-webui-userauth.js, ctrl-details, keystonerc, service.token
* In /etc/neutron/neutron.conf
* In /etc/neutron/plugins/opencontrail/ContrailPlugin.ini


In /etc/neutron/plugins/opencontrail/ContrailPlugin.ini , set auth_url 

In /etc/nova/nova.conf, set neutron_admin_auth_url 

In /etc/contrail/vnc_api_lib.ini, set AUTHN_SERVER 

In /etc/contrail/contrail-keystone-auth.conf, set memcache_servers to the newIP:port and auth_host to the new Keystone IP

In /etc/contrail/ctrl-details, set CONTROLLER to new keystone ip

In /etc/neutron/neutron.conf, In section, [keystone_authtoken], set auth_host to keystone IP

In /etc/haproxy/haproxy.conf, change ‘keystone-admin-backend’ section with new server IP


On the Webui node :<br>
In /etc/contrail/config.global.js, set ‘config.identityManager.ip’ <br>

On each glance node: <br>
Update /etc/glance/glance-api.conf, /etc/glance/glance-registry.conf:
set keystone_authtoken/auth_host, identity_uri <br>
You may also need to update swift_store_auth_address <br>

On compute nodes :<br> 
set /etc/contrail/ctrl-details with CONTROLLER and SERVICE_TOKEN <br>
Update /etc/contrail/openstackrc with keystone ip <br>
Update /etc/nova/nova.conf's neutron_admin_auth_url <br>
Update /etc/nova/nova.conf's keystone_authtoken/auth_host <br>

Do service zookeeper start on all database nodes <br>
Start all Contrail services (check contrail-status) <br>

From config node, add neutron service and endpoint on the new keystone IP (10.204.216.173 below)
setup-quantum-in-keystone --ks_server_ip     10.204.216.173 --quant_server_ip  10.204.216.184 --tenant           admin --user             admin --password         contrail123 --svc_password     contrail123 --svc_tenant_name  service --root_password    None --region_name RegionOne
On the new Keystone server, make sure that endpoints for nova, glance, cinder services are pointing to the right URLs. (keystone endpoint-list)


Update testbed.py to refer to the new keystone IP (env.keystone section) <br>
Run fab prov_control_bgp , prov_external_bgp, prov_metadata_services, prov_encap_type, 
or python provision_control.py --api_server_ip 10.204.216.58 --api_server_port 8082 --router_asn 64512  --admin_user admin --admin_password contrail123 --admin_tenant_name admin

For each compute node : <br>
Add each compute node to the Contrail Config(except TA/TSN)<br>
/opt/contrail/utils/provision_vrouter.py --host_name nodek3 --host_ip 10.204.216.223 --api_server_ip 10.204.216.184 --oper add --admin_user admin --admin_password contrail123 --admin_tenant_name admin --openstack_ip 10.204.216.184

For each TSN : <br>
Run provision_vrouter.py  with router_type set to tor-service-node <br>
Ex : python /opt/contrail/utils/provision_vrouter.py --host_name nodek3 --host_ip 10.204.216.223 --api_server_ip 10.204.216.184 --oper add --admin_user admin --admin_password contrail123 --admin_tenant_name admin --openstack_ip 10.204.216.184 --router_type tor-service-node

For each tor-agent : <br>
Run provision_vrouter.py  with router_type set to tor-agent <br>
python /opt/contrail/utils/provision_vrouter.py --host_name nodek3-1 --host_ip 10.204.216.223 --api_server_ip 10.204.216.184 --oper add --admin_user admin --admin_password contrail123 --admin_tenant_name admin                     --openstack_ip 10.204.216.184 --router_type tor-agent

Restart nova-compute on all compute nodes

On horizon node:<br>
In /etc/openstack_dashboard/local_settings.py, set OPENSTACK_HOST <br>
service apache2 restart <br>