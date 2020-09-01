In a 2n+1 Contrail controller HA setup, a single node failure can be accomodated. 

For instance, a disk on one of the nodes may be bad. In such scenarios, you could re-install and bringup the same node( with a new disk, ofcourse) with the below steps 
The controller here does role of config, database, analytics/collector, webui, control-node

* Install contrail-install-packages package and run /opt/contrail/contrail_packages/setup.sh
* fab upgrade_kernel_node:"host_string" , and reboot the node
* fab setup_interface_node:"host_string"
* fab install_database_node:False,"host_string"
* fab install_cfgm_node:"host_string"
* fab install_collector_node:host_string
* fab install_control_node:host_string
* fab install_webui_node:host_string
* fab setup_common_node:host_string
* fab setup_contrail_keepalived
* fab setup_rabbitmq_cluster
* fab increase_limits_node:"host_string"
* fab setup_database_node:"host_string"
* fab setup_cfgm_node:"host_string"
* fab setup_control_node:"host_string"
* fab setup_collector_node:"host_string"
* fab setup_webui_node:"host_string"

host_string above is of the form 'root@x.y.z.a'
