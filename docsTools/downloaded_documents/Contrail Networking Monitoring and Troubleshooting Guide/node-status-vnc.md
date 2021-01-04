# Getting Contrail Node Status

 

## Overview

This topic describes how to view the status of a Contrail node on a
physical server. Contrail nodes include config, control, analytics,
compute, and so on.

## UVE for NodeStatus

The User-Visible Entity (UVE) mechanism is used to aggregate and send
the status information. All node types send a NodeStatus structure in
their respective node UVEs. The following is a control node UVE of
NodeStatus:

<div id="jd0e25" class="example" dir="ltr">

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

</div>

## Node Status Features

The most important features of NodeStatus include:

ProcessStatus

ProcessInfo

<div id="jd0e39" class="example" dir="ltr">

### ProcessStatus

Also process\_status, is sent by the processes corresponding to the
virtual node, and displays the status of the process and an aggregate
state indicating if the process is functional or non-functional. The
process\_status includes the state of the process connections
(ConnectionInfo) to important services and other information necessary
for the process to be functional. Each process sends its NodeStatus
information, which is aggregated as union (aggtype="union") at the
analytics node. The following is the ProcessStatus structure:

    1.   struct ProcessStatus {

    2.       1: string module_id

    3.       2: string instance_id

    4.       3: string state

    5.       4: optional list<ConnectionInfo> connection_infos

    6.       5: optional string description

    7.   }

    8.    

    9.   struct ConnectionInfo {

    10.      1: string type

    11.      2: string name

    12.      3: optional list<string> server_addrs

    13.      4: string status

    14.      5: optional string description

    15.  }

</div>

<div id="jd0e47" class="example" dir="ltr">

### ProcessInfo

Sent by the node manager, /usr/bin/contrail-nodemgr. Node manager is a
monitor process per contrail virtual node that tracks the running state
of the processes. The following is the ProcessInfo structure:

    16.  struct ProcessInfo {

    17.       1: string                              process_name

    18.       2: string                              process_state

    19.       3: u32                                 start_count

    20.       4: u32                                 stop_count

    21.       5: u32                                 exit_count

    22.       // time when the process last entered running stage

    23.       6: optional string                     last_start_time

    24.       7: optional string                     last_stop_time

    25.       8: optional string                     last_exit_time

    26.       9: optional list<string>               core_file_list

    27.   }

</div>

<div id="jd0e55" class="example" dir="ltr">

### Example: NodeStatus

The following is an example output of NodeStatus obtained from the Rest
API:

    http://:8081/analytics/uves/control-...ilt=NodeStatus .

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

</div>

## Using Introspect to Get Process Status

The user can also view the state of a specific process by using the
introspect mechanism.

<div id="jd0e70" class="example" dir="ltr">

### Example: Introspect of NodeStatus

The following is an example of the process state of contrail-control
that is obtained by using

`http://server-ip:8083/Snh_SandeshUVECacheReq?x=NodeStatus  `

**Note**

The example output is the ProcessStatus of only one process of
contrail-control. It does not show the full aggregated status of the
control node through its UVE (as in the previous example).

    root@a6s45:~# curl http://10.84.13.45:8083/Snh_SandeshU...q?x=NodeStatus

    <?xml-stylesheet type="text/xsl" href="/universal_parse.xsl"?><__NodeStatusUVE_list type="slist"><NodeStatusUVE type="sandesh"><data type="struct" identifier="1"><NodeStatus><name type="string" identifier="1" key="ObjectBgpRouter">a6s45</name><process_status type="list" identifier="4" aggtype="union"><list type="struct" size="1"><ProcessStatus><module_id type="string" identifier="1">ControlNode</module_id><instance_id type="string" identifier="2">0</instance_id><state type="string" identifier="3">Functional</state><connection_infos type="list" identifier="4"><list type="struct" size="5"><ConnectionInfo><type type="string" identifier="1">IFMap</type><name type="string" identifier="2">IFMapServer</name><server_addrs type="list" identifier="3"><list type="string" size="1"><element>10.84.13.45:8443</element></list></server_addrs><status type="string" identifier="4">Up</status><description type="string" identifier="5">Connection with IFMap Server (irond)</description></ConnectionInfo><ConnectionInfo><type type="string" identifier="1">Collector</type><name type="string" identifier="2"></name><server_addrs type="list" identifier="3"><list type="string" size="1"><element>10.84.13.45:8086</element></list></server_addrs><status type="string" identifier="4">Up</status><description type="string" identifier="5">Established</description></ConnectionInfo><ConnectionInfo><type type="string" identifier="1">Discovery</type><name type="string" identifier="2">Collector</name><server_addrs type="list" identifier="3"><list type="string" size="1"><element>10.84.13.45:5998</element></list></server_addrs><status type="string" identifier="4">Up</status><description type="string" identifier="5">SubscribeResponse</description></ConnectionInfo><ConnectionInfo><type type="string" identifier="1">Discovery</type><name type="string" identifier="2">IfmapServer</name><server_addrs type="list" identifier="3"><list type="string" size="1"><element>10.84.13.45:5998</element></list></server_addrs><status type="string" identifier="4">Up</status><description type="string" identifier="5">SubscribeResponse</description></ConnectionInfo><ConnectionInfo><type type="string" identifier="1">Discovery</type><name type="string" identifier="2">xmpp-server</name><server_addrs type="list" identifier="3"><list type="string" size="1"><element>10.84.13.45:5998</element></list></server_addrs><status type="string" identifier="4">Up</status><description type="string" identifier="5">Publish Response - HeartBeat</description></ConnectionInfo></list></connection_infos><description type="string" identifier="5"></description></ProcessStatus></list></process_status></NodeStatus></data></NodeStatusUVE><SandeshUVECacheResp type="sandesh"><returned type="u32" identifier="1">1</returned><more type="bool" identifier="0">false</more></SandeshUVECacheResp></__NodeStatusUVE_list>

</div>

## contrail-status script

The contrail-status script is used to give the status of the Contrail
processes on a server.

The contrail-status script first checks if a process is running, and if
it is, performs introspect into the process to get its functionality
status, then outputs the aggregate status.

The possible states to display include:

-   active - the process is running and functional; the internal state
    is good

-   inactive - not started or stopped by user

-   failed – the process exited too quickly and has not restarted

-   initializing - the process is running, but the internal state is not
    yet functional.

<div id="jd0e108" class="example" dir="ltr">

### Example Output: Contrail-Status Script

The following is an example output from the contrail-status script.

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

    contrail-schema               active

    contrail-svc-monitor          active


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

</div>

 
