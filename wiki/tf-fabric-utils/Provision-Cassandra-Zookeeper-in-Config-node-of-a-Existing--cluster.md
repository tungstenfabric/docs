# Introduction
Steps to provision cassandra/zookeeper in config node of an existing cluster with config and database roles in different set of nodes.

Managing separate Cassandra database for config and analytics DB's in a existing contrail cluster by migrating config key-spaces and zookeeper data to config node. This is achieved by,
 
1. Provisioning Cassandra/zookeeper in config node for config key-spaces and migrating data to config node.
2. Using the existing database node for analytics key-spaces.
3. Stopping zookeeper in database nodes.

# Assumptions
    s1, s2, s3 -- Nodes playing config roles
    s4, s5, s6 -- Nodes playing analytics and database roles.

## 1. Installation
1.1 Install database packages in config servers

        fab -R cfgm -- "apt-get install contrail-openstack-database"

## 2. Backup config key-space's and zookeeper.

2.1 Populate testbed.py with following backup information

        backup_node="root@x.y.x.z"
        cassandra_backup="custom"
        backup_db_path = ["/root/"]
        skip_keyspace=["ContrailAnalyticsCql", "useragent", "system_auth", "system_distributed", "system_traces",  "system"]  # Skip all existing key-space's except  confid_db_uuid,svc_monitor_keyspace,to_bgp_keyspace,DISCOVERY_SERVER,dm_keyspace 
        Populate ‘backup’ role in env.roledefs with backup_node 
        set root password for the backup_node in env.password

2.2 Backup the config key-spaces

        fab backup_cassandra_db

2.3 Backup the zookeeper

        fab backup_zookeeper_data

## 3. Provision Database for analytics DB

3.1 Populate testbed.py with following information,

        ssd_data_dir = '<commit-logs-partition>/commit_logs_data'
        database_dir = '<cassandra-data-partition>/cassandra’

3.2 Provision database services in config servers

        fab setup_database_node:<user@s1>,<user@s2>,<user@s3>

## 4. Restore config key-spaces

4.1 Rename the backed up data dir to config servers host names in the backup node

        BACKUP_NODE# cd /root
        BACKUP_NODE# mv s4_HOSTNAME_DIR/ s1_HOSTNAME_DIR/
        BACKUP_NODE# mv s5_HOSTNAME_DIR/ s2_HOSTNAME_DIR/
        BACKUP_NODE# mv s6_HOSTNAME_DIR/ s3_HOSTNAME_DIR/

4.2 Restore the config key-space's from the backup node to config servers

        fab restore_cassandra_db

4.3 Restore the zookeeper data from the backup node to config servers

        fab restore_zookeeper_data

## 5. Direct analytics services to point to zookeeper services in config servers

        fab -R collector -- "openstack-config --set /etc/contrail/contrail-alarm-gen.conf DEFAULTS zk_list <s1>:2181 <s2>:2181 <s3>:2181"
        fab -R collector -- "openstack-config --set /etc/contrail/contrail-collector.conf DEFAULT zookeeper_server_list <s1>:2181,<s2>:2181,<s3>:2181"
        fab -R collector -- "openstack-config --set /etc/contrail/contrail-snmp-collector.conf DEFAULTS zookeeper <s1>:2181,<s2>:2181,<s3>:2181"
        fab -R collector -- "openstack-config --set /etc/contrail/contrail-topology.conf DEFAULTS zookeeper <s1>:2181,<s2>:2181,<s3>:2181"

## 6. Direct kafka service to point to zookeeper services in config servers

        fab -R database -- "sed -i 's/zookeeper.connect=.*/zookeeper.connect=<s1>:2181,<s2>:2181,<s3>:2181/g'  /usr/share/kafka/config/server.properties"

## 7. Direct config services to point to zookeeper services in config servers

        fab -R cfgm -- "openstack-config --set /etc/contrail/contrail-api.conf DEFAULTS zk_server_ip <s1>:2181,<s2>:2181,<s3>:2181"

        fab -R cfgm -- "openstack-config --set /etc/contrail/contrail-device-manager.conf DEFAULTS zk_server_ip <s1>:2181,<s2>:2181,<s3>:2181"
        fab -R cfgm -- "openstack-config --set /etc/contrail/contrail-schema.conf DEFAULTS zk_server_ip <s1>:2181,<s2>:2181,<s3>:2181"
        fab -R cfgm -- "openstack-config --set /etc/contrail/contrail-svc-monitor.conf DEFAULTS zk_server_ip <s1>:2181,<s2>:2181,<s3>:2181"

## 8. Stop/disable zookeeper services in database servers

        fab -H <user@s4>,<user@s5>,<user@s6> -- "service zookeeper stop"
        fab -H <user@s4>,<user@s5>,<user@s6> -- 'echo "manual" > /etc/init/zookeeper.override'

## 9. Restart kafka services

        fab -R database -- "service kafka restart"

## 10. Restart contrail services, including neutron service

        fab restart_cfgm

## 11. Restart contrail analytics services

        fab restart_collector


# Conclusion
After executing the above steps, 

1. Config services will use the new Cassandra provisioned in servers (s1, s2, s3)
and analytics service will use the existing Cassandra in the new servers( s4, s5, s6).

2. Config/collector/kafka services will use the new zookeeper provisioned in servers (s1, s2, s3)