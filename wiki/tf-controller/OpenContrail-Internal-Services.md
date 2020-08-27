# 1 Configuration Node

## 1.1 Configuration API Server
* Mode: Active/Active
* Launched using: /etc/contrail/supervisord_config_files/contrail-api.ini
* Process configuration files:
    + /etc/contrail/contrail-api.conf
    + /etc/contrail/contrail-keystone-auth.conf [in case of openstack]
* Log: Defined in configuration, typically
    + /var/log/contrail/contrail-api-0.log and /var/log/contrail/contrail-api.log (when setup by fab)
    + /var/log/contrail/contrail-api-0-stdout.log and /var/log/contrail/contrail-api.log (when setup by server manager)
* Storage: User created configurations (VN etc.) in Cassandra
* Port:
  * 8082: REST API for reading and writing configuration
  * 8084: introspect for debugging

#### Cassandra
* Read: Read configuration.
* Write: Write configuration.

#### IF-MAP Server (local)
* Read: None
* Write: Publish configuration. This is driven by the messages received from RabbitMQ.

#### RabbitMQ (default is local, configurable)
* Read: Receive configuration sent from the API server who got user request originally.
* Write: The API server getting user request writes configuration to RabbitMQ for all API servers including itself. Then each API server will publish the configuration to IF-MAP server after receiving from RabbitMQ.

#### Collector
* Read: None
* Write: Send positive (updates) and negative (error, failures) logs, and running stats.

#### Discovery
* Read: Get info of other services, like collector.
* Write: Register itself and IF-MAP server. Send heartbeat. Send request for other services.


## 1.2 Discovery
* Mode: Active/Active
* Launched using: /etc/contrail/supervisord_config_files/contrail-discovery.ini
* Process configuration files: /etc/contrail/contrail-discovery.conf
* Log: Defined in configuration, typically
    + /var/log/contrail/contrail-discovery-0.log and /var/log/contrail/contrail-discovery.log (when setup by fab)
    + /var/log/contrail/contrail-discovery-0-stdout.log and /var/log/contrail/contrail-discovery.log (when setup by server manager)
* Storage: Registration of services in Cassandra
* Port:
  * 5998: REST API for register and request services

#### Other Services
* Read: Receive registration (with VIP in HA case), service request and heartbeat.
* Write: Send requested service info.

#### Collector
* Read: None
* Write: Send positive (updates) and negative (error, failures) logs, and running stats.


## 1.3 Schema Transformer
* Mode: Active/Passive
* Configuration: /etc/contrail/contrail-schema.conf
* Log: Defined in configuration, typically
    + /var/log/contrail/contrail-schema.log when setup by fab
    + /var/log/contrail/schema.log when setup by server-manager
    + Exceptions are stored in /var/log/contrail/schema.err (search up for 'A problem' from bottom of file)
* Storage: 
  + Non-UUID Unique items from Zookeeper, eg. route-target numbers, virtual-network-ids, security-group-ids.
  + Private persistent data in Cassandra.
* Port:
  * 8087: introspect for debugging

#### Configuration updates from IF-MAP Server (<R3.0) and RabbitMQ (>=R3.0)
* Read: Receive configuration published by configuration API server.
* Write: None

#### Configuration API Server
* Write: Write transformed configurations (routing instance, access control list and route target).

#### Zookeeper
* Read: None
* Write: Register, first register, first being active(aka master election recipe). A callback is invoked if it is active. All other instances of schema transformer are passive and stuck at callback. Once the active one is down, one of the passive will be woken up by callback. Only the active schema transformer connects to local IF-MAP server on port 8443.

#### Cassandra
* Read: On startup to rebuild internal state from previous run. Ongoing reads of objects on message updates.
* Write: Data associated with User and System objects that are specific to schema transformer and that need to survive restarts

#### Collector
* Read: None
* Write: Send positive (updates) and negative (error, failures) logs, and running stats.


## 1.4 Service Monitor
* Mode: Active/Passive
* Configuration: /etc/contrail/contrail-svc-monitor.conf
* Log: Defined in configuration
* Storage:
  + Zookeeper for master election recipe (see schema-transformer section). 
  + Cassandra for private persistent data
* Port:
  * 8088: introspect for debugging

#### RabbitMQ Server
* Read: Receive configuration published by configuration API server.
* Write: None

#### Configuration API Server
* Write: Write generated configuration objects.

#### Zookeeper
* Read: None
* Write: Register, first register, first being active. A callback is invoked if it is active. All other instances of svc-monitor are passive and stuck at callback. Once the active one is down, one of the passive will be waked up by callback.

#### Cassandra
* Read: On startup to rebuild internal state from previous run, Ongoing reads of objects on message updates.
* Write: Data associated with User and System objects that are specific to service monitor and that need to survive restarts

#### Collector/Opserver(contrail-analytics-api)
* Read: Read VRouter UVE to select host for launching service VM/netns.
* Write: Send positive (updates) and negative (error, failures) logs, and running stats.

#### Nova-API
* Read: For monitoring service-instance's VM state.
* Write: For (re)launching service-instance VM.

## 1.5 IF-MAP Server
* Configuration: /etc/ifmap-server/
* Log: Defined in configuration. /var/log/contrail/ifmap-server*.log
* Storage: Published configurations in-memory
* Port:
  * 8443

#### Configuration API Server
* Read: Read configuration published by API server, and store in memory (not persistent).
* Write: None

#### Schema Transformer (for <R3.0)
* Read: None
* Write: Send published configuration.

#### Control (BGP)
* Read: None
* Write: Send published configuration.

#### DNS
* Read: None
* Write: Send published configuration.


## 1.6 RabbitMQ
* Configuration: /etc/rabbitmq/rabbitmq.config
* Log: Defined in configuration. /var/log/rabbitmq
* Port:
  * 5672

#### Configuration API Server
* Read: Read configuration update message.
* Write: Send configuration update message.

#### Schema Transformer (>=R3.0)
* Read: Read configuration update message.
* Write: None.

#### Service Monitor
* Read: Read configuration update message.
* Write: None.


## 1.7 Configuration Node Manager (server layer)
Monitor all config services in this node, send all stats and process status to collector.

#### Collector
* Read: None
* Write: Send positive (updates) and negative (error, failures) logs, and running stats.


## 1.8 User Configuration Flow
User Request
-> Original API Server
-> Local RabbitMQ
-> All API Servers
-> Local IF-MAP Server
-> Schema Transformer and Service Monitor


## 1.9 Transformed Configuration Flow
Schema Transformer
-> Configuration API Server
-> Local RabbitMQ
-> All API Servers
-> Local IF-MAP Server
-> Control and DNS


# 2 Analytics Node

## 2.1 Analytics API Server
* Mode: Active/Active
* Configuration: /etc/contrail/contrail-analytics-api.conf
* Log: Defined in configuration
* Storage: Analytics info in Cassandra
* Port:
  * 8081: REST API for querying analytics info
  * 8090: introspect for debugging

#### Cassandra
* Read: Read logs (UVEs can be read as format of log)
* Write: None

#### Redis
* Read: Read UVEs from Redis on all analytics nodes and aggregate them, and logs published by query engine.
* Write: Subscribe to receive logs published by query engine.

#### Query Engine
* Read: None
* Write: Send queries.

#### Collector
* Read: None
* Write: Send logs and running stats


## 2.2 Collector
* Mode: Active/Active
* Configuration: /etc/contrail/contrail-collector.conf
* Log: Defined in configuration
* Storage: Analytics info in Redis and Cassandra
* Port:
  * 8086: collect analytics info
  * 8089: introspect for debugging

#### Other Services (Generators)
* Read: Receive UVEs and logs from all generators (services).
* Write: None

#### Redis Server
* Read: None
* Write: Write UVEs into Redis server (caching).

#### Cassandra
* Read: None
* Write: Write all collected info including both logs and UVEs.


## 2.3 Query Engine
* Mode: Active/Active
* Configuration: /etc/contrail/contrail-query-engine.conf
* Log: Defined in configuration
* Storage: Query result in Redis
* Port:
  * 8091: receive queries

#### Cassandra
* Read: Read logs (UVEs can be read as format of log)
* Write: None

#### Analytics API Server
* Read: Receive queries.
* Write: None

#### Redis Server
* Read: None
* Write: Write query result.

#### Collector
* Read: None
* Write: Send logs and running stats


## 2.4 Redis Server
One Redis server supports query engine and caches UVEs.
* Configuration: /etc/redis/redis.conf
* Log: Defined in configuration
* Storage: Memory
* Port:
  * 6379:

## 2.5 Analytics Node Manager
Monitor all analytics services in this node, send all stats to collector.

#### Collector
* Read: None
* Write: Send logs and running stats.


# 3 Database

## 3.1 Cassandra
* For Configuration related keyspaces[TBD: enumerate], replication factor = cluster size. Write and Read consistency levels are Quorum. With 2n+1 cluster/replication-factor, reads are consistent. Survive the loss of n nodes. Really read from and write to n+1 nodes (quorum). Each node holds 100% of data. So strict consistency.
* For Analytics related keyspaces[TBD: enumerate], replication factor = 2. Write and Read consistency is Single. So eventual consistency.
* See http://www.ecyrd.com/cassandracalculator/ for more details regarding consistency.

## 3.2 Database Node Manager
Monitor all database services in this node, send all stats to collector.

#### Collector
* Read: None
* Write: Send logs and running stats.


## 3.3 Zookeeper

#### Schema Transformer
* Master election
* Allocate shared resources e.g. route-target values(0-2^16-1), virtual-network IDs[TBD:values], security-group IDs[TBD:values]
* Security group ID and virtual network ID used by BGP/XMPP.

#### Configuration API Server
* Allocate IP address in subnet.
* Check fq-name in case 2 objects are created with the same name in fly.

#### Service Monitor
* Master election


# 4 Control Node

## 4.1 Control
* Mode: Active/Active
* Configuration: /etc/contrail/contrail-control.conf
* Log: Defined in configuration
* Storage:
* Port:
  * 179: BGP
  * 5269: XMPP server for vRouter agent to connect to
  * 8083: introspect for debugging

#### Discovery
* Read: Receive info of requested services.
* Write: Request service info, eg. IF-MAP server.

#### IF-MAP Server
* Read: Receive configurations published by configuration API server.
* Write: Subscribe to receive configurations.

#### vRouter Agent
* Read: Receive XMPP messages.
* Write: Send XMPP messages.

#### BGP Peers
* Read: Receive BGP messages.
* Write: Send BGP messages.

#### Collector
* Read: None
* Write: Send logs and running stats.


## 4.2 DNS (Contrail)
This is the front-end of name resolving. Host native named is the back-end.

#### Discovery
* Read: Receive info of requested services.
* Write: Request service info, eg. IF-MAP server.

#### IF-MAP Server
* Read: Receive configurations published by configuration API server.
* Write: Subscribe to receive configurations.

#### vRouger Agent
* Read: Receive XMPP messages.
* Write: Send XMPP messages.

#### Collector
* Read: None
* Write: Send logs and running stats.


## 4.3 Control Node Manager
Monitor all control services in this node, send all stats to collector.

#### Collector
* Read: None
* Write: Send logs and running stats.


# 5 Compute Node

## 5.1 vRouter Agent
* Configuration: /etc/contrail/contrail-vrouter-agent.conf
* Log: Defined in configuration
* Storage:
* Port:
  * 8085: introspec for debugging

#### Discovery
* Read: Receive info of requested services.
* Write: Request service info, e.g. control server.

#### Control
* Read: XMPP messages.
* Write: XMPP messages.

#### Collector
* Read: None
* Write: Send logs and running stats.


## 5.2 vRouter
Kernel Module


## 5.3 vRouter Node Manager
Monitor all vRouter services in this node, send all stats to collector.

#### Collector
* Read: None
* Write: Send logs and running stats.
