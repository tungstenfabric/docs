This document gives details of the utility scripts that allow you to query and get data from contrail analytics. The collection and storage of the data is not discussed here.

* _contrail-logs_: contrail-logs can be used to get system logs and object logs in the contrail system
* _contrail-stats_: contrail-stats can be used to get generic stats using the virtual stat tables
* _contrail-flows_: contrail-flows can be used to get flow information  
  
Each of the commands allow you filter, aggregate data in any slice and dice manner and are powerful debug tools. All of these queries can be done through Contrail UI as well.

# contrail-logs
--help option provides all the information with respect to the command's options as below.  

> root@a7s30:~# contrail-logs --help  
> usage: contrail-logs [-h] [--analytics-api-ip ANALYTICS_API_IP]  
>                      [--analytics-api-port ANALYTICS_API_PORT]  
>                      [--start-time START_TIME] [--end-time END_TIME]  
>                      [--last LAST] [--source SOURCE]  
>                      [--node-type {Invalid,Config,Control,Analytics,Compute,WebUI,Database,OpenStack,ServerMgr}]  
>                      [--module {contrail-control,contrail-vrouter-agent,contrail-api,contrail-schema,contrail-analytics-api,contrail-collector,contrail-query-engine,contrail-svc-monitor,DeviceManager,contrail-dns,contrail-discovery,IfmapServer,XmppServer,contrail-analytics-nodemgr,contrail-control-nodemgr,contrail-config-nodemgr,contrail-database-nodemgr,Contrail-WebUI-Nodemgr,contrail-vrouter-nodemgr,Storage-Stats-mgr,Ipmi-Stats-mgr,contrail-snmp-collector,contrail-topology,InventoryAgent,contrail-alarm-gen,contrail-tor-agent}]  
>                      [--instance-id INSTANCE_ID] [--category CATEGORY]  
>                      [--level LEVEL] [--message-type MESSAGE_TYPE] [--reverse]  
>                      [--verbose] [--all] [--raw]  
>                      [--object-type {service-chain,database-node,routing-instance,xmpp-connection,analytics-query,virtual-machine-interface,config-user,analytics-query-id,None,logical-interface,xmpp-peer,generator,virtual-network,analytics-node,prouter,bgp-peer,config,dns-node,control-node,physical-interface,None,virtual-machine,vrouter,None,None,service-instance,config-node}]  
>                      [--object-values] [--object-id OBJECT_ID]  
>                      [--object-select-field {ObjectLog,SystemLog}]  
>                      [--trace TRACE] [--limit LIMIT] [--send-syslog]  
>                      [--syslog-server SYSLOG_SERVER]  
>                      [--syslog-port SYSLOG_PORT] [--f] [--keywords KEYWORDS]  
>   
>   
> optional arguments:  
>   -h, --help            show this help message and exit  
>   --analytics-api-ip ANALYTICS_API_IP  
>                         IP address of Analytics API Server (default:  
>                         127.0.0.1)  
>   --analytics-api-port ANALYTICS_API_PORT  
>                         Port of Analytics API Server (default: 8081)  
>   --start-time START_TIME  
>                         Logs start time (format now-10m, now-1h) (default:  
> ...  
>   --syslog-port SYSLOG_PORT  
>                         Port to send syslog to (default: 514)  
>   --f                   Tail logs from now (default: False)  
>   --keywords KEYWORDS   comma seperated list of keywords (default: None)  
>   --message-types       Display list of message type (default: False)  

## contrail-logs systemlog examples:

* View all logs from all the boxes for the default time [which is last 10 minutes]:

`/usr/bin/contrail-logs`

* View all logs from all the boxes for the last hour:

`/usr/bin/contrail-logs --last 1h`

* View all logs from all boxes for 1 hour between 11 hours ago and 10 hours ago:

`/usr/bin/contrail-logs --start-time now-11h --end-time now-10h`

* View logs in a specific time interval specificed in date format:

`/usr/bin/contrail-logs --start-time "2013 May 12 18:30:27.0" --end-time "2013 May 12 18:31:27.0"`

* View all logs from all boxes for the last 10 minutes in reverse chronological order:

`/usr/bin/contrail-logs --reverse`

* module filtering: View the contrail-control daemon logs from all the boxes for the last 10 minutes:

`/usr/bin/contrail-logs --module contrail-control`

* module and source filtering: View the contrail-control daemon logs from source a6s23.contrail.juniper.net for the last 10 minutes:

`/usr/bin/contrail-logs --module contrail-control --source a6s23.contrail.juniper.net`

## contrail-logs objectlog examples:
This is used to get all the logs relevant for a particular object in the system

* View logs relevant to a virtual network object by name demo:admin:vn1 from all the boxes for the last 10 minutes:

`/usr/bin/contrail-logs --object-type virtual-network --object-id demo:admin:vn1`

* View logs relevant to an analytics-node object with name a7s30 for the last 10 minutes:

`contrail-logs --object-type analytics-node --object-id a7s30`

## object-logs object-values example
Typical work flow would be to find out all the object-values [keys] of a particular object-type and then get detailed logs of a particular object-id. The following example shows how to get object-values of type control-node, and then subsequently get logs of a particular object-id.

* List all the objects of type control-node for which messages have been received in the last 10 minutes:

`/usr/bin/contrail-logs --object-type control-node --object-values`

* View logs of a particular object of control-node type

`/usr/bin/contrail-logs --object-type control-node --object-id a7s30`

## contrail config audit example
Auditing of config is of very particular importance as it tells the sequence of operations on the config objects.
The object-type used in this case is config.

* List all the objects of type config for which messages have been received in the last 10 minutes:
`contrail-logs --object-type config --object-values`

* List all the logs of object routing_instance:default-domain:admin:vn5:vn5 of type config in the last 10 minutes:
`contrail-logs --object-type config --object-id routing_instance:default-domain:admin:vn5:vn5`

Please use the `--help` option to list the arguments supported by contrail-logs.

# contrail-stats
generic stats are provided using the virtual tables whose schemas are provided through analytics api. contrail-stats utility can be used as an easy command line interface in lieu of raw REST API. The following --help gives an idea of the options available in contrail-stats.  

> root@a7s30:~# contrail-stats --help  
> usage: contrail-stats [-h] [--analytics-api-ip ANALYTICS_API_IP]  
>                       [--analytics-api-port ANALYTICS_API_PORT]  
>                       [--start-time START_TIME] [--end-time END_TIME]  
>                       [--last LAST]  
>                       [--table {AnalyticsCpuState.cpu_info,ConfigCpuState.cpu_info,ControlCpuState.cpu_info,PRouterEntry.ifStats,ComputeCpuState.cpu_info,VirtualMachineStats.cpu_stats,ComputeStoragePool
> .info_stats,ComputeStorageOsd.info_stats,ComputeStorageDisk.info_stats,ServerMonitoringInfo.sensor_stats,ServerMonitoringInfo.disk_usage_stats,ServerMonitoringSummary.network_info_stats,ServerMonitoring
> Summary.resource_info_stats,ServerMonitoringInfo.file_system_view_stats.physical_disks,SandeshMessageStat.msg_info,GeneratorDbStats.table_info,GeneratorDbStats.statistics_table_info,GeneratorDbStats.err
> ors,FieldNames.fields,FieldNames.fieldi,QueryPerfInfo.query_stats,UveVirtualNetworkAgent.vn_stats,DatabasePurgeInfo.stats,DatabaseUsageInfo.database_usage,ProtobufCollectorStats.tx_socket_stats,Protobuf
> CollectorStats.rx_socket_stats,ProtobufCollectorStats.rx_message_stats,ProtobufCollectorStats.db_table_info,ProtobufCollectorStats.db_statistics_table_info,ProtobufCollectorStats.db_errors,PFEHeapInfo.h
> eap_info,npu_mem.stats,fabric_message.edges.class_stats.transmit_counts,g_lsp_stats.lsp_records,UFlowData.flow,AlarmgenUpdate.keys,AlarmgenUpdate.notifs,UveLoadbalancer.virtual_ip_stats,UveLoadbalancer.
> listener_stats,UveLoadbalancer.pool_stats,UveLoadbalancer.member_stats,NodeStatus.disk_usage_info,NodeStatus.disk_usage_info,NodeStatus.disk_usage_info,NodeStatus.disk_usage_info,NodeStatus.disk_usage_i
> nfo,UveVMInterfaceAgent.fip_diff_stats,UveVMInterfaceAgent.if_stats,VrouterStatsAgent.flow_rate}]  
>                       [--dtable DTABLE] [--select SELECT [SELECT ...]]  
>                       [--where WHERE [WHERE ...]] [--sort SORT [SORT ...]]  
>   
> optional arguments:  
>   -h, --help            show this help message and exit  
>   --analytics-api-ip ANALYTICS_API_IP  
>                         IP address of Analytics API Server (default:  
>                         127.0.0.1)  
>   --analytics-api-port ANALYTICS_API_PORT  
>                         Port of Analytcis API Server (default: 8081)  
>   --start-time START_TIME  
>                         Logs start time (format now-10m, now-1h) (default:  
>                         now-10m)  
>   --end-time END_TIME   Logs end time (default: now)  
>   --last LAST           Logs from last time period (format 10m, 1d) (default:  
>                         None)  
>   --table {AnalyticsCpuState.cpu_info,ConfigCpuState.cpu_info,ControlCpuState.cpu_info,PRouterEntry.ifStats,ComputeCpuState.cpu_info,VirtualMachineStats.cpu_stats,ComputeStoragePool.info_stats,ComputeSt
> orageOsd.info_stats,ComputeStorageDisk.info_stats,ServerMonitoringInfo.sensor_stats,ServerMonitoringInfo.disk_usage_stats,ServerMonitoringSummary.network_info_stats,ServerMonitoringSummary.resource_info
> _stats,ServerMonitoringInfo.file_system_view_stats.physical_disks,SandeshMessageStat.msg_info,GeneratorDbStats.table_info,GeneratorDbStats.statistics_table_info,GeneratorDbStats.errors,FieldNames.fields
> ,FieldNames.fieldi,QueryPerfInfo.query_stats,UveVirtualNetworkAgent.vn_stats,DatabasePurgeInfo.stats,DatabaseUsageInfo.database_usage,ProtobufCollectorStats.tx_socket_stats,ProtobufCollectorStats.rx_soc
> ket_stats,ProtobufCollectorStats.rx_message_stats,ProtobufCollectorStats.db_table_info,ProtobufCollectorStats.db_statistics_table_info,ProtobufCollectorStats.db_errors,PFEHeapInfo.heap_info,npu_mem.stat
> s,fabric_message.edges.class_stats.transmit_counts,g_lsp_stats.lsp_records,UFlowData.flow,AlarmgenUpdate.keys,AlarmgenUpdate.notifs,UveLoadbalancer.virtual_ip_stats,UveLoadbalancer.listener_stats,UveLoa
> dbalancer.pool_stats,UveLoadbalancer.member_stats,NodeStatus.disk_usage_info,NodeStatus.disk_usage_info,NodeStatus.disk_usage_info,NodeStatus.disk_usage_info,NodeStatus.disk_usage_info,UveVMInterfaceAge
> nt.fip_diff_stats,UveVMInterfaceAgent.if_stats,VrouterStatsAgent.flow_rate}  
>                         StatTable to query (default: None)  
>   --dtable DTABLE       Dynamic StatTable to query (default: None)  
>   --select SELECT [SELECT ...]  
>                         List of Select Terms (default: [])  
>   --where WHERE [WHERE ...]  
>                         List of Where Terms to be ANDed (default: [])  
>   --sort SORT [SORT ...]  
>                         List of Sort Terms (default: [])  

## contrail-stats examples
* View schema of stat table AnalyticsCpuState.cpu_info  
`contrail-stats --table AnalyticsCpuState.cpu_info`

* View samples of (name, cpu_info.cpu_share) tuples over the default period [last 10 minutes].  
`contrail-stats --table AnalyticsCpuState.cpu_info --select cpu_info.cpu_share name --where name="*"`

* View ("SUM(cpu_info.cpu_share)" "COUNT(cpu_info)") tuple for module contrail-collector, this is used to calculate Average cpu_info.cpu_share over the specified period.  
`contrail-stats --table AnalyticsCpuState.cpu_info --select "SUM(cpu_info.cpu_share)" "COUNT(cpu_info)" --where name="a7s30" cpu_info.module_id=contrail-collector`

* View time series data in intervals of 60s over a period of last 1h of a virtual networks in_bytes stats.  
`contrail-stats --table UveVirtualNetworkAgent.vn_stats --select "T=60" "SUM(vn_stats.in_bytes)" --where name=default-domain:admin:vn1 --last 1h`

* View (name, SUM(if_stats.in_bytes)) tuple, which will give total in_bytes of each virtual machine interface, over a period of 1h covering 11h back to 10h back.  
`contrail-stats --table UveVMInterfaceAgent.if_stats --select "SUM(if_stats.in_bytes)" name --where name="*" --start-time now-11h --end-time now-10h`

# contrail-flows
contrail-flows is used to flow record information from the contrail analytics.

> root@a7s30:~# contrail-flows --help  
> usage: contrail-flows [-h] [--analytics-api-ip ANALYTICS_API_IP]  
>                       [--analytics-api-port ANALYTICS_API_PORT]  
>                       [--start-time START_TIME] [--end-time END_TIME]  
>                       [--last LAST] [--vrouter VROUTER]  
>                       [--source-vn SOURCE_VN]  
>                       [--destination-vn DESTINATION_VN]  
>                       [--source-ip SOURCE_IP]  
>                       [--destination-ip DESTINATION_IP] [--protocol PROTOCOL]  
>                       [--source-port SOURCE_PORT]  
>                       [--destination-port DESTINATION_PORT] [--action ACTION]  
>                       [--direction {ingress,egress}] [--vrouter-ip VROUTER_IP]  
>                       [--other-vrouter-ip OTHER_VROUTER_IP] [--tunnel-info]  
>                       [--verbose]  
>   
> optional arguments:  
>   -h, --help            show this help message and exit  
>   --analytics-api-ip ANALYTICS_API_IP  
>                         IP address of Analytics API Server (default:  
>                         127.0.0.1)  
> ...
>   --tunnel-info         Show flow tunnel information (default: False)  
>   --verbose             Show internal information (default: False)  

## contrail-flows examples
* View all active flows over the default period [last 10 minutes]  
`contrail-flows`

* View all active flows from a particular source-vn and a particular source-ip, in the last 1h  
`contrail-flows --source-vn default-domain:admin:vn1 --source-ip 1.1.1.11 --last 1h`
