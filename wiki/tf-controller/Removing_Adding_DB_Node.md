## TL;DR (but highly recommend reading details)
* Install contrail-openstack-database package on new DB node
* When using fab based setup, run fab setup_database_node:root@<new-db-node-ip> with right testbed.py changes
* Fixup server-id for zookeeper, restart zookeeper on every DB node, one-by-one
* Fixup cassandra data directories symlinks to right partition (if different than default)
* Start cassandra service, wait for ``nodetool netstats`` to show ``NORMAL`` status
* Remove old cassandra node
* Generic information (we use vnodes) to [add a cassandra node](http://www.datastax.com/documentation/cassandra/1.2/cassandra/operations/ops_add_node_to_cluster_t.html) and [remove a cassandra node.] (http://www.datastax.com/documentation/cassandra/1.2/cassandra/operations/ops_remove_node_t.html)
* Information for [add and remove of zookeeper node.](http://stackoverflow.com/questions/11375126/zookeeper-adding-peers-dynamically)
## Details

The description below assumes a testbed that had 3 DB nodes (host1,host2,host3 in testbed.py of fab) where host3 is to be replaced by a new DB node. For zookeeper purposes this will be with a new server id 4.

* Install container package, setup repo, install database package
   
  + dpkg -i contrail-install-packages_version_all.deb
  + cd /opt/contrail/contrail_packages/
  + ./setup.sh
  + echo "manual" >> /etc/init/supervisord-contrail-database.override
  + apt-get install contrail-openstack-database

  If using fab,
    + add new db node instead of old db node in testbed.py for host3
    + fab setup_database_node:root@new-db-node

* Get zookeeper online ensuring new server is id 4
   + vi /etc/zookeeper/conf/myid - fixup server id as 4 instead of 3
   + vi /etc/zookeeper/conf/zoo.cfg  - fixup server id as 4 instead of 3
       (Do this on existing DB nodes too to add server with id 4 in above files)
   + service zookeeper restart
     (Do this one-by-one from all followers to leader verifying node count in telnet localhost:2181 stat command)

* Start cassandra so /var/lib/cassandra dir is created
   + service supervisord-contrail-database start
   + service supervisord-contrail-database stop

* [Optional] Fix symlinks for keyspaces in /var/lib/cassandra/data to right partition
   + cd /var/lib/cassandra/data/
   + mkdir -p /``partition``/config_db_uuid
   + mkdir -p /``partition``/ContrailAnalytics
   + mkdir -p /``partition``/svc_monitor_keyspace
   + mkdir -p /``partition``/to_bgp_keyspace
   + mkdir -p /``partition``/useragent
   + ln -sf /``partition``/config_db_uuid
   + ln -sf /``partition``/ContrailAnalytics
   + ln -sf /``partition``/svc_monitor_keyspace
   + ln -sf /``partition``/to_bgp_keyspace
   + ln -sf /``partition``/useragent

* Start cassandra it will go online after a long sync
   + rm supervisord-contrail-database.override
   + service supervisord-contrail-database start
   + nodetool netstats #(WAIT for a long time for new node to sync up the data)

* Remove old node
   + nodetool removenode ``host-id`` (where host-id of the down/DN node is found by ``nodetool status``)
   + nodetool removenode force # This is needed if node 3 was DEAD instead of alive but being decommissioned)