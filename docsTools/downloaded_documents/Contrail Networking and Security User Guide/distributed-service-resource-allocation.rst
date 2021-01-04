Distributed Service Resource Allocation with Containerized Contrail
===================================================================

 

.. raw:: html

   <div id="intro">

.. raw:: html

   <div class="mini-toc-intro">

Starting with Contrail Release 4.0, the existing centralized Contrail
discovery service is replaced with a distributed method of allocating
service resources.

.. raw:: html

   </div>

.. raw:: html

   </div>

Replacement of Centralized Discovery Service
--------------------------------------------

In Contrail releases prior to Release 4.0, the Contrail discovery
service is a centralized service resource allocation module with high
availability, used primarily to automatically load-balance service
resources in the system.

In the previous centralized discovery method, new service resources are
registered (published) directly to the Contrail discovery module and
allocated to the requester (subscriber) of the service resource, without
disrupting the running state of the subscribers.

The centralized discovery method requires using a database to:

-  synchronize across Contrail discovery nodes.

-  maintain the list of publishers, subscribers, and the health of
   published services across reloads.

-  provide a centralized view of the service allocation and health of
   the services.

This centralized discovery method resulted in unnecessary system churn
when services were falsely marked as down, due to periodic health
updates of services made to the database nodes, resulting in
reallocation of healthy services.

Starting with Contrail 4.0, the Contrail discovery services centralized
resource allocation manager has been removed. Its replacement is a
distributed resource allocation list of service nodes, maintained in
each module of the system.

New Distributed Resource Allocation Manager
-------------------------------------------

Starting with Contrail Release 4.0, service resources are managed with a
distributed allocation manager, with the following features:

-  Each system module is provisioned with a list of service nodes
   (publishers).

-  Each system module randomizes the list of service nodes and uses the
   resources. The randomized list is expected to be fairly
   load-balanced.

-  When currently-used services are down, the system module detects the
   down immediately and reacts with no downtime by selecting another
   service from the list. This is distinctly different from the previous
   model, in which the module would need to contact the discovery
   service to check for available services, resulting in a finite time
   loss for allocation, distribution, and application of a new set of
   services.

-  When service nodes are added or deleted, the system administrator
   updates the configuration file of all daemons using the service type
   of the service node added or deleted, sending a SIGHUP to the
   respective daemons.

-  Each daemon randomizes the service list independently and reallocates
   the resources.

Deprecation of IF-MAP
~~~~~~~~~~~~~~~~~~~~~

In Contrail 4.0, the Interface for Metadata Access Points (IF-MAP)
methodology has been deprecated. Contrail 4.0 uses CONFIGDB sections in
configuration files instead of IF-MAP sections.

Changes in Configuration Files
------------------------------

`Table 1 <distributed-service-resource-allocation.html#discoverytable1>`__
lists configuration files in the Contrail system that have changes to
enable the distributed service resource allocation system, starting with
Contrail 4.0. In general, the changes include removing (deprecating)
discovery server sections and subsections, and adding parameters needed
to identify service resources in all modules.

Each daemon randomizes the published service list and uses the
resources. Additionally, each daemon provides a SIGHUP handler to manage
the addition or deletion of publishers.

Table 1: Contrail 4.0 Changes in Configuration Files

Configuration File

Configuration Parameter

Changes

``contrail-vrouter-agent.conf``

``[DISCOVERY]``

Section deprecated

``[CONTROL-NODE].servers``

| Provisioned list of control-node [role=control] service providers in
  the format:
| ip-address:port ip-address2:port
| Example: 10.1.1.1:5269 10.1.1.12:5269

``[DNS].servers``

Provisioned list of DNS [role=control] service providers in the format:

| ip-address:port ip-address2:port
| Example: 10.1.1.1:53 10.1.1.2:5

``[DEFAULT].collectors``

Provisioned list of Collector [role=collector] service providers in the
format:

ip-address:port ip-address2:port Example: 10.1.1.1:8086 10.1.1.2:8086

``contrail-control.conf``

``[DISCOVERY]``

Section deprecated

 

``[DEFAULT].collectors``

Provisioned list of Collector [role=collector] service providers in the
format:

ip-address:port ip-address2:port Example: 10.1.1.1:8086 10.1.1.2:8086

 

``[CONFIGDB].rabbitmq_server_list``

Provisioned list of config-node [role=cfgm] service providers in the
format:

ip-address:port ip-address2:port Example: 10.1.1.1:5672 10.1.1.2:5672

 

``[CONFIGDB].rabbitmq_user``

guest (default string)

 

``[CONFIGDB].rabbitmq_password``

guest (default string)

 

``[CONFIGDB].config_db_server_list``

Provisioned list of Config DB [role=database] service providers in the
format:

ip-address:port ip-address2:port Example: 10.1.1.1:9042 10.1.1.2:9042

NOTE: Docker uses 9041 as port

``[CONFIGDB].certs_store``

Deprecated

``[CONFIGDB].password``

Deprecated

``[CONFIGDB].server_url``

Deprecated

``[CONFIGDB].user``

Deprecated

``[CONFIGDB].stale_entries_cleanup_timeout``

Deprecated

``[CONFIGDB].end_of_rib_timeout``

Deprecated

``contrail-dns.conf``

``[DISCOVERY]``

Deprecated

``[DEFAULT].collectors``

Provisioned list of Collector [role=collector] service providers in the
format:

ip-address:port ip-address2:port Example: 10.1.1.1:8086 10.1.1.2:8086

``[CONFIGDB].rabbitmq_server_list``

Provisioned list of config-node [role=cfgm] service providers in the
format:

ip-address:port ip-address2:port Example: 10.1.1.1:5672 10.1.1.2:5672

``[CONFIGDB].rabbitmq_user``

guest (default string)

``[CONFIGDB].rabbitmq_password``

guest (default string)

``[CONFIGDB].config_db_server_list``

Provisioned list of Config DB [role=database] service providers in the
format:

ip-address:port ip-address2:port Example: 10.1.1.1:9042 10.1.1.2:9042
NOTE: Dockers use 9041 as port

``[CONFIGDB].certs_store``

Deprecated

``[CONFIGDB].password``

Deprecated

``[CONFIGDB].server_url``

Deprecated

``[CONFIGDB].user``

Deprecated

``[CONFIGDB].stale_entries_cleanup_timeout``

Deprecated

``[CONFIGDB].end_of_rib_timeout``

Deprecated

``contrail-collector.conf``

``[DISCOVERY]``

Deprecated

``[API_SERVER].api_server_list``

Provisioned list of api-servers [role=config] in the format:

ip-address:port

Example: 10.1.1.1:8082 10.1.1.2:8082

``contrail-alarm-gen.conf``

``[DISCOVERY]``

Deprecated

``[DEFAULTS].collectors``

Provisioned list of Collector [role=collector] service providers in the
format:

ip-address:port ip-address2:port

Example: 10.1.1.1:8086 10.1.1.2:8086

``[API_SERVER].api_server_list``

Provisioned list of api-servers [role=config] in the format:

ip-address:port

Example: 10.1.1.1:8082 10.1.1.2:8082

``[REDIS].redis_uve_list``

Provisioned list of redis instances [role=collector]

Example: 192.168.0.29:6379 192.168.0.30:6379

``contrail-analytics-api.conf``

``[DISCOVERY]``

Section deprecated

``[DEFAULTS].collectors``

Provisioned list of collector [role=collector] service providers in the
format:

ip-address:port ip-address2:port

Example: 10.1.1.1:8086 10.1.1.2:8086

``[REDIS].redis_uve_list``

Provisioned list of redis instances [role=collector]

Example: 192.168.0.29:6379 192.168.0.30:6379

``contrail-api.conf``

``[DISCOVERY]``

Section deprecated

``[DEFAULTS].collectors``

Provisioned list of collector [role=collector] service providers in the
format:

ip-address:port ip-address2:port

Example: 10.1.1.1:8086 10.1.1.2:8086

``contrail-schema.conf``

``[DISCOVERY]``

Section deprecated

``[DEFAULTS].collectors``

Provisioned list of Collector [role=collector] service providers in
ip-address:port ip-address2:port

Example: 10.1.1.1:8086 10.1.1.2:8086

``contrail-svc-monitor.conf``

``[DISCOVERY]``

Section deprecated

``[DEFAULTS].collectors``

Provisioned list of Collector [role=collector] service providers in the
format:

ip-address:port ip-address2:port

Example: 10.1.1.1:8086 10.1.1.2:8086

``contrail-device-manager.conf``

``[DISCOVERY]``

Section deprecated

``[DEFAULTS].collectors``

Provisioned list of Collector [role=collector] service providers in
ip-address:port ip-address2:port format

Example: 10.1.1.1:8086 10.1.1.2:8086

``contrail-analytics-nodemgr.conf``

``[DISCOVERY]``

Section deprecated

``[COLLECTOR].server_list``

Provisioned list of Collector [role=collector] service providers in the
format:

ip-address:port ip-address2:port Example: 10.1.1.1:8086 10.1.1.2:8086

``contrail-config-nodemgr.conf``

``[DISCOVERY]``

Section deprecated

``[COLLECTOR].server_list``

Provisioned list of Collector [role=collector] service providers in the
format:

ip-address:port ip-address2:port

Example: 10.1.1.1:8086 10.1.1.2:8086

``contrail-control-nodemgr.conf``

``[DISCOVERY]``

Section deprecated

``[COLLECTOR].server_list``

Provisioned list of Collector [role=collector] service providers in
ip-address:port ip-address2:port

Example: 10.1.1.1:8086 10.1.1.2:8086

``contrail-database-nodemgr.conf``

``[DISCOVERY]``

Section deprecated

``[COLLECTOR].server_list``

Provisioned list of Collector [role=collector] service providers in the
format:

ip-address:port ip-address2:port

Example: 10.1.1.1:8086 10.1.1.2:8086

``contrail-vrouter-nodemgr.conf``

``[DISCOVERY``]

Section deprecated

``[COLLECTOR].server_list``

Provisioned list of Collector [role=collector] service providers in the
format:

ip-address:port ip-address2:port

Example: 10.1.1.1:8086 10.1.1.2:8086

``contrail-query-engine.conf``

``[DISCOVERY]``

Section deprecated

``[COLLECTOR].server_list``

Provisioned list of Collector [role=collector] service providers in the
format:

ip-address:port ip-address2:port

Example: 10.1.1.1:8086 10.1.1.2:8086

``contrail-snmp-collector.conf``

``[DISCOVERY]``

Section deprecated

``[DEFAULTS].collectors``

Provisioned list of Collector [role=collector] service providers in the
format:

ip-address:port ip-address2:port

Example: 10.1.1.1:8086 10.1.1.2:8086

``[API_SERVER].api_server_list``

Provisioned list of api-servers [role=config] in the format:

ip-address:port

Example: 10.1.1.1:8082 10.1.1.2:8082

``contrail-topology.conf``

``[DISCOVERY]``

Section deprecated

``[DEFAULTS].collectors``

Provisioned list of Collector [role=collector] service providers in the
format:

ip-address:port ip-address2:port Example: 10.1.1.1:8086 10.1.1.2:8086

``[API_SERVER].api_server_list``

Provisioned list of api-servers [role=config] in ip-address:port

Example: 10.1.1.1:8082 10.1.1.2:8082

**Contrail Web UI**

``config.global.js``

``config.discovery.server``

Discovery subsection deprecated

``config.discovery.port``

Discovery subsection deprecated

``config.cnfg.server_ip``

Provisioned list of Config [role=cfgm] service providers as list of
ip-address

Example: ['10.1.1.1 10.1.1.2']

``config.cnfg.server_port``

Server port as a string

Example: '8082'

``config.analytics.server_ip``

Provisioned list of Collector [role=collector] service providers as a
list of ip-address

Example: ['10.1.1.1 10.1.1.2']

``config.analytics.server_port``

Server port as a string

Example: '8081'

``config.dns.server_ip``

Provisioned list of Controller [role=control] service providers as a
list of ip-address

Example: ['10.1.1.1 10.1.1.2']

``config.dns.server_port``

Server port as a string

Example: '8092'

 
