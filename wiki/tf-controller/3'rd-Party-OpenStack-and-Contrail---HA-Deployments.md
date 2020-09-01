Contrail and OpenStack both support variety of deployment options e.g. on bare-metal servers
inside VM, co-located or separate.  

Regardless of manner of deployment, high availability of OpenStack with respect to it being able to 
handle Service, Node and Link failures relies on the support provided by OpenStack provider.  
This document talks about the requirements around services that intersect both Contrail
and OpenStack in a typical deployment with the goal of achieving a highly available Contrail
installation.

1) High Availability of Contrail requires deploying multiple redundant instances of Contrail services 
behind a load-balancer. Virtual IP Addresses (VIP) would need to provisioned, one from internal
network for the services to communicate across nodes and one from management/external network for 
user-facing services (api-server, webui) to be reached from outside. Following section in testbed.py 
handles this this aspect and would need to filled appropriately.
env.ha = {
    'contrail_internal_vip'   : '172.16.41.100',      #Internal Virtual IP of the contrail HA Nodes.
    'contrail_external_vip'   : '10.88.125.75',       #External Virtual IP of the contrail HA Nodes.
}
  

2) Keystone service is provisioned during OpenStack install & provisioning. Contrail would need 
the following keystone related attributes specified as part of provisioning. 
env.keystone = {
    'keystone_ip'   : 'x.y.z.a',
    'auth_protocol' : 'http',                  #Default is http
    'auth_port'     : '35357',                 #Default is 35357
    'admin_token'   : '33c57636fbc2c5552fd2',  #admin_token in keystone.conf
    'admin_user'    : 'admin',                 #Default is admin
    'admin_password': 'contrail123',           #Default is contrail123
    'service_tenant': 'service',               #Default is service
    'admin_tenant'  : 'admin',                 #Default is admin
    'region_name'   : 'RegionOne',             #Default is RegionOne
    'insecure'      : 'True',                  #Default = False
    'manage_neutron': 'no',                    #Default = 'yes'
}

Note: The above specification is not explicitly required when Juniper OpenStack gets deployed as it 
takes care of installing both OpenStack and Contrail.   

3) Neutron installation & deployment is included in Contrail. The 
'manage_neutron' attribute above can be set as 'no' if third parties do not want Contrail to 
provision neutron, otherwise by default Contrail will provision neutron using the keystone 
attributes specified. 
Important Note : Neutron will also be behind VIP, so care should be taken to access neutron using the 
appropriate virtual IP address. 

4) Contrail HA requires that RabbitMQ be deployed in a cluster with ha-mode set to all 
to mirror queues across all the rabbit nodes. If OpenStack services from 3'rd parties are able to 
operate in this ha-mode of Rabbit, it would be possible to share the RabbitMQ instance. 
To keep things simple though, for now sharing is not allowed between OpenStack
provisioned outside of Juniper and Contrail services.
