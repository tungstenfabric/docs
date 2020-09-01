Disk usage by analytics db can be monitored from the contrail UI page at  
**Monitor -> Infrastructure -> Database Nodes**  
or
from database-node UVEs at  
_\<analytics-node-ip\>:8081/analytics/uves/database-node/*?cfilt=DatabaseUsageInfo_  

In an ideal scenario, the sizing should be done such that an **external** purging [as opposed to cassandra's own compaction] is not required.  

When the above [ideal sizing] does not happen, one can rely on the following purge methods  

_contrail-analytics-api_ process continuously monitors the disk usage and tries to purge the data when it exceeds certain value. 

If one needs to manually send a request to _contrail-analytics-api_, to purge beyond what it does automatically, it can be done from the UI using the grid's menu button at  
**Monitor -> Infrastructure -> Database Nodes**  
Another way to send a request to _contrail-analytics-api_ to purge is to do a POST request to    
_\<analytics-node-ip\>:8081/analytics/operation/database-purge_  
the POST data is the percentage to purge and is input in JSON format, as below,  
{ "purge_input" : 30 }

The above purge method is a slow process, as deleting the data from database does not immediately free up the disk space which depends on cassandra doing the compaction, which may depend on various factors including system load etc..  
In extreme cases, where one needs to manually purge analytics data, one of the following methods can be used  

**Method 1**: lose all analytics data, and involves stopping cassandra on all nodes [this will disrupt config operations]
 
a) stop config and analytics processes on all nodes [_service supervisor-analytics stop, service supervisor-config stop_] 

b) drain cassandra on all nodes [_nodetool drain_]; then stop cassandra on all nodes [_service contrail-database stop_]  

c) delete analytics keyspace directory - /var/lib/cassandra/data/ContrailAnalytics or /var/lib/cassandra/data/ContrailAnalyticsCql 

d) restart cassandra [_service contrail-database start_]

e) start config and analytics processes on all nodes [_service supervisor-analytics start, service supervisor-config start_]  

**Method 2**: lose all analytics data, but cassandra can serve config operations
  
a) stop analytics processes on all nodes  [_service supervisor-analytics stop_]

b) using cqlsh or cassandra-cli - drop analytics keyspace - ContrailAnalytics or ContrailAnalyticsCql [this will take a bit of time and might timeout but the data should be eventually deleted]
  
c) verify analytics keyspace - ContrailAnalytics or ContrailAnalyticsCql is indeed not present in any node using cqlsh or cassandra-cli

d) verify that the data is deleted using nodetool status and verify that the load is gone down
  
e) delete analytics keyspace directory - /var/lib/cassandra/data/ContrailAnalytics or /var/lib/cassandra/data/ContrailAnalyticsCql

f) start analytics processes on all nodes [_service supervisor-analytics start_]
