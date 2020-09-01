# Contrail Node Status
A physical server can be assigned multiple contrail roles and have the corresponding software installed on it. Examples of such roles is Config, Control, Analytics, Compute. We define these roles as a contrail virtual node. This write up describes how the status of a contrail virtual node and contrail process' status is derived. 

We use the UVE mechanism to send and aggregate the status information. All node types - Config, Compute, Analytics, Control will send a NodeStatus structure in their respective node UVEs. A Control Node UVE is given below as an example.

    struct NodeStatus {
        1: string name (key="ObjectBgpRouter")
        2: optional bool deleted
        3: optional string status
        // Sent by process
        4: optional list<process_info.ProcessStatus> process_status (aggtype="union")
        // Sent by node manager
        5: optional list<process_info.ProcessInfo> process_info (aggtype="union")
        6: optional string description
    }

    uve sandesh NodeStatusUVE {
        1: NodeStatus data
    }

The NodeStatus structure consists of 2 structures:
 
1. A ProcessStatus which is sent by the processes, corresponding to that virtual node, called process_status. The data in this structure corresponds to various status information of the process and an aggregate state which says if the process is Functional or Non-Functional. The status information will be the state of a process's connections (ConnectionInfo) to important services and other information necessary for the process to be Functional. The ProcessStatus structure is given below. Each process sends its NodeStatus information which is aggregated as 'union' (based on the annotation aggtype="union") at the Analytics node.  

        struct ProcessStatus {
            1: string module_id
            2: string instance_id
            3: string state
            4: optional list<ConnectionInfo> connection_infos
            5: optional string description
        }

        struct ConnectionInfo {
            1: string type
            2: string name
            3: optional list<string> server_addrs
            4: string status
            5: optional string description
        }

2. a ProcessInfo which is sent by the node manager (/usr/bin/contrail-nodemgr). Node manager is a monitor process per contrail virtual node, which tracks the running state of the processes. The ProcessInfo structure is given below.  

        struct ProcessInfo {
             1: string                              process_name
             2: string                              process_state
             3: u32                                 start_count
             4: u32                                 stop_count
             5: u32                                 exit_count
             // time when the process last entered running stage
             6: optional string                     last_start_time
             7: optional string                     last_stop_time
             8: optional string                     last_exit_time
             9: optional list<string>               core_file_list
         }

An example output of NodeStatus obtained from the Rest API
http://<server-ip>:8081/analytics/uves/control-node/a6s45?cfilt=NodeStatus
is given below.

    {
		NodeStatus:  {
		process_info:  [
		 {
		process_name: "contrail-control",
		process_state: "PROCESS_STATE_RUNNING",
		last_stop_time: null,
		start_count: 1,
		core_file_list: [ ],
		last_start_time: "1409002143776558",
		stop_count: 0,
		last_exit_time: null,
		exit_count: 0
		},
		 {
		process_name: "contrail-control-nodemgr",
		process_state: "PROCESS_STATE_RUNNING",
		last_stop_time: null,
		start_count: 1,
		core_file_list: [ ],
		last_start_time: "1409002141773481",
		stop_count: 0,
		last_exit_time: null,
		exit_count: 0
		},
		 {
		process_name: "contrail-dns",
		process_state: "PROCESS_STATE_RUNNING",
		last_stop_time: null,
		start_count: 1,
		core_file_list: [ ],
		last_start_time: "1409002145778383",
		stop_count: 0,
		last_exit_time: null,
		exit_count: 0
		},
		 {
		process_name: "contrail-named",
		process_state: "PROCESS_STATE_RUNNING",
		last_stop_time: null,
		start_count: 1,
		core_file_list: [ ],
		last_start_time: "1409002147780118",
		stop_count: 0,
		last_exit_time: null,
		exit_count: 0
		}
		],
		process_status:  [
		 {
		instance_id: "0",
		module_id: "ControlNode",
		state: "Functional",
		description: null,
		connection_infos:  [
		 {
		server_addrs:  [
		"10.84.13.45:8443"
		],
		status: "Up",
		type: "IFMap",
		name: "IFMapServer",
		description: "Connection with IFMap Server (irond)"
		},
		 {
		server_addrs:  [
		"10.84.13.45:8086"
		],
		status: "Up",
		type: "Collector",
		name: null,
		description: "Established"
		},
		 {
		server_addrs:  [
		"10.84.13.45:5998"
		],
		status: "Up",
		type: "Discovery",
		name: "Collector",
		description: "SubscribeResponse"
		},
		 {
		server_addrs:  [
		"10.84.13.45:5998"
		],
		status: "Up",
		type: "Discovery",
		name: "IfmapServer",
		description: "SubscribeResponse"
		},
		 {
		server_addrs:  [
		"10.84.13.45:5998"
		],
		status: "Up",
		type: "Discovery",
		name: "xmpp-server",
		description: "Publish Response - HeartBeat"
		}
		]
		}
		]
		}
    }

We can also obtain a specific process's state using the introspect mechanism. For e.g, contrail-control's process state is obtained using
http://server-ip:8083/Snh_SandeshUVECacheReq?x=NodeStatus


    root@a6s10:~# curl -s http://10.84.13.10:8083/Snh_SandeshUVECacheReq?x=NodeStatus | xmllint --format -
    <?xml version="1.0"?>
    <?xml-stylesheet type="text/xsl" href="/universal_parse.xsl"?>
    <__NodeStatusUVE_list type="slist">
      <NodeStatusUVE type="sandesh">
        <data type="struct" identifier="1">
          <NodeStatus>
            <name type="string" identifier="1" key="ObjectBgpRouter">a6s10</name>
            <process_status type="list" identifier="4" aggtype="union">
              <list type="struct" size="1">
                <ProcessStatus>
                  <module_id type="string" identifier="1">ControlNode</module_id>
                  <instance_id type="string" identifier="2">0</instance_id>
                  <state type="string" identifier="3">Functional</state>
                  <connection_infos type="list" identifier="4">
                    <list type="struct" size="5">
                      <ConnectionInfo>
                        <type type="string" identifier="1">IFMap</type>
                        <name type="string" identifier="2">IFMapServer</name>
                        <server_addrs type="list" identifier="3">
                          <list type="string" size="1">
                            <element>10.84.13.10:8443</element>
                          </list>
                        </server_addrs>
                        <status type="string" identifier="4">Up</status>
                        <description type="string" identifier="5">Connection with IFMap Server (irond)</description>
                      </ConnectionInfo>
                      <ConnectionInfo>
                        <type type="string" identifier="1">Collector</type>
                        <name type="string" identifier="2"/>
                        <server_addrs type="list" identifier="3">
                          <list type="string" size="1">
                            <element>10.84.13.10:8086</element>
                          </list>
                        </server_addrs>
                        <status type="string" identifier="4">Up</status>
                        <description type="string" identifier="5">Established</description>
                      </ConnectionInfo>
                      <ConnectionInfo>
                        <type type="string" identifier="1">Discovery</type>
                        <name type="string" identifier="2">Collector</name>
                        <server_addrs type="list" identifier="3">
                          <list type="string" size="1">
                            <element>10.84.13.10:5998</element>
                          </list>
                        </server_addrs>
                        <status type="string" identifier="4">Up</status>
                        <description type="string" identifier="5">SubscribeResponse</description>
                      </ConnectionInfo>
                      <ConnectionInfo>
                        <type type="string" identifier="1">Discovery</type>
                        <name type="string" identifier="2">IfmapServer</name>
                        <server_addrs type="list" identifier="3">
                          <list type="string" size="1">
                            <element>10.84.13.10:5998</element>
                          </list>
                        </server_addrs>
                        <status type="string" identifier="4">Up</status>
                        <description type="string" identifier="5">SubscribeResponse</description>
                      </ConnectionInfo>
                    </list>
                  </connection_infos>
                  <description type="string" identifier="5"/>
                </ProcessStatus>
              </list>
            </process_status>
          </NodeStatus>
        </data>
      </NodeStatusUVE>
      <SandeshUVECacheResp type="sandesh">
        <returned type="u32" identifier="1">1</returned>
        <more type="bool" identifier="0">false</more>
      </SandeshUVECacheResp>
    </__NodeStatusUVE_list>
    root@a6s10:~#

The above output is ProcessStatus of only one process - contrail-control vs. the earlier output that showed aggregated status of Control Node through its UVE.

# contrail-status script
contrail-status script is used to give status of contrail processes on a server, an example output looks as below

    root@a6s45:~# contrail-status
    == Contrail vRouter ==
    supervisor-vrouter:           active
    contrail-vrouter-agent        active
    contrail-vrouter-nodemgr      active

    == Contrail Control ==
    supervisor-control:           active
    contrail-control              active
    contrail-control-nodemgr      active
    contrail-dns                  active
    contrail-named                active

    == Contrail Analytics ==
    supervisor-analytics:         active
    contrail-analytics-api        active
    contrail-analytics-nodemgr    active
    contrail-collector            active
    contrail-query-engine         active

    == Contrail Config ==
    supervisor-config:            active
    contrail-api:0                active
    contrail-config-nodemgr       active
    contrail-discovery:0          active
    contrail-schema               active
    contrail-svc-monitor          active
    ifmap                         active
    rabbitmq-server               active

    == Contrail Web UI ==
    supervisor-webui:             active
    contrail-webui                active
    contrail-webui-middleware     active
    redis-webui                   active

    == Contrail Database ==
    supervisord-contrail-database:active
    contrail-database             active
    contrail-database-nodemgr     active

contrail-status first checks if a process is running, and if it is, it does introspect into the process to get
it's functionality status, and outputs the 'aggregate' status. The states displayed are
* active - if the process is running and functional [internal state is good]
* inactive - stopped by user
* failed - process exited too quickly and not restarted
* initializing - if the process is running, but internal state is not yet functional.