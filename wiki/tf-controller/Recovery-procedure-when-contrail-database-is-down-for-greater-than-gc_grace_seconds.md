When contrail-database has been down (either due to network partitioning or process stopped) for greater than gc_grace_seconds (defaulted to 10 days), the contrail-database init.d script will not start it. On issuing the `service contrail-database start` command, user will see a message similar to 

`Cassandra has been down for at least 777600 seconds, not starting`

In this scenario, if contrail-database is brought online without following the below procedure, then it can result in inconsistent configuration database.

To recover from this situation the following steps need to be followed:

### Remove the cassandra node.

For cassandra 1.2.x, the steps are at https://docs.datastax.com/en/cassandra/1.2/cassandra/operations/ops_remove_node_t.html.

For cassandra 2.1.x, the steps are at https://docs.datastax.com/en/cassandra/2.1/cassandra/operations/opsRemoveNode.html

Note: The `nodetool removenode` command mentioned in the steps above needs to run on the other cassandra nodes since cassandra is already stopped on the node to be removed.

### If this is the analytics DB, clear the analytics data (the one that gets corrupted more often). 

`rm -rf /var/lib/cassandra/commitlog/*`

`rm -rf /var/lib/cassandra/ContrailAnalyticsCql/*`

### Delete the cassandra cluster status file 
`rm -f /var/log/cassandra/status-up`

### Start contrail-database
`service contrail-database start`
