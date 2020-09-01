# Introduction
Manage separate Cassandra database for config and analytics DB's in a existing MOS/Contrail cluster. This is achieved by,
 
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
    s4, s5, s6 -- New nodes intended to play analytics and database roles.

## 1. Installation
1.1 Install 3 new servers with base OS s4, s5, s6

1.2 Populate testbed.py with new servers information s4, s5, s6 in env.passwords only, Should not
modify roledefs at this step

1.3 Copy this file from one of the Contrail nodes to the database nodes that were newly created

        scp /etc/apt/preferences.d/contrail-pin-100 <user@s4/s5/s6>:/etc/apt/preferences.d/

1.4 Install fabric on both Contrail & new DB nodes,

        apt-get install fabric contrail-fabric-utils (Contrail nodes)
        apt-get update && apt-get install fabric (New DB nodes)

1.5 Install database and analytics packages in new servers

        fab install_pkg_node:<contrail-install-packages>,<user@s4>,<user@s5>,<user@s6>
        fab create_install_repo_node:<user@s4>,<user@s5>,<user@s6>
        fab install_database_node:True,<user@s4>,<user@s5>,<user@s6>
        fab install_collector_node:<user@s4>,<user@s5>,<user@s6>

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
        env.roledefs with new servers [<user@s4>,<user@s5>,<user@s6>] as 'database' roles.
        env.roledefs with new servers [<user@s4>,<user@s5>,<user@s6>] as 'collector' roles.

3.2 Provision database services in new servers

        fab setup_database_node:<user@s4>,<user@s5>,<user@s6>

3.3 Add new database nodes in the config DB

        python provision_database_node.py --api_server_ip <api-server-ip> --host_name <new_db_name> --host_ip <new_db_ip> --oper add --admin_user admin --admin_password admin --admin_tenant_name admin

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

        python provision_analytics_node.py --api_server_ip <api-server-ip> --host_name <new_db_name> --host_ip <new_db_ip> --oper add --admin_user admin --admin_password admin --admin_tenant_name admin

## 6. Set haproxy collector backend server ip's to new nodes and restart haproxy service
This step required only if multiple collector nodes are in the cluster.

        fab fixup_restart_haproxy_in_collector

## 7. Stop analytics services in old analytics  nodes

        fab -H <user@s1>,<user@s2>,<user@s3> -- "service supervisor-analytics stop"

## 8. Remove old nodes information from the config DB
8.1 Remove old database nodes from the config DB

        python provision_database_node.py --api_server_ip <api-server-ip> --host_name <old_db_name> --host_ip <old_db_ip> --oper del --admin_user admin --admin_password admin --admin_tenant_name admin

8.2 Remove old analytics nodes from the config DB

        python provision_analytics_node.py --api_server_ip <api-server-ip> --host_name <old_db_name> --host_ip <old_db_ip> --oper del --admin_user admin --admin_password admin --admin_tenant_name admin

8.3 Drop the 'ContrailAnalytics | ContrailAnalyticsCql' keyspace from the old database nodes

    For releases >= 3.0, the analytics key-space name is ContrailAnalyticsCql, older releases use the name
    ContrailAnalytics

        fab -H <user@s1> -- "echo 'drop keyspace \"ContrailAnalyticsCql\";' > /tmp/cassandra_commands_file"
        fab -H <user@s1> -- "cqlsh <s1_control_ip> 9160 -f /tmp/cassandra_commands_file"
        fab -H <user@s1>,<user@s2>,<user@s3> -- "rm -rf /var/lib/cassandra/data/ContrailAnalyticsCql"

## 9. Restart contrail services
9.1 Restart contrail config services, including neutron service

        fab restart_cfgm

9.2 Restart contrail webui services

        fab restart_webui

# Conclusion
After executing the above steps, the config services will use the existing Cassandra provisioned in servers (s1, s2, s3)
and analytics service will use the Cassandra provisioned in the new servers( s4, s5, s6)