# Introduction
Contrail upgrade procedure to support roll back to old contrail CONTROLLER in case of upgrade/post upgrade performance issues with the new CONTROLLER, also during upgrade the data traffic disruption will be minimal. 

This is achieved by provisioning new set of CONTROLLERs node with the new contrail release/build and then switching the XMPP connection of compute to new control node one by one.

Backup/restore of Cassandra is based on http://datascale.io/cloning-cassandra-clusters-fast-way/


## Keywords: 

* **CONTROLLER**  - config, database, collector, control and webui Nodes
* **OLD_CONTROLLER_VIP** – Virtual IP of the old controller nodes
* **NEW_CONTROLLER_VIP** – Virtual IP of the new controller nodes
* **NEW_FAB_NODE** – Node from which fab commands are triggered to provision new controllers (node that contains the new testbed.py)
* **OLD_FAB_NODE** – Existing node from which fab commands were triggered to provision the old Cluster
* **OLD_DATABASE<n> | OLD_DATABASE<n>_IP** – Nth old database node
* **NEW_DATABASE<n> | NEW_DATABASE<n>_IP** – Nth new database node 
* **OLD_CONFIG<n> | OLD_CONFIG<n>_IP** – Nth old config node
* **NEW_CONFIG<n> | NEW_CONFIG<n>_IP** – Nth new config node
* **OLD_CONTROL<n> | OLD_CONTROL<n>_IP**   – Nth old database node
* **NEW_CONTROL<n> | NEW_CONTROL<n>_IP** – Nth new config node
* **BACKUP_NODE** – Node in which the cassandra snapshots and zookeeper data dir is to be backed up


# Disk and partitioning recommendation:
It is strongly recommended that cassandra commit logs and cassandra data to be on different disks. Recommendation is the following,
- 2 separate local disks - one for commit logs and one for data those can be set in testbed.py as the following parameters so the fab scripts will do the provisioning appropriately
- database_dir = '<cassandra-data-partition>/cassandra’
- ssd_data_dir = '<commit-logs-partition>/commit_logs_data'

### Example:

    database_dir = '/var/lib/cassandra/mydata'
    ssd_data_dir = '/var/lib/cassandra/commit_logs_data'


# Contrail Upgrade Procedure
Steps to upgrade contrail cluster is explained below with fab commands and manual commands

## 1 Bring up new contrail CONTROLLERS
Following is the steps to bring up new controllers. 
Involves installing old database/config package and then upgrading them to newer version. 
This two step method is followed because in Contrail Release 3.00 cassandra is upgraded to a 2.1.9 version from 1.2.12(Which involves Cassandra SSTables upgrade and intermediate version (2.0.7) upgrade)


### 1.1 Install OLD contrail package in one of the new config node
Old version of contrail-install-packages needs to be installed in one of the config node to get the new provisioning code, using which the new controllers can be provisioned.
Copy old contrail-install-packages to one of the new config node
Execute from **NEW_FAB_NODE**

    dpkg -i contrail-install-packages
    /opt/contrail/contrail_packages/setup.sh


### 1.2 Create new testbed.py
New testbed.py should be created in the one of the new database node to provision the new contrail databases
Populate existing testbed.py in **OLD_FAB_NODE** with the parameters required for backup/restore of databases(cassandra/zookeeper), following are the parameters,

    backup_node="root@x.y.x.z"
    cassandra_backup="custom "
    backup_db_path = ["/root/ "]
    skip_keyspace=["DISCOVERY_SERVER",  "system_traces",  "system"]  # Add ContrailAnalytics|ContrailAnalyticsCql if it needs to be skipped during backup/restore 
    Populate ‘backup’ role in env.roledefs with backup_node and set root password for the backup_node in env.password
    Populate existing testbed.py with the parameters required for separate database and ssd dir locations

    ssd_data_dir = '<commit-logs-partition>/commit_logs_data'
    database_dir = '<cassandra-data-partition>/cassandra’

    OLD_FAB_NODE# scp /opt/contail/utils/fabfile/testbeds/testbed.py root@NEW_FAB_NODE#:/opt/contrail/utils/fabfile/testbeds/testbed.py
    NEW_FAB_NODE# vi  fabfile/testbeds/testbed.py 
    Replace the "cfgm/collector/database/control/webui” nodes with new node ip’s/passwords
    Set new contrail_internal_vip in the env.ha section
    Set new contrail_external_vip in case of multi interface setup


### 1.3 Install old release contrail packages in the new database and config nodes
From **NEW_FAB_NODE**

    fab install_pkg_node:<old contrail-install-pkg>,root@newcontroller1,root@newcontroller2,root@newcontroller3
    fab create_install_repo_node: root@newcontroller1,root@newcontroller2,root@newcontroller3
    fab install_database
    fab install_cfgm
    fab install_collector


### 1.4 Provision the new database and config nodes with old release
Execute from **NEW_FAB_NODE**

    fab setup_interface_node: root@<newcontroller1>, root@<newcontroller2>, root@<newcontroller3>
    # (Testing purpose: Following three steps needed only in vm cluster if interfaces.d files exists)
    fab all_command:"cat /etc/network/interfaces.d/eth0.cfg  >> /etc/network/interfaces" 
    fab all_command:"sed -i '/source*/d' /etc/network/interfaces"
    fab setup_interface,root@controller1,root@controller2,root@controller3

    fab setup_contrail_keepalived   #verify new vip
    fab setup_database
    fab verify_database

OPTIONAL(ONLY IF SPLIT-DB SETUP):  
 
    fab setup_database_node:<root@OLD_CFGM_NODE1>,<root@OLD_CFGM_NODE2>,<root@OLD_CFGM_NODE3>


### 1.5 Collect the schema and tokens from the old cassandra nodes 
Execute from **OLD_FAB_NODE**

    fab -R database -- mkdir -p /tmp/tokens/

    cqlsh <OLD_DATABASE_NODE_CTRL_IP1> -e 'DESCRIBE SCHEMA' > /tmp/tokens/schema.cql

    fab -H <root@OLD_DATABASE_NODE1> -- "nodetool ring | grep <OLD_DATABASE_NODE_CTRL_IP1> | awk '{print \$NF \",\"}' | xargs > /tmp/tokens/initial_tokens" 
     fab -H <root@OLD_DATABASE_NODE2> -- "nodetool ring | grep <OLD_DATABASE_NODE_CTRL_IP2> | awk '{print \$NF \",\"}' | xargs > /tmp/tokens/initial_tokens"
    fab -H <root@OLD_DATABASE_NODE3> -- "nodetool ring | grep <OLD_DATABASE_NODE_CTRL_IP3> | awk '{print \$NF \",\"}' | xargs > /tmp/tokens/initial_tokens"

    fab copydir:/tmp/tokens,src_host=<OLD_DATABASE_NODE1>,dst_host=<NEW_DATABASE_NODE1>
    fab copydir:/tmp/tokens,src_host=<OLD_DATABASE_NODE2>,dst_host=<NEW_DATABASE_NODE2>
    fab copydir:/tmp/tokens,src_host=<OLD_DATABASE_NODE3>,dst_host=<NEW_DATABASE_NODE3>

OPTIONAL(ONLY IF SPLIT-DB SETUP):  

    fab -R cfgm -- mkdir -p /tmp/tokens/

    cqlsh <OLD_CFGM_NODE_CTRL_IP1> -e 'DESCRIBE SCHEMA' > /tmp/tokens/schema.cql

    fab -H <root@OLD_CFGM_NODE1> -- "nodetool ring | grep <OLD_CFGM_NODE_CTRL_IP1> | awk '{print \$NF \",\"}' | xargs > /tmp/tokens/initial_tokens" 
     fab -H <root@OLD_CFGM_NODE2> -- "nodetool ring | grep <OLD_CFGM_NODE_CTRL_IP2> | awk '{print \$NF \",\"}' | xargs > /tmp/tokens/initial_tokens"
    fab -H <root@OLD_CFGM_NODE3> -- "nodetool ring | grep <OLD_CFGM_NODE_CTRL_IP3> | awk '{print \$NF \",\"}' | xargs > /tmp/tokens/initial_tokens"

    fab copydir:/tmp/tokens,src_host=<root@OLD_CFGM_NODE1>,dst_host=<root@NEW_CFGM_NODE1>
    fab copydir:/tmp/tokens,src_host=<root@OLD_CFGM_NODE2>,dst_host=<root@NEW_CFGM_NODE2>
    fab copydir:/tmp/tokens,src_host=<root@OLD_CFGM_NODE3>,dst_host=<root@NEW_CFGM_NODE3>


### 1.6 Update cassandra conf with the initial_tokens/bootstrap settings
Execute from **NEW_FAB_NODE**

    fab stop_database
    fab -R database -- "service contrail-database stop"
    fab -R database -- "rm -rf <database_dir>/system/*"   # 'database_dir' set in the testbed.py
    fab -R database -- 'echo "initial_token: $(cat /tmp/tokens/initial_tokens)" >> /etc/cassandra/cassandra.yaml'
    fab -R database -- "sudo sed -i '$ a\auto_bootstrap: false' /etc/cassandra/cassandra.yaml"
    fab -R database -- "sed -i '$ a\JVM_OPTS=\"\$JVM_OPTS -Dcassandra.load_ring_state=false\"' /etc/cassandra/cassandra-env.sh"
    fab start_database
    fab -R database -- "service contrail-database start"
    netstat -nalp | grep 9042 # make sure cqlsh port is open, wait for it
    cqlsh <NEW_DATABASE_NODE_CTRL_IP1> -f /tmp/tokens/schema.cql
    fab -R database -- "nodetool status" # Make sure all the cassandra nodes in the cluster displays (UN)-(Up/Normal)

OPTIONAL(ONLY IF SPLIT-DB SETUP):

    fab stop_cfgm_db
    fab -R cfgm -- "service contrail-database stop"
    fab -R cfgm -- "rm -rf <database_dir>/system/*"   # 'database_dir' set in the testbed.py
    fab -R cfgm -- 'echo "initial_token: $(cat /tmp/tokens/initial_tokens)" >> /etc/cassandra/cassandra.yaml'
    fab -R cfgm -- "sudo sed -i '$ a\auto_bootstrap: false' /etc/cassandra/cassandra.yaml"
    fab -R cfgm -- "sed -i '$ a\JVM_OPTS=\"\$JVM_OPTS -Dcassandra.load_ring_state=false\"' /etc/cassandra/cassandra-env.sh"
    fab start_cfgm_db
    fab -R cfgm -- "service contrail-database start"
    netstat -nalp | grep 9042 # make sure cqlsh port is open, wait for it
    cqlsh <NEW_CFGM_NODE_CTRL_1> -f /tmp/tokens/schema.cql
    fab -R cfgm -- "nodetool status" # Make sure all the cassandra nodes in the cluster displays (UN)-(Up/Normal)


### 1.7 Add the new control node as BGP routers in the old controllers
Execute from **OLD_CONFIG**

    cd /opt/contrail/utils
    python provision_control.py --api_server_ip <OLD_CONTROLLER_INTERNAL_VIP> --api_server_port 8082 --host_name <NEW_CONTROL1> --host_ip <NEW_CONTROL1_IP> --oper add --admin_user admin --admin_tenant_name admin --admin_password contrail123 --router_asn 64512
    # Verify in GUI that the addition is successful	
    python provision_control.py --api_server_ip <OLD_CONTROLLER_INTERNAL_VIP> --api_server_port 8082 --host_name <NEW_CONTROL2> --host_ip <NEW_CONTROL2_IP> --oper add --admin_user admin --admin_tenant_name admin --admin_password contrail123 --router_asn 64512
    python provision_control.py --api_server_ip <OLD_CONTROLLER_INTERNAL_VIP> --api_server_port 8082 --host_name <NEW_CONTROL3> --host_ip <NEW_CONTROL3_IP> --oper add --admin_user admin --admin_tenant_name admin --admin_password contrail123 --router_asn 64512


### 1.8 Stop config services in old config Nodes
Stop config services (supervisor-config and neutron-server) in the old config nodes to not let any new configuration during the next step of database snapshot/restore

Execute from **OLD_FAB_NODE**

    fab stop_cfgm 
    NOTE: No CRUD operations are possible after stopping config services.



## 2 Backup Databases
### 2.1 Backup zookeeper database
Execute from **OLD_FAB_NODE**

    fab backup_zookeeper_data

### 2.2 Snapshot/backup Cassandra Database
Execute from **OLD_FAB_NODE**

    fab backup_cassandra_db
    fab stop_database



## 3 Restore Databases
Following are the steps to restore the database (CASSANDRA) from old database to the new database.

###3.1 Move Backup Data To New Database Hostname Dirs
Execute from **BACKUP_NODE**

    cd /root
    mv OLD_DB1_HOSTNAME_DIR/ NEW_DB1_HOSTNAME_DIR/
    mv OLD_DB2_HOSTNAME_DIR/ NEW_DB2_HOSTNAME_DIR/
    mv OLD_DB3_HOSTNAME_DIR/ NEW_DB3_HOSTNAME_DIR/
    
OPTIONAL(ONLY IF SPLIT-DB SETUP):

    mv OLD_CFGM1_HOSTNAME_DIR/ NEW_CFGM1_HOSTNAME_DIR/
    mv OLD_CFGM2_HOSTNAME_DIR/ NEW_CFGM2_HOSTNAME_DIR/
    mv OLD_CFGM3_HOSTNAME_DIR/ NEW_CFGM3_HOSTNAME_DIR/


### 3.2 Restore Cassandra SNAPSHOTS to New database 
Execute from **NEW_FAB_NODE**

    #OPTIONAL(ONLY IF SPLIT-DB SETUP): fab stop_cfgm_db
    fab -R database -- "service contrail-database stop"
    fab -R database,cfgm -- 'mv /opt/contrail/utils/cass-db-restore.sh /opt/contrail/utils/cass-db-restore.sh.old'
    fab -R database,cfgm -- 'wget -O /opt/contrail/utils/cass-db-restore.sh https://raw.githubusercontent.com/Juniper/contrail-controller/R3.2/src/config/utils/cass-db-restore.sh'
    fab -R database,cfgm  -- 'chmod 755 /opt/contrail/utils/cass-db-restore.sh'
    fab restore_cassandra_db
    fab -R database -- "service contrail-database start"
    #OPTIONAL(ONLY IF SPLIT-DB SETUP): fab restart_cfgm_db


### 3.3 Verify restored cassandra database
Execute from **NEW_FAB_NODE**,

    fab verify_database
    # Verify Cassandra cluster using node tool status
    fab -R database -- "nodetool status"
    #OPTIONAL(ONLY IF SPLIT-DB SETUP): fab -R cfgm -- "nodetool status"


### 3.4 Provision the new config nodes with old release
Execute from **NEW_FAB_NODE**

    fab setup_rabbitmq_cluster
    fab setup_cfgm
    fab verify_cfgm

### 3.5 Restore Zookeeper DATA to new node
Execute from **NEW_FAB_NODE**

    fab restore_zookeeper_data
    fab restart_cfgm
    fab verify_cfgm

### 3.6 Provision the new collector nodes with old release
Execute from **NEW_FAB_NODE**

    fab setup_collector
    fab verify_collector
    fab -R cfgm -- "contrail-status"   # Make sure database/config/collector services are up

Execute from **NEW_CONFIG_NODE**,

    # Make sure that the objects created in old database are available in new cassandra after restore
    curl -u <adminUser>:<adminPassword> http://localhost:8095/virtual-networks | python -m json.tool
    curl -u <adminUser>:<adminPassword> http://localhost:8095/virtual-machines | python -m json.tool



## 4 Bring-up/Upgrade new contrail CONTROLLERS with New Release

### 4.1 Install new release of contrail packages in the new controller nodes
Execute from **NEW_FAB_NODE**

    fab install_pkg_node:<new contrail-install-pkg>, root@<new_controller1>, root@<new_controller2>, root@<new_controller3>
    fab create_install_repo_node: root@<new_controller1>, root@<new_controller2>, root@<new_controller3>
    fab upgrade_database:<from_rel>,<new contrail-install-pkg>
    fab verify_database
    # Make sure the objects created in old database are available in new after Cassandra upgrade
    curl -u <adminUser>:<adminPassword> http://localhost:8095/virtual-networks | python -m json.tool
    curl -u <adminUser>:<adminPassword> http://localhost:8095/virtual-machines | python -m json.tool
    fab upgrade_config:<from_rel>,<new contrail-install-pkg>
    fab restart_cfgm
    fab verify_cfgm
    fab install_control
    fab upgrade_collector:<from_rel>,<new contrail-install-pkg>
    fab verify_collector
    fab install_webui	

### 4.2 Provision New Controller nodes 
Execute from **NEW_FAB_NODE**

    fab setup_ha 
    fab fixup_restart_haproxy_in_collector 
    fab setup_control
    fab verify_control
    fab setup_webui	
    fab verify_webui
    fab prov_config
    fab prov_database
    fab prov_analytics
    fab prov_control_bgp
    fab prov_external_bgp

## 5 Direct Openstack to the new neutron/rabbit

### 5.1 Edit Heat.conf in openstack nodes to point new rabbit

    Set  rabbit_host and api-server in /etc/heat/heat.conf file of all openstack nodes to NEW_CONTROLLER_VIP (contrail_internal_vip)
    Set plugin_dirs in heat.conf
    plugin_dirs = /usr/lib/python2.7/dist-packages/vnc_api/gen/heat/resources,/usr/lib/python2.7/dist-packages/contrail_heat/resources
    Restart all heat services
    service heat-api restart; service heat-api-cfn restart; service heat-engine restart

### 5.2 Edit nova.conf in openstack nodes to point new neutron/rabbit

    Set  rabbit_host and neutron_url  in /etc/nova/nova.conf file of all openstack nodes to NEW_CONTROLLER_VIP (contrail_internal_vip)
    Restart all nova services
    service nova-api restart
    service nova-scheduler restart
    service nova-conductor restart

## 6 Upgrade Computes

### 6.1 Upgrade the compute nodes
Upgrade the compute nodes, one by one and then reboot the compute node. Make sure not to reboot the compute node after upgrade before changing the discovery ip in config files
Execute from **NEW_FAB_NODE**

    fab upgrade_compute_node:<old_from_rel>,<path_to_new_package>,root@compute1
	
### 6.2 Edit the compute node config files to point to new Discovery server

    Set “[DISCOVERY] server" to NEW_CONTROLLER_VIP in /etc/contrail/contrail-vrouter-agent.conf of all the compute nodes
    Set “DISCOVERY” to NEW_CONTROLLER_VIP   in /etc/contrail/contrail-vrouter-nodemgr.conf file of all the compute nodes

### 6.3 Edit the compute nodes nova config files to point to new Neutron/rabbit

    Set  rabbit_host and neutron_url  in /etc/nova/nova.conf file of all compute nodes to NEW_CONTROLLER_VIP
    service nova-compute restart

### 6.4 Switch the compute nodes to new CONTROLLER

Repeat steps in section 5.1, 5.2 and 5.3 and reboot compute nodes one by one to switch compute from OLD_CONTROLLER to NEW_CONTROLLER, so that the traffic in the other computes will not be disturbed and the traffic from/to the rebooted compute can be restored after reboot.

    reboot
    or
    service supervisor-vrouter stop;modprobe -r vrouter;modprobe vrouter;service supervisor-vrouter start;service nova-compute restart

## 7 Upgrade Openstack

### 7.1 Upgrade the openstack nodes
Execute from **NEW_FAB_NODE**

    fab upgrade_openstack:<old_from_rel>,/path/to/contrail/new/package

## 8 Remove old Controllers info from new controller

### 8.1 Remove the old control nodes information
Execute from **NEW_CONFIG**

    python provision_control.py --api_server_ip  <NEW_CONTROLLER_VIP> --api_server_port 8082 --host_name <OLD_CONTROL1> --host_ip <OLD_CONTROL1_IP> --oper del --admin_user admin --admin_tenant_name admin --admin_password contrail123 --router_asn 64512
    python provision_control.py --api_server_ip  <NEW_CONTROLLER_VIP> --api_server_port 8082 --host_name <OLD_CONTROL2> --host_ip <OLD_CONTROL2_IP> --oper del --admin_user admin --admin_tenant_name admin --admin_password contrail123 --router_asn 64512
    python provision_control.py --api_server_ip  <NEW_CONTROLLER_VIP> --api_server_port 8082 --host_name <OLD_CONTROL3> --host_ip <OLD_CONTROL3_IP> --oper del --admin_user admin --admin_tenant_name admin --admin_password contrail123 --router_asn 64512

### 8.2 Remove the old config, database, analytics nodes information
Execute from **NEW_CONFIG**

    python provision_config_node.py --api_server_ip <NEW_CONTROLLER_VIP> --host_name <OLD_CONFIG1> --host_ip <OLD_CONFIG1_IP> --oper del --admin_user admin --admin_tenant_name admin --admin_password contrail123
    python provision_config_node.py --api_server_ip <NEW_CONTROLLER_VIP> --host_name <OLD_CONFIG2> --host_ip <OLD_CONFIG2_IP> --oper del --admin_user admin --admin_tenant_name admin --admin_password contrail123
    python provision_config_node.py --api_server_ip <NEW_CONTROLLER_VIP> --host_name <OLD_CONFIG3> --host_ip <OLD_CONFIG3_IP> --oper del --admin_user admin --admin_tenant_name admin --admin_password contrail123
    python provision_database_node.py --api_server_ip <NEW_CONTROLLER_VIP> --host_name <OLD_DATABASE1> --host_ip  <OLD_DATABASE1_IP>--oper del --admin_user admin --admin_tenant_name admin --admin_password contrail123
    python provision_database_node.py --api_server_ip <NEW_CONTROLLER_VIP> --host_name <OLD_DATABASE2> --host_ip <OLD_DATABASE2_IP> --oper del --admin_user admin --admin_tenant_name admin --admin_password contrail123
    python provision_database_node.py --api_server_ip <NEW_CONTROLLER_VIP> --host_name <OLD_DATABASE3> --host_ip  <OLD_DATABASE3_IP> --oper del --admin_user admin --admin_tenant_name admin --admin_password contrail123
    python provision_analytics_node.py --api_server_ip <NEW_CONTROLLER_VIP> --host_name <OLD_ANALYTICS1> --host_ip <OLD_ANALYTICS1_IP> --oper del --admin_user admin --admin_tenant_name admin --admin_password contrail123
    python provision_analytics_node.py --api_server_ip <NEW_CONTROLLER_VIP> –host_name <OLD_ANALYTICS2>  --host_ip <OLD_ANALYTICS2_IP> --oper del --admin_user admin --admin_tenant_name admin --admin_password contrail123
    python provision_analytics_node.py --api_server_ip <NEW_CONTROLLER_VIP> --host_name <OLD_ANALYTICS3> --host_ip <OLD_ANALYTICS3_IP> --oper del --admin_user admin --admin_tenant_name admin --admin_password contrail123

## 9 Rolling back to old controller
In case of post upgrade issues, we can roll back to use the old version of contrail controllers, as we have detached it from the cluster without disturbing its configs and introduced new version of controllers in the above steps.

### 9.1 Start database and config services in old controller
Execute from **OLD_FAB_NODE**

    fab restart_database
    fab restart_cfgm

### 9.2 Add the old control nodes information
Execute from **NEW_CONFIG**

    python provision_control.py --api_server_ip  <NEW_CONTROLLER_VIP> --api_server_port 8082 --host_name <OLD_CONTROL1> --host_ip <OLD_CONTROL1_IP> --oper add --admin_user admin --admin_tenant_name admin --admin_password contrail123 --router_asn 64512
    python provision_control.py --api_server_ip  <NEW_CONTROLLER_VIP> --api_server_port 8082 --host_name <OLD_CONTROL2> --host_ip <OLD_CONTROL2_IP> --oper add --admin_user admin --admin_tenant_name admin --admin_password contrail123 --router_asn 64512
    python provision_control.py --api_server_ip  <NEW_CONTROLLER_VIP> --api_server_port 8082 --host_name <OLD_CONTROL3> --host_ip <OLD_CONTROL3_IP> --oper add --admin_user admin --admin_tenant_name admin --admin_password contrail123 --router_asn 64512

### 9.3 Edit nova.conf in openstack nodes to point old neutron/rabbit

    Set rabbit_host and neutron_url  in /etc/nova/nova.conf file of all openstack nodes to **OLD_CONTROLLER_VIP**
    Restart all nova services

### 9.4 Edit the compute node config files to point to old Discovery server

    Set “[DISCOVERY] server" to **OLD_CONTROLLER_VIP** in /etc/contrail/contrail-vrouter-agent.conf of all the compute nodes
    Set “DISCOVERY” to **OLD_CONTROLLER_VIP** in /etc/contrail/contrail-vrouter-nodemgr.conf file of all the compute nodes

### 9.5 Edit the compute nodes nova config files to point to OLD Neutron/rabbit

    Set  rabbit_host and neutron_url  in /etc/nova/nova.conf file of all compute nodes to **OLD_CONTROLLER_VIP**

### 9.6 Switch the compute nodes to **OLD CONTROLLER**

    Repeat steps in section 9.3 and 9.5 and restart compute services in compute nodes one by one to switch compute from **NEW_CONTROLLER** to **OLD_CONTROLLER**, so that the traffic in the other computes will not be disturbed and the traffic from/to the restarted compute can be restored after restart.
    service supervisor-vrouter restart; service nova-compute restart