# Introduction
This procedure can be used to backup contrail database (except the ContrailAnalytics keyspace) and restore to same version of Contrail.The below procedure can be used to backup/restore contrail database except the Contrail Analytics keyspace.

# Recommendations and Assumptions
It is strongly recommended that cassandra commit logs and cassandra data to be on different disks. Recommendation is the following,
   - Two separate local disks - one for commit logs and one for data
   - those can be set in testbed.py as the following parameters so the fab scripts will do the provisioning appropriately

            database_dir = '<cassandra-data-partition>/cassandra’
            ssd_data_dir = '<commit-logs-partition>/commit_logs_data'
            Example : 
            database_dir = '/var/lib/cassandra/mydata'
            ssd_data_dir = '/var/lib/cassandra/commit_logs_data'
        The below steps are assuming that database_dir and ssd_data_dir have the values as mentioned in the example. 

 The following nomenclature is used in this procedure:

        FAB_NODE : The node from where the fabric commands are run.
        BACKUP_SERVER : Server where the backed up data is stored
        DATABASE1, DATABASE2, DATABASE3 : Contrail database node 1,2,3.
        DATABASE4, DATABASE5, DATABASE6 : New Config Database node 4,5,6. 

## 1.  Drop the 'ContrailAnalytics | ContrailAnalyticsCql' keyspace from the Database nodes (OPTIONAL)

    For releases >= 3.0, the analytics key-space name is ContrailAnalyticsCql, older releases use the name
    ContrailAnalytics

        fab stop_collector
        fab -H <user@s1> -- "echo 'drop keyspace \"ContrailAnalyticsCql\";' > /tmp/cassandra_commands_file"
        fab -H <user@s1> -- "cqlsh <s1_control_ip> 9160 -f /tmp/cassandra_commands_file"
        fab -H <user@s1>,<user@s2>,<user@s3> -- "rm -rf /var/lib/cassandra/data/ContrailAnalyticsCql"

## 2. Backup Config Database

2.1   Backup Zookeeper data

       FAB_NODE# fab stop_cfgm

       On BACKUP_SERVER create:
           mkdir -p <backup_path>/db1/var/lib/zookeeper/
           mkdir -p <backup_path>/db2/var/lib/zookeeper/
           mkdir -p <backup_path>/db3/var/lib/zookeeper/

       DATABASE1# scp -r /var/lib/zookeeper/* root@<BACKUP_SERVER>:<backup_path>/db1/var/lib/zookeeper/
       DATABASE2# scp -r /var/lib/zookeeper/* root@<BACKUP_SERVER>:<backup_path>/db2/var/lib/zookeeper/
       DATABASE3# scp -r /var/lib/zookeeper/* root@<BACKUP_SERVER>:<backup_path>/db3/var/lib/zookeeper/

2.2	Create snapshot of the database:

       Create database snapshot on all the database nodes using the following commands.

       FAB_NODE# fab -R database -- "nodetool -h localhost -p 7199 snapshot config_db_uuid"
       FAB_NODE# fab -R database -- "nodetool -h localhost -p 7199 snapshot to_bgp_keyspace"
       FAB_NODE# fab -R database -- "nodetool -h localhost -p 7199 snapshot svc_monitor_keyspace"

2.3	Copy the snapshots to the Backup Server

2.3.1	Copy config_db_uuid snapshot to the backup server

         DATABASE1# cd /var/lib/cassandra/data/config_db_uuid/; for dir in $(ls); do if [ -d "$dir/snapshots/" ]; then echo /var/lib/cassandra/data/config_db_uuid/$dir/snapshots/$(ls -t $dir/snapshots/ | head -n1)/; fi; done

         On BACKUP_SERVER create:
            mkdir -p <backup_path>/db1/<of all the directories listed during above step>

         DATABASE1# cd /var/lib/cassandra/data/config_db_uuid/; for dir in $(ls); do if [ -d "$dir/snapshots/" ]; then  snapshot_dir=$dir/snapshots/$(ls -t $dir/snapshots/ | head -n1); scp -r $snapshot_dir/* root@<BACKUP_SERVER>:<backup_path>/db1/var/lib/cassandra/data/config_db_uuid/$snapshot_dir/; fi; done

         DATABASE2# cd /var/lib/cassandra/data/config_db_uuid/; for dir in $(ls); do if [ -d "$dir/snapshots/" ]; then echo /var/lib/cassandra/data/config_db_uuid/$dir/snapshots/$(ls -t $dir/snapshots/ | head -n1)/; fi; done

         On BACKUP_SERVER create:
              mkdir -p <backup_path>/db2/<of all the directories listed during above step>

         DATABASE2# cd /var/lib/cassandra/data/config_db_uuid/; for dir in $(ls); do if [ -d "$dir/snapshots/" ]; then snapshot_dir=$dir/snapshots/$(ls -t $dir/snapshots/ | head -n1); scp -r $snapshot_dir/* root@<BACKUP_SERVER>:<backup_path>/db2/var/lib/cassandra/data/config_db_uuid/$snapshot_dir/; fi; done

         DATABASE3# cd /var/lib/cassandra/data/config_db_uuid/; for dir in $(ls); do if [ -d "$dir/snapshots/" ]; then echo /var/lib/cassandra/data/config_db_uuid/$dir/snapshots/$(ls -t $dir/snapshots/ | head -n1)/; fi; done

         On BACKUP_SERVER create:
               mkdir -p <backup_path>/db3/<of all the directories listed during above step>

         DATABASE3# cd /var/lib/cassandra/data/config_db_uuid/; for dir in $(ls); do if [ -d "$dir/snapshots/" ]; then snapshot_dir=$dir/snapshots/$(ls -t $dir/snapshots/ | head -n1); scp -r $snapshot_dir/* root@<BACKUP_SERVER>:<backup_path>/db3/var/lib/cassandra/data/config_db_uuid/$snapshot_dir/; fi; done

2.3.2	Copy to_bgp_keyspace snapshot to the backup server

          DATABASE1# cd /var/lib/cassandra/data/to_bgp_keyspace/; for dir in $(ls); do if [ -d "$dir/snapshots/" ]; then echo /var/lib/cassandra/data/to_bgp_keyspace/$dir/snapshots/$(ls -t $dir/snapshots/ | head -n1)/; fi; done

          On BACKUP_SERVER create:
                 mkdir -p <backup_path>/db1/<of all the directories listed during above step>

          DATABASE1# cd /var/lib/cassandra/data/to_bgp_keyspace/; for dir in $(ls); do if [ -d "$dir/snapshots/" ]; then  snapshot_dir=$dir/snapshots/$(ls -t $dir/snapshots/ | head -n1); scp -r $snapshot_dir/* root@<BACKUP_SERVER>:<backup_path>/db1/var/lib/cassandra/data/to_bgp_keyspace/$snapshot_dir/; fi; done

          DATABASE2# cd /var/lib/cassandra/data/to_bgp_keyspace/; for dir in $(ls); do if [ -d "$dir/snapshots/" ]; then echo /var/lib/cassandra/data/to_bgp_keyspace/$dir/snapshots/$(ls -t $dir/snapshots/ | head -n1)/; fi; done

           On BACKUP_SERVER create:
                   mkdir -p <backup_path>/db2/<of all the directories listed during above step>

          DATABASE2# cd /var/lib/cassandra/data/to_bgp_keyspace/; for dir in $(ls); do if [ -d "$dir/snapshots/" ]; then  snapshot_dir=$dir/snapshots/$(ls -t $dir/snapshots/ | head -n1); scp -r $snapshot_dir/* root@<BACKUP_SERVER>:<backup_path>/db2/var/lib/cassandra/data/to_bgp_keyspace/$snapshot_dir/; fi; done

          DATABASE3# cd /var/lib/cassandra/data/to_bgp_keyspace/; for dir in $(ls); do if [ -d "$dir/snapshots/" ]; then echo /var/lib/cassandra/data/to_bgp_keyspace/$dir/snapshots/$(ls -t $dir/snapshots/ | head -n1)/; fi; done

           On BACKUP_SERVER create:
                    mkdir -p <backup_path>/db3/<of all the directories listed during above step>

          DATABASE3# cd /var/lib/cassandra/data/to_bgp_keyspace/; for dir in $(ls); do if [ -d "$dir/snapshots/" ]; then snapshot_dir=$dir/snapshots/$(ls -t $dir/snapshots/ | head -n1); scp -r $snapshot_dir/* root@<BACKUP_SERVER>:<backup_path>/db3/var/lib/cassandra/data/to_bgp_keyspace/$snapshot_dir/; fi; done

2.3.3	Copy svc_monitor_keyspace snapshot to the backup server

       DATABASE1# cd /var/lib/cassandra/data/svc_monitor_keyspace/; for dir in $(ls); do if [ -d "$dir/snapshots/" ]; then echo /var/lib/cassandra/data/svc_monitor_keyspace/$dir/snapshots/$(ls -t $dir/snapshots/ | head -n1)/; fi; done
 
       On BACKUP_SERVER create:
           mkdir -p <backup_path>/db1/<of all the directories listed during above step>

       DATABASE1# cd /var/lib/cassandra/data/svc_monitor_keyspace/; for dir in $(ls); do if [ -d "$dir/snapshots/" ]; then snapshot_dir=$dir/snapshots/$(ls -t $dir/snapshots/ | head -n1); scp -r $snapshot_dir/* root@<BACKUP_SERVER>:<backup_path>/db1/var/lib/cassandra/data/svc_monitor_keyspace/$snapshot_dir/; fi; done

        DATABASE2# cd /var/lib/cassandra/data/svc_monitor_keyspace/; for dir in $(ls); do if [ -d "$dir/snapshots/" ]; then echo /var/lib/cassandra/data/svc_monitor_keyspace/$dir/snapshots/$(ls -t $dir/snapshots/ | head -n1)/; fi; done

        On BACKUP_SERVER create:
             mkdir -p <backup_path>/db2/<of all the directories listed during above step>

        DATABASE2# cd /var/lib/cassandra/data/svc_monitor_keyspace/; for dir in $(ls); do if [ -d "$dir/snapshots/" ]; then snapshot_dir=$dir/snapshots/$(ls -t $dir/snapshots/ | head -n1); scp -r $snapshot_dir/* root@<BACKUP_SERVER>:<backup_path>/db2/var/lib/cassandra/data/svc_monitor_keyspace/$snapshot_dir/; fi; done

        DATABASE3# cd /var/lib/cassandra/data/svc_monitor_keyspace/; for dir in $(ls); do if [ -d "$dir/snapshots/" ]; then echo /var/lib/cassandra/data/svc_monitor_keyspace/$dir/snapshots/$(ls -t $dir/snapshots/ | head -n1)/; fi; done

        On BACKUP_SERVER create:
           mkdir -p <backup_path>/db3/<of all the directories listed during above step>

        DATABASE3# cd /var/lib/cassandra/data/svc_monitor_keyspace/; for dir in $(ls); do if [ -d "$dir/snapshots/" ]; then snapshot_dir=$dir/snapshots/$(ls -t $dir/snapshots/ | head -n1); scp -r $snapshot_dir/* root@<BACKUP_SERVER>:<backup_path>/db3/var/lib/cassandra/data/svc_monitor_keyspace/$snapshot_dir/; fi; done

2.3.4	Copy the database initial tokens

          On BACKUP_SERVER create:
              mkdir -p <backup_path>/db1/initial_tokens/
              mkdir -p <backup_path>/db2/initial_tokens/
              mkdir -p <backup_path>/db3/initial_tokens/

          DATABASE1: nodetool ring | grep <DATABASE1_Internal_IP> | awk '{print $NF ","}' | xargs > /tmp/initial_tokens
          DATABASE1: scp /tmp/initial_tokens root@<BACKUP_SERVER>:<backup_path>/db1/initial_tokens/
          DATABASE2: nodetool ring | grep <DATABASE2_Internal_IP> | awk '{print $NF ","}' | xargs > /tmp/initial_tokens
          DATABASE2: scp /tmp/initial_tokens root@<BACKUP_SERVER>:<backup_path>/db2/initial_tokens/
          DATABASE3: nodetool ring | grep <DATABASE3_Internal_IP> | awk '{print $NF ","}' | xargs > /tmp/initial_tokens
          DATABASE3: scp /tmp/initial_tokens root@<BACKUP_SERVER>:<backup_path>/db3/initial_tokens/

##3 Restore Config on new nodes 

3.1 Populate testbed.py with following information,

        ssd_data_dir = '<commit-logs-partition>/commit_logs_data'
        database_dir = '<cassandra-data-partition>/cassandra’
        env.roledefs with new servers [DATABASE4,DATABASE5,DATABASE6] as 'cfgm roles.


3.2 Stop Contrail Config and Database process

        fab stop_cfgm
        fab stop_database

3.3 Restore Zookeeper data 

        Copy the previously backed up corresponding /var/lib/zookeeper/* files from the  BACKUP_SERVER to DATABASE4, DATABASE5, DATABASE6

         FAB_NODE# fab -H <user@DATABASE4>,<user@DATABASE5>,<user@DATABASE6> -- "chown -R zookeeper:zookeeper /var/lib/zookeeper/"

        ON DATABASE4,5,6
           Delete the following if it exists
            /var/lib/cassandra/data/config_db_uuid/*
            /var/lib/cassandra/data/to_bgp_keyspace/*
            /var/lib/cassandra/data/svc_monitor_keyspace/*

3.4	Restore Cassandra data

3.4.1	Restore config_db_uuid keyspace

         On BACKUP_SERVER
            cd <backup_path>/db1/var/lib/cassandra/data/config_db_uuid/; for dir in $(ls); do if [ -d "$dir/snapshots" ]; then ssh root@<DATABASE1> "mkdir -p /var/lib/cassandra/data/config_db_uuid/$dir";  scp -r $dir/snapshots/$(ls $dir/snapshots/ | head -n1)/* root@<DATABASE1>:/var/lib/cassandra/data/config_db_uuid/$dir/; fi; done

            cd <backup_path>/db2/var/lib/cassandra/data/config_db_uuid/; for dir in $(ls); do if [ -d "$dir/snapshots" ]; then ssh root@<DATABASE2> "mkdir -p /var/lib/cassandra/data/config_db_uuid/$dir";  scp -r $dir/snapshots/$(ls $dir/snapshots/ | head -n1)/* root@<DATABASE2>:/var/lib/cassandra/data/config_db_uuid/$dir/; fi; done

            cd <backup_path>/db3/var/lib/cassandra/data/config_db_uuid/; for dir in $(ls); do if [ -d "$dir/snapshots" ]; then ssh root@<DATABASE3> "mkdir -p /var/lib/cassandra/data/config_db_uuid/$dir";  scp -r $dir/snapshots/$(ls $dir/snapshots/ | head -n1)/* root@<DATABASE3>:/var/lib/cassandra/data/config_db_uuid/$dir/; fi; done

3.4.2	Restore to_bgp_keyspace keyspace

        On BACKUP_SERVER
            cd <backup_path>/db1/var/lib/cassandra/data/to_bgp_keyspace/; for dir in $(ls); do if [ -d "$dir/snapshots" ]; then ssh root@<DATABASE1> "mkdir -p /var/lib/cassandra/data/to_bgp_keyspace/$dir";  scp -r $dir/snapshots/$(ls $dir/snapshots/ | head -n1)/* root@<DATABASE1>:/var/lib/cassandra/data/to_bgp_keyspace/$dir/; fi; done

            cd <backup_path>/db2/var/lib/cassandra/data/to_bgp_keyspace/; for dir in $(ls); do if [ -d "$dir/snapshots" ]; then ssh root@<DATABASE2> "mkdir -p /var/lib/cassandra/data/to_bgp_keyspace/$dir";  scp -r $dir/snapshots/$(ls $dir/snapshots/ | head -n1)/* root@<DATABASE2>:/var/lib/cassandra/data/to_bgp_keyspace/$dir/; fi; done

            cd <backup_path>/db3/var/lib/cassandra/data/to_bgp_keyspace/; for dir in $(ls); do if [ -d "$dir/snapshots" ]; then ssh root@<DATABASE3> "mkdir -p /var/lib/cassandra/data/to_bgp_keyspace/$dir";  scp -r $dir/snapshots/$(ls $dir/snapshots/ | head -n1)/* root@<DATABASE3>:/var/lib/cassandra/data/to_bgp_keyspace/$dir/; fi; done

3.4.3	Restore svc_monitor_keyspace keyspace

        On BACKUP_SERVER
            cd <backup_path>/db1/var/lib/cassandra/data/svc_monitor_keyspace/; for dir in $(ls); do if [ -d "$dir/snapshots" ]; then ssh root@<DATABASE1> "mkdir -p /var/lib/cassandra/data/svc_monitor_keyspace/$dir";  scp -r $dir/snapshots/$(ls $dir/snapshots/ | head -n1)/* root@<DATABASE1>:/var/lib/cassandra/data/svc_monitor_keyspace/$dir/; fi; done

            cd <backup_path>/db2/var/lib/cassandra/data/svc_monitor_keyspace/; for dir in $(ls); do if [ -d "$dir/snapshots" ]; then ssh root@<DATABASE2> "mkdir -p /var/lib/cassandra/data/svc_monitor_keyspace/$dir";  scp -r $dir/snapshots/$(ls $dir/snapshots/ | head -n1)/* root@<DATABASE2>:/var/lib/cassandra/data/svc_monitor_keyspace/$dir/; fi; done

             cd <backup_path>/db3/var/lib/cassandra/data/svc_monitor_keyspace/; for dir in $(ls); do if [ -d "$dir/snapshots" ]; then ssh root@<DATABASE3> "mkdir -p /var/lib/cassandra/data/svc_monitor_keyspace/$dir";  scp -r $dir/snapshots/$(ls $dir/snapshots/ | head -n1)/* root@<DATABASE3>:/var/lib/cassandra/data/svc_monitor_keyspace/$dir/; fi; done

3.4.4	Restore initial_tokens

On each of database node, copy the corresponding initial_token from BACKUP_SERVER to /tmp/initial_tokens

          DATABASE4: echo "initial_token: $(cat /tmp/initial_tokens)" >> /etc/cassandra/cassandra.yaml
          DATABASE5: echo "initial_token: $(cat /tmp/initial_tokens)" >> /etc/cassandra/cassandra.yaml
          DATABASE6: echo "initial_token: $(cat /tmp/initial_tokens)" >> /etc/cassandra/cassandra.yaml

          FAB_NODE# fab -H <user@DATABASE4>,<user@DATABASE5>,<user@DATABASE6>  -- "chown -R cassandra:cassandra /var/lib/cassandra/"

1.3.2.5	Repair and verify database

          FAB_NODE# fab start_database
          FAB_NODE# fab verify_database
          FAB_NODE: fab -H <user@DATABASE4>,<user@DATABASE5>,<user@DATABASE6>  -- "nodetool repair  -- config_db_uuid"
          FAB_NODE: fab -H <user@DATABASE4>,<user@DATABASE5>,<user@DATABASE6>  -- "nodetool repair  -- to_bgp_keyspace"
          FAB_NODE: fab -H <user@DATABASE4>,<user@DATABASE5>,<user@DATABASE6>  -- "nodetool repair  -- svc_monitor_keyspace"

          FAB_NODE# fab restart_cfgm


