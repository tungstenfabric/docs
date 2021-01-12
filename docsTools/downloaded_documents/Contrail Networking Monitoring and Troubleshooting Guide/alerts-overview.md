# Contrail Alert Streaming

 

Contrail alerts are provided on a per-user visible entity (UVE) basis.
Contrail analytics raise or clear alerts using Python-coded rules that
examine the contents of the UVE and the configuration of the object.
Some rules are built in. Others can be added using Python *stevedore*
plugins.

This topic describes Contrail alerts capabilities.

## Alert API Format

The Contrail alert analytics API provides the following:

-   Read access to the alerts as part of the UVE GET APIs.

-   Alert acknowledgement using POST requests.

-   UVE and alert streaming using server-sent events (SSEs).

For example:

<span class="cli" v-pre="">GET
http://`<analytics-ip>`:8081/analytics/alarms</span>

<div id="jd0e48" class="example" dir="ltr">

    {
        analytics-node: [
            {
                name: "nodec40",
                value: {
                    UVEAlarms: {
                        alarms: [
                            {
                                any_of: [
                                    {
                                        all_of: [
                                            {
                                                json_operand1_value: ""PROCESS_STATE_STOPPED"",
                                                rule: {
                                                    oper: "!=",
                                                    operand1: {
                                                        keys: [
                                                            "NodeStatus",
                                                            "process_info",
                                                            "process_state"
                                                        ]
                                                    },
                                                    operand2: {
                                                        json_value: ""PROCESS_STATE_RUNNING""
                                                    }
                                                },
                                                json_vars: {
                                                    NodeStatus.process_info.process_name: "contrail-topology"
                                                }
                                            }
                                        ]
                                    }
                                ],
                                severity: 3,
                                ack: false,
                                timestamp: 1457395052889182,
                                token: "eyJ0aW1lc3RhbXAiOiAxNDU3Mzk1MDUyODg5MTgyLCAiaHR0cF9wb3J0I
    ................................... jogNTk5NSwgImhvc3RfaXAiOiAiMTAuMjA0LjIxNy4yNCJ9",
                                type: "ProcessStatus"
                            }
                        ]
                    }
                }
            }
        ]
    }

</div>

In the example:

-   An `any_of` attribute contains alarm rules defined in the format
    `[ [rule1 AND rule2 AND ... AND ruleN] ... OR [rule11 AND rule22 AND ... AND ruleNN] ]`

-   Alerts are raised on a per-UVE basis and can be retrieved by a GET
    on a UVE.

-   An `ack` indicates if the alert has been acknowledged or not.

-   A `token` is used by clients when requesting acknowledgements.

## Analytics APIs for Alerts

The following examples show the API to use to display alerts and alarms
and to acknowledge alarms.

-   To retrieve a list of alerts raised against the control node named
    `aXXsYY`.

    <div id="jd0e91" class="example" dir="ltr">

        GET http://<analytics-ip>:<rest-api-port>/analytics/uves/control-node/aXXsYY&cfilt=UVEAlarms

    </div>

    This is available for all UVE table types.

-   To retrieve a list of all alarms in the system.

    <div id="jd0e105" class="example" dir="ltr">

        GET http://<analytics-ip>:<rest-api-port>/analytics/alarms

    </div>

-   To acknowledge an alarm.

    <div id="jd0e114" class="example" dir="ltr">

        POST http://<analytics-ip>:<rest-api-port>/analytics/alarms/acknowledge
        Body: {“table”: <object-type>,“name”: <key>, “type”: <alarm type>, “token”: <token>}

    </div>

    Acknowledged and unacknowledged alarms can be queried specifically
    using the following URL query parameters along with the GET
    operations listed previously.

    <div id="jd0e134" class="example" dir="ltr">

        ackFilt=True
        ackFilt=False

    </div>

## Analytics APIs for SSE Streaming

The following examples show the API to use to retrieve all or portions
of SE streams.

-   To retrieve an SSE-based stream of UVE updates for the control node
    alarms.

    <div id="jd0e146" class="example" dir="ltr">

        GET http://<analytics-ip>:<rest-api-port>/analytics/uve-stream?tablefilt=control-node

    </div>

    This is available for all UVE table types. If the `tablefilt` URL
    query parameter is not provided, all UVEs are retrieved.

-   To retrieve only the alerts portion of the SSE-based stream of UVE
    updates instead of the entire content.

    <div id="jd0e160" class="example" dir="ltr">

        GET http://<analytics-ip>:<rest-api-port>/analytics/alarm-stream?tablefilt=control-node

    </div>

    This is available for all UVE table types. If the `tablefilt` URL
    query parameter is not provided, all UVEs are retrieved.

## Built-in Node Alerts

The following built-in node alerts can be retrieved using the APIs
listed in *Analytics APIs for Alerts*.

<div id="jd0e180" class="example" dir="ltr">

    control‐node: {
    PartialSysinfoControl: "Basic System Information is absent for this node in BgpRouterState.build_info",
    ProcessStatus: "NodeMgr reports abnormal status for process(es) in NodeStatus.process_info",
    XmppConnectivity: "Not enough XMPP peers are up in BgpRouterState.num_up_bgp_peer",
    BgpConnectivity: "Not enough BGP peers are up in BgpRouterState.num_up_bgp_peer",
    AddressMismatch: “Mismatch between configured IP Address and operational IP Address",
    ProcessConnectivity: "Process(es) are reporting non‐functional components in NodeStatus.process_status"
    },

    vrouter: {
    PartialSysinfoCompute: "Basic System Information is absent for this node in VrouterAgent.build_info",
    ProcessStatus: "NodeMgr reports abnormal status for process(es) in NodeStatus.process_info",
    ProcessConnectivity: "Process(es) are reporting non‐functional components in NodeStatus.process_status",
    VrouterInterface: "VrouterAgent has interfaces in error state in VrouterAgent.error_intf_list”,
    VrouterConfigAbsent: “Vrouter is not present in Configuration”,
    },

    config‐node: {
    PartialSysinfoConfig: "Basic System Information is absent for this node in ModuleCpuState.build_info",
    ProcessStatus: "NodeMgr reports abnormal status for process(es) in NodeStatus.process_info",
    ProcessConnectivity: "Process(es) are reporting non‐functional components in NodeStatus.process_status"
    },

    analytics‐node: {
    ProcessStatus: "NodeMgr reports abnormal status for process(es) in NodeStatus.process_info"
    PartialSysinfoAnalytics: "Basic System Information is absent for this node in CollectorState.build_info",
    ProcessConnectivity: "Process(es) are reporting non‐functional components in NodeStatus.process_status"
    },

    database‐node: {
    ProcessStatus: "NodeMgr reports abnormal status for process(es) in NodeStatus.process_info",
    ProcessConnectivity: "Process(es) are reporting non‐functional components in NodeStatus.process_status"
    },

</div>

 
