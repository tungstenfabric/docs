# Summary  

Alerts will be provided on a per-UVE basis.
Contrail Analytics will raise (or clear) alerts using python-coded “rules” that examine the contents of the UVE and the object’s config.
Some rules will be built-in. Others can be added using python stevedore plugins.  
  
The Contrail Analytics API will provide the following.  
* Read access to the Alerts as part of the UVE GET APIs   
* Alert acknowledgement using POST requests.  
* UVE and Alert streaming using Server-Sent Events :http://dev.w3.org/html5/eventsource/  
  
## Alert format:  
  
GET http://\<analytics-ip\>:8081/analytics/alarms  

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
                                token: "eyJ0aW1lc3RhbXAiOiAxNDU3Mzk1MDUyODg5MTgyLCAiaHR0cF9wb3J0IjogNTk5NSwgImhvc3RfaXAiOiAiMTAuMjA0LjIxNy4yNCJ9",
                                type: "ProcessStatus"
                            }
                        ]
                    }
                }
            }
        ]
    }

"_any_of_" attribute contains alarm rules defined in the format         
    [ [rule1 _AND_ rule2 _AND_ ... _AND_ ruleN] ... _OR_ [rule11 _AND_ rule22 _AND_ ... _AND_ ruleNN] ]        
“_ack_” indicates if the alert has been acknowledged or not        
“_token_” is to be used by clients when requesting acknowledgements        
  

## Analytics APIs for Alerts:  
  
1. GET _http://\<analytics-ip\>:\<rest-api-port\>/analytics/uves/control-node/aXXsYY&cfilt=UVEAlarms_  
This will give a list of alerts raised against Control Node aXXsYY.
This is available for all UVE table-types.
 
2. GET _http://\<analytics-ip\>:\<rest-api-port\>/analytics/alarms_  
This will give a list of all alarms in the system.
 
3. POST _http://\<analytics-ip\>:\<rest-api-port\>/analytics/alarms/acknowledge_  
       Body: {“table”: \<object-type\>, “name”: \<key\>, “type”: \<alarm type\>, “token”: \<token\>}
This allows the user to acknowledge an alarm.
Acknowledged/un-acknowledged alarms can be queried specifically by using the URL Query Parameter “ackFilt=True” or “ackFilt=False” with APIs #1 and #2 above.  
 
## Analytics APIs for SSE streams:

4. GET _http://\<analytics-ip\>:\<rest-api-port\>/analytics/uve-stream?tablefilt=control-node_  
This provides a SSE-based stream of UVE updates for Control Node alarms.
This is available for all UVE table-types. If the “tablefilt” URL Query parameter is not provided, all UVEs will be seen.
 
5. GET _http://\<analytics-ip\>:\<rest-api-port\>/analytics/alarms-stream?tablefilt=control-node_  
This is similar to #4 above, but it provides only the Alerts portion of UVEs instead of providing the entire content of the UVEs.  
This is available for all UVE table-types. If the “tablefilt” URL Query parameter is not provided, alerts for all UVEs will be seen.
  

## Contrail Alarm Notification:

contrail-alarm-notify script (/usr/bin in analytics nodes) can be used to send email notification for alarms.
The script receives real-time update of alarms from the /analytics/alarms-stream API and sends email to the intended recipients.

**_Example:_**

contrail-alarms-notify --smtp-server smtp.juniper.net --smtp-server-port 25 --sender-email xyz@juniper.net --receiver-email-list someone@juniper.net someone@gmail.com

It may be noted there is no option to specify the sender's password. This script tries to send email notification without sender credentials. However, if the SMTP server requires the sender to be authenticated, then the script would prompt the user to enter the sender's password to proceed further.
 
**_Sample email notification for Process Failure alarm:_**

_**Subject:**_ [Contrail Alarm] Process Failure -- analytics-node:nodec40    
_**Body:**_   

    Source : analytics-node:nodec40    
    Type : ProcessStatus    
    Severity : 3    
    Timestamp : 2016-03-04 00:30:36    
    Status : Unacknowledged    
    Description : NodeMgr reports abnormal status for process(es) in NodeStatus.process_info    
    Details : [    
        {    
            "all_of": [    
                {    
                    "json_operand1_value": "\"PROCESS_STATE_STOPPED\"",    
                    "json_vars": {    
                        "NodeStatus.process_info.process_name": "contrail-snmp-collector"
                    },
                    "rule": {
                        "oper": "!=",
                        "operand1": {
                            "keys": [
                                "NodeStatus",
                                "process_info",
                                "process_state"
                            ]
                        },
                        "operand2": {
                            "json_value": "\"PROCESS_STATE_RUNNING\""
                        }
                    }
                }
            ]
        }
    ]

  
## Built-in Node Alerts:  
The following built-in node alerts are supported and can be retrieved using APIs listed in the previous section.  
  
    control-node:  {
        PartialSysinfoControl: "Basic System Information is absent for this node in BgpRouterState.build_info",
        ProcessStatus: "NodeMgr reports abnormal status for process(es) in NodeStatus.process_info",
        XmppConnectivity: "Not enough XMPP peers are up in BgpRouterState.num_up_bgp_peer",
        BgpConnectivity: "Not enough BGP peers are up in BgpRouterState.num_up_bgp_peer",
        AddressMismatch: “Mismatch between configured IP Address and operational IP Address",
        ProcessConnectivity: "Process(es) are reporting non-functional components in NodeStatus.process_status"
    },
 
    vrouter:  {
        PartialSysinfoCompute: "Basic System Information is absent for this node in VrouterAgent.build_info",
        ProcessStatus: "NodeMgr reports abnormal status for process(es) in NodeStatus.process_info",
        ProcessConnectivity: "Process(es) are reporting non-functional components in NodeStatus.process_status",
        VrouterInterface: "VrouterAgent has interfaces in error state in VrouterAgent.error_intf_list”,
        VrouterConfigAbsent: “Vrouter is not present in Configuration”,
    },
 
    config-node:  {
        PartialSysinfoConfig: "Basic System Information is absent for this node in ModuleCpuState.build_info",
        ProcessStatus: "NodeMgr reports abnormal status for process(es) in NodeStatus.process_info",
        ProcessConnectivity: "Process(es) are reporting non-functional components in NodeStatus.process_status"
    },
 
    analytics-node:  {
        ProcessStatus: "NodeMgr reports abnormal status for process(es) in NodeStatus.process_info",
        PartialSysinfoAnalytics: "Basic System Information is absent for this node in CollectorState.build_info",
        ProcessConnectivity: "Process(es) are reporting non-functional components in NodeStatus.process_status"
    },
    
    database-node: {
        ProcessStatus: "NodeMgr reports abnormal status for process(es) in NodeStatus.process_info",
        ProcessConnectivity: "Process(es) are reporting non-functional components in NodeStatus.process_status"
    },