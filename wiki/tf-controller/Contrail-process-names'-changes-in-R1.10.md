The names of contrail specific services, processes, configuration files and log files are changed in R1.10.
This is done for consistency and to clearly identify contrail specific parts in the system.

The following are the visible changes
* discovery-server -> contrail-discovery
* vnc_cfg_api_server/api_server -> contrail-api
* to_bgp -> contrail-schema
* control-node -> contrail-control
* vizd/collector -> contrail-collector
* opserver -> contrail-analytics-api
* contrail-qe -> contrail-analytics-api
* vswad -> contrail-vrouter-agent

Contrail processes include the following
* /usr/bin/contrail-control
* /usr/bin/contrail-vrouter-agent
* /usr/bin/contrail-collector
* /usr/bin/contrail-query-engine
* /usr/bin/python /usr/bin/contrail-analytics-api
* /usr/bin/python /usr/bin/contrail-discovery
* /usr/bin/python /usr/bin/contrail-api
* /usr/bin/python /usr/bin/contrail-schema
* /usr/bin/python /usr/bin/contrail-svc-monitor

Contrail services include the following
* /etc/init.d/contrail-analytics-api
* /etc/init.d/contrail-api
* /etc/init.d/contrail-collector
* /etc/init.d/contrail-control
* /etc/init.d/contrail-database
* /etc/init.d/contrail-discovery
* /etc/init.d/contrail-dns
* /etc/init.d/contrail-named
* /etc/init.d/contrail-query-engine
* /etc/init.d/contrail-schema
* /etc/init.d/contrail-svc-monitor
* /etc/init.d/contrail-vrouter-agent
* /etc/init.d/contrail-webui
* /etc/init.d/contrail-webui-middleware


Contrail configuration files include the following
* /etc/contrail/contrail-analytics-api.conf
* /etc/contrail/contrail-api.conf
* /etc/contrail/contrail-collector.conf
* /etc/contrail/contrail-control.conf
* /etc/contrail/contrail-discovery.conf
* /etc/contrail/contrail-nodemgr-database.conf
* /etc/contrail/contrail-query-engine.conf
* /etc/contrail/contrail-schema.conf
* /etc/contrail/contrail-vrouter-agent.conf

Contrail log files are of multiple types
* _\<process-name\>_.log: this is the traditional log file that is passed on command line the process and the process writes its log to this file
* _\<process-name\>_-stdout.log: sometimes instead of using the file passed on the command line, a process can use syslog mechanism, in that case, the data goes into _\<process-name\>_-stdout.log or _\<process-name_\>-stderr.log
* _\<process-name_\>-stderr.log

Contrail logs files are located in /var/log/contrail