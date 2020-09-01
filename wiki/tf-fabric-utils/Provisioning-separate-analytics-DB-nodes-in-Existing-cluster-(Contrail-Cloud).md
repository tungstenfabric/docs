# Introduction
Steps to provision separate database node in a existing cluster with config and config DB roles in same set of nodes;
managing separate Cassandra database for config and analytics DB's in a existing contrail cluster and migrate analytics key-space to new database node(if required). This is achieved by,
 
1. Bringing up new set of servers for analytics and database role for analytics keyspace.
2. Using the existing database node for config keyspaces.

# Analytics DB Recommendations
    It is strongly recommended that cassandra commit logs and cassandra data be on different disks. Recommendation follows,
    Two separate local disks - one for commit logs and one for data; they can be set in testbed.py in the following parameters so the fab scripts will do the provisioning appropriately
        database_dir = '<cassandra-data-partition>/cassandra’
        ssd_data_dir = '<commit-logs-partition>/commit_logs_data'
        Example : 
            database_dir = '/var/lib/cassandra/mydata'
            ssd_data_dir = '/var/lib/cassandra/commit_logs_data'


# Assumptions
    s1, s2, s3 -- Existing nodes playing config/analytics/database roles
    s4, s5, s6 -- New nodes intended to play analytics role.
    s7, s8, s9 -- New nodes intended to play Analytics DB role

## 1. Installation
1.1 Install 6 new servers with base OS s4, s5, s6, s7, s8, s9

1.2 Populate testbed.py with new servers information s4, s5, s6, s7, s8, s9 in env.passwords only, Should not
modify roledefs at this step.

1.3 Install database and analytics packages in new servers

        fab install_pkg_node:<contrail-install-packages>,<user@s4>,<user@s5>,<user@s6>
        fab create_install_repo_node:<user@s4>,<user@s5>,<user@s6>,<user@s7>,<user@s8>,<user@s9>
        fab install_collector_node:<user@s4>,<user@s5>,<user@s6>
        fab install_database_node:True,<user@s7>,<user@s8>,<user@s9>

## 2. Backup analytics keyspace (OPTIONAL)
This step is required Only in case of migrating analytics keyspace to new database nodes

2.1 Populate testbed.py with following backup information

        backup_node="root@x.y.x.z"
        cassandra_backup="custom"
        backup_db_path = ["/root/"]
        skip_keyspace=["confid_db_uuid", "svc_monitor_keyspace", "to_bgp_keyspace", "DISCOVERY_SERVER",  "dm_keyspace", "useragent", "system_auth", "system_distributed", "system_traces",  "system"]  # Skip all existing keyspaces except ContrailAnalytics
        Populate ‘backup’ role in env.roledefs with backup_node 
        set root password for the backup_node in env.password

2.2 Backup the analytics keyspace from the old database nodes to new servers

        fab backup_cassandra_db

## 3. Provision Database for analytics DB

3.1 Populate testbed.py with following information,

        ssd_data_dir = '<commit-logs-partition>/commit_logs_data'
        database_dir = '<cassandra-data-partition>/cassandra’
        env.roledefs with new servers [<user@s4>,<user@s5>,<user@s6>] as 'collector' roles.
        env.roledefs with new servers [<user@s7>,<user@s8>,<user@s9>] as 'database' roles.

3.2 Provision database services in new servers

        fab setup_database_node:<user@s7>,<user@s8>,<user@s9>

3.3 Add new database nodes in the config DB

        fab prov_database_node:<user@s7>,<user@s8>,<user@s9>

## 4. Restore analytics keyspace (OPTIONAL)
This step is required Only in case of migrating analytics keyspace to new database nodes)

4.1 Rename the backed up data dir to new servers host names in the backup node

        BACKUP_NODE# cd /root
        BACKUP_NODE# mv OLD_DB1_HOSTNAME_DIR/ NEW_DB1_HOSTNAME_DIR/
        BACKUP_NODE# mv OLD_DB2_HOSTNAME_DIR/ NEW_DB2_HOSTNAME_DIR/
        BACKUP_NODE# mv OLD_DB3_HOSTNAME_DIR/ NEW_DB3_HOSTNAME_DIR/

4.2 Restore the analytics keyspace from the backup node to new servers

        fab restore_cassandra_db

## 5. Provision Analytics

5.1 Provision analytics services in new servers

        fab setup_collector_node:<user@s4>,<user@s5>,<user@s6>

5.2 Add new analytics nodes in the config DB

        fab prov_analytics_node:<user@s4>,<user@s5>,<user@s6>

## 6. Set haproxy collector backend server ip's to new nodes and restart haproxy service
This step required only if multiple collector nodes are in the cluster.

        fab fixup_restart_haproxy_in_collector

## 7. Stop/disable analytics services in old analytics  nodes

        fab -H <user@s1>,<user@s2>,<user@s3> -- "service supervisor-analytics stop"
        fab -H <user@s1>,<user@s2>,<user@s3> -- 'echo "manual" >> /etc/init/supervisor-analytics.override'

## 8. Stop/disable supervisor-database services in old database  nodes

        fab -H <user@s1>,<user@s2>,<user@s3> -- "service supervisor-database stop"
        fab -H <user@s1>,<user@s2>,<user@s3> -- 'echo "manual" >> /etc/init/supervisor-database.override'

## 9. Remove old nodes information from the config DB
9.1 Remove old database nodes from the config DB

        fab prov_database_node:<user@s1>,<user@s2>,<user@s3>,oper=del

9.2 Remove old analytics nodes from the config DB

        fab prov_analytics_node:<user@s1>,<user@s2>,<user@s3>,oper=del

9.3 Drop the 'ContrailAnalytics | ContrailAnalyticsCql' keyspace from the old database nodes

    For releases >= 3.0, the analytics key-space name is ContrailAnalyticsCql, older releases use the name
    ContrailAnalytics

        fab -H <user@s1> -- "echo 'drop keyspace \"ContrailAnalyticsCql\";' > /tmp/cassandra_commands_file"
        fab --warn-only -H <user@s1> -- "cqlsh <s1_control_ip> -f /tmp/cassandra_commands_file"
        fab -H <user@s1>,<user@s2>,<user@s3> -- "rm -rf /var/lib/cassandra/data/ContrailAnalyticsCql"

## 10. Restart contrail services
10.1 Restart contrail config services, including neutron service

        fab restart_cfgm

10.2 Restart contrail webui services

        fab restart_webui

# Conclusion
After executing the above steps, 

1. Config services will use the existing Cassandra provisioned in servers (s1, s2, s3)
and analytics service will use the Cassandra provisioned in the new servers( s7, s8, s9)

2. Config/Collector/Kafka services will use the zookeeper in servers (s1, s2, s3)