# Backup



* Simple Backup:

       python db_json_exim.py --export-to db-dump.json

  db_json_exim.py is found at /usr/lib/python2.7/dist-packages/cfgm_common

* To see prettified version of dump:

      cat db-dump.json | python -m json.tool | less

* To omit a keyspace in the dump (for e.g. to share with Juniper)

       python db_json_exim.py --export-to db-dump.json --omit-keyspace dm_keyspace
     
# Restore

* Steps for restore
  - Stop supervisor-config on all controllers or ensure it is already stopped
  - Stop cassandra on all controllers (config-db) or ensure it is already stopped
  - Stop zookeeper on all controllers or ensure it is already stopped
  - Stop kafka on all controllers (maybe in analytics controllers)
  - Stop contrail-hamon on all controllers (if it is running on controllers)
  - Backup zookeeper data directory on all controllers
  - Backup cassandra data directory on all controllers
  - Wipe out zookeeper data directory contents on all controllers
  - Wipe out cassandra data directory contents on all controllers
  - Start zookeeper on all controllers
  - Start cassandra on all controllers
  - Run `python db_json_exim.py --import-from db-dump.json` on any *one* controller
  - Start supervisor-config on all controllers
  - Start kafka on all controllers (maybe in analytics controllers)
  - Start contrail-hamon on all controllers (if previously stopped)

  
# Example

* Testbed has 3 controllers with config-db with IPs 10.87.65.30 (5b5s42), 10.87.65.31(5b5s43), 10.87.65.32(5b5s44)

* Backup

      root@5b5s42:~# python db_json_exim.py --export-to db-dump.json
      root@5b5s42:~# cat db-dump.json | python -m json.tool | less
       {
           "cassandra": {
               "config_db_uuid": {
              "obj_fq_name_table": {
                       "access_control_list": {
                       
        <snip>
 
 * Restore
 
   - Stop supervisor-config on all controllers
   
         root@5b5s42:~# service supervisor-config stop
         supervisor-config stop/waiting
         root@5b5s42:~#
         root@5b5s43:~# service supervisor-config stop
         supervisor-config stop/waiting
         root@5b5s43:~#
         root@5b5s44:~# service supervisor-config stop
         supervisor-config stop/waiting
         root@5b5s44:~#
         
    - Stop cassandra on all controllers
    
          root@5b5s42:~# service cassandra stop
          root@5b5s42:~#
          root@5b5s43:~# service cassandra stop
          root@5b5s43:~#
          root@5b5s44:~# service cassandra stop
          root@5b5s44:~#
          
     - Stop zookeeper on all controllers
     
           root@5b5s42:~# service zookeeper stop
           zookeeper stop/waiting
           root@5b5s42:~#
           root@5b5s43:~# service zookeeper stop
           zookeeper stop/waiting
           root@5b5s43:~#
           root@5b5s44:~# service zookeeper stop
           zookeeper stop/waiting
           root@5b5s44:~#

      - Stop kafka on all controllers (if it is running)

            root@5b5s42:~# service kafka stop
            kafka: stopped
            root@5b5s42:~#
            root@5b5s43:~# service kafka stop
            kafka: stopped
            root@5b5s43:~#
            root@5b5s44:~# service kafka stop
            kafka: stopped
            root@5b5s44:~#

      - Stop contrail-hamon on all controllers (if it is running on controllers)

            root@5b5s42:~# service contrail-hamon stop
            contrail-hamon stop/waiting
            root@5b5s43:~# service contrail-hamon stop
            contrail-hamon stop/waiting
            root@5b5s44:~# service contrail-hamon stop
            contrail-hamon stop/waiting

      - Stop all controller services if they are sharing Cassandra


      - Backup zookeeper data directory on all controllers

            root@5b5s42:~# cd /var/lib/zookeeper/
            root@5b5s42:/var/lib/zookeeper# cp -R version-2/ version-2-save
            root@5b5s42:/var/lib/zookeeper#
            root@5b5s43:~# cd /var/lib/zookeeper/
            root@5b5s43:/var/lib/zookeeper# cp -R version-2/ version-2-save
            root@5b5s43:/var/lib/zookeeper#
            root@5b5s44:~# cd /var/lib/zookeeper/
            root@5b5s44:/var/lib/zookeeper# cp -R version-2/ version-2-save
            root@5b5s44:/var/lib/zookeeper#
            
      - Backup cassandra data directory on all controllers
      
            root@5b5s42:~# cd /var/lib/
            root@5b5s42:/var/lib# cp -R cassandra/data/* cassandra-save/data
            root@5b5s42:/var/lib# cp -R cassandra/saved_caches/* cassandra-save/saved_caches
            root@5b5s42:/var/lib# cp -R cassandra/commitlog/* cassandra-save/commitlog
            root@5b5s43:~# cd /var/lib/
            root@5b5s43:/var/lib# cp -R cassandra/data/* cassandra-save/data
            root@5b5s43:/var/lib# cp -R cassandra/saved_caches/* cassandra-save/saved_caches
            root@5b5s43:/var/lib# cp -R cassandra/commitlog/* cassandra-save/commitlog
            root@5b5s44:~# cd /var/lib/
            root@5b5s44:/var/lib# cp -R cassandra/data/* cassandra-save/data
            root@5b5s44:/var/lib# cp -R cassandra/saved_caches/* cassandra-save/saved_caches
            root@5b5s44:/var/lib# cp -R cassandra/commitlog/* cassandra-save/commitlog            
      - Wipe out zookeeper data directory contents on all controllers
       
            root@5b5s42:~# rm -rf /var/lib/zookeeper/version-2/*
            root@5b5s42:~#
            root@5b5s43:~# rm -rf /var/lib/zookeeper/version-2/*
            root@5b5s43:~#
            root@5b5s44:~# rm -rf /var/lib/zookeeper/version-2/*
            root@5b5s44:~#
            
      - Wipe out cassandra data directory contents on all controllers
      
            root@5b5s42:~# rm -rf /var/lib/cassandra/data/*
            root@5b5s42:~# rm -rf /var/lib/cassandra/saved_caches/*
            root@5b5s42:~# rm -rf /var/lib/cassandra/commitlog/*
            root@5b5s43:~# rm -rf /var/lib/cassandra/data/*
            root@5b5s43:~# rm -rf /var/lib/cassandra/saved_caches/*
            root@5b5s43:~# rm -rf /var/lib/cassandra/commitlog/*
            root@5b5s44:~# rm -rf /var/lib/cassandra/data/*
            root@5b5s44:~# rm -rf /var/lib/cassandra/saved_caches/*
            root@5b5s44:~# rm -rf /var/lib/cassandra/commitlog/*            

      - Start zookeeper on all controllers

            root@5b5s42:~# service zookeeper start
            zookeeper start/running, process 14180
            root@5b5s42:~#
            root@5b5s43:~# service zookeeper start
            zookeeper start/running, process 11635
            root@5b5s43:~#
            root@5b5s44:~# service zookeeper start
            zookeeper start/running, process 28040
            root@5b5s44:~#
            
     - Start cassandra on all controllers
     
            root@5b5s42:~# service cassandra start
            root@5b5s42:~#
            root@5b5s43:~# service cassandra start
            root@5b5s43:~#
            root@5b5s44:~# service cassandra start
            root@5b5s44:~#


     - Run `python db_json_exim.py --import-from db-dump.json` on any *one* controller
     
            root@5b5s42:~# python db_json_exim.py --import-from db-dump.json
            root@5b5s42:~#
            
     - Start supervisor-config on all controllers

            root@5b5s42:~# service supervisor-config start
            supervisor-config start/running, process 19286
            root@5b5s42:~#
            root@5b5s43:~# service supervisor-config start
            supervisor-config start/running, process 28937
            root@5b5s43:~#
            root@5b5s44:~# service supervisor-config start
            supervisor-config start/running, process 21242
            root@5b5s44:~#

      - Start all contrail services, if they were stopped previously
            
      - Start kafka on all controllers (maybe in analytics controllers)

            root@5b5s42:~# service kafka start
            kafka: started
            root@5b5s42:~#
            root@5b5s43:~# service kafka start
            kafka: started
            root@5b5s43:~#
            root@5b5s44:~# service kafka start
            kafka: started
            root@5b5s44:~#
            
      - Start contrail-hamon on all controllers (if previously stopped)

            root@5b5s42:~# service contrail-hamon start
            contrail-hamon start/running, process 1379
            root@5b5s42:~#
            root@5b5s43:~# service contrail-hamon start
            contrail-hamon start/running, process 1230
            root@5b5s43:~#
            root@5b5s44:~# service contrail-hamon start
            contrail-hamon start/running, process 26843
            root@5b5s44:~#

     