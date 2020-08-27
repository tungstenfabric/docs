Most of the analytics documentation and information can be obtained from the REST API
of the contrail-analytics-api server.

_http://\<contrail-analytics-api-IP\>:8081/documentation/index.html_  
Provides information regarding the data available from contrail-analytics-api server
and how to query for the same.

In the following a brief description of different types of information provided through contrail-analytics-api server is given.  


# UVE [User Visible Entities]
_http://\<contrail-analytics-api-IP\>:8081/analytics/uves_  
Provides list of all UVE-types available in the system, examples include
virtual-networks, analytics-nodes, service-chains, bgp-peers, prouters etc.
The type names should be self explanatory.  
And on drilling down each set for e.g  
_http://\<contrail-analytics-api-IP\>:8081/analytics/uves/virtual-networks_  
provides all instances of this UVE type.  
And drilling down further for e.g.  
_http://\<contrail-analytics-api-IP\>:8081/analytics/uves/virtual-network/default-domain:admin:vn3?flat_  
provides the operating data for a specific UVE, in this case, for virtual network _default-domain:admin:vn3_

Same goes for other UVE types, for e.g. the following give operating data for
prouters - Physical Routers.  
_http://\<contrail-analytics-api-IP\>:8081/analytics/uves/prouters_  
_http://\<contrail-analytics-api-IP\>:8081/analytics/uves/prouter/a7-ex1?flat_  

A raw dump of the various UVEs is given in section [Per-UVE type contents](https://github.com/Juniper/contrail-controller/wiki/Contrail-Analytics-Documentation#per-uve-type-contents).  

# Analytics Table Queries
Most analytics data is queried using SQL-like queries into tables whose schema
are exposed via REST API - exact mechanism is in contrail-analytics-api server
documentation.  
_http://\<contrail-analytics-api-IP\>:8081/analytics/tables_  
Provides the list of all queryable tables and drilling down will give schema
for each of the tables, for e.g.  
_http://\<contrail-analytics-api-IP\>:8081/analytics/table/StatTable.VirtualMachineStats.cpu_stats/schema_  
provides schema for a table named StatTable.VirtualMachineStats.cpu_stats

There are a few types of tables - their type returned in the return list of tables  
* LOG - Only MessageTable is of this type and is used to query system logs  
* OBJECT - There are multipe tables of this type each corresponding to a particular object  
* FLOW - FlowRecordTable and FlowSeriesTable fall into category and are used to get flow information  
* STAT - There are many generic statistics tables  

To reiterate the query will be of the same format, SQL-like query in JSON, for all
tables. An example would be  

{  
start_time: "now-10m" ,   
end_time: "now" ,  
table: "StatTable.UveVirtualNetworkAgent.vn_stats" ,   
select_fields: ["SUM(vn_stats.in_bytes)", "vn_stats.other_vn"] ,   
where: [[{"value": "default-domain:admin:vn1", "op": 1, "suffix": null, "name": "name", "value2": null}]] }  

Queries can be done using [contrail-stats](https://github.com/Juniper/contrail-controller/wiki/Contrail-utility-scripts-for-getting-logs,-stats-and-flows-from-analytics#contrail-stats) for Statistics Tables, [contrail-logs](https://github.com/Juniper/contrail-controller/wiki/Contrail-utility-scripts-for-getting-logs,-stats-and-flows-from-analytics#contrail-logs) for Message Table and [contrail-flows](https://github.com/Juniper/contrail-controller/wiki/Contrail-utility-scripts-for-getting-logs,-stats-and-flows-from-analytics#contrail-flows) for Flow Tables.

The schemas of the available tables is given in section [Query-able Table Schemas](https://github.com/Juniper/contrail-controller/wiki/Contrail-Analytics-Documentation#query-able-table-schemas).  
  
# Data Collection Frequency

Tables of most interest and their corresponding frequency are as below

**The following info is collected every 60 seconds**  
_http://\<contrail-analytics-api-IP\>:8081/analytics/table/StatTable.AnalyticsCpuState.cpu_info_  
_http://\<contrail-analytics-api-IP\>:8081/analytics/table/StatTable.ConfigCpuState.cpu_info_  
_http://\<contrail-analytics-api-IP\>:8081/analytics/table/StatTable.ControlCpuState.cpu_info_  
_http://\<contrail-analytics-api-IP\>:8081/analytics/table/StatTable.ComputeCpuState.cpu_info_  

**The below stats are collected every 30 seconds**  
_http://\<contrail-analytics-api-IP\>:8081/analytics/table/StatTable.UveVirtualNetworkAgent.vn_stats_  
_http://\<contrail-analytics-api-IP\>:8081/analytics/table/StatTable.VirtualMachineStats.cpu_stats_  
_http://\<contrail-analytics-api-IP\>:8081/analytics/table/StatTable.UveVMInterfaceAgent.fip_diff_stats_  
_http://\<contrail-analytics-api-IP\>:8081/analytics/table/StatTable.UveVMInterfaceAgent.if_stats_  

# Per-UVE type contents

This section lists the contents of most UVEs as a list of dictionaries with each dictionary describing a UVE type. Each  dict is of the format:

    { "uve-type": <UVE_TYPE>,
      "uve-key": <UVE_KEY>,
      "uve-value": <UVE_CONTENTS> }
___
    [
    {
    "uve-type": "bgp-peers",
    "uve-key": "default-domain:default-project:ip-fabric:__default__:a7s33:default-domain:default-project:ip-fabric:__default__:a7-mx80-1",
    "uve-value": 
    {
      "BgpPeerInfoData": {
        "admin_down": false, 
        "configured_families": [
          "route-target", 
          "inet-vpn", 
          "e-vpn", 
          "erm-vpn", 
          "inet6-vpn"
        ], 
        "event_info": {
          "last_event": "fsm::EvBgpUpdate", 
          "last_event_at": 1454939215915845
        }, 
        "families": [
          "inet-vpn", 
          "inet6-vpn", 
          "route-target"
        ], 
        "hold_time": 90, 
        "local_asn": 64512, 
        "local_id": 3374208010, 
        "negotiated_families": [
          "inet-vpn", 
          "inet6-vpn", 
          "route-target"
        ], 


        "passive": false, 
        "peer_address": "10.84.30.149", 
        "peer_asn": 64512, 
        "peer_id": 2501792778, 
        "peer_port": 0, 
        "peer_stats_info": {
          "rx_error_stats": {
            "inet6_error_stats": {
              "bad_inet6_afi_safi_count": 0, 
              "bad_inet6_nexthop_count": 0, 
              "bad_inet6_prefix_count": 0, 
              "bad_inet6_xml_token_count": 0
            }
          }, 
          "rx_proto_stats": {
            "close": 0, 
            "keepalive": 31339, 
            "notification": 0, 
            "open": 1, 
            "total": 31349, 
            "update": 9
          }, 
          "rx_update_stats": {
            "end_of_rib": 0, 
            "reach": 6, 
            "total": 0, 
            "unreach": 2
          }, 
          "tx_proto_stats": {
            "close": 0, 
            "keepalive": 28212, 
            "notification": 0, 
            "open": 1, 
            "total": 28246, 
            "update": 33
          }, 
          "tx_update_stats": {
            "end_of_rib": 0, 
            "reach": 23, 
            "total": 0, 
            "unreach": 9
          }
        }, 
        "peer_type": "internal", 
        "router_type": null, 
        "send_state": "in sync", 
        "state_info": {
          "last_state": "OpenConfirm", 
          "last_state_at": 1454107271782346, 
          "state": "Established"
        }
      }
    }
    },
    {
    "uve-type": "xmpp-peers",
    "uve-key": "a7s33:10.84.30.129",
    "uve-value": 
    {
      "XmppPeerInfoData": {
        "event_info": {
          "last_event": "xmsm::EvXmppIqReceive", 
          "last_event_at": 1454939930750579
        }, 
        "identifier": "a7s37", 
        "peer_stats_info": {
          "rx_error_stats": {
            "inet6_error_stats": {
              "bad_inet6_afi_safi_count": 0, 
              "bad_inet6_nexthop_count": 0, 
              "bad_inet6_prefix_count": 0, 
              "bad_inet6_xml_token_count": 0
            }
          }, 
          "rx_proto_stats": {
            "close": 0, 
            "keepalive": 31341, 
            "notification": 0, 
            "open": 1, 
            "total": 31623, 
            "update": 281
          }, 
          "rx_update_stats": {
            "end_of_rib": 0, 
            "reach": 97, 
            "total": 132, 
            "unreach": 35
          }, 
          "tx_proto_stats": {
            "close": 0, 
            "keepalive": 31059, 
            "notification": 0, 
            "open": 1, 
            "total": 31409, 
            "update": 349
          }, 
          "tx_update_stats": {
            "end_of_rib": 0, 
            "reach": 216, 
            "total": 240, 
            "unreach": 65
          }
        }, 
        "send_state": "not advertising", 
        "state_info": {
          "last_state": "Active", 
          "last_state_at": 1454021824159078, 
          "state": "Established"
        }
      }
    }
    },
    {
    "uve-type": "analytics-nodes",
    "uve-key": "a7s33",
    "uve-value": 
    {
      "AnalyticsCpuState": {
        "cpu_info": [
          {
            "cpu_share": 0.00138889, 
            "inst_id": "0", 
            "mem_res": 270752, 
            "mem_virt": 7014636, 
            "module_id": "contrail-query-engine"
          }, 
          {
            "cpu_share": 0.631145, 
            "inst_id": "0", 
            "mem_res": 32712992, 
            "mem_virt": 34819244, 
            "module_id": "contrail-collector"
          }, 
          {
            "cpu_share": 0.4125, 
            "inst_id": "0", 
            "mem_res": 69632, 
            "mem_virt": 426784, 
            "module_id": "contrail-alarm-gen"
          }, 
          {
            "cpu_share": 0.4125, 
            "inst_id": "0", 
            "mem_res": 57392, 
            "mem_virt": 401548, 
            "module_id": "contrail-analytics-api"
          }
        ]
      }, 
      "ModuleCpuState": {
        "module_cpu_info": [
          {
            "cpu_info": {
              "cpu_share": 0.00138889, 
              "meminfo": {
                "peakvirt": 7016056, 
                "res": 270752, 
                "virt": 7014636
              }, 
              "num_cpu": 24
            }, 
            "instance_id": "0", 
            "module_id": "contrail-query-engine"
          }, 
          {
            "cpu_info": {
              "cpu_share": 0.631145, 
              "meminfo": {
                "peakvirt": 34819244, 
                "res": 32712992, 
                "virt": 34819244
              }, 
              "num_cpu": 24
            }, 
            "instance_id": "0", 
            "module_id": "contrail-collector"
          }, 
          {
            "cpu_info": {
              "cpu_share": 0.4125, 
              "meminfo": {
                "peakvirt": 426784, 
                "res": 69632, 
                "virt": 426784
              }
            }, 
            "instance_id": "0", 
            "module_id": "contrail-alarm-gen"
          }, 
          {
            "cpu_info": {
              "cpu_share": 0.4125, 
              "meminfo": {
                "peakvirt": 401548, 
                "res": 57392, 
                "virt": 401548
              }
            }, 
            "instance_id": "0", 
            "module_id": "contrail-analytics-api"
          }
        ]
      }, 
      "NodeStatus": {
        "deleted": false, 
        "disk_usage_info": [
          {
            "partition_name": "/dev/mapper/a7s33--vg-root", 
            "partition_space_available_1k": 737918284, 
            "partition_space_used_1k": 48879628, 
            "partition_type": "ext4"
          }, 
          {
            "partition_name": "/dev/sda1", 
            "partition_space_available_1k": 192002, 
            "partition_space_used_1k": 36529, 
            "partition_type": "ext2"
          }
        ], 
        "process_info": [
          {
            "core_file_list": [], 
            "exit_count": 0, 
            "last_exit_time": null, 
            "last_start_time": "1454087761501197", 
            "last_stop_time": "1454087755583847", 
            "process_name": "contrail-topology", 
            "process_state": "PROCESS_STATE_RUNNING", 
            "start_count": 2, 
            "stop_count": 1
          }, 
          {
            "core_file_list": [], 
            "exit_count": 0, 
            "last_exit_time": null, 
            "last_start_time": "1454087743841177", 
            "last_stop_time": "1454087738321053", 
            "process_name": "contrail-snmp-collector", 
            "process_state": "PROCESS_STATE_RUNNING", 
            "start_count": 2, 
            "stop_count": 1
          }, 
          {
            "core_file_list": [], 
            "exit_count": 0, 
            "last_exit_time": null, 
            "last_start_time": "1454021671874647", 
            "last_stop_time": null, 
            "process_name": "contrail-query-engine", 
            "process_state": "PROCESS_STATE_RUNNING", 
            "start_count": 1, 
            "stop_count": 0
          }, 
          {
            "core_file_list": [], 
            "exit_count": 0, 
            "last_exit_time": null, 
            "last_start_time": "1454021668637768", 
            "last_stop_time": null, 
            "process_name": "contrail-analytics-nodemgr", 
            "process_state": "PROCESS_STATE_RUNNING", 
            "start_count": 1, 
            "stop_count": 0
          }, 
          {
            "core_file_list": [], 
            "exit_count": 0, 
            "last_exit_time": null, 
            "last_start_time": "1454368846581874", 
            "last_stop_time": "1454368840804994", 
            "process_name": "contrail-analytics-api", 
            "process_state": "PROCESS_STATE_RUNNING", 
            "start_count": 3, 
            "stop_count": 2
          }, 
          {
            "core_file_list": [], 
            "exit_count": 0, 
            "last_exit_time": null, 
            "last_start_time": "1454021671872699", 
            "last_stop_time": null, 
            "process_name": "contrail-collector", 
            "process_state": "PROCESS_STATE_RUNNING", 
            "start_count": 1, 
            "stop_count": 0
          }, 
          {
            "core_file_list": [], 
            "exit_count": 0, 
            "last_exit_time": null, 
            "last_start_time": "1454021671877119", 
            "last_stop_time": null, 
            "process_name": "contrail-alarm-gen", 
            "process_state": "PROCESS_STATE_RUNNING", 
            "start_count": 1, 
            "stop_count": 0
          }
        ], 
        "process_status": [
          {
            "connection_infos": [
              {
                "description": "Subscribe Response", 
                "name": "Collector", 
                "server_addrs": [
                  "10.84.30.201:5998"
                ], 
                "status": "Up", 
                "type": "Discovery"
              }, 
              {
                "description": "ClientInit to Established on EvSandeshCtrlMessageRecv", 
                "name": null, 
                "server_addrs": [
                  "10.84.30.201:8086"
                ], 
                "status": "Up", 
                "type": "Collector"
              }, 
              {
                "description": "Publish Response", 
                "name": "AlarmGenerator", 
                "server_addrs": [
                  "10.84.30.201:5998"
                ], 
                "status": "Up", 
                "type": "Discovery"
              }, 
              {
                "description": null, 
                "name": "Zookeeper", 
                "server_addrs": [
                  "10.84.30.201:2181"
                ], 
                "status": "Up", 
                "type": "Zookeeper"
              }, 
              {
                "name": "10.84.30.201:6379", 
                "status": "Up", 
                "type": "Redis-UVE"
              }
            ], 
            "description": null, 
            "instance_id": "0", 
            "module_id": "contrail-alarm-gen", 
            "state": "Functional"
          }, 
          {
            "connection_infos": [
              {
                "name": "Query", 
                "server_addrs": [
                  "127.0.0.1:6379"
                ], 
                "status": "Up", 
                "type": "Redis-Query"
              }, 
              {
                "description": "ClientInit to Established on EvSandeshCtrlMessageRecv", 
                "name": null, 
                "server_addrs": [
                  "10.84.30.201:8086"
                ], 
                "status": "Up", 
                "type": "Collector"
              }, 
              {
                "description": "Subscribe Response", 
                "name": "Collector", 
                "server_addrs": [
                  "10.84.30.201:5998"
                ], 
                "status": "Up", 
                "type": "Discovery"
              }, 
              {
                "description": "Subscribe Response", 
                "name": "AlarmGenerator", 
                "server_addrs": [
                  "10.84.30.201:5998"
                ], 
                "status": "Up", 
                "type": "Discovery"
              }, 
              {
                "name": "10.84.30.201:6379", 
                "status": "Up", 
                "type": "Redis-UVE"
              }, 
              {
                "description": "Partitions:15", 
                "name": "UVE-Aggregation", 
                "status": "Up", 
                "type": "UvePartitions"
              }, 
              {
                "name": "LOCAL", 
                "status": "Up", 
                "type": "Redis-UVE"
              }, 
              {
                "description": "Publish Response", 
                "name": "OpServer", 
                "server_addrs": [
                  "10.84.30.201:5998"
                ], 
                "status": "Up", 
                "type": "Discovery"
              }
            ], 
            "description": null, 
            "instance_id": "0", 
            "module_id": "contrail-analytics-api", 
            "state": "Functional"
          }, 
          {
            "connection_infos": [
              {
                "description": "Established", 
                "name": null, 
                "server_addrs": [
                  "127.0.0.1:8086"
                ], 
                "status": "Up", 
                "type": "Collector"
              }, 
              {
                "description": null, 
                "name": null, 
                "server_addrs": [
                  "0.0.0.0:65535"
                ], 
                "status": "Up", 
                "type": "Database"
              }, 
              {
                "description": null, 
                "name": "Query", 
                "server_addrs": [
                  "127.0.0.1:6379"
                ], 
                "status": "Up", 
                "type": "Redis-Query"
              }
            ], 
            "description": null, 
            "instance_id": "0", 
            "module_id": "contrail-query-engine", 
            "state": "Functional"
          }, 
          {
            "connection_infos": [
              {
                "description": "Established", 
                "name": null, 
                "server_addrs": [
                  "127.0.0.1:8086"
                ], 
                "status": "Up", 
                "type": "Collector"
              }, 
              {
                "description": null, 
                "name": "a7s33:Global", 
                "server_addrs": [
                  "0.0.0.0:65535"
                ], 
                "status": "Up", 
                "type": "Database"
              }, 
              {
                "description": "Publish Response - HeartBeat", 
                "name": "Collector", 
                "server_addrs": [
                  "10.84.30.201:5998"
                ], 
                "status": "Up", 
                "type": "Discovery"
              }, 
              {
                "description": null, 
                "name": "From", 
                "server_addrs": [
                  "127.0.0.1:6379"
                ], 
                "status": "Up", 
                "type": "Redis-UVE"
              }, 
              {
                "description": null, 
                "name": "To", 
                "server_addrs": [
                  "127.0.0.1:6379"
                ], 
                "status": "Up", 
                "type": "Redis-UVE"
              }
            ], 
            "description": null, 
            "instance_id": "0", 
            "module_id": "contrail-collector", 
            "state": "Functional"
          }, 
          {
            "description": null, 
            "instance_id": "0", 
            "module_id": "contrail-analytics-nodemgr", 
            "state": "Functional"
          }, 
          {
            "connection_infos": [
              {
                "description": "Subscribe Response", 
                "name": "Collector", 
                "server_addrs": [
                  "10.84.30.201:5998"
                ], 
                "status": "Up", 
                "type": "Discovery"
              }, 
              {
                "description": "ClientInit to Established on EvSandeshCtrlMessageRecv", 
                "name": null, 
                "server_addrs": [
                  "10.84.30.201:8086"
                ], 
                "status": "Up", 
                "type": "Collector"
              }, 
              {
                "description": "Subscribe Response", 
                "name": "ApiServer", 
                "server_addrs": [
                  "10.84.30.201:5998"
                ], 
                "status": "Up", 
                "type": "Discovery"
              }, 
              {
                "description": null, 
                "name": "Zookeeper", 
                "server_addrs": [
                  "10.84.30.201:2181"
                ], 
                "status": "Up", 
                "type": "Zookeeper"
              }, 
              {
                "description": "Connected", 
                "name": "SNMP", 
                "server_addrs": [
                  "10.84.30.201:9100"
                ], 
                "status": "Up", 
                "type": "ApiServer"
              }
            ], 
            "description": null, 
            "instance_id": "0", 
            "module_id": "contrail-snmp-collector", 
            "state": "Functional"
          }, 
          {
            "connection_infos": [
              {
                "description": "Subscribe Response", 
                "name": "Collector", 
                "server_addrs": [
                  "127.0.0.1:5998"
                ], 
                "status": "Up", 
                "type": "Discovery"
              }, 
              {
                "description": "ClientInit to Established on EvSandeshCtrlMessageRecv", 
                "name": null, 
                "server_addrs": [
                  "10.84.30.201:8086"
                ], 
                "status": "Up", 
                "type": "Collector"
              }, 
              {
                "description": null, 
                "name": "Zookeeper", 
                "server_addrs": [
                  "10.84.30.201:2181"
                ], 
                "status": "Up", 
                "type": "Zookeeper"
              }
            ], 
            "description": null, 
            "instance_id": "0", 
            "module_id": "contrail-topology", 
            "state": "Functional"
          }
        ]
      }
    }
    },
    {
    "uve-type": "config-nodes",
    "uve-key": "a7s33",
    "uve-value": 
    {
      "ConfigCpuState": {
        "cpu_info": [
          {
            "cpu_share": 0.0, 
            "inst_id": "0", 
            "mem_res": 55364, 
            "mem_virt": 311328, 
            "module_id": "contrail-svc-monitor"
          }, 
          {
            "cpu_share": 0.0, 
            "inst_id": "0", 
            "mem_res": 48812, 
            "mem_virt": 275252, 
            "module_id": "contrail-schema"
          }, 
          {
            "cpu_share": 0.4125, 
            "inst_id": "0", 
            "mem_res": 93532, 
            "mem_virt": 356960, 
            "module_id": "contrail-api"
          }
        ]
      }, 
      "ModuleCpuState": {
        "build_info": "{\"build-info\" : [{\"build-version\" : \"3.0\", \"build-time\" : \"2016-01-28 14:05:46.137577\", \"build-user\" : \"contrail-builder\", \"build-hostname\" : \"contrail-ec-build16\", \"build-git-ver\" : \"0022e08\", \"build-id\" : \"3.0-2706\", \"build-number\" : \"2706\"}]}", 
        "config_node_ip": [
          "10.84.30.201"
        ], 
        "module_cpu_info": [
          {
            "cpu_info": {
              "cpu_share": 0.0, 
              "meminfo": {
                "peakvirt": 311584, 
                "res": 55364, 
                "virt": 311328
              }, 
              "num_cpu": 24
            }, 
            "instance_id": "0", 
            "module_id": "contrail-svc-monitor"
          }, 
          {
            "cpu_info": {
              "cpu_share": 0.4125, 
              "cpuload": {
                "fifteen_min_avg": 1.12, 
                "five_min_avg": 1.05, 
                "one_min_avg": 0.8
              }, 
              "meminfo": {
                "peakvirt": 356960, 
                "res": 93532, 
                "virt": 356960
              }, 
              "num_cpu": 24, 
              "sys_mem_info": {
                "buffers": 237596, 
                "free": 19876292, 
                "total": 132008712, 
                "used": 112132420
              }
            }, 
            "instance_id": "0", 
            "module_id": "contrail-api"
          }, 
          {
            "cpu_info": {
              "cpu_share": 0.0, 
              "meminfo": {
                "peakvirt": 275252, 
                "res": 48812, 
                "virt": 275252
              }, 
              "num_cpu": 24
            }, 
            "instance_id": "0", 
            "module_id": "contrail-schema"
          }
        ]
      }, 
      "NodeStatus": {
        "deleted": false, 
        "disk_usage_info": [
          {
            "partition_name": "/dev/mapper/a7s33--vg-root", 
            "partition_space_available_1k": 737919672, 
            "partition_space_used_1k": 48878240, 
            "partition_type": "ext4"
          }, 
          {
            "partition_name": "/dev/sda1", 
            "partition_space_available_1k": 192002, 
            "partition_space_used_1k": 36529, 
            "partition_type": "ext2"
          }
        ], 
        "process_info": [
          {
            "core_file_list": [], 
            "exit_count": 0, 
            "last_exit_time": null, 
            "last_start_time": "1454107265750306", 
            "last_stop_time": null, 
            "process_name": "contrail-api:0", 
            "process_state": "PROCESS_STATE_RUNNING", 
            "start_count": 1, 
            "stop_count": 0
          }, 
          {
            "core_file_list": [], 
            "exit_count": 0, 
            "last_exit_time": null, 
            "last_start_time": "1454107265701532", 
            "last_stop_time": null, 
            "process_name": "contrail-config-nodemgr", 
            "process_state": "PROCESS_STATE_RUNNING", 
            "start_count": 1, 
            "stop_count": 0
          }, 
          {
            "core_file_list": [], 
            "exit_count": 0, 
            "last_exit_time": null, 
            "last_start_time": "1454610012973152", 
            "last_stop_time": "1454610011808756", 
            "process_name": "contrail-discovery:0", 
            "process_state": "PROCESS_STATE_RUNNING", 
            "start_count": 3, 
            "stop_count": 2
          }, 
          {
            "core_file_list": [], 
            "exit_count": 0, 
            "last_exit_time": null, 
            "last_start_time": "1454107265839177", 
            "last_stop_time": null, 
            "process_name": "contrail-svc-monitor", 
            "process_state": "PROCESS_STATE_RUNNING", 
            "start_count": 1, 
            "stop_count": 0
          }, 
          {
            "core_file_list": [], 
            "exit_count": 0, 
            "last_exit_time": null, 
            "last_start_time": "1454107265704365", 
            "last_stop_time": null, 
            "process_name": "ifmap", 
            "process_state": "PROCESS_STATE_RUNNING", 
            "start_count": 1, 
            "stop_count": 0
          }, 
          {
            "core_file_list": [], 
            "exit_count": 0, 
            "last_exit_time": null, 
            "last_start_time": "1454641987068291", 
            "last_stop_time": "1454641702800710", 
            "process_name": "contrail-device-manager", 
            "process_state": "PROCESS_STATE_RUNNING", 
            "start_count": 6, 
            "stop_count": 5
          }, 
          {
            "core_file_list": [], 
            "exit_count": 0, 
            "last_exit_time": null, 
            "last_start_time": "1454107265817193", 
            "last_stop_time": null, 
            "process_name": "contrail-schema", 
            "process_state": "PROCESS_STATE_RUNNING", 
            "start_count": 1, 
            "stop_count": 0
          }
        ], 
        "process_status": [
          {
            "connection_infos": [
              {
                "description": null, 
                "name": "Zookeeper", 
                "server_addrs": [
                  "10.84.30.201:2181"
                ], 
                "status": "Up", 
                "type": "Zookeeper"
              }, 
              {
                "description": null, 
                "name": "RabbitMQ", 
                "server_addrs": [
                  "10.84.30.201:5672"
                ], 
                "status": "Up", 
                "type": "Database"
              }, 
              {
                "description": "ClientInit to Established on EvSandeshCtrlMessageRecv", 
                "name": null, 
                "server_addrs": [
                  "10.84.30.201:8086"
                ], 
                "status": "Up", 
                "type": "Collector"
              }, 
              {
                "description": "Subscribe Response", 
                "name": "Collector", 
                "server_addrs": [
                  "10.84.30.201:5998"
                ], 
                "status": "Up", 
                "type": "Discovery"
              }, 
              {
                "description": null, 
                "name": "Cassandra", 
                "server_addrs": [
                  "10.84.30.201:9160"
                ], 
                "status": "Up", 
                "type": "Database"
              }, 
              {
                "description": null, 
                "name": "ApiServer", 
                "server_addrs": [
                  "10.84.30.201:8082"
                ], 
                "status": "Up", 
                "type": "ApiServer"
              }
            ], 
            "description": null, 
            "instance_id": "0", 
            "module_id": "DeviceManager", 
            "state": "Functional"
          }, 
          {
            "connection_infos": [
              {
                "description": null, 
                "name": "Zookeeper", 
                "server_addrs": [
                  "10.84.30.201:2181"
                ], 
                "status": "Up", 
                "type": "Zookeeper"
              }, 
              {
                "description": null, 
                "name": "RabbitMQ", 
                "server_addrs": [
                  "10.84.30.201:5672:5672"
                ], 
                "status": "Up", 
                "type": "Database"
              }, 
              {
                "description": "ClientInit to Established on EvSandeshCtrlMessageRecv", 
                "name": null, 
                "server_addrs": [
                  "10.84.30.201:8086"
                ], 
                "status": "Up", 
                "type": "Collector"
              }, 
              {
                "description": "Subscribe Response", 
                "name": "Collector", 
                "server_addrs": [
                  "10.84.30.201:5998"
                ], 
                "status": "Up", 
                "type": "Discovery"
              }, 
              {
                "description": null, 
                "name": "Cassandra", 
                "server_addrs": [
                  "10.84.30.201:9160"
                ], 
                "status": "Up", 
                "type": "Database"
              }, 
              {
                "name": "ApiServer", 
                "server_addrs": [
                  "10.84.30.201:8082"
                ], 
                "status": "Up", 
                "type": "ApiServer"
              }
            ], 
            "description": null, 
            "instance_id": "0", 
            "module_id": "contrail-svc-monitor", 
            "state": "Functional"
          }, 
          {
            "description": null, 
            "instance_id": "0", 
            "module_id": "contrail-config-nodemgr", 
            "state": "Functional"
          }, 
          {
            "connection_infos": [
              {
                "description": null, 
                "name": "Zookeeper", 
                "server_addrs": [
                  "10.84.30.201:2181"
                ], 
                "status": "Up", 
                "type": "Zookeeper"
              }, 
              {
                "description": null, 
                "name": "RabbitMQ", 
                "server_addrs": [
                  "10.84.30.201:5672:5672"
                ], 
                "status": "Up", 
                "type": "Database"
              }, 
              {
                "description": "ClientInit to Established on EvSandeshCtrlMessageRecv", 
                "name": null, 
                "server_addrs": [
                  "10.84.30.201:8086"
                ], 
                "status": "Up", 
                "type": "Collector"
              }, 
              {
                "description": "Subscribe Response", 
                "name": "Collector", 
                "server_addrs": [
                  "10.84.30.201:5998"
                ], 
                "status": "Up", 
                "type": "Discovery"
              }, 
              {
                "description": null, 
                "name": "Cassandra", 
                "server_addrs": [
                  "10.84.30.201:9160"
                ], 
                "status": "Up", 
                "type": "Database"
              }, 
              {
                "description": null, 
                "name": "ApiServer", 
                "server_addrs": [
                  "10.84.30.201:8082"
                ], 
                "status": "Up", 
                "type": "ApiServer"
              }
            ], 
            "description": null, 
            "instance_id": "0", 
            "module_id": "contrail-schema", 
            "state": "Functional"
          }, 
          {
            "connection_infos": [
              {
                "description": null, 
                "name": "IfMap", 
                "server_addrs": [
                  "10.84.30.201:8443"
                ], 
                "status": "Up", 
                "type": "IFMap"
              }, 
              {
                "description": "ClientInit to Established on EvSandeshCtrlMessageRecv", 
                "name": null, 
                "server_addrs": [
                  "10.84.30.201:8086"
                ], 
                "status": "Up", 
                "type": "Collector"
              }, 
              {
                "description": null, 
                "name": "RabbitMQ", 
                "server_addrs": [
                  "10.84.30.201:5672:5672"
                ], 
                "status": "Up", 
                "type": "Database"
              }, 
              {
                "description": null, 
                "name": "Zookeeper", 
                "server_addrs": [
                  "10.84.30.201:2181"
                ], 
                "status": "Up", 
                "type": "Zookeeper"
              }, 
              {
                "description": "Publish Response", 
                "name": "ApiServer", 
                "server_addrs": [
                  "10.84.30.201:5998"
                ], 
                "status": "Up", 
                "type": "Discovery"
              }, 
              {
                "description": "Publish Response", 
                "name": "IfmapServer", 
                "server_addrs": [
                  "10.84.30.201:5998"
                ], 
                "status": "Up", 
                "type": "Discovery"
              }, 
              {
                "description": "Subscribe Response", 
                "name": "Collector", 
                "server_addrs": [
                  "10.84.30.201:5998"
                ], 
                "status": "Up", 
                "type": "Discovery"
              }, 
              {
                "description": null, 
                "name": "Cassandra", 
                "server_addrs": [
                  "10.84.30.201:9160"
                ], 
                "status": "Up", 
                "type": "Database"
              }
            ], 
            "description": null, 
            "instance_id": "0", 
            "module_id": "contrail-api", 
            "state": "Functional"
          }
        ]
      }
    }
    },
    {
    "uve-type": "virtual-machines",
    "uve-key": "97427379-dc73-4e1b-91b3-54f6bd8b3d5d",
    "uve-value": 
    {
      "UveVirtualMachineAgent": {
        "cpu_info": {
          "cpu_one_min_avg": 0.0, 
          "disk_allocated_bytes": 4294967295, 
          "disk_used_bytes": 12525568, 
          "peak_virt_memory": 7463072, 
          "rss": 249160, 
          "virt_memory": 7011448, 
          "vm_memory_quota": 2097152
        }, 
        "interface_list": [
          "default-domain:admin:56408f9a-bc97-42ef-8872-5be449817ca5"
        ], 
        "tcp_dport_bitmap": [
          "1", 
          "0", 
          "0", 
          "0", 
          "0", 
          "8192", 
          "0", 
          "0"
        ], 
        "tcp_sport_bitmap": [
          "1", 
          "0", 
          "0", 
          "0", 
          "0", 
          "9728", 
          "0", 
          "0"
        ], 
        "udp_dport_bitmap": [
          "1", 
          "0", 
          "0", 
          "0", 
          "0", 
          "0", 
          "0", 
          "0"
        ], 
        "udp_sport_bitmap": [
          "1", 
          "0", 
          "0", 
          "0", 
          "9602", 
          "546571019", 
          "18123336", 
          "18"
        ], 
        "uuid": "97427379-dc73-4e1b-91b3-54f6bd8b3d5d", 
        "vm_name": "vn1-vm1", 
        "vrouter": "a7s29"
      }, 
      "VirtualMachineStats": {
        "cpu_stats": [
          {
            "cpu_one_min_avg": 0.0, 
            "disk_allocated_bytes": 4294967295, 
            "disk_used_bytes": 12525568, 
            "peak_virt_memory": 7463072, 
            "rss": 249160, 
            "virt_memory": 7011448, 
            "vm_memory_quota": 2097152
          }
        ]
      }
    }
    },
    {
    "uve-type": "control-nodes",
    "uve-key": "a7s33",
    "uve-value": 
    {
      "BgpRouterState": {
        "admin_down": false, 
        "bgp_router_ip_list": [
          "10.84.30.201"
        ], 
        "build_info": "{\"build-info\":[{\"build-time\":\"2016-01-28 14:05:58.663583\",\"build-hostname\":\"contrail-ec-build16\",\"build-git-ver\":\"0022e08\",\"build-user\":\"contrail-builder\",\"build-version\":\"3.0\",\"build-id\":\"3.0-2706\",\"build-number\":\"2706\"}]}", 
        "global_asn": 64512, 
        "ifmap_info": {
          "connection_status": "Up", 
          "connection_status_change_at": 1454107267924300, 
          "url": "10.84.30.201:8443"
        }, 
        "ifmap_server_info": {
          "num_peer_clients": 4
        }, 
        "local_asn": 64512, 
        "num_bgp_peer": 1, 
        "num_closing_bgp_peer": 0, 
        "num_closing_xmpp_peer": 0, 
        "num_deleted_routing_instance": 0, 
        "num_down_service_chains": 0, 
        "num_down_static_routes": 0, 
        "num_routing_instance": 9, 
        "num_service_chains": 0, 
        "num_static_routes": 0, 
        "num_up_bgp_peer": 1, 
        "num_up_xmpp_peer": 4, 
        "num_xmpp_peer": 4, 
        "output_queue_depth": 0, 
        "router_id": "10.84.30.201", 
        "uptime": 1454021640802275
      }, 
      "ControlCpuState": {
        "cpu_info": [
          {
            "cpu_share": 0.0868056, 
            "inst_id": "0", 
            "mem_res": 43076, 
            "mem_virt": 1916808, 
            "module_id": "contrail-control"
          }
        ]
      }, 
      "NodeStatus": {
        "deleted": false, 
        "disk_usage_info": [
          {
            "partition_name": "/dev/mapper/a7s33--vg-root", 
            "partition_space_available_1k": 737917748, 
            "partition_space_used_1k": 48880164, 
            "partition_type": "ext4"
          }, 
          {
            "partition_name": "/dev/sda1", 
            "partition_space_available_1k": 192002, 
            "partition_space_used_1k": 36529, 
            "partition_type": "ext2"
          }
        ], 
        "process_info": [
          {
            "core_file_list": [], 
            "exit_count": 0, 
            "last_exit_time": null, 
            "last_start_time": "1454021646206680", 
            "last_stop_time": null, 
            "process_name": "contrail-control", 
            "process_state": "PROCESS_STATE_RUNNING", 
            "start_count": 1, 
            "stop_count": 0
          }, 
          {
            "core_file_list": [], 
            "exit_count": 0, 
            "last_exit_time": null, 
            "last_start_time": "1454021642354835", 
            "last_stop_time": null, 
            "process_name": "contrail-control-nodemgr", 
            "process_state": "PROCESS_STATE_RUNNING", 
            "start_count": 1, 
            "stop_count": 0
          }, 
          {
            "core_file_list": [], 
            "exit_count": 0, 
            "last_exit_time": null, 
            "last_start_time": "1454021652222040", 
            "last_stop_time": null, 
            "process_name": "contrail-dns", 
            "process_state": "PROCESS_STATE_RUNNING", 
            "start_count": 1, 
            "stop_count": 0
          }, 
          {
            "core_file_list": [], 
            "exit_count": 0, 
            "last_exit_time": null, 
            "last_start_time": "1454021646208942", 
            "last_stop_time": null, 
            "process_name": "contrail-named", 
            "process_state": "PROCESS_STATE_RUNNING", 
            "start_count": 1, 
            "stop_count": 0
          }
        ], 
        "process_status": [
          {
            "description": null, 
            "instance_id": "0", 
            "module_id": "contrail-control-nodemgr", 
            "state": "Functional"
          }, 
          {
            "connection_infos": [
              {
                "description": "Connection with IFMap Server (irond)", 
                "name": "IFMapServer", 
                "server_addrs": [
                  "10.84.30.201:8443"
                ], 
                "status": "Up", 
                "type": "IFMap"
              }, 
              {
                "description": "Established", 
                "name": null, 
                "server_addrs": [
                  "10.84.30.201:8086"
                ], 
                "status": "Up", 
                "type": "Collector"
              }, 
              {
                "description": "SubscribeResponse", 
                "name": "Collector", 
                "server_addrs": [
                  "10.84.30.201:5998"
                ], 
                "status": "Up", 
                "type": "Discovery"
              }, 
              {
                "description": "SubscribeResponse", 
                "name": "IfmapServer", 
                "server_addrs": [
                  "10.84.30.201:5998"
                ], 
                "status": "Up", 
                "type": "Discovery"
              }, 
              {
                "description": "Publish Response - HeartBeat", 
                "name": "xmpp-server", 
                "server_addrs": [
                  "10.84.30.201:5998"
                ], 
                "status": "Up", 
                "type": "Discovery"
              }
            ], 
            "description": null, 
            "instance_id": "0", 
            "module_id": "contrail-control", 
            "state": "Functional"
          }
        ]
      }
    }
    },
    {
    "uve-type": "prouters",
    "uve-key": "a7-mx80-1",
    "uve-value": 
    {
      "PRouterEntry": {
        "arpTable": [
          {
            "ip": "10.84.61.203", 
            "localIfIndex": 13, 
            "mac": "28:8a:1c:50:b0:ff"
          }, 
          {
            "ip": "10.0.0.4", 
            "localIfIndex": 18, 
            "mac": "02:00:00:00:00:04"
          }, 
    #...
          {
            "ip": "10.84.30.142", 
            "localIfIndex": 588, 
            "mac": "28:8a:1c:50:b0:c0"
          }
        ], 
        "ifIndexOperStatusTable": [
          {
            "ifIndex": 512, 
            "ifOperStatus": 1
          }, 
    #...
          {
            "ifIndex": 511, 
            "ifOperStatus": 1
          }
        ], 
        "ifStats": [
          {
            "ifInDiscards": 0, 
            "ifInErrors": 0, 
            "ifInOctets": 0, 
            "ifInPkts": 0, 
            "ifIndex": 501, 
            "ifName": "demux0", 
            "ifOutDiscards": 0, 
            "ifOutErrors": 0, 
            "ifOutOctets": 0, 
            "ifOutPkts": 0
          }, 
    #...
          {
            "ifInDiscards": 0, 
            "ifInErrors": 0, 
            "ifInOctets": 0, 
            "ifInPkts": 0, 
            "ifIndex": 513, 
            "ifName": "xe-0/0/1", 
            "ifOutDiscards": 0, 
            "ifOutErrors": 0, 
            "ifOutOctets": 0, 
            "ifOutPkts": 0
          }
        ], 
        "ifTable": [
          {
            "ifAdminStatus": 1, 
            "ifDescr": "xe-0/0/0", 
            "ifInDiscards": 0, 
            "ifInErrors": 0, 
            "ifInNUcastPkts": 0, 
            "ifInOctets": 0, 
            "ifInUcastPkts": 0, 
            "ifInUnknownProtos": 0, 
            "ifIndex": 512, 
            "ifLastChange": 833397, 
            "ifMtu": 1514, 
            "ifOperStatus": 1, 
            "ifOutDiscards": 0, 
            "ifOutErrors": 0, 
            "ifOutNUcastPkts": 17894, 
            "ifOutOctets": 3739685, 
            "ifOutQLen": 0, 
            "ifOutUcastPkts": 0, 
            "ifPhysAddress": "28:8a:1c:50:b0:00", 
            "ifSpecific": ".0.0", 
            "ifSpeed": -1, 
            "ifType": 6
          }, 
    #...
          {
            "ifAdminStatus": 1, 
            "ifDescr": "pfh-0/0/0.16383", 
            "ifInDiscards": 0, 
            "ifInErrors": 0, 
            "ifInNUcastPkts": 0, 
            "ifInOctets": 0, 
            "ifInUcastPkts": 0, 
            "ifInUnknownProtos": 0, 
            "ifIndex": 511, 
            "ifLastChange": 6269, 
            "ifMtu": 2147483647, 
            "ifOperStatus": 1, 
            "ifOutDiscards": 0, 
            "ifOutErrors": 0, 
            "ifOutNUcastPkts": 0, 
            "ifOutOctets": 0, 
            "ifOutQLen": 0, 
            "ifOutUcastPkts": 0, 
            "ifPhysAddress": null, 
            "ifSpecific": ".0.0", 
            "ifSpeed": 0, 
            "ifType": 53
          }
        ], 
        "ifXTable": [
          {
            "ifAlias": null, 
            "ifConnectorPresent": 1, 
            "ifCounterDiscontinuityTime": 0, 
            "ifHCInBroadcastPkts": 0, 
            "ifHCInMulticastPkts": 0, 
            "ifHCInOctets": 0, 
            "ifHCInUcastPkts": 0, 
            "ifHCOutBroadcastPkts": 1, 
            "ifHCOutMulticastPkts": 17893, 
            "ifHCOutOctets": 3739685, 
            "ifHCOutUcastPkts": 0, 
            "ifHighSpeed": 10000, 
            "ifInBroadcastPkts": 0, 
            "ifInMulticastPkts": 0, 
            "ifIndex": 512, 
            "ifLinkUpDownTrapEnable": 1, 
            "ifName": "xe-0/0/0", 
            "ifOutBroadcastPkts": 1, 
            "ifOutMulticastPkts": 17893, 
            "ifPromiscuousMode": 2
          }, 
    #...
          {
            "ifAlias": null, 
            "ifConnectorPresent": 2, 
            "ifCounterDiscontinuityTime": 0, 
            "ifHCInBroadcastPkts": 0, 
            "ifHCInMulticastPkts": 0, 
            "ifHCInOctets": 0, 
            "ifHCInUcastPkts": 0, 
            "ifHCOutBroadcastPkts": 0, 
            "ifHCOutMulticastPkts": 0, 
            "ifHCOutOctets": 0, 
            "ifHCOutUcastPkts": 0, 
            "ifHighSpeed": 0, 
            "ifInBroadcastPkts": 0, 
            "ifInMulticastPkts": 0, 
            "ifIndex": 511, 
            "ifLinkUpDownTrapEnable": 1, 
            "ifName": "pfh-0/0/0.16383", 
            "ifOutBroadcastPkts": 0, 
            "ifOutMulticastPkts": 0, 
            "ifPromiscuousMode": 2
          }
        ], 
        "ipMib": [
          {
            "ifIndex": 18, 
            "ipAdEntIfIndex": "10.0.0.4"
          }, 
          {
            "ifIndex": 588, 
            "ipAdEntIfIndex": "10.84.30.142"
          }, 
          {
            "ifIndex": 559, 
            "ipAdEntIfIndex": "10.84.30.146"
          }, 
          {
            "ifIndex": 556, 
            "ipAdEntIfIndex": "10.84.30.149"
          }, 
          {
            "ifIndex": 572, 
            "ipAdEntIfIndex": "10.84.30.158"
          }, 
          {
            "ifIndex": 573, 
            "ipAdEntIfIndex": "10.84.30.166"
          }, 
          {
            "ifIndex": 574, 
            "ipAdEntIfIndex": "10.84.30.174"
          }, 
          {
            "ifIndex": 570, 
            "ipAdEntIfIndex": "10.84.30.246"
          }, 
          {
            "ifIndex": 13, 
            "ipAdEntIfIndex": "10.84.61.203"
          }, 
          {
            "ifIndex": 21, 
            "ipAdEntIfIndex": "127.0.0.1"
          }, 
          {
            "ifIndex": 18, 
            "ipAdEntIfIndex": "128.0.0.1"
          }, 
          {
            "ifIndex": 18, 
            "ipAdEntIfIndex": "128.0.0.4"
          }
        ], 
        "lldpTable": {
          "lldpLocalSystemData": {
            "lldpLocChassisId": "28:8a:1c:50:b0:c0", 
            "lldpLocChassisIdSubtype": 4, 
            "lldpLocManAddrEntry": {
              "lldpLocManAddr": "10.84.61.203", 
              "lldpLocManAddrOID": ".1.3.6.1.2.1.31.1.1.1.1.1", 
              "lldpLocManAddrOIDLen": 4, 
              "lldpLocManAddrSubtype": 1
            }, 
            "lldpLocPortTable": [
              {
                "lldpLocPortDesc": "ge-1/2/9", 
                "lldpLocPortId": "545", 
                "lldpLocPortIdSubtype": 7, 
                "lldpLocPortNum": 545
              }, 
              {
                "lldpLocPortDesc": "ge-1/0/0", 
                "lldpLocPortId": "516", 
                "lldpLocPortIdSubtype": 7, 
                "lldpLocPortNum": 516
              }, 
              {
                "lldpLocPortDesc": "ge-1/0/1", 
                "lldpLocPortId": "517", 
                "lldpLocPortIdSubtype": 7, 
                "lldpLocPortNum": 517
              }, 
              {
                "lldpLocPortDesc": "ge-1/0/2", 
                "lldpLocPortId": "518", 
                "lldpLocPortIdSubtype": 7, 
                "lldpLocPortNum": 518
              }, 
              {
                "lldpLocPortDesc": "ge-1/0/3", 
                "lldpLocPortId": "519", 
                "lldpLocPortIdSubtype": 7, 
                "lldpLocPortNum": 519
              }, 
              {
                "lldpLocPortDesc": "ge-1/2/5", 
                "lldpLocPortId": "541", 
                "lldpLocPortIdSubtype": 7, 
                "lldpLocPortNum": 541
              }, 
              {
                "lldpLocPortDesc": "ge-1/2/6", 
                "lldpLocPortId": "542", 
                "lldpLocPortIdSubtype": 7, 
                "lldpLocPortNum": 542
              }
            ], 
            "lldpLocSysCapEnabled": [
              "2", 
              "4"
            ], 
            "lldpLocSysCapSupported": [
              "2", 
              "4"
            ], 
            "lldpLocSysDesc": "Juniper Networks, Inc. mx80 , version 12.3R4.6 Build date: 2013-09-13 04:30:20 UTC", 
            "lldpLocSysName": "a7-mx80-1"
          }, 
          "lldpRemoteSystemsData": [
            {
              "lldpRemChassisId": "54:e0:32:88:73:80", 
              "lldpRemChassisIdSubtype": 4, 
              "lldpRemIndex": 47, 
              "lldpRemLocalPortNum": 519, 
              "lldpRemOrgDefInfoEntry": {
                "lldpRemOrgDefInfoOUI": "01815", 
                "lldpRemOrgDefInfoSubtype": 1, 
                "lldpRemOrgDefInfoTable": [
                  {
                    "lldpRemOrgDefInfo": "00:12:0f:01:03", 
                    "lldpRemOrgDefInfoIndex": 1
                  }, 
                  {
                    "lldpRemOrgDefInfo": "00:12:0f:03:03", 
                    "lldpRemOrgDefInfoIndex": 2
                  }, 
                  {
                    "lldpRemOrgDefInfo": "00:12", 
                    "lldpRemOrgDefInfoIndex": 3
                  }, 
                  {
                    "lldpRemOrgDefInfo": "00:90:69:01:46:50:30:32:31:33:30:34", 
                    "lldpRemOrgDefInfoIndex": 4
                  }, 
                  {
                    "lldpRemOrgDefInfo": "00:12:bb", 
                    "lldpRemOrgDefInfoIndex": 5
                  }
                ]
              }, 
              "lldpRemPortDesc": "ge-0/0/5.0", 
              "lldpRemPortId": "513", 
              "lldpRemPortIdSubtype": 7, 
              "lldpRemSysCapEnabled": [
                "2", 
                "4"
              ], 
              "lldpRemSysCapSupported": [
                "2", 
                "4"
              ], 
              "lldpRemSysDesc": "Juniper Networks, Inc. ex4200-48px , version 12.3R9.4 Build date: 2015-02-12 12:01:56 UTC", 
              "lldpRemSysName": "a7-ex2", 
              "lldpRemTimeMark": 16931094
            }, 
            {
              "lldpRemChassisId": "10:0e:7e:ab:df:80", 
              "lldpRemChassisIdSubtype": 4, 
              "lldpRemIndex": 53, 
              "lldpRemLocalPortNum": 542, 
              "lldpRemOrgDefInfoEntry": {
                "lldpRemOrgDefInfoOUI": "01815", 
                "lldpRemOrgDefInfoSubtype": 1, 
                "lldpRemOrgDefInfoTable": [
                  {
                    "lldpRemOrgDefInfo": "00:12:0f:01:00", 
                    "lldpRemOrgDefInfoIndex": 1
                  }, 
                  {
                    "lldpRemOrgDefInfo": "00:12:0f:03:01", 
                    "lldpRemOrgDefInfoIndex": 2
                  }, 
                  {
                    "lldpRemOrgDefInfo": "00:12", 
                    "lldpRemOrgDefInfoIndex": 3
                  }, 
                  {
                    "lldpRemOrgDefInfo": "00:90:69:01:54:41:33:37:31:34:30:34", 
                    "lldpRemOrgDefInfoIndex": 4
                  }, 
                  {
                    "lldpRemOrgDefInfo": "00:12:bb", 
                    "lldpRemOrgDefInfoIndex": 5
                  }
                ]
              }, 
              "lldpRemPortDesc": "ge-0/0/1", 
              "lldpRemPortId": "531", 
              "lldpRemPortIdSubtype": 7, 
              "lldpRemSysCapEnabled": [
                "2", 
                "4"
              ], 
              "lldpRemSysCapSupported": [
                "2", 
                "4"
              ], 
              "lldpRemSysDesc": "Juniper Networks, Inc. qfx5100-48s-6q Ethernet Switch, kernel JUNOS 14.1X53-D30.6, Build date: 2015-11-19 04:56:28 UTC Copyright (c) 1996-2015 Juniper Networks, Inc.", 
              "lldpRemSysName": "a7-qfx4", 
              "lldpRemTimeMark": 19118894
            }, 
            {
              "lldpRemChassisId": "b0:00:b4:8b:e1:80", 
              "lldpRemChassisIdSubtype": 4, 
              "lldpRemIndex": 9, 
              "lldpRemLocalPortNum": 545, 
              "lldpRemManAddrEntry": {
                "lldpRemManAddr": "10.84.30.157", 
                "lldpRemManAddrIfId": 1, 
                "lldpRemManAddrIfSubtype": 3, 
                "lldpRemManAddrOIDLen": 4, 
                "lldpRemManAddrSubtype": 1, 
                "lldpRemTimeMark": 1289864
              }, 
              "lldpRemOrgDefInfoEntry": {
                "lldpRemOrgDefInfoOUI": "01815", 
                "lldpRemOrgDefInfoSubtype": 1, 
                "lldpRemOrgDefInfoTable": [
                  {
                    "lldpRemOrgDefInfo": "00:12:0f:01:03", 
                    "lldpRemOrgDefInfoIndex": 1
                  }
                ]
              }, 
              "lldpRemPortDesc": "GigabitEthernet1/0/1", 
              "lldpRemPortId": "Gi1/0/1", 
              "lldpRemPortIdSubtype": 5, 
              "lldpRemSysCapEnabled": [
                "2", 
                "4"
              ], 
              "lldpRemSysCapSupported": [
                "2", 
                "4"
              ], 
              "lldpRemSysDesc": "Cisco IOS Software, C2960X Software (C2960X-UNIVERSALK9-M), Version 15.0(2)EX4, RELEASE SOFTWARE (fc1)\nTechnical Support: http://www.cisco.com/techsupport\nCopyright (c) 1986-2013 by Cisco Systems, Inc.\nCompiled Thu 14-Nov-13 11:33 by prod_rel_team", 
              "lldpRemSysName": "a7-c2960", 
              "lldpRemTimeMark": 1289864
            }, 
            {
              "lldpRemChassisId": "3c:94:d5:90:4b:80", 
              "lldpRemChassisIdSubtype": 4, 
              "lldpRemIndex": 13, 
              "lldpRemLocalPortNum": 518, 
              "lldpRemOrgDefInfoEntry": {
                "lldpRemOrgDefInfoOUI": "01815", 
                "lldpRemOrgDefInfoSubtype": 1, 
                "lldpRemOrgDefInfoTable": [
                  {
                    "lldpRemOrgDefInfo": "00:12:0f:01:03", 
                    "lldpRemOrgDefInfoIndex": 1
                  }, 
                  {
                    "lldpRemOrgDefInfo": "00:12:0f:03:01", 
                    "lldpRemOrgDefInfoIndex": 2
                  }, 
                  {
                    "lldpRemOrgDefInfo": "00:12", 
                    "lldpRemOrgDefInfoIndex": 3
                  }, 
                  {
                    "lldpRemOrgDefInfo": "00:90:69:01:42:50:30:32:31:33:31:39", 
                    "lldpRemOrgDefInfoIndex": 4
                  }, 
                  {
                    "lldpRemOrgDefInfo": "00:12:bb", 
                    "lldpRemOrgDefInfoIndex": 5
                  }
                ]
              }, 
              "lldpRemPortDesc": "ge-0/0/46.0", 
              "lldpRemPortId": "596", 
              "lldpRemPortIdSubtype": 7, 
              "lldpRemSysCapEnabled": [
                "2", 
                "4"
              ], 
              "lldpRemSysCapSupported": [
                "2", 
                "4"
              ], 
              "lldpRemSysDesc": "Juniper Networks, Inc. ex4200-48t , version 11.4R7.5 Build date: 2013-03-01 10:55:26 UTC", 
              "lldpRemSysName": "a7-ex1", 
              "lldpRemTimeMark": 1289881
            }, 
            {
              "lldpRemChassisId": "10:0e:7e:bf:0f:00", 
              "lldpRemChassisIdSubtype": 4, 
              "lldpRemIndex": 52, 
              "lldpRemLocalPortNum": 541, 
              "lldpRemOrgDefInfoEntry": {
                "lldpRemOrgDefInfoOUI": "01815", 
                "lldpRemOrgDefInfoSubtype": 1, 
                "lldpRemOrgDefInfoTable": [
                  {
                    "lldpRemOrgDefInfo": "00:12:0f:01:00", 
                    "lldpRemOrgDefInfoIndex": 1
                  }, 
                  {
                    "lldpRemOrgDefInfo": "00:12:0f:03:01", 
                    "lldpRemOrgDefInfoIndex": 2
                  }, 
                  {
                    "lldpRemOrgDefInfo": "00:12", 
                    "lldpRemOrgDefInfoIndex": 3
                  }, 
                  {
                    "lldpRemOrgDefInfo": "00:90:69:01:54:41:33:37:31:34:30:34", 
                    "lldpRemOrgDefInfoIndex": 4
                  }, 
                  {
                    "lldpRemOrgDefInfo": "00:12:bb", 
                    "lldpRemOrgDefInfoIndex": 5
                  }
                ]
              }, 
              "lldpRemPortDesc": "ge-0/0/1", 
              "lldpRemPortId": "514", 
              "lldpRemPortIdSubtype": 7, 
              "lldpRemSysCapEnabled": [
                "2", 
                "4"
              ], 
              "lldpRemSysCapSupported": [
                "2", 
                "4"
              ], 
              "lldpRemSysDesc": "Juniper Networks, Inc. qfx5100-48s-6q Ethernet Switch, kernel JUNOS 14.1X53-D30.6, Build date: 2015-11-19 04:56:28 UTC Copyright (c) 1996-2015 Juniper Networks, Inc.", 
              "lldpRemSysName": "a7-qfx3", 
              "lldpRemTimeMark": 19118859
            }, 
            {
              "lldpRemChassisId": "3c:8a:b0:1a:61:00", 
              "lldpRemChassisIdSubtype": 4, 
              "lldpRemIndex": 14, 
              "lldpRemLocalPortNum": 517, 
              "lldpRemOrgDefInfoEntry": {
                "lldpRemOrgDefInfoOUI": "01815", 
                "lldpRemOrgDefInfoSubtype": 1, 
                "lldpRemOrgDefInfoTable": [
                  {
                    "lldpRemOrgDefInfo": "00:12:0f:01:03", 
                    "lldpRemOrgDefInfoIndex": 1
                  }, 
                  {
                    "lldpRemOrgDefInfo": "00:12:0f", 
                    "lldpRemOrgDefInfoIndex": 2
                  }, 
                  {
                    "lldpRemOrgDefInfo": "00:12:0f:03:01", 
                    "lldpRemOrgDefInfoIndex": 3
                  }, 
                  {
                    "lldpRemOrgDefInfo": "00:12", 
                    "lldpRemOrgDefInfoIndex": 4
                  }, 
                  {
                    "lldpRemOrgDefInfo": "00:90:69:01:42:50:30:32:31:33:32:33", 
                    "lldpRemOrgDefInfoIndex": 5
                  }, 
                  {
                    "lldpRemOrgDefInfo": "00:12:bb", 
                    "lldpRemOrgDefInfoIndex": 6
                  }, 
                  {
                    "lldpRemOrgDefInfo": "00:12:bb", 
                    "lldpRemOrgDefInfoIndex": 7
                  }
                ]
              }, 
              "lldpRemPortDesc": "ge-0/0/0.0", 
              "lldpRemPortId": "503", 
              "lldpRemPortIdSubtype": 7, 
              "lldpRemSysCapEnabled": [
                "2", 
                "4"
              ], 
              "lldpRemSysCapSupported": [
                "2", 
                "4"
              ], 
              "lldpRemSysDesc": "Juniper Networks, Inc. ex4200-48t , version 12.3R4.6 Build date: 2013-09-13 04:12:57 UTC", 
              "lldpRemSysName": "a7-ex3", 
              "lldpRemTimeMark": 1716371
            }, 
            {
              "lldpRemChassisId": "54:e0:32:88:73:80", 
              "lldpRemChassisIdSubtype": 4, 
              "lldpRemIndex": 46, 
              "lldpRemLocalPortNum": 516, 
              "lldpRemOrgDefInfoEntry": {
                "lldpRemOrgDefInfoOUI": "01815", 
                "lldpRemOrgDefInfoSubtype": 1, 
                "lldpRemOrgDefInfoTable": [
                  {
                    "lldpRemOrgDefInfo": "00:12:0f:01:03", 
                    "lldpRemOrgDefInfoIndex": 1
                  }, 
                  {
                    "lldpRemOrgDefInfo": "00:12:0f:03:03", 
                    "lldpRemOrgDefInfoIndex": 2
                  }, 
                  {
                    "lldpRemOrgDefInfo": "00:12", 
                    "lldpRemOrgDefInfoIndex": 3
                  }, 
                  {
                    "lldpRemOrgDefInfo": "00:90:69:01:46:50:30:32:31:33:30:34", 
                    "lldpRemOrgDefInfoIndex": 4
                  }, 
                  {
                    "lldpRemOrgDefInfo": "00:12:bb", 
                    "lldpRemOrgDefInfoIndex": 5
                  }
                ]
              }, 
              "lldpRemPortDesc": "ge-0/0/0.0", 
              "lldpRemPortId": "503", 
              "lldpRemPortIdSubtype": 7, 
              "lldpRemSysCapEnabled": [
                "2", 
                "4"
              ], 
              "lldpRemSysCapSupported": [
                "2", 
                "4"
              ], 
              "lldpRemSysDesc": "Juniper Networks, Inc. ex4200-48px , version 12.3R9.4 Build date: 2015-02-12 12:01:56 UTC", 
              "lldpRemSysName": "a7-ex2", 
              "lldpRemTimeMark": 16931093
            }
          ]
        }
      }, 
      "PRouterFlowEntry": {
        "flow_export_source_ip": "10.84.30.149"
      }, 
      "PRouterLinkEntry": {
        "link_table": [
          {
            "local_interface_index": 519, 
            "local_interface_name": "ge-1/0/3", 
            "remote_interface_index": 513, 
            "remote_interface_name": "ge-0/0/5.0", 
            "remote_system_name": "a7-ex2", 
            "type": 1
          }, 
          {
            "local_interface_index": 542, 
            "local_interface_name": "ge-1/2/6", 
            "remote_interface_index": 531, 
            "remote_interface_name": "ge-0/0/1", 
            "remote_system_name": "a7-qfx4", 
            "type": 1
          }, 
          {
            "local_interface_index": 545, 
            "local_interface_name": "ge-1/2/9", 
            "remote_interface_index": 10101, 
            "remote_interface_name": "GigabitEthernet1/0/1", 
            "remote_system_name": "a7-c2960", 
            "type": 1
          }, 
          {
            "local_interface_index": 518, 
            "local_interface_name": "ge-1/0/2", 
            "remote_interface_index": 596, 
            "remote_interface_name": "ge-0/0/46.0", 
            "remote_system_name": "a7-ex1", 
            "type": 1
          }, 
          {
            "local_interface_index": 541, 
            "local_interface_name": "ge-1/2/5", 
            "remote_interface_index": 514, 
            "remote_interface_name": "ge-0/0/1", 
            "remote_system_name": "a7-qfx3", 
            "type": 1
          }, 
          {
            "local_interface_index": 517, 
            "local_interface_name": "ge-1/0/1", 
            "remote_interface_index": 503, 
            "remote_interface_name": "ge-0/0/0.0", 
            "remote_system_name": "a7-ex3", 
            "type": 1
          }, 
          {
            "local_interface_index": 516, 
            "local_interface_name": "ge-1/0/0", 
            "remote_interface_index": 503, 
            "remote_interface_name": "ge-0/0/0.0", 
            "remote_system_name": "a7-ex2", 
            "type": 1
          }
        ]
      }, 
      "UvePhysicalRouterConfig": {
        "auto_conf_enabled": true, 
        "commit_status_message": "success", 
        "connected_bgp_router": "126397c5-4a75-4b45-89c6-8c00ad86579d", 
        "ip_address": "10.84.30.149", 
        "last_commit_duration": "7.26668596268", 
        "last_commit_time": "2016-02-04 19:13:17", 
        "netconf_enabled_status": true, 
        "product_info": "Juniper:MX", 
        "total_commits_sent_since_up": 1
      }
    }
    },
    {
    "uve-type": "database-nodes",
    "uve-key": "a7s33",
    "uve-value": 
    {
      "DatabaseUsageInfo": {
        "database_usage": [
          {
            "analytics_db_size_1k": 16037836, 
            "disk_space_available_1k": 737917692, 
            "disk_space_used_1k": 48880220
          }
        ]
      }, 
      "NodeStatus": {
        "deleted": false, 
        "disk_usage_info": [
          {
            "partition_name": "/dev/mapper/a7s33--vg-root", 
            "partition_space_available_1k": 737917368, 
            "partition_space_used_1k": 48880544, 
            "partition_type": "ext4"
          }, 
          {
            "partition_name": "/dev/sda1", 
            "partition_space_available_1k": 192002, 
            "partition_space_used_1k": 36529, 
            "partition_type": "ext2"
          }
        ], 
        "process_info": [
          {
            "core_file_list": [], 
            "exit_count": 0, 
            "last_exit_time": null, 
            "last_start_time": "1454021096352632", 
            "last_stop_time": null, 
            "process_name": "contrail-database-nodemgr", 
            "process_state": "PROCESS_STATE_RUNNING", 
            "start_count": 1, 
            "stop_count": 0
          }, 
          {
            "core_file_list": [], 
            "exit_count": 0, 
            "last_exit_time": null, 
            "last_start_time": "1454021096354946", 
            "last_stop_time": null, 
            "process_name": "kafka", 
            "process_state": "PROCESS_STATE_RUNNING", 
            "start_count": 1, 
            "stop_count": 0
          }
        ], 
        "process_status": [
          {
            "description": null, 
            "instance_id": "0", 
            "module_id": "contrail-database-nodemgr", 
            "state": "Functional"
          }
        ]
      }
    }
    },
    {
    "uve-type": "virtual-machine-interfaces",
    "uve-key": "default-domain:admin:7322c95c-4a52-4496-b3a9-365de52e5dc7",
    "uve-value": 
    {
      "UveVMInterfaceAgent": {
        "active": true, 
        "gateway": "2.2.2.1", 
        "if_stats": {
          "in_bytes": 294, 
          "in_pkts": 3, 
          "out_bytes": 0, 
          "out_pkts": 0
        }, 
        "in_bw_usage": 0, 
        "ip4_active": true, 
        "ip6_active": false, 
        "ip6_address": "::", 
        "ip_address": "2.2.2.5", 
        "l2_active": true, 
        "label": 16, 
        "mac_address": "02:73:22:c9:5c:4a", 
        "out_bw_usage": 0, 
        "port_bucket_bmap": {
          "tcp_dport_bitmap": [
            "1", 
            "0", 
            "0", 
            "0", 
            "0", 
            "4194370", 
            "262144", 
            "4"
          ], 
          "tcp_sport_bitmap": [
            "1", 
            "0", 
            "0", 
            "0", 
            "0", 
            "4194370", 
            "262144", 
            "4"
          ], 
          "udp_dport_bitmap": [
            "1", 
            "0", 
            "0", 
            "0", 
            "0", 
            "0", 
            "0", 
            "0"
          ], 
          "udp_sport_bitmap": [
            "0", 
            "0", 
            "0", 
            "0", 
            "67108864", 
            "1610612800", 
            "2147491904", 
            "32"
          ]
        }, 
        "uuid": "7322c95c-4a52-4496-b3a9-365de52e5dc7", 
        "virtual_network": "default-domain:admin:vn2", 
        "vm_name": "vn2vm-a7s37-3", 
        "vm_uuid": "cd5dbd71-8a76-4c14-afc3-bcc27f2c5cd4"
      }
    }
    },
    {
    "uve-type": "virtual-networks",
    "uve-key": "default-domain:admin:vn1",
    "uve-value": 
    {
      "UveVirtualNetworkAgent": {
        "acl": "default-domain:admin:vn1:vn1", 
        "associated_fip_count": 0, 
        "egress_flow_count": 58, 
        "in_bandwidth_usage": 12791, 
        "in_stats": [
          {
            "bytes": 844424944668776, 
            "other_vn": "__UNKNOWN__", 
            "tpkts": 148423
          }, 
          {
            "bytes": 115041014, 
            "other_vn": "default-domain:admin:vn1", 
            "tpkts": 1173932
          }, 
          {
            "bytes": 1120684431, 
            "other_vn": "default-domain:admin:vn2", 
            "tpkts": 3210468
          }, 
          {
            "bytes": 38502, 
            "other_vn": "default-domain:default-project:ip-fabric", 
            "tpkts": 416
          }
        ], 
        "ingress_flow_count": 58, 
        "interface_list": [
          "default-domain:admin:834a0ab1-91d9-410c-b1da-245edf990fc7", 
          "default-domain:admin:e9ad858d-adb5-45f3-bf76-8c3bdb9671a1", 
          "default-domain:admin:faaf8474-a06f-4f98-885a-3df0199653a2", 
          "default-domain:admin:56408f9a-bc97-42ef-8872-5be449817ca5"
        ], 
        "mirror_acl": null, 
        "out_bandwidth_usage": 12550, 
        "out_stats": [
          {
            "bytes": 0, 
            "other_vn": "__UNKNOWN__", 
            "tpkts": 0
          }, 
          {
            "bytes": 115037054, 
            "other_vn": "default-domain:admin:vn1", 
            "tpkts": 1173872
          }, 
          {
            "bytes": 1069528509, 
            "other_vn": "default-domain:admin:vn2", 
            "tpkts": 3079006
          }, 
          {
            "bytes": 31919, 
            "other_vn": "default-domain:default-project:ip-fabric", 
            "tpkts": 416
          }
        ], 
        "tcp_dport_bitmap": [
          [
            [
              "1", 
              "8", 
              "0", 
              "0", 
              "801382400", 
              "4292349960", 
              "2835079189", 
              "1036"
            ], 
            "a7s34:Compute:contrail-vrouter-agent:0"
          ], 
          [
            [
              "1", 
              "0", 
              "0", 
              "0", 
              "0", 
              "9728", 
              "0", 
              "0"
            ], 
            "a7s29:Compute:contrail-vrouter-agent:0"
          ]
        ], 
        "tcp_sport_bitmap": [
          [
            [
              "1", 
              "8", 
              "0", 
              "0", 
              "801382400", 
              "4292349960", 
              "2835079189", 
              "1036"
            ], 
            "a7s34:Compute:contrail-vrouter-agent:0"
          ], 
          [
            [
              "1", 
              "0", 
              "0", 
              "0", 
              "0", 
              "9792", 
              "0", 
              "0"
            ], 
            "a7s29:Compute:contrail-vrouter-agent:0"
          ]
        ], 
        "total_acl_rules": 4, 
        "udp_dport_bitmap": [
          [
            [
              "1", 
              "0", 
              "0", 
              "0", 
              "2817740667", 
              "4210010940", 
              "2080185951", 
              "3125"
            ], 
            "a7s34:Compute:contrail-vrouter-agent:0"
          ], 
          [
            [
              "1", 
              "0", 
              "0", 
              "0", 
              "9602", 
              "546571019", 
              "18123336", 
              "18"
            ], 
            "a7s29:Compute:contrail-vrouter-agent:0"
          ]
        ], 
        "udp_sport_bitmap": [
          [
            [
              "1", 
              "0", 
              "0", 
              "0", 
              "2817740667", 
              "4210010940", 
              "2080185951", 
              "3125"
            ], 
            "a7s34:Compute:contrail-vrouter-agent:0"
          ], 
          [
            [
              "1", 
              "0", 
              "0", 
              "0", 
              "9602", 
              "546571019", 
              "18123336", 
              "18"
            ], 
            "a7s29:Compute:contrail-vrouter-agent:0"
          ]
        ], 
        "virtualmachine_list": [
          "ca59ae0b-d509-4d84-91ae-1aacc0062cf2", 
          "d0d90ba2-a2b1-4da3-951a-a293a1763c79", 
          "d1127528-999d-4aab-9bb9-1b888367f042", 
          "97427379-dc73-4e1b-91b3-54f6bd8b3d5d"
        ], 
        "vn_stats": [
          [
            [
              {
                "in_bytes": 0, 
                "in_tpkts": 0, 
                "other_vn": "__UNKNOWN__", 
                "out_bytes": 0, 
                "out_tpkts": 0, 
                "vrouter": "a7s34"
              }, 
              {
                "in_bytes": 8820, 
                "in_tpkts": 90, 
                "other_vn": "default-domain:admin:vn1", 
                "out_bytes": 8820, 
                "out_tpkts": 90, 
                "vrouter": "a7s34"
              }, 
              {
                "in_bytes": 38998, 
                "in_tpkts": 119, 
                "other_vn": "default-domain:admin:vn2", 
                "out_bytes": 38096, 
                "out_tpkts": 116, 
                "vrouter": "a7s34"
              }, 
              {
                "in_bytes": 0, 
                "in_tpkts": 0, 
                "other_vn": "default-domain:default-project:ip-fabric", 
                "out_bytes": 0, 
                "out_tpkts": 0, 
                "vrouter": "a7s34"
              }
            ], 
            "a7s34:Compute:contrail-vrouter-agent:0"
          ], 
          [
            [
              {
                "in_bytes": 0, 
                "in_tpkts": 0, 
                "other_vn": "__UNKNOWN__", 
                "out_bytes": 0, 
                "out_tpkts": 0, 
                "vrouter": "a7s29"
              }, 
              {
                "in_bytes": 152, 
                "in_tpkts": 2, 
                "other_vn": "default-domain:admin:vn1", 
                "out_bytes": 152, 
                "out_tpkts": 2, 
                "vrouter": "a7s29"
              }, 
              {
                "in_bytes": 0, 
                "in_tpkts": 0, 
                "other_vn": "default-domain:default-project:ip-fabric", 
                "out_bytes": 0, 
                "out_tpkts": 0, 
                "vrouter": "a7s29"
              }
            ], 
            "a7s29:Compute:contrail-vrouter-agent:0"
          ]
        ], 
        "vrf_stats_list": [
          {
            "arp_packet_counts": {
              "from_physical_interface": {
                "stats": {
                  "floods": 0, 
                  "proxies": 0, 
                  "stitches": 0
                }
              }, 
              "from_vm_interface": {
                "stats": {
                  "floods": 0, 
                  "proxies": 74, 
                  "stitches": 34536
                }
              }
            }, 
            "diag_packet_count": 0, 
            "name": "default-domain:admin:vn1:vn1", 
            "nh_packet_counts": {
              "comp_nh_stats": {
                "edge_replication_forwards": 0, 
                "local_vm_l3_forwards": 0, 
                "source_replication_forwards": 0, 
                "total_multicast_forwards": 0
              }, 
              "discards": 0, 
              "ecmp_forwards": 0, 
              "l2_receives": 0, 
              "l3_receives": 0, 
              "local_vm_l2_forwards": 0, 
              "local_vm_l3_forwards": 0, 
              "resolves": 0, 
              "tunnel_nh_stats": {
                "mpls_over_gre_encaps": 0, 
                "mpls_over_udp_encaps": 0, 
                "udp_encaps": 0, 
                "vxlan_encaps": 0
              }, 
              "vrf_translates": 0
            }, 
            "offload_packet_counts": {
              "gro": 4279278
            }, 
            "unknown_unicast_floods": 0
          }
        ]
      }, 
      "UveVirtualNetworkConfig": {
        "connected_networks": [
          "default-domain:admin:vn2"
        ], 
        "routing_instance_list": [
          "default-domain:admin:vn1:vn1"
        ], 
        "total_acl_rules": 4
      }
    }
    }
    {
    "uve-type": "vrouters",
    "uve-key": "a7s37",
    "uve-value": 
    {
      "ComputeCpuState": {
        "cpu_info": [
          {
            "cpu_share": 0.1875, 
            "mem_res": 172372, 
            "mem_virt": 907644, 
            "one_min_cpuload": 0.005, 
            "used_sys_mem": 3713316
          }
        ]
      }, 
      "NodeStatus": {
        "deleted": false, 
        "disk_usage_info": [
          {
            "partition_name": "/dev/mapper/a7s37--vg-root", 
            "partition_space_available_1k": 419280236, 
            "partition_space_used_1k": 5269824, 
            "partition_type": "ext4"
          }, 
          {
            "partition_name": "/dev/sda1", 
            "partition_space_available_1k": 192015, 
            "partition_space_used_1k": 36516, 
            "partition_type": "ext2"
          }
        ], 
        "process_info": [
          {
            "core_file_list": [], 
            "exit_count": 0, 
            "last_exit_time": null, 
            "last_start_time": "1454021819713631", 
            "last_stop_time": null, 
            "process_name": "contrail-vrouter-agent", 
            "process_state": "PROCESS_STATE_RUNNING", 
            "start_count": 2, 
            "stop_count": 0
          }, 
          {
            "core_file_list": [], 
            "exit_count": 0, 
            "last_exit_time": null, 
            "last_start_time": "1454021819709926", 
            "last_stop_time": null, 
            "process_name": "contrail-vrouter-nodemgr", 
            "process_state": "PROCESS_STATE_RUNNING", 
            "start_count": 2, 
            "stop_count": 0
          }, 
          {
            "core_file_list": [], 
            "exit_count": 0, 
            "last_exit_time": null, 
            "last_start_time": "1454021819593245", 
            "last_stop_time": null, 
            "process_name": "openstack-nova-compute", 
            "process_state": "PROCESS_STATE_RUNNING", 
            "start_count": 1, 
            "stop_count": 0
          }
        ], 
        "process_status": [
          {
            "connection_infos": [
              {
                "description": "OpenSent", 
                "name": "control-node:10.84.30.201", 
                "server_addrs": [
                  "10.84.30.201:5269"
                ], 
                "status": "Up", 
                "type": "XMPP"
              }, 
              {
                "description": "OpenSent", 
                "name": "dns-server:10.84.30.201", 
                "server_addrs": [
                  "10.84.30.201:53"
                ], 
                "status": "Up", 
                "type": "XMPP"
              }, 
              {
                "description": "Established", 
                "name": null, 
                "server_addrs": [
                  "10.84.30.201:8086"
                ], 
                "status": "Up", 
                "type": "Collector"
              }, 
              {
                "description": "SubscribeResponse", 
                "name": "Collector", 
                "server_addrs": [
                  "10.84.30.201:5998"
                ], 
                "status": "Up", 
                "type": "Discovery"
              }, 
              {
                "description": "SubscribeResponse", 
                "name": "dns-server", 
                "server_addrs": [
                  "10.84.30.201:5998"
                ], 
                "status": "Up", 
                "type": "Discovery"
              }, 
              {
                "description": "SubscribeResponse", 
                "name": "xmpp-server", 
                "server_addrs": [
                  "10.84.30.201:5998"
                ], 
                "status": "Up", 
                "type": "Discovery"
              }
            ], 
            "description": null, 
            "instance_id": "0", 
            "module_id": "contrail-vrouter-agent", 
            "state": "Functional"
          }, 
          {
            "description": null, 
            "instance_id": "0", 
            "module_id": "contrail-vrouter-nodemgr", 
            "state": "Functional"
          }
        ]
      }, 
      "VrouterAgent": {
        "build_info": "{\"build-info\":[{\"build-time\":\"2016-01-28 13:37:54.796522\",\"build-hostname\":\"contrail-ec-build16\",\"build-git-ver\":\"0022e08\",\"build-user\":\"contrail-builder\",\"build-version\":\"3.0\",\"build-id\":\"3.0-2706\",\"build-number\":\"2706\"}]}", 
        "config_file": "/etc/contrail/contrail-vrouter-agent.conf", 
        "connected_networks": [
          "default-domain:admin:vn2"
        ], 
        "control_ip": "10.84.30.129", 
        "control_node_list_cfg": [
          "0.0.0.0", 
          "0.0.0.0"
        ], 
        "dns_server_list_cfg": [
          "0.0.0.0", 
          "0.0.0.0"
        ], 
        "dns_servers": [
          "10.84.30.201"
        ], 
        "down_interface_count": 0, 
        "ds_addr": "10.84.30.201", 
        "ds_xs_instances": 1, 
        "eth_name": "p4p1", 
        "flow_cache_timeout_cfg": 0, 
        "headless_mode_cfg": false, 
        "hostname_cfg": "a7s37", 
        "hypervisor": "kvm", 
        "interface_list": [
          "default-domain:admin:580fb8aa-ff53-47e6-a11a-720df25f8ce7", 
          "default-domain:admin:7322c95c-4a52-4496-b3a9-365de52e5dc7", 
          "default-domain:admin:b54c4008-b083-4758-a319-4ae5bb70d909"
        ], 
        "ll_max_system_flows_cfg": 2048, 
        "ll_max_vm_flows_cfg": 2048, 
        "log_category": "*", 
        "log_file": "/var/log/contrail/contrail-vrouter-agent.log", 
        "log_flow": false, 
        "log_level": "SYS_NOTICE", 
        "log_local": true, 
        "max_vm_flows_cfg": 100, 
        "mode": "VROUTER", 
        "phy_if": [
          {
            "mac_address": "00:25:90:7e:52:de", 
            "name": "p4p1"
          }
        ], 
        "platform": "HOST", 
        "sandesh_http_port": 8085, 
        "self_ip_list": [
          "10.84.30.129"
        ], 
        "total_interface_count": 3, 
        "tunnel_type": "MPLSoGRE", 
        "vhost_cfg": {
          "gateway": "10.84.30.130", 
          "ip": "10.84.30.129", 
          "ip_prefix_len": 30, 
          "name": "vhost0"
        }, 
        "vhost_if": {
          "mac_address": "00:25:90:7e:52:de", 
          "name": "vhost0"
        }, 
        "virtual_machine_list": [
          "18c3e1f1-6c08-41b5-ab09-25318f83a43b", 
          "6eadcfd3-11fb-4bda-a8ff-8f7027f82cce", 
          "cd5dbd71-8a76-4c14-afc3-bcc27f2c5cd4"
        ], 
        "vn_count": 1, 
        "xmpp_peer_list": [
          {
            "ip": "10.84.30.201", 
            "primary": true, 
            "setup_time": 1454021824159330, 
            "status": true
          }
        ]
      }, 
      "VrouterStatsAgent": {
        "active_flows": 10, 
        "aged_flows": 1972, 
        "cpu_info": {
          "cpu_share": 0.1875, 
          "cpuload": {
            "fifteen_min_avg": 0.05, 
            "five_min_avg": 0.0275, 
            "one_min_avg": 0.005
          }, 
          "meminfo": {
            "peakvirt": 907676, 
            "res": 172372, 
            "virt": 907644
          }, 
          "num_cpu": 4, 
          "sys_mem_info": {
            "buffers": 175656, 
            "free": 28946468, 
            "total": 32659784, 
            "used": 3713316
          }
        }, 
        "drop_stats": {
          "ds_arp_no_route": 0, 
          "ds_arp_no_where_to_go": 0, 
          "ds_arp_reply_no_route": 0, 
          "ds_cksum_err": 0, 
          "ds_clone_fail": 0, 
          "ds_cloned_original": 12, 
          "ds_composite_invalid_interface": 0, 
          "ds_discard": 0, 
          "ds_duplicated": 0, 
          "ds_flood": 0, 
          "ds_flow_action_drop": 192, 
          "ds_flow_action_invalid": 0, 
          "ds_flow_invalid_protocol": 0, 
          "ds_flow_nat_no_rflow": 0, 
          "ds_flow_no_memory": 0, 
          "ds_flow_queue_limit_exceeded": 0, 
          "ds_flow_table_full": 0, 
          "ds_flow_unusable": 0, 
          "ds_frag_err": 0, 
          "ds_garp_from_vm": 0, 
          "ds_head_alloc_fail": 0, 
          "ds_head_space_reserve_fail": 0, 
          "ds_interface_drop": 0, 
          "ds_interface_rx_discard": 0, 
          "ds_interface_tx_discard": 0, 
          "ds_invalid_arp": 0, 
          "ds_invalid_if": 0, 
          "ds_invalid_label": 0, 
          "ds_invalid_mcast_source": 0, 
          "ds_invalid_nh": 13, 
          "ds_invalid_packet": 0, 
          "ds_invalid_protocol": 0, 
          "ds_invalid_source": 0, 
          "ds_invalid_vnid": 0, 
          "ds_l2_no_route": 3, 
          "ds_mcast_clone_fail": 0, 
          "ds_mcast_df_bit": 0, 
          "ds_misc": 3, 
          "ds_no_fmd": 0, 
          "ds_nowhere_to_go": 0, 
          "ds_pcow_fail": 0, 
          "ds_pull": 0, 
          "ds_push": 0, 
          "ds_rewrite_fail": 0, 
          "ds_trap_no_if": 0, 
          "ds_ttl_exceeded": 0
        }, 
        "exception_packets": 36845, 
        "exception_packets_allowed": 36821, 
        "exception_packets_dropped": 24, 
        "flow_rate": {
          "added_flows": 0, 
          "deleted_flows": 0, 
          "max_flow_adds_per_second": 0, 
          "max_flow_deletes_per_second": 0, 
          "min_flow_adds_per_second": 0, 
          "min_flow_deletes_per_second": 0
        }, 
        "in_bytes": 324353425, 
        "in_tpkts": 899102, 
        "out_bytes": 326337131, 
        "out_tpkts": 938339, 
        "phy_if_10min_usage": [
          {
            "in_bandwidth_usage": 0, 
            "name": "p4p1", 
            "out_bandwidth_usage": 0
          }
        ], 
        "phy_if_5min_usage": [
          {
            "in_bandwidth_usage": 0, 
            "name": "p4p1", 
            "out_bandwidth_usage": 0
          }
        ], 
        "phy_if_band": [
          {
            "in_bandwidth_usage": 0, 
            "name": "p4p1", 
            "out_bandwidth_usage": 0
          }
        ], 
        "phy_if_stats_list": [
          {
            "duplexity": 1, 
            "in_bytes": 3184155082, 
            "in_pkts": 3807681, 
            "name": "p4p1", 
            "out_bytes": 3633822146, 
            "out_pkts": 4627354, 
            "speed": 1000
          }
        ], 
        "tcp_dport_bitmap": [
          "1", 
          "8", 
          "0", 
          "0", 
          "12582912", 
          "817901794", 
          "2152626688", 
          "2052"
        ], 
        "tcp_sport_bitmap": [
          "1", 
          "8", 
          "0", 
          "0", 
          "12582912", 
          "817901794", 
          "2152626688", 
          "2308"
        ], 
        "total_flows": 1982, 
        "total_in_bandwidth_utilization": 0, 
        "total_out_bandwidth_utilization": 0, 
        "udp_dport_bitmap": [
          "1", 
          "0", 
          "0", 
          "0", 
          "4294967295", 
          "4294967295", 
          "4261412863", 
          "28667"
        ], 
        "udp_sport_bitmap": [
          "1", 
          "0", 
          "0", 
          "0", 
          "4294967295", 
          "4294967295", 
          "4261412863", 
          "28667"
        ], 
        "uptime": 1454021821870455, 
        "vhost_stats": {
          "duplexity": -1, 
          "in_bytes": 3286539599, 
          "in_pkts": 3721726, 
          "name": "vhost0", 
          "out_bytes": 2834587286, 
          "out_pkts": 2864314, 
          "speed": -1
        }, 
        "xmpp_stats_list": [
          {
            "in_msgs": 112, 
            "ip": "10.84.30.201", 
            "out_msgs": 205, 
            "reconnects": 1
          }
        ]
      }
    }
    },
    {
    "uve-type": "dns-nodes",
    "uve-key": "a7s33",
    "uve-value": 
    {
      "DnsState": {
        "build_info": "{\"build-info\":[{\"build-time\":\"2016-01-28 11:50:18.537769\",\"build-hostname\":\"contrail-ec-build16\",\"build-git-ver\":\"0022e08\",\"build-user\":\"contrail-builder\",\"build-version\":\"3.0\",\"build-id\":\"3.0-2706\",\"build-number\":\"2706\"}]}", 
        "collector": null, 
        "self_ip_list": [
          "10.84.30.201"
        ], 
        "start_time": 1454021642207258
      }
    }
    },
    {
    "uve-type": "service-instances",
    "uve-key": "default-domain:bgp-test:snat_fbe6b9bf-ef56-4c31-a56e-ff426317cffe_55ab965c-8b0a-4251-afae-e6fb4b626eb6",
    "uve-value": 
    {
      "UveSvcInstanceConfig": {
        "create_ts": 1454886890213816, 
        "deleted": false, 
        "st_name": "default-domain:netns-snat-template", 
        "status": "CREATE", 
        "vm_list": [
          {
            "ha": "active: 200", 
            "uuid": "5af69f50-efc8-4e61-89e7-cb593207f7fd", 
            "vr_name": "csol2-node16"
          }, 
          {
            "ha": "standby: 100", 
            "uuid": "eac09aa8-a832-4d98-b547-972ff60111d2", 
            "vr_name": "csol2-node11"
          }
        ]
      }
    }
    },
    {
    "uve-type": "service-chains",
    "uve-key": "b1425912-f822-468d-8cf7-5c0b8b8c65c8",
    "uve-value": 
    {
      "UveServiceChainData": {
        "destination_ports": "0-65535", 
        "destination_virtual_network": "default-domain:bgp-test:GW", 
        "direction": "<>", 
        "protocol": "any", 
        "services": [
          "default-domain:bgp-test:snat_fbe6b9bf-ef56-4c31-a56e-ff426317cffe_55ab965c-8b0a-4251-afae-e6fb4b626eb6"
        ], 
        "source_ports": "0-65535", 
        "source_virtual_network": "default-domain:bgp-test:snat-si-left_snat_fbe6b9bf-ef56-4c31-a56e-ff426317cffe_55ab965c-8b0a-4251-afae-e6fb4b626eb6"
      }
    }
    },
    {
    "uve-type": "physical-interfaces",
    "uve-key": "default-global-system-config:a7-qfx4:ge-0/0/8",
    "uve-value": 
    {
      "UvePhysicalInterfaceAgent": {
        "logical_interface_list": [
          "c0896cfe-d85c-470e-bc5f-77a4ebc3f0db"
        ], 
        "uuid": "00000000-0000-0000-0000-000000000000"
      }
    }
    },
    {
    "uve-type": "logical-interfaces",
    "uve-key": "c0896cfe-d85c-470e-bc5f-77a4ebc3f0db",
    "uve-value": 
    {
      "UveLogicalInterfaceAgent": {
        "config_name": "default-global-system-config:a7-qfx4:ge-0/0/8:ge-0/0/8.100", 
        "vlan": 100, 
        "vm_interface_list": [
          "default-domain:admin:a77d3514-cc8a-4ed9-96eb-6f6b65c22e64"
        ]
      }
    }
    }
    ]

# Query-able Table Schemas
This section lists all the query-able tables available from analytics-api server and their schemas. It is presented as a list of dict with each dict corresponding to one table type. Each dict is of the following format:

    {
    "table-name": <TABLE_NAME>,
    "table-schema": <TABLE_SCHEMA> }
___  
    [
    {
    "table-name": "MessageTable",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "int", 
          "index": false, 
          "name": "MessageTS", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ModuleId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Category", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "Level", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "Type", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "InstanceId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "NodeType", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Messagetype", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SequenceNum", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "Context", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Keyword", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "Xmlmessage", 
          "select": null, 
          "suffixes": null
        }
      ], 
      "type": "LOG"
    }
    },
    {
    "table-name": "FlowRecordTable",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "vrouter", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "sourcevn", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "ipaddr", 
          "index": true, 
          "name": "sourceip", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "destvn", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "ipaddr", 
          "index": true, 
          "name": "destip", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "protocol", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "sport", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "dport", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "direction_ing", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UuidKey", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "long", 
          "index": false, 
          "name": "setup_time", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "long", 
          "index": false, 
          "name": "teardown_time", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "long", 
          "index": false, 
          "name": "agg-packets", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "long", 
          "index": false, 
          "name": "agg-bytes", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "action", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "sg_rule_uuid", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "nw_ace_uuid", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "vrouter_ip", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "other_vrouter_ip", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "underlay_proto", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "underlay_source_port", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "vmi_uuid", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "drop_reason", 
          "select": null, 
          "suffixes": null
        }
      ], 
      "type": "FLOW"
    }
    },
    {
    "table-name": "FlowSeriesTable",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "vrouter", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "sourcevn", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "ipaddr", 
          "index": true, 
          "name": "sourceip", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "destvn", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "ipaddr", 
          "index": true, 
          "name": "destip", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "protocol", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "sport", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "dport", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "direction_ing", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "flow_class_id", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "packets", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "bytes", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "sum(packets)", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "sum(bytes)", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "flow_count", 
          "select": null, 
          "suffixes": null
        }
      ], 
      "type": "FLOW"
    }
    },
    {
    "table-name": "OverlayToUnderlayFlowMap",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "o_svn", 
          "select": false, 
          "suffixes": [
            "o_sip"
          ]
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "o_sip", 
          "select": false, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "o_dvn", 
          "select": false, 
          "suffixes": [
            "o_dip"
          ]
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "o_dip", 
          "select": false, 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "o_sport", 
          "select": false, 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "o_dport", 
          "select": false, 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "o_protocol", 
          "select": false, 
          "suffixes": [
            "o_sport", 
            "o_dport"
          ]
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "o_vrouter", 
          "select": false, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "u_prouter", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "u_pifindex", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "u_vlan", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "u_sip", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "u_dip", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "u_sport", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "u_dport", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "u_protocol", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "u_flowtype", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "u_otherinfo", 
          "select": null, 
          "suffixes": null
        }
      ], 
      "type": "FLOW"
    }
    },
    {
    "table-name": "ServiceChain",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "int", 
          "index": false, 
          "name": "MessageTS", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ObjectId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ModuleId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Messagetype", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "ObjectLog", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "SystemLog", 
          "select": null, 
          "suffixes": null
        }
      ], 
      "type": "OBJECT"
    }
    },
    {
    "table-name": "ObjectDatabaseInfo",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "int", 
          "index": false, 
          "name": "MessageTS", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ObjectId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ModuleId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Messagetype", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "ObjectLog", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "SystemLog", 
          "select": null, 
          "suffixes": null
        }
      ], 
      "type": "OBJECT"
    }
    },
    {
    "table-name": "ObjectRoutingInstance",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "int", 
          "index": false, 
          "name": "MessageTS", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ObjectId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ModuleId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Messagetype", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "ObjectLog", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "SystemLog", 
          "select": null, 
          "suffixes": null
        }
      ], 
      "type": "OBJECT"
    }
    },
    {
    "table-name": "ObjectXmppConnection",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "int", 
          "index": false, 
          "name": "MessageTS", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ObjectId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ModuleId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Messagetype", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "ObjectLog", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "SystemLog", 
          "select": null, 
          "suffixes": null
        }
      ], 
      "type": "OBJECT"
    }
    },
    {
    "table-name": "ObjectQueryTable",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "int", 
          "index": false, 
          "name": "MessageTS", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ObjectId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ModuleId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Messagetype", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "ObjectLog", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "SystemLog", 
          "select": null, 
          "suffixes": null
        }
      ], 
      "type": "OBJECT"
    }
    },
    {
    "table-name": "ObjectVMITable",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "int", 
          "index": false, 
          "name": "MessageTS", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ObjectId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ModuleId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Messagetype", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "ObjectLog", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "SystemLog", 
          "select": null, 
          "suffixes": null
        }
      ], 
      "type": "OBJECT"
    }
    },
    {
    "table-name": "ConfigObjectTableByUser",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "int", 
          "index": false, 
          "name": "MessageTS", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ObjectId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ModuleId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Messagetype", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "ObjectLog", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "SystemLog", 
          "select": null, 
          "suffixes": null
        }
      ], 
      "type": "OBJECT"
    }
    },
    {
    "table-name": "ObjectQueryQid",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "int", 
          "index": false, 
          "name": "MessageTS", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ObjectId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ModuleId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Messagetype", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "ObjectLog", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "SystemLog", 
          "select": null, 
          "suffixes": null
        }
      ], 
      "type": "OBJECT"
    }
    },
    {
    "table-name": "ObjectOsdTable",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "int", 
          "index": false, 
          "name": "MessageTS", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ObjectId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ModuleId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Messagetype", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "ObjectLog", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "SystemLog", 
          "select": null, 
          "suffixes": null
        }
      ], 
      "type": "OBJECT"
    }
    },
    {
    "table-name": "ObjectLogicalInterfaceTable",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "int", 
          "index": false, 
          "name": "MessageTS", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ObjectId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ModuleId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Messagetype", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "ObjectLog", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "SystemLog", 
          "select": null, 
          "suffixes": null
        }
      ], 
      "type": "OBJECT"
    }
    },
    {
    "table-name": "ObjectXmppPeerInfo",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "int", 
          "index": false, 
          "name": "MessageTS", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ObjectId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ModuleId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Messagetype", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "ObjectLog", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "SystemLog", 
          "select": null, 
          "suffixes": null
        }
      ], 
      "type": "OBJECT"
    }
    },
    {
    "table-name": "ObjectGeneratorInfo",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "int", 
          "index": false, 
          "name": "MessageTS", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ObjectId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ModuleId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Messagetype", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "ObjectLog", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "SystemLog", 
          "select": null, 
          "suffixes": null
        }
      ], 
      "type": "OBJECT"
    }
    },
    {
    "table-name": "ObjectVNTable",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "int", 
          "index": false, 
          "name": "MessageTS", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ObjectId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ModuleId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Messagetype", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "ObjectLog", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "SystemLog", 
          "select": null, 
          "suffixes": null
        }
      ], 
      "type": "OBJECT"
    }
    },
    {
    "table-name": "ObjectCollectorInfo",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "int", 
          "index": false, 
          "name": "MessageTS", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ObjectId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ModuleId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Messagetype", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "ObjectLog", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "SystemLog", 
          "select": null, 
          "suffixes": null
        }
      ], 
      "type": "OBJECT"
    }
    },
    {
    "table-name": "ObjectPRouter",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "int", 
          "index": false, 
          "name": "MessageTS", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ObjectId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ModuleId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Messagetype", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "ObjectLog", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "SystemLog", 
          "select": null, 
          "suffixes": null
        }
      ], 
      "type": "OBJECT"
    }
    },
    {
    "table-name": "ObjectBgpPeer",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "int", 
          "index": false, 
          "name": "MessageTS", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ObjectId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ModuleId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Messagetype", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "ObjectLog", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "SystemLog", 
          "select": null, 
          "suffixes": null
        }
      ], 
      "type": "OBJECT"
    }
    },
    {
    "table-name": "ConfigObjectTable",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "int", 
          "index": false, 
          "name": "MessageTS", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ObjectId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ModuleId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Messagetype", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "ObjectLog", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "SystemLog", 
          "select": null, 
          "suffixes": null
        }
      ], 
      "type": "OBJECT"
    }
    },
    {
    "table-name": "ObjectDns",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "int", 
          "index": false, 
          "name": "MessageTS", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ObjectId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ModuleId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Messagetype", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "ObjectLog", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "SystemLog", 
          "select": null, 
          "suffixes": null
        }
      ], 
      "type": "OBJECT"
    }
    },
    {
    "table-name": "ObjectStorageClusterTable",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "int", 
          "index": false, 
          "name": "MessageTS", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ObjectId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ModuleId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Messagetype", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "ObjectLog", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "SystemLog", 
          "select": null, 
          "suffixes": null
        }
      ], 
      "type": "OBJECT"
    }
    },
    {
    "table-name": "ObjectBgpRouter",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "int", 
          "index": false, 
          "name": "MessageTS", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ObjectId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ModuleId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Messagetype", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "ObjectLog", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "SystemLog", 
          "select": null, 
          "suffixes": null
        }
      ], 
      "type": "OBJECT"
    }
    },
    {
    "table-name": "ObjectPhysicalInterfaceTable",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "int", 
          "index": false, 
          "name": "MessageTS", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ObjectId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ModuleId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Messagetype", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "ObjectLog", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "SystemLog", 
          "select": null, 
          "suffixes": null
        }
      ], 
      "type": "OBJECT"
    }
    },
    {
    "table-name": "ObjectServerTable",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "int", 
          "index": false, 
          "name": "MessageTS", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ObjectId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ModuleId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Messagetype", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "ObjectLog", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "SystemLog", 
          "select": null, 
          "suffixes": null
        }
      ], 
      "type": "OBJECT"
    }
    },
    {
    "table-name": "ObjectVMTable",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "int", 
          "index": false, 
          "name": "MessageTS", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ObjectId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ModuleId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Messagetype", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "ObjectLog", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "SystemLog", 
          "select": null, 
          "suffixes": null
        }
      ], 
      "type": "OBJECT"
    }
    },
    {
    "table-name": "ObjectVRouter",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "int", 
          "index": false, 
          "name": "MessageTS", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ObjectId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ModuleId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Messagetype", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "ObjectLog", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "SystemLog", 
          "select": null, 
          "suffixes": null
        }
      ], 
      "type": "OBJECT"
    }
    },
    {
    "table-name": "ObjectDiskTable",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "int", 
          "index": false, 
          "name": "MessageTS", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ObjectId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ModuleId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Messagetype", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "ObjectLog", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "SystemLog", 
          "select": null, 
          "suffixes": null
        }
      ], 
      "type": "OBJECT"
    }
    },
    {
    "table-name": "ObjectPoolTable",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "int", 
          "index": false, 
          "name": "MessageTS", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ObjectId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ModuleId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Messagetype", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "ObjectLog", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "SystemLog", 
          "select": null, 
          "suffixes": null
        }
      ], 
      "type": "OBJECT"
    }
    },
    {
    "table-name": "ObjectSITable",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "int", 
          "index": false, 
          "name": "MessageTS", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ObjectId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ModuleId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Messagetype", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "ObjectLog", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "SystemLog", 
          "select": null, 
          "suffixes": null
        }
      ], 
      "type": "OBJECT"
    }
    },
    {
    "table-name": "ObjectConfigNode",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "int", 
          "index": false, 
          "name": "MessageTS", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ObjectId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ModuleId", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "Messagetype", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "ObjectLog", 
          "select": null, 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "SystemLog", 
          "select": null, 
          "suffixes": null
        }
      ], 
      "type": "OBJECT"
    }
    },
    {
    "table-name": "StatTable.AnalyticsCpuState.cpu_info",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(cpu_info)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "cpu_info.mem_virt", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(cpu_info.mem_virt)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(cpu_info.mem_virt)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(cpu_info.mem_virt)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(cpu_info.mem_virt)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "cpu_info.mem_res", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(cpu_info.mem_res)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(cpu_info.mem_res)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(cpu_info.mem_res)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(cpu_info.mem_res)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": true, 
          "name": "cpu_info.cpu_share", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "SUM(cpu_info.cpu_share)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "CLASS(cpu_info.cpu_share)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "MAX(cpu_info.cpu_share)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "MIN(cpu_info.cpu_share)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "cpu_info.inst_id", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "cpu_info.module_id", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.ConfigCpuState.cpu_info",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(cpu_info)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "cpu_info.mem_virt", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(cpu_info.mem_virt)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(cpu_info.mem_virt)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(cpu_info.mem_virt)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(cpu_info.mem_virt)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "cpu_info.mem_res", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(cpu_info.mem_res)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(cpu_info.mem_res)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(cpu_info.mem_res)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(cpu_info.mem_res)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": true, 
          "name": "cpu_info.cpu_share", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "SUM(cpu_info.cpu_share)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "CLASS(cpu_info.cpu_share)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "MAX(cpu_info.cpu_share)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "MIN(cpu_info.cpu_share)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "cpu_info.inst_id", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "cpu_info.module_id", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.ControlCpuState.cpu_info",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(cpu_info)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "cpu_info.mem_virt", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(cpu_info.mem_virt)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(cpu_info.mem_virt)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(cpu_info.mem_virt)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(cpu_info.mem_virt)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "cpu_info.mem_res", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(cpu_info.mem_res)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(cpu_info.mem_res)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(cpu_info.mem_res)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(cpu_info.mem_res)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": true, 
          "name": "cpu_info.cpu_share", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "SUM(cpu_info.cpu_share)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "CLASS(cpu_info.cpu_share)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "MAX(cpu_info.cpu_share)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "MIN(cpu_info.cpu_share)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "cpu_info.inst_id", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "cpu_info.module_id", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.PRouterEntry.ifStats",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(ifStats)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": [
            "ifStats.ifIndex", 
            "ifStats.ifName"
          ]
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "ifStats.ifInPkts", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(ifStats.ifInPkts)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(ifStats.ifInPkts)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(ifStats.ifInPkts)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(ifStats.ifInPkts)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "ifStats.ifOutPkts", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(ifStats.ifOutPkts)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(ifStats.ifOutPkts)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(ifStats.ifOutPkts)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(ifStats.ifOutPkts)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "ifStats.ifInOctets", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(ifStats.ifInOctets)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(ifStats.ifInOctets)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(ifStats.ifInOctets)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(ifStats.ifInOctets)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "ifStats.ifOutOctets", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(ifStats.ifOutOctets)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(ifStats.ifOutOctets)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(ifStats.ifOutOctets)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(ifStats.ifOutOctets)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "ifStats.ifInDiscards", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(ifStats.ifInDiscards)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(ifStats.ifInDiscards)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(ifStats.ifInDiscards)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(ifStats.ifInDiscards)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "ifStats.ifInErrors", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(ifStats.ifInErrors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(ifStats.ifInErrors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(ifStats.ifInErrors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(ifStats.ifInErrors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "ifStats.ifOutDiscards", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(ifStats.ifOutDiscards)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(ifStats.ifOutDiscards)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(ifStats.ifOutDiscards)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(ifStats.ifOutDiscards)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "ifStats.ifOutErrors", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(ifStats.ifOutErrors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(ifStats.ifOutErrors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(ifStats.ifOutErrors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(ifStats.ifOutErrors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "ifStats.ifIndex", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(ifStats.ifIndex)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(ifStats.ifIndex)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(ifStats.ifIndex)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(ifStats.ifIndex)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "ifStats.ifName", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.ComputeCpuState.cpu_info",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(cpu_info)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "cpu_info.mem_virt", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(cpu_info.mem_virt)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(cpu_info.mem_virt)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(cpu_info.mem_virt)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(cpu_info.mem_virt)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "cpu_info.mem_res", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(cpu_info.mem_res)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(cpu_info.mem_res)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(cpu_info.mem_res)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(cpu_info.mem_res)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": true, 
          "name": "cpu_info.cpu_share", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "SUM(cpu_info.cpu_share)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "CLASS(cpu_info.cpu_share)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "MAX(cpu_info.cpu_share)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "MIN(cpu_info.cpu_share)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "cpu_info.used_sys_mem", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(cpu_info.used_sys_mem)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(cpu_info.used_sys_mem)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(cpu_info.used_sys_mem)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(cpu_info.used_sys_mem)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "cpu_info.one_min_cpuload", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "SUM(cpu_info.one_min_cpuload)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "CLASS(cpu_info.one_min_cpuload)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "MAX(cpu_info.one_min_cpuload)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "MIN(cpu_info.one_min_cpuload)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.VirtualMachineStats.cpu_stats",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(cpu_stats)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "cpu_stats.cpu_one_min_avg", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "SUM(cpu_stats.cpu_one_min_avg)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "CLASS(cpu_stats.cpu_one_min_avg)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "MAX(cpu_stats.cpu_one_min_avg)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "MIN(cpu_stats.cpu_one_min_avg)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "cpu_stats.vm_memory_quota", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(cpu_stats.vm_memory_quota)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(cpu_stats.vm_memory_quota)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(cpu_stats.vm_memory_quota)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(cpu_stats.vm_memory_quota)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "cpu_stats.rss", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(cpu_stats.rss)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(cpu_stats.rss)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(cpu_stats.rss)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(cpu_stats.rss)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "cpu_stats.virt_memory", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "SUM(cpu_stats.virt_memory)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "CLASS(cpu_stats.virt_memory)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "MAX(cpu_stats.virt_memory)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "MIN(cpu_stats.virt_memory)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "cpu_stats.peak_virt_memory", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(cpu_stats.peak_virt_memory)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(cpu_stats.peak_virt_memory)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(cpu_stats.peak_virt_memory)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(cpu_stats.peak_virt_memory)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.StorageCluster.info_stats",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(info_stats)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "cluster_id", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "info_stats.status", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(info_stats.status)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(info_stats.status)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(info_stats.status)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(info_stats.status)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "info_stats.health_detail", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "info_stats.health_summary", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "info_stats.monitor_count", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(info_stats.monitor_count)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(info_stats.monitor_count)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(info_stats.monitor_count)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(info_stats.monitor_count)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "info_stats.monitor_active", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(info_stats.monitor_active)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(info_stats.monitor_active)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(info_stats.monitor_active)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(info_stats.monitor_active)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "info_stats.osd_full", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(info_stats.osd_full)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(info_stats.osd_full)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(info_stats.osd_full)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(info_stats.osd_full)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "info_stats.osd_near_full", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(info_stats.osd_near_full)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(info_stats.osd_near_full)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(info_stats.osd_near_full)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(info_stats.osd_near_full)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "info_stats.osds_conf", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(info_stats.osds_conf)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(info_stats.osds_conf)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(info_stats.osds_conf)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(info_stats.osds_conf)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "info_stats.osds_in", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(info_stats.osds_in)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(info_stats.osds_in)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(info_stats.osds_in)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(info_stats.osds_in)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "info_stats.osds_out", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(info_stats.osds_out)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(info_stats.osds_out)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(info_stats.osds_out)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(info_stats.osds_out)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "info_stats.osds_up", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(info_stats.osds_up)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(info_stats.osds_up)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(info_stats.osds_up)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(info_stats.osds_up)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "info_stats.osds_down", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(info_stats.osds_down)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(info_stats.osds_down)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(info_stats.osds_down)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(info_stats.osds_down)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "info_stats.osd_full_ratio", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(info_stats.osd_full_ratio)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(info_stats.osd_full_ratio)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(info_stats.osd_full_ratio)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(info_stats.osd_full_ratio)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "info_stats.osd_near_full_ratio", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(info_stats.osd_near_full_ratio)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(info_stats.osd_near_full_ratio)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(info_stats.osd_near_full_ratio)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(info_stats.osd_near_full_ratio)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.ComputeStoragePool.info_stats",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(info_stats)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "info_stats.reads", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(info_stats.reads)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(info_stats.reads)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(info_stats.reads)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(info_stats.reads)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "info_stats.writes", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(info_stats.writes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(info_stats.writes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(info_stats.writes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(info_stats.writes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "info_stats.read_kbytes", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(info_stats.read_kbytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(info_stats.read_kbytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(info_stats.read_kbytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(info_stats.read_kbytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "info_stats.write_kbytes", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(info_stats.write_kbytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(info_stats.write_kbytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(info_stats.write_kbytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(info_stats.write_kbytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.ComputeStorageOsd.info_stats",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(info_stats)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "uuid", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "info_stats.reads", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(info_stats.reads)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(info_stats.reads)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(info_stats.reads)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(info_stats.reads)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "info_stats.writes", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(info_stats.writes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(info_stats.writes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(info_stats.writes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(info_stats.writes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "info_stats.read_kbytes", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(info_stats.read_kbytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(info_stats.read_kbytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(info_stats.read_kbytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(info_stats.read_kbytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "info_stats.write_kbytes", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(info_stats.write_kbytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(info_stats.write_kbytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(info_stats.write_kbytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(info_stats.write_kbytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "info_stats.op_r_latency", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(info_stats.op_r_latency)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(info_stats.op_r_latency)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(info_stats.op_r_latency)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(info_stats.op_r_latency)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "info_stats.op_w_latency", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(info_stats.op_w_latency)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(info_stats.op_w_latency)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(info_stats.op_w_latency)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(info_stats.op_w_latency)", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.ComputeStorageDisk.info_stats",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(info_stats)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "uuid", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "info_stats.reads", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(info_stats.reads)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(info_stats.reads)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(info_stats.reads)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(info_stats.reads)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "info_stats.writes", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(info_stats.writes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(info_stats.writes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(info_stats.writes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(info_stats.writes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "info_stats.read_kbytes", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(info_stats.read_kbytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(info_stats.read_kbytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(info_stats.read_kbytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(info_stats.read_kbytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "info_stats.write_kbytes", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(info_stats.write_kbytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(info_stats.write_kbytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(info_stats.write_kbytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(info_stats.write_kbytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "info_stats.iops", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(info_stats.iops)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(info_stats.iops)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(info_stats.iops)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(info_stats.iops)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "info_stats.bw", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(info_stats.bw)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(info_stats.bw)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(info_stats.bw)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(info_stats.bw)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "info_stats.op_r_latency", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(info_stats.op_r_latency)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(info_stats.op_r_latency)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(info_stats.op_r_latency)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(info_stats.op_r_latency)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "info_stats.op_w_latency", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(info_stats.op_w_latency)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(info_stats.op_w_latency)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(info_stats.op_w_latency)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(info_stats.op_w_latency)", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.ServerMonitoringInfo.sensor_stats",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(sensor_stats)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "sensor_stats.sensor", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "sensor_stats.status", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "sensor_stats.reading", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(sensor_stats.reading)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(sensor_stats.reading)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(sensor_stats.reading)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(sensor_stats.reading)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "sensor_stats.unit", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "sensor_stats.sensor_type", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.ServerMonitoringInfo.disk_usage_stats",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(disk_usage_stats)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "disk_usage_stats.disk_name", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "disk_usage_stats.read_bytes", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(disk_usage_stats.read_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(disk_usage_stats.read_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(disk_usage_stats.read_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(disk_usage_stats.read_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "disk_usage_stats.write_bytes", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(disk_usage_stats.write_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(disk_usage_stats.write_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(disk_usage_stats.write_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(disk_usage_stats.write_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.ServerMonitoringSummary.network_info_stats",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(network_info_stats)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "network_info_stats.interface_name", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "network_info.tx_bytes", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(network_info.tx_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(network_info.tx_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(network_info.tx_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(network_info.tx_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "network_info.tx_packets", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(network_info.tx_packets)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(network_info.tx_packets)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(network_info.tx_packets)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(network_info.tx_packets)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "network_info.rx_bytes", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(network_info.rx_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(network_info.rx_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(network_info.rx_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(network_info.rx_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "network_info.rx_packets", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(network_info.rx_packets)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(network_info.rx_packets)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(network_info.rx_packets)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(network_info.rx_packets)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.ServerMonitoringSummary.resource_info_stats",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(resource_info_stats)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "resource_info_stats.cpu_usage_percentage", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "SUM(resource_info_stats.cpu_usage_percentage)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "CLASS(resource_info_stats.cpu_usage_percentage)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "MAX(resource_info_stats.cpu_usage_percentage)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "MIN(resource_info_stats.cpu_usage_percentage)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "resource_info_stats.mem_usage_mb", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "SUM(resource_info_stats.mem_usage_mb)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "CLASS(resource_info_stats.mem_usage_mb)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "MAX(resource_info_stats.mem_usage_mb)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "MIN(resource_info_stats.mem_usage_mb)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "resource_info_stats.mem_usage_percent", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "SUM(resource_info_stats.mem_usage_percent)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "CLASS(resource_info_stats.mem_usage_percent)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "MAX(resource_info_stats.mem_usage_percent)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "MIN(resource_info_stats.mem_usage_percent)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.ServerMonitoringInfo.file_system_view_stats.physical_disks",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(file_system_view_stats.physical_disks)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "file_system_view_stats.fs_name", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "file_system_view_stats.size_kb", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(file_system_view_stats.size_kb)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(file_system_view_stats.size_kb)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(file_system_view_stats.size_kb)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(file_system_view_stats.size_kb)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "file_system_view_stats.used_kb", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(file_system_view_stats.used_kb)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(file_system_view_stats.used_kb)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(file_system_view_stats.used_kb)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(file_system_view_stats.used_kb)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "file_system_view_stats.available_kb", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(file_system_view_stats.available_kb)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(file_system_view_stats.available_kb)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(file_system_view_stats.available_kb)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(file_system_view_stats.available_kb)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "file_system_view_stats.used_percentage", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(file_system_view_stats.used_percentage)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(file_system_view_stats.used_percentage)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(file_system_view_stats.used_percentage)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(file_system_view_stats.used_percentage)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "file_system_view_stats.mountpoint", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "file_system_view_stats.type", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "file_system_view_stats.physical_disks.disk_name", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "file_system_view_stats.physical_disks.disk_size_kb", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(file_system_view_stats.physical_disks.disk_size_kb)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(file_system_view_stats.physical_disks.disk_size_kb)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(file_system_view_stats.physical_disks.disk_size_kb)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(file_system_view_stats.physical_disks.disk_size_kb)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "file_system_view_stats.physical_disks.disk_used_kb", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(file_system_view_stats.physical_disks.disk_used_kb)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(file_system_view_stats.physical_disks.disk_used_kb)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(file_system_view_stats.physical_disks.disk_used_kb)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(file_system_view_stats.physical_disks.disk_used_kb)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "file_system_view_stats.physical_disks.disk_available_kb", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(file_system_view_stats.physical_disks.disk_available_kb)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(file_system_view_stats.physical_disks.disk_available_kb)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(file_system_view_stats.physical_disks.disk_available_kb)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(file_system_view_stats.physical_disks.disk_available_kb)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "file_system_view_stats.physical_disks.disk_used_percentage", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(file_system_view_stats.physical_disks.disk_used_percentage)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(file_system_view_stats.physical_disks.disk_used_percentage)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(file_system_view_stats.physical_disks.disk_used_percentage)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(file_system_view_stats.physical_disks.disk_used_percentage)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.SandeshMessageStat.msg_info",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(msg_info)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "msg_info.type", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "msg_info.level", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "msg_info.messages", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(msg_info.messages)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(msg_info.messages)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(msg_info.messages)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(msg_info.messages)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "msg_info.bytes", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(msg_info.bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(msg_info.bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(msg_info.bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(msg_info.bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.GeneratorDbStats.table_info",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(table_info)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "table_info.table_name", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "table_info.reads", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(table_info.reads)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(table_info.reads)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(table_info.reads)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(table_info.reads)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "table_info.read_fails", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(table_info.read_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(table_info.read_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(table_info.read_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(table_info.read_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "table_info.writes", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(table_info.writes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(table_info.writes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(table_info.writes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(table_info.writes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "table_info.write_fails", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(table_info.write_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(table_info.write_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(table_info.write_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(table_info.write_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.GeneratorDbStats.statistics_table_info",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(statistics_table_info)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "statistics_table_info.table_name", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "statistics_table_info.reads", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(statistics_table_info.reads)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(statistics_table_info.reads)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(statistics_table_info.reads)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(statistics_table_info.reads)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "statistics_table_info.read_fails", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(statistics_table_info.read_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(statistics_table_info.read_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(statistics_table_info.read_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(statistics_table_info.read_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "statistics_table_info.writes", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(statistics_table_info.writes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(statistics_table_info.writes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(statistics_table_info.writes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(statistics_table_info.writes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "statistics_table_info.write_fails", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(statistics_table_info.write_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(statistics_table_info.write_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(statistics_table_info.write_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(statistics_table_info.write_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.GeneratorDbStats.errors",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "errors.write_tablespace_fails", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(errors.write_tablespace_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(errors.write_tablespace_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(errors.write_tablespace_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(errors.write_tablespace_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "errors.read_tablespace_fails", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(errors.read_tablespace_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(errors.read_tablespace_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(errors.read_tablespace_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(errors.read_tablespace_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "errors.write_table_fails", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(errors.write_table_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(errors.write_table_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(errors.write_table_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(errors.write_table_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "errors.read_table_fails", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(errors.read_table_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(errors.read_table_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(errors.read_table_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(errors.read_table_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "errors.write_column_fails", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(errors.write_column_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(errors.write_column_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(errors.write_column_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(errors.write_column_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "errors.write_batch_column_fails", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(errors.write_batch_column_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(errors.write_batch_column_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(errors.write_batch_column_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(errors.write_batch_column_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "errors.read_column_fails", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(errors.read_column_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(errors.read_column_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(errors.read_column_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(errors.read_column_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.FieldNames.fields",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(fields)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "fields.value", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.FieldNames.fieldi",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(fieldi)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "fieldi.value", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(fieldi.value)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(fieldi.value)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(fieldi.value)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(fieldi.value)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.QueryPerfInfo.query_stats",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(query_stats)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "table", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": [
            "query_stats.qid"
          ]
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "query_stats.time", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(query_stats.time)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(query_stats.time)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(query_stats.time)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(query_stats.time)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "query_stats.rows", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(query_stats.rows)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(query_stats.rows)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(query_stats.rows)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(query_stats.rows)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "query_stats.qid", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "query_stats.where", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "query_stats.select", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "query_stats.post", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "query_stats.time_span", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(query_stats.time_span)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(query_stats.time_span)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(query_stats.time_span)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(query_stats.time_span)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "query_stats.chunks", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(query_stats.chunks)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(query_stats.chunks)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(query_stats.chunks)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(query_stats.chunks)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "query_stats.chunk_where_time", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "query_stats.chunk_select_time", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "query_stats.chunk_postproc_time", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "query_stats.chunk_merge_time", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "query_stats.final_merge_time", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(query_stats.final_merge_time)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(query_stats.final_merge_time)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(query_stats.final_merge_time)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(query_stats.final_merge_time)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "query_stats.enq_delay", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(query_stats.enq_delay)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(query_stats.enq_delay)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(query_stats.enq_delay)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(query_stats.enq_delay)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "query_stats.error", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.UveVirtualNetworkAgent.vn_stats",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(vn_stats)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "vn_stats.other_vn", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "vn_stats.vrouter", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "vn_stats.in_tpkts", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(vn_stats.in_tpkts)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(vn_stats.in_tpkts)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(vn_stats.in_tpkts)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(vn_stats.in_tpkts)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "vn_stats.in_bytes", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(vn_stats.in_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(vn_stats.in_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(vn_stats.in_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(vn_stats.in_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "vn_stats.out_tpkts", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(vn_stats.out_tpkts)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(vn_stats.out_tpkts)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(vn_stats.out_tpkts)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(vn_stats.out_tpkts)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "vn_stats.out_bytes", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(vn_stats.out_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(vn_stats.out_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(vn_stats.out_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(vn_stats.out_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.DatabasePurgeInfo.stats",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(stats)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "stats.purge_id", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "stats.request_time", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(stats.request_time)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(stats.request_time)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(stats.request_time)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(stats.request_time)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "stats.rows_deleted", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(stats.rows_deleted)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(stats.rows_deleted)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(stats.rows_deleted)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(stats.rows_deleted)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "stats.duration", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(stats.duration)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(stats.duration)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(stats.duration)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(stats.duration)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "stats.purge_status", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "stats.purge_status_details", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.DatabaseUsageInfo.database_usage",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(database_usage)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "database_usage.disk_space_used_1k", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(database_usage.disk_space_used_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(database_usage.disk_space_used_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(database_usage.disk_space_used_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(database_usage.disk_space_used_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "database_usage.disk_space_available_1k", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(database_usage.disk_space_available_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(database_usage.disk_space_available_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(database_usage.disk_space_available_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(database_usage.disk_space_available_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "database_usage.analytics_db_size_1k", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(database_usage.analytics_db_size_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(database_usage.analytics_db_size_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(database_usage.analytics_db_size_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(database_usage.analytics_db_size_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.ProtobufCollectorStats.tx_socket_stats",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(tx_socket_stats)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "tx_socket_stats.bytes", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(tx_socket_stats.bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(tx_socket_stats.bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(tx_socket_stats.bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(tx_socket_stats.bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "tx_socket_stats.calls", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(tx_socket_stats.calls)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(tx_socket_stats.calls)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(tx_socket_stats.calls)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(tx_socket_stats.calls)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "tx_socket_stats.average_bytes", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "SUM(tx_socket_stats.average_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "CLASS(tx_socket_stats.average_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "MAX(tx_socket_stats.average_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "MIN(tx_socket_stats.average_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "tx_socket_stats.blocked_duration", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "tx_socket_stats.blocked_count", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(tx_socket_stats.blocked_count)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(tx_socket_stats.blocked_count)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(tx_socket_stats.blocked_count)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(tx_socket_stats.blocked_count)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "tx_socket_stats.average_blocked_duration", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "tx_socket_stats.errors", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(tx_socket_stats.errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(tx_socket_stats.errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(tx_socket_stats.errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(tx_socket_stats.errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.ProtobufCollectorStats.rx_socket_stats",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(rx_socket_stats)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "rx_socket_stats.bytes", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(rx_socket_stats.bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(rx_socket_stats.bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(rx_socket_stats.bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(rx_socket_stats.bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "rx_socket_stats.calls", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(rx_socket_stats.calls)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(rx_socket_stats.calls)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(rx_socket_stats.calls)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(rx_socket_stats.calls)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "rx_socket_stats.average_bytes", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "SUM(rx_socket_stats.average_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "CLASS(rx_socket_stats.average_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "MAX(rx_socket_stats.average_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "MIN(rx_socket_stats.average_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "rx_socket_stats.blocked_duration", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "rx_socket_stats.blocked_count", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(rx_socket_stats.blocked_count)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(rx_socket_stats.blocked_count)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(rx_socket_stats.blocked_count)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(rx_socket_stats.blocked_count)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "rx_socket_stats.average_blocked_duration", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "rx_socket_stats.errors", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(rx_socket_stats.errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(rx_socket_stats.errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(rx_socket_stats.errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(rx_socket_stats.errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.ProtobufCollectorStats.rx_message_stats",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(rx_message_stats)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "rx_message_stats.endpoint_name", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "rx_message_stats.message_name", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "rx_message_stats.messages", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(rx_message_stats.messages)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(rx_message_stats.messages)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(rx_message_stats.messages)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(rx_message_stats.messages)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "rx_message_stats.bytes", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(rx_message_stats.bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(rx_message_stats.bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(rx_message_stats.bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(rx_message_stats.bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "rx_message_stats.errors", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(rx_message_stats.errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(rx_message_stats.errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(rx_message_stats.errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(rx_message_stats.errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "rx_message_stats.last_timestamp", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(rx_message_stats.last_timestamp)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(rx_message_stats.last_timestamp)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(rx_message_stats.last_timestamp)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(rx_message_stats.last_timestamp)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.ProtobufCollectorStats.db_table_info",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(db_table_info)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "db_table_info.table_name", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "db_table_info.reads", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(db_table_info.reads)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(db_table_info.reads)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(db_table_info.reads)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(db_table_info.reads)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "db_table_info.read_fails", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(db_table_info.read_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(db_table_info.read_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(db_table_info.read_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(db_table_info.read_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "db_table_info.writes", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(db_table_info.writes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(db_table_info.writes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(db_table_info.writes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(db_table_info.writes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "db_table_info.write_fails", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(db_table_info.write_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(db_table_info.write_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(db_table_info.write_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(db_table_info.write_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.ProtobufCollectorStats.db_statistics_table_info",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(db_statistics_table_info)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "db_statistics_table_info.table_name", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "db_statistics_table_info.reads", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(db_statistics_table_info.reads)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(db_statistics_table_info.reads)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(db_statistics_table_info.reads)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(db_statistics_table_info.reads)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "db_statistics_table_info.read_fails", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(db_statistics_table_info.read_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(db_statistics_table_info.read_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(db_statistics_table_info.read_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(db_statistics_table_info.read_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "db_statistics_table_info.writes", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(db_statistics_table_info.writes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(db_statistics_table_info.writes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(db_statistics_table_info.writes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(db_statistics_table_info.writes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "db_statistics_table_info.write_fails", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(db_statistics_table_info.write_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(db_statistics_table_info.write_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(db_statistics_table_info.write_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(db_statistics_table_info.write_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.ProtobufCollectorStats.db_errors",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(db_errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "db_errors.write_tablespace_fails", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(db_errors.write_tablespace_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(db_errors.write_tablespace_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(db_errors.write_tablespace_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(db_errors.write_tablespace_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "db_errors.read_tablespace_fails", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(db_errors.read_tablespace_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(db_errors.read_tablespace_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(db_errors.read_tablespace_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(db_errors.read_tablespace_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "db_errors.write_table_fails", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(db_errors.write_table_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(db_errors.write_table_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(db_errors.write_table_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(db_errors.write_table_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "db_errors.read_table_fails", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(db_errors.read_table_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(db_errors.read_table_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(db_errors.read_table_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(db_errors.read_table_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "db_errors.write_column_fails", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(db_errors.write_column_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(db_errors.write_column_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(db_errors.write_column_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(db_errors.write_column_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "db_errors.write_batch_column_fails", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(db_errors.write_batch_column_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(db_errors.write_batch_column_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(db_errors.write_batch_column_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(db_errors.write_batch_column_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "db_errors.read_column_fails", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(db_errors.read_column_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(db_errors.read_column_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(db_errors.read_column_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(db_errors.read_column_fails)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.UFlowData.flow",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(flow)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": [
            "flow.pifindex"
          ]
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "flow.pifindex", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(flow.pifindex)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(flow.pifindex)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(flow.pifindex)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(flow.pifindex)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "flow.sport", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(flow.sport)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(flow.sport)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(flow.sport)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(flow.sport)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "flow.dport", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(flow.dport)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(flow.dport)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(flow.dport)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(flow.dport)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "flow.protocol", 
          "suffixes": [
            "flow.sport", 
            "flow.dport"
          ]
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(flow.protocol)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(flow.protocol)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(flow.protocol)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(flow.protocol)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "flow.sip", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "flow.dip", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "flow.vlan", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "flow.flowtype", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "flow.otherinfo", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.AlarmgenUpdate.o",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(o)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "partition", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(partition)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(partition)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(partition)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(partition)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "o.key", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "o.count", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(o.count)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(o.count)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(o.count)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(o.count)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.AlarmgenUpdate.i",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(i)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "partition", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(partition)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(partition)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(partition)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(partition)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "table", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "i.collector", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "i.generator", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "i.type", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "i.count", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(i.count)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(i.count)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(i.count)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(i.count)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.AlarmgenStatus.counters",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(counters)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": [
            "counters.instance"
          ]
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "counters.instance", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "counters.partitions", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(counters.partitions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(counters.partitions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(counters.partitions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(counters.partitions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "counters.keys", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(counters.keys)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(counters.keys)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(counters.keys)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(counters.keys)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "counters.updates", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(counters.updates)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(counters.updates)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(counters.updates)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(counters.updates)", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.UveLoadbalancer.virtual_ip_stats",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(virtual_ip_stats)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "virtual_ip_stats.obj_name", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "virtual_ip_stats.uuid", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "virtual_ip_stats.status", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "virtual_ip_stats.vrouter", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "virtual_ip_stats.active_connections", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(virtual_ip_stats.active_connections)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(virtual_ip_stats.active_connections)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(virtual_ip_stats.active_connections)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(virtual_ip_stats.active_connections)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "virtual_ip_stats.max_connections", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(virtual_ip_stats.max_connections)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(virtual_ip_stats.max_connections)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(virtual_ip_stats.max_connections)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(virtual_ip_stats.max_connections)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "virtual_ip_stats.current_sessions", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(virtual_ip_stats.current_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(virtual_ip_stats.current_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(virtual_ip_stats.current_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(virtual_ip_stats.current_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "virtual_ip_stats.max_sessions", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(virtual_ip_stats.max_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(virtual_ip_stats.max_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(virtual_ip_stats.max_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(virtual_ip_stats.max_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "virtual_ip_stats.total_sessions", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(virtual_ip_stats.total_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(virtual_ip_stats.total_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(virtual_ip_stats.total_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(virtual_ip_stats.total_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "virtual_ip_stats.bytes_in", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(virtual_ip_stats.bytes_in)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(virtual_ip_stats.bytes_in)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(virtual_ip_stats.bytes_in)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(virtual_ip_stats.bytes_in)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "virtual_ip_stats.bytes_out", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(virtual_ip_stats.bytes_out)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(virtual_ip_stats.bytes_out)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(virtual_ip_stats.bytes_out)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(virtual_ip_stats.bytes_out)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "virtual_ip_stats.connection_errors", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(virtual_ip_stats.connection_errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(virtual_ip_stats.connection_errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(virtual_ip_stats.connection_errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(virtual_ip_stats.connection_errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "virtual_ip_stats.reponse_errors", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(virtual_ip_stats.reponse_errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(virtual_ip_stats.reponse_errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(virtual_ip_stats.reponse_errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(virtual_ip_stats.reponse_errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.UveLoadbalancer.listener_stats",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(listener_stats)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "listener_stats.obj_name", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "listener_stats.uuid", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "listener_stats.status", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "listener_stats.vrouter", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "listener_stats.active_connections", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(listener_stats.active_connections)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(listener_stats.active_connections)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(listener_stats.active_connections)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(listener_stats.active_connections)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "listener_stats.max_connections", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(listener_stats.max_connections)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(listener_stats.max_connections)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(listener_stats.max_connections)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(listener_stats.max_connections)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "listener_stats.current_sessions", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(listener_stats.current_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(listener_stats.current_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(listener_stats.current_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(listener_stats.current_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "listener_stats.max_sessions", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(listener_stats.max_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(listener_stats.max_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(listener_stats.max_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(listener_stats.max_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "listener_stats.total_sessions", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(listener_stats.total_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(listener_stats.total_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(listener_stats.total_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(listener_stats.total_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "listener_stats.bytes_in", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(listener_stats.bytes_in)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(listener_stats.bytes_in)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(listener_stats.bytes_in)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(listener_stats.bytes_in)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "listener_stats.bytes_out", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(listener_stats.bytes_out)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(listener_stats.bytes_out)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(listener_stats.bytes_out)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(listener_stats.bytes_out)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "listener_stats.connection_errors", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(listener_stats.connection_errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(listener_stats.connection_errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(listener_stats.connection_errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(listener_stats.connection_errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "listener_stats.reponse_errors", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(listener_stats.reponse_errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(listener_stats.reponse_errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(listener_stats.reponse_errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(listener_stats.reponse_errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.UveLoadbalancer.pool_stats",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(pool_stats)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "pool_stats.obj_name", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "pool_stats.uuid", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "pool_stats.status", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "pool_stats.vrouter", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "pool_stats.active_connections", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(pool_stats.active_connections)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(pool_stats.active_connections)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(pool_stats.active_connections)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(pool_stats.active_connections)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "pool_stats.max_connections", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(pool_stats.max_connections)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(pool_stats.max_connections)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(pool_stats.max_connections)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(pool_stats.max_connections)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "pool_stats.current_sessions", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(pool_stats.current_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(pool_stats.current_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(pool_stats.current_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(pool_stats.current_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "pool_stats.max_sessions", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(pool_stats.max_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(pool_stats.max_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(pool_stats.max_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(pool_stats.max_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "pool_stats.total_sessions", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(pool_stats.total_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(pool_stats.total_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(pool_stats.total_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(pool_stats.total_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "pool_stats.bytes_in", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(pool_stats.bytes_in)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(pool_stats.bytes_in)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(pool_stats.bytes_in)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(pool_stats.bytes_in)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "pool_stats.bytes_out", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(pool_stats.bytes_out)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(pool_stats.bytes_out)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(pool_stats.bytes_out)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(pool_stats.bytes_out)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "pool_stats.connection_errors", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(pool_stats.connection_errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(pool_stats.connection_errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(pool_stats.connection_errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(pool_stats.connection_errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "pool_stats.reponse_errors", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(pool_stats.reponse_errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(pool_stats.reponse_errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(pool_stats.reponse_errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(pool_stats.reponse_errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.UveLoadbalancer.member_stats",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(member_stats)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "member_stats.obj_name", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "member_stats.uuid", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "member_stats.status", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "member_stats.vrouter", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "member_stats.active_connections", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(member_stats.active_connections)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(member_stats.active_connections)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(member_stats.active_connections)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(member_stats.active_connections)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "member_stats.max_connections", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(member_stats.max_connections)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(member_stats.max_connections)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(member_stats.max_connections)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(member_stats.max_connections)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "member_stats.current_sessions", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(member_stats.current_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(member_stats.current_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(member_stats.current_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(member_stats.current_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "member_stats.max_sessions", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(member_stats.max_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(member_stats.max_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(member_stats.max_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(member_stats.max_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "member_stats.total_sessions", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(member_stats.total_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(member_stats.total_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(member_stats.total_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(member_stats.total_sessions)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "member_stats.bytes_in", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(member_stats.bytes_in)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(member_stats.bytes_in)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(member_stats.bytes_in)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(member_stats.bytes_in)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "member_stats.bytes_out", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(member_stats.bytes_out)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(member_stats.bytes_out)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(member_stats.bytes_out)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(member_stats.bytes_out)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "member_stats.connection_errors", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(member_stats.connection_errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(member_stats.connection_errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(member_stats.connection_errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(member_stats.connection_errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "member_stats.reponse_errors", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(member_stats.reponse_errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(member_stats.reponse_errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(member_stats.reponse_errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(member_stats.reponse_errors)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.NodeStatus.disk_usage_info",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(disk_usage_info)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "disk_usage_info.partition_type", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "disk_usage_info.partition_name", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "disk_usage_info.partition_space_used_1k", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(disk_usage_info.partition_space_used_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(disk_usage_info.partition_space_used_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(disk_usage_info.partition_space_used_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(disk_usage_info.partition_space_used_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "disk_usage_info.partition_space_available_1k", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(disk_usage_info.partition_space_available_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(disk_usage_info.partition_space_available_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(disk_usage_info.partition_space_available_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(disk_usage_info.partition_space_available_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.NodeStatus.disk_usage_info",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(disk_usage_info)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "disk_usage_info.partition_type", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "disk_usage_info.partition_name", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "disk_usage_info.partition_space_used_1k", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(disk_usage_info.partition_space_used_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(disk_usage_info.partition_space_used_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(disk_usage_info.partition_space_used_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(disk_usage_info.partition_space_used_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "disk_usage_info.partition_space_available_1k", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(disk_usage_info.partition_space_available_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(disk_usage_info.partition_space_available_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(disk_usage_info.partition_space_available_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(disk_usage_info.partition_space_available_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.NodeStatus.disk_usage_info",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(disk_usage_info)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "disk_usage_info.partition_type", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "disk_usage_info.partition_name", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "disk_usage_info.partition_space_used_1k", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(disk_usage_info.partition_space_used_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(disk_usage_info.partition_space_used_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(disk_usage_info.partition_space_used_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(disk_usage_info.partition_space_used_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "disk_usage_info.partition_space_available_1k", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(disk_usage_info.partition_space_available_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(disk_usage_info.partition_space_available_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(disk_usage_info.partition_space_available_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(disk_usage_info.partition_space_available_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.NodeStatus.disk_usage_info",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(disk_usage_info)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "disk_usage_info.partition_type", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "disk_usage_info.partition_name", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "disk_usage_info.partition_space_used_1k", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(disk_usage_info.partition_space_used_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(disk_usage_info.partition_space_used_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(disk_usage_info.partition_space_used_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(disk_usage_info.partition_space_used_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "disk_usage_info.partition_space_available_1k", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(disk_usage_info.partition_space_available_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(disk_usage_info.partition_space_available_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(disk_usage_info.partition_space_available_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(disk_usage_info.partition_space_available_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.NodeStatus.disk_usage_info",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(disk_usage_info)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "disk_usage_info.partition_type", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "disk_usage_info.partition_name", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "disk_usage_info.partition_space_used_1k", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(disk_usage_info.partition_space_used_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(disk_usage_info.partition_space_used_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(disk_usage_info.partition_space_used_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(disk_usage_info.partition_space_used_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "disk_usage_info.partition_space_available_1k", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(disk_usage_info.partition_space_available_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(disk_usage_info.partition_space_available_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(disk_usage_info.partition_space_available_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(disk_usage_info.partition_space_available_1k)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.UveVMInterfaceAgent.fip_diff_stats",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(fip_diff_stats)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "virtual_network", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "fip_diff_stats.other_vn", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "fip_diff_stats.ip_address", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "fip_diff_stats.in_pkts", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(fip_diff_stats.in_pkts)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(fip_diff_stats.in_pkts)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(fip_diff_stats.in_pkts)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(fip_diff_stats.in_pkts)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "fip_diff_stats.in_bytes", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(fip_diff_stats.in_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(fip_diff_stats.in_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(fip_diff_stats.in_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(fip_diff_stats.in_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "fip_diff_stats.out_pkts", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(fip_diff_stats.out_pkts)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(fip_diff_stats.out_pkts)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(fip_diff_stats.out_pkts)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(fip_diff_stats.out_pkts)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "fip_diff_stats.out_bytes", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(fip_diff_stats.out_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(fip_diff_stats.out_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(fip_diff_stats.out_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(fip_diff_stats.out_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.UveVMInterfaceAgent.if_stats",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(if_stats)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "vm_name", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "vm_uuid", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "if_stats.in_pkts", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(if_stats.in_pkts)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(if_stats.in_pkts)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(if_stats.in_pkts)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(if_stats.in_pkts)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "if_stats.in_bytes", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(if_stats.in_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(if_stats.in_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(if_stats.in_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(if_stats.in_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "if_stats.out_pkts", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(if_stats.out_pkts)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(if_stats.out_pkts)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(if_stats.out_pkts)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(if_stats.out_pkts)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "if_stats.out_bytes", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(if_stats.out_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(if_stats.out_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(if_stats.out_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(if_stats.out_bytes)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "if_stats.in_bw_usage", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(if_stats.in_bw_usage)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(if_stats.in_bw_usage)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(if_stats.in_bw_usage)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(if_stats.in_bw_usage)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "if_stats.out_bw_usage", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(if_stats.out_bw_usage)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(if_stats.out_bw_usage)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(if_stats.out_bw_usage)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(if_stats.out_bw_usage)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.VrouterStatsAgent.flow_rate",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(flow_rate)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "flow_rate.added_flows", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(flow_rate.added_flows)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(flow_rate.added_flows)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(flow_rate.added_flows)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(flow_rate.added_flows)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "flow_rate.max_flow_adds_per_second", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(flow_rate.max_flow_adds_per_second)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(flow_rate.max_flow_adds_per_second)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(flow_rate.max_flow_adds_per_second)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(flow_rate.max_flow_adds_per_second)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "flow_rate.min_flow_adds_per_second", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(flow_rate.min_flow_adds_per_second)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(flow_rate.min_flow_adds_per_second)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(flow_rate.min_flow_adds_per_second)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(flow_rate.min_flow_adds_per_second)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "flow_rate.deleted_flows", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(flow_rate.deleted_flows)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(flow_rate.deleted_flows)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(flow_rate.deleted_flows)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(flow_rate.deleted_flows)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "flow_rate.max_flow_deletes_per_second", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(flow_rate.max_flow_deletes_per_second)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(flow_rate.max_flow_deletes_per_second)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(flow_rate.max_flow_deletes_per_second)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(flow_rate.max_flow_deletes_per_second)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "flow_rate.min_flow_deletes_per_second", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(flow_rate.min_flow_deletes_per_second)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(flow_rate.min_flow_deletes_per_second)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(flow_rate.min_flow_deletes_per_second)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(flow_rate.min_flow_deletes_per_second)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.AnalyticsApiStats.api_stats",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(api_stats)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "api_stats.operation_type", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "api_stats.remote_ip", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "api_stats.object_type", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "api_stats.request_url", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "api_stats.response_time_in_usec", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(api_stats.response_time_in_usec)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(api_stats.response_time_in_usec)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(api_stats.response_time_in_usec)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(api_stats.response_time_in_usec)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "api_stats.response_size", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(api_stats.response_size)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(api_stats.response_size)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(api_stats.response_size)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(api_stats.response_size)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": false, 
          "name": "api_stats.node", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.VncApiStatsLog.api_stats",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(api_stats)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "api_stats.operation_type", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "api_stats.user", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "api_stats.useragent", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "api_stats.remote_ip", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "api_stats.domain_name", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "api_stats.project_name", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "api_stats.object_type", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": true, 
          "name": "api_stats.response_time_in_usec", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "SUM(api_stats.response_time_in_usec)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "CLASS(api_stats.response_time_in_usec)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "MAX(api_stats.response_time_in_usec)", 
          "suffixes": null
        }, 
        {
          "datatype": "double", 
          "index": false, 
          "name": "MIN(api_stats.response_time_in_usec)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "api_stats.response_size", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(api_stats.response_size)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(api_stats.response_size)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(api_stats.response_size)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(api_stats.response_size)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "api_stats.response_code", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(api_stats.response_code)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(api_stats.response_code)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(api_stats.response_code)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(api_stats.response_code)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.VrouterStatsAgent.phy_if_band",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(phy_if_band)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "phy_if_band.name", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "phy_if_band.in_bandwidth_usage", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(phy_if_band.in_bandwidth_usage)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(phy_if_band.in_bandwidth_usage)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(phy_if_band.in_bandwidth_usage)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(phy_if_band.in_bandwidth_usage)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "phy_if_band.out_bandwidth_usage", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(phy_if_band.out_bandwidth_usage)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(phy_if_band.out_bandwidth_usage)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(phy_if_band.out_bandwidth_usage)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(phy_if_band.out_bandwidth_usage)", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.PRouterBroadViewInfo.ingressPortPriorityGroup",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(ingressPortPriorityGroup)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "asic_id", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ingressPortPriorityGroup.port", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "ingressPortPriorityGroup.priorityGroup", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(ingressPortPriorityGroup.priorityGroup)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(ingressPortPriorityGroup.priorityGroup)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(ingressPortPriorityGroup.priorityGroup)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(ingressPortPriorityGroup.priorityGroup)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "ingressPortPriorityGroup.umShareBufferCount", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(ingressPortPriorityGroup.umShareBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(ingressPortPriorityGroup.umShareBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(ingressPortPriorityGroup.umShareBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(ingressPortPriorityGroup.umShareBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "ingressPortPriorityGroup.umHeadroomBufferCount", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(ingressPortPriorityGroup.umHeadroomBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(ingressPortPriorityGroup.umHeadroomBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(ingressPortPriorityGroup.umHeadroomBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(ingressPortPriorityGroup.umHeadroomBufferCount)", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.PRouterBroadViewInfo.ingressPortServicePool",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(ingressPortServicePool)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "asic_id", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "ingressPortServicePool.port", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "ingressPortServicePool.servicePool", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(ingressPortServicePool.servicePool)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(ingressPortServicePool.servicePool)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(ingressPortServicePool.servicePool)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(ingressPortServicePool.servicePool)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "ingressPortServicePool.umShareBufferCount", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(ingressPortServicePool.umShareBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(ingressPortServicePool.umShareBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(ingressPortServicePool.umShareBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(ingressPortServicePool.umShareBufferCount)", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.PRouterBroadViewInfo.ingressServicePool",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(ingressServicePool)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "asic_id", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "ingressServicePool.servicePool", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(ingressServicePool.servicePool)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(ingressServicePool.servicePool)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(ingressServicePool.servicePool)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(ingressServicePool.servicePool)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "ingressServicePool.umShareBufferCount", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(ingressServicePool.umShareBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(ingressServicePool.umShareBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(ingressServicePool.umShareBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(ingressServicePool.umShareBufferCount)", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.PRouterBroadViewInfo.egressPortServicePool",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(egressPortServicePool)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "asic_id", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "egressPortServicePool.port", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "egressPortServicePool.servicePool", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(egressPortServicePool.servicePool)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(egressPortServicePool.servicePool)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(egressPortServicePool.servicePool)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(egressPortServicePool.servicePool)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "egressPortServicePool.ucShareBufferCount", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(egressPortServicePool.ucShareBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(egressPortServicePool.ucShareBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(egressPortServicePool.ucShareBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(egressPortServicePool.ucShareBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "egressPortServicePool.umShareBufferCount", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(egressPortServicePool.umShareBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(egressPortServicePool.umShareBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(egressPortServicePool.umShareBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(egressPortServicePool.umShareBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "egressPortServicePool.mcShareBufferCount", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(egressPortServicePool.mcShareBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(egressPortServicePool.mcShareBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(egressPortServicePool.mcShareBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(egressPortServicePool.mcShareBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "egressPortServicePool.mcShareQueueEntries", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(egressPortServicePool.mcShareQueueEntries)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(egressPortServicePool.mcShareQueueEntries)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(egressPortServicePool.mcShareQueueEntries)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(egressPortServicePool.mcShareQueueEntries)", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.PRouterBroadViewInfo.egressServicePool",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(egressServicePool)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "asic_id", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "egressServicePool.servicePool", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(egressServicePool.servicePool)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(egressServicePool.servicePool)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(egressServicePool.servicePool)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(egressServicePool.servicePool)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "egressServicePool.umShareBufferCount", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(egressServicePool.umShareBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(egressServicePool.umShareBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(egressServicePool.umShareBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(egressServicePool.umShareBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "egressServicePool.mcShareBufferCount", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(egressServicePool.mcShareBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(egressServicePool.mcShareBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(egressServicePool.mcShareBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(egressServicePool.mcShareBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "egressServicePool.mcShareQueueEntries", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(egressServicePool.mcShareQueueEntries)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(egressServicePool.mcShareQueueEntries)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(egressServicePool.mcShareQueueEntries)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(egressServicePool.mcShareQueueEntries)", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.PRouterBroadViewInfo.egressUcQueue",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(egressUcQueue)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "asic_id", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "egressUcQueue.queue", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(egressUcQueue.queue)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(egressUcQueue.queue)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(egressUcQueue.queue)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(egressUcQueue.queue)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "egressUcQueue.ucBufferCount", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(egressUcQueue.ucBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(egressUcQueue.ucBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(egressUcQueue.ucBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(egressUcQueue.ucBufferCount)", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.PRouterBroadViewInfo.egressUcQueueGroup",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(egressUcQueueGroup)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "asic_id", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "egressUcQueueGroup.queueGroup", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(egressUcQueueGroup.queueGroup)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(egressUcQueueGroup.queueGroup)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(egressUcQueueGroup.queueGroup)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(egressUcQueueGroup.queueGroup)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "egressUcQueueGroup.ucBufferCount", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(egressUcQueueGroup.ucBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(egressUcQueueGroup.ucBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(egressUcQueueGroup.ucBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(egressUcQueueGroup.ucBufferCount)", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.PRouterBroadViewInfo.egressMcQueue",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(egressMcQueue)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "asic_id", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "egressMcQueue.queue", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(egressMcQueue.queue)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(egressMcQueue.queue)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(egressMcQueue.queue)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(egressMcQueue.queue)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "egressMcQueue.mcBufferCount", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(egressMcQueue.mcBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(egressMcQueue.mcBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(egressMcQueue.mcBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(egressMcQueue.mcBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "egressMcQueue.mcQueueEntries", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(egressMcQueue.mcQueueEntries)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(egressMcQueue.mcQueueEntries)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(egressMcQueue.mcQueueEntries)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(egressMcQueue.mcQueueEntries)", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.PRouterBroadViewInfo.egressCpuQueue",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(egressCpuQueue)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "asic_id", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "egressCpuQueue.queue", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(egressCpuQueue.queue)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(egressCpuQueue.queue)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(egressCpuQueue.queue)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(egressCpuQueue.queue)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "egressCpuQueue.cpuBufferCount", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(egressCpuQueue.cpuBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(egressCpuQueue.cpuBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(egressCpuQueue.cpuBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(egressCpuQueue.cpuBufferCount)", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    {
    "table-name": "StatTable.PRouterBroadViewInfo.egressRqeQueue",
    "table-schema": 
    {
      "columns": [
        {
          "datatype": "string", 
          "index": true, 
          "name": "Source", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "T=", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(T=)", 
          "suffixes": null
        }, 
        {
          "datatype": "uuid", 
          "index": false, 
          "name": "UUID", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "COUNT(egressRqeQueue)", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "name", 
          "suffixes": null
        }, 
        {
          "datatype": "string", 
          "index": true, 
          "name": "asic_id", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": true, 
          "name": "egressRqeQueue.queue", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(egressRqeQueue.queue)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(egressRqeQueue.queue)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(egressRqeQueue.queue)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(egressRqeQueue.queue)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "egressRqeQueue.rqeBufferCount", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "SUM(egressRqeQueue.rqeBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "CLASS(egressRqeQueue.rqeBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MAX(egressRqeQueue.rqeBufferCount)", 
          "suffixes": null
        }, 
        {
          "datatype": "int", 
          "index": false, 
          "name": "MIN(egressRqeQueue.rqeBufferCount)", 
          "suffixes": null
        }
      ], 
      "type": "STAT"
    }
    },
    ]

