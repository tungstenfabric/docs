Cassandra database allows to specify a TTL (time to live) for all the data written to the database. After the TTL, that data expires and is no longer available for queries.

To provide flexibility for the availability time of various types of contrail analytics data, we have configuration mechanism to set different TTL for different types of data.

We provide four TTL parameters defined as below in /etc/contrail/contrail-collector.conf  
* analytics_configaudit_ttl -- ttl for config audit data coming into collector,
* analytics_statsdata_ttl -- ttl for statistics data,
* analytics_flowdata_ttl -- ttl for flow data,
* analytics_data_ttl -- for messages and object logs

TTL is specified in number of hours and a typical configuration in /etc/contrail/contrail-collector.conf could be  
analytics_data_ttl=48  
analytics_config_audit_ttl=2160  
analytics_statistics_ttl=168  
analytics_flow_ttl=2  

In this case, we save the config audit logs for 90 days, statistics data for 7 days, messages and object logs for 2 days, and flow data for 2 hours.

If one is using fabric-utils to do the contrail provisioning, the following parameters in the testbed.py will translate to the above config parameters for contrail-collector  
database_ttl = 48  
analytics_config_audit_ttl = 2160  
analytics_statistics_ttl = 168  
analytics_flow_ttl = 2  

For all values:

- 0 means keep forever
- 1 means 1 hour
- 2 means 2 hours and so on
- -1 or unset value is a special setting which will result in the value matching another reference value. For example (from `contrail-collector.conf`):

```
# analytics_config_audit_ttl, if not set (or set to -1), defaults to analytics_data_ttl
# analytics_statistics_ttl, if not set (or set to -1), defaults to analytics_data_ttl
# analytics_flow_ttl, if not set (or set to -1), defaults to analytics_statsdata_ttl
```
