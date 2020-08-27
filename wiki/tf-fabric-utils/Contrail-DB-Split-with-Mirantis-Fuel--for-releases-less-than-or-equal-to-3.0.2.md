# Introduction
The recommended best practice for production deployment of Contrail is to separate database for Contrail Config and Contrail Analytics. 

The Contrail Analytics along with Analytics DB would be installed on a separate node (physical host or VM) while Contrail Config along with Config DB would be a separate node. 

Below are the recommended roles: 

    Contrail Controller: Contrail Config, Config DB (Config Cassandra and zookeeper), Control, WebUI
    Contrail Analytics: Contrail Analytics, Analytics DB (Analytics Cassandra and kafka) 

## Mirantis Fuel plugin roles
At present, Fuel has the following roles for Contrail: 

    contrail-config 
    contrail-control
    contrail-db 

For splitting up Cassandra for Config and Analytics, we are suggesting to have following roles in Fuel plugin: 

    contrail-config: This role is contrail config along with config DB (Cassandra and zookeeper) 
    contrail-control: Contrail control node 
    contrail-analytics: This would be a new role. This is contrail analytics node.
    contrail-db: This role would now refer to only Contrail Analytics DB. 

## Fab based deployment steps:

Below are the provisioning steps based on current fab scripts (available in 3.0.2-51) to setup the above-described deployment: 

### 1. Populate the testbed.py such that same host(s) have analytics and database role

    #Role definition of the hosts.
    env.roledefs = {
        'all': [host1, host2, host3, host4, host5, host6, host7, host8, host9],
        'cfgm': [host1, host2, host3],
        'openstack': [host1, host2, host3],
        'control': [host1, host2, host3],
        'compute': [host8, host9],
        'collector': [host4, host5, host6],
        'webui': [host1, host2, host3],
        'database': [host4, host5, host6],
        'build': [host_build],
        #'storage-master': [host1],
        #'storage-compute': [host4, host5, host6, host7, host8, host9, host10],
        #'rally': [host11], # Optional, to enable/setup rally, it can be a seprate node from contrail cluster
        # 'vgw': [host4, host5], # Optional, Only to enable VGW. Only compute can support vgw
        # 'tsn': [host1], # Optional, Only to enable TSN. Only compute can support TSN
        # 'toragent': [host1], Optional, Only to enable Tor Agent. Only compute can
        # support Tor Agent
        #   'backup':[backup_node],  # only if the backup_node is defined
    }

### 2. Install contrail packages in all the nodes

    fab install_pkg_all:<path/to/contrail-install-packages>
    fab install_contrail 

### 3. Edit the testbed.py such that host having config role(s) also have database roles 

    #Role definition of the hosts.
        env.roledefs = {
        'all': [host1, host2, host3, host4, host5, host6, host7, host8, host9],
        'cfgm': [host1, host2, host3],
        'openstack': [host1, host2, host3],
        'control': [host1, host2, host3],
        'compute': [host8, host9],
        'collector': [host4, host5, host6],
        'webui': [host1, host2, host3],
        'database': [host1, host2, host3],
        'build': [host_build],
        #'storage-master': [host1],
        #'storage-compute': [host4, host5, host6, host7, host8, host9, host10],
        #'rally': [host11], # Optional, to enable/setup rally, it can be a seprate node from contrail cluster
        # 'vgw': [host4, host5], # Optional, Only to enable VGW. Only compute can support vgw
        # 'tsn': [host1], # Optional, Only to enable TSN. Only compute can support TSN
        # 'toragent': [host1], Optional, Only to enable Tor Agent. Only compute can
        # support Tor Agent
        #   'backup':[backup_node],  # only if the backup_node is defined
    }

### 4. Install database package in config node and Provision the cluster with config node as DB node.   

    fab install_database  
    fab setup_database  
    fab verify_database 
    fab setup_common
    fab setup_ha
    fab setup_rabbitmq_cluster
    fab increase_limits
    fab setup_orchestrator
    fab setup_cfgm
    fab verify_cfgm 
    fab setup_control
    fab verify_control 

### 5. Change the testbed.py back to as shown in #1 

    fab setup_database
    fab -R database -- "sed -i 's/zookeeper.connect=.*/zookeeper.connect=<host1>:2181,<host2>:2181,<host3>:2181/g'  /usr/share/kafka/config/server.properties"
    fab -R database -- "service zookeeper stop"
    fab -R database -- 'echo "manual" > /etc/init/zookeeper.override'
    fab restart_database
    fab verify_database
    fab setup_collector
    fab -R collector -- "openstack-config --set /etc/contrail/contrail-alarm-gen.conf DEFAULTS zk_list <host1>:2181 <host2>:2181 <host3>:2181"
    fab -R collector -- "openstack-config --set /etc/contrail/contrail-collector.conf DEFAULT zookeeper_server_list <host1>:2181,<host2>:2181,<host3>:2181"
    fab -R collector -- "openstack-config --set /etc/contrail/contrail-snmp-collector.conf DEFAULTS zookeeper <host1>:2181,<host2>:2181,<host3>:2181"
    fab -R collector -- "openstack-config --set /etc/contrail/contrail-topology.conf DEFAULTS zookeeper <host1>:2181,<host2>:2181,<host3>:2181"
    fab restart_collector
    fab setup_webui
    fab verify_webui 
    fab setup_vrouter
    fab prov_config
    fab prov_database
    fab prov_analytics
    fab prov_control_bgp
    fab prov_external_bgp
    fab prov_metadata_services
    fab prov_encap_type
    fab setup_remote_syslog 
    fab increase_vrouter_limits
    #if there is openstack internal VIP,  do fab setup_cluster_monitors
    fab compute_reboot
    fab verify_compute
    fab setup_nova_aggregate
