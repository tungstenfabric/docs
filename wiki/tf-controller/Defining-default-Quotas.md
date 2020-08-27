Default Quota values can be configured in the VNC API server configuration file (/etc/contrail/api_server.conf) under the section [QUOTA]

Below is the mapping between the neutron quota names and the OpenContrail quota names  

quota_network : virtual-network  
quota_subnet : subnet  
quota_floatingip : floating-ip  
quota_route_table : logical-router  
quota_security_group : security-group  
quota_security_group_rule': security-group-rule  
quota_port : virtual-machine-interface  
  
Below is an example in api_server.conf file  
[QUOTA]  
subnet=50  
virtual-network=30  
floating-ip=10  
logical-router=20  
security-group=50  
security-group_rule=50  
virtual-machine-interface=30  
  
The security-group 'default' will also be considered while checking the quota limits. Any security-group-rules added by default to a SG will also be considered while checking the quota limits