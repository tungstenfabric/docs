Service discovery (SD) is a network daemon implementing HTTP API. SD is built around concepts of service and client. Services can publish information, and send heartbeat messages testifying they are alive. Clients can subscribe to a service, effectively showing intention to use a published service.

A service can be for example contrail-controller:IfmapServer, or contrail-controller:xmpp-server, or contrail-controller:ApiServer. A client could be for example contrail-controller:contrail-control using IfmapServer or contrail-vrouter-agent:0 talking to contrail-controller:dns-server.

This main function is implemented using 3 HTTP endpoints: /publish, /subscribe, and /heartbeat. Once a service is published, it must periodically request /heartbeat endpoint, otherwise it’s considered down. Once a client is subscribes, it must re-send requests to /subscribe during time-to-live (TTL) set in response for request to /subscribe. Failing to do so removes the client from subscribe list.

## Showcase of pub-sub

SD is a component of Contrail config node, and services are components of contrail-config. Clients are typically parts of control node. But in fact, SD is generic, and we can subscribe any service we like:

> $ curl -H "Content-Type: application/json" -X POST -d '{"service-type": "my", "my": {"ip": "10.140.64.135", "port": 3333}}' http://10.140.64.135:9110/publish
>
> {"cookie": "eaf8752ee73713bc49e1419e14bdf10f:my"}

Once a service is registered, it is not deleted on it’s own. But it’s initial status “up” will change to “down” after a configured number of missed heartbeats.

Cookie in the response from /publish is the value required for heartbeat.

> $ curl -H "Content-Type: application/json" -X POST -d '{"cookie": "eaf8752ee73713bc49e1419e14bdf10f:my"}' http://10.140.64.10/heartbeat
>
> 200 OK

> $ curl -s  http://10.140.64.135:9110/services.json | python -m json.tool | grep '"my"'
> 
>             "service_type": "my",

> $ curl -s  http://10.140.64.135:9110/services.json | python -m json.tool | grep '"my"' -C 5
>
>             "oper_state_msg": "",
>             "prov_state": "up",
>             "remote": "10.140.64.135",
>             "sequence": "1513611923contrail-controller",
>             "service_id": "eaf8752ee73713bc49e1419e14bdf10f:my",
>             "service_type": "my",
>             "status": "down",
>             "ts_created": 1513611923,
>             "ts_use": 0
>         },

> $ curl -H "Content-Type: application/json" -X POST -d '{"cookie": "eaf8752ee73713bc49e1419e14bdf10f:my"}' http://10.140.64.135:9110/heartbeat
>
> 200 OK

> $ curl -s  http://10.140.64.135:9110/services.json | python -m json.tool | grep '"my"' -C 5
>
>             "oper_state_msg": "",
>             "prov_state": "up",
>             "remote": "10.140.64.135",
>             "sequence": "1513611923contrail-controller",
>             "service_id": "eaf8752ee73713bc49e1419e14bdf10f:my",
>             "service_type": "my",
>             "status": "up",
>             "ts_created": 1513611923,
>             "ts_use": 0
>         },

Now we can subscribe a client of type “my-client” with ID "3c2207a2-58a6-4e16-8053-9350d5f6bf72" to the service “my” . Let’s list instances first:

> $ curl -s -X POST -H "Content-Type: application/json" -d '{"service": "my", "client": "3c2207a2-58a6-4e16-8053-9350d5f6bf72", "client-type": "my-client", "instances": 0}' http://10.140.64.135:9110/subscribe
>
> {"my": [], "ttl": 952}

No instances, we missed heartbeat. Send heartbeat, subscribe for 1 instance.

> $ curl -H "Content-Type: application/json" -X POST -d '{"cookie": "eaf8752ee73713bc49e1419e14bdf10f:my"}' http://10.140.64.135:9110/heartbeat
>
> 200 OK

> $ curl -s -X POST -H "Content-Type: application/json" -d '{"service": "my", "client": "3c2207a2-58a6-4e16-8053-9350d5f6bf72", "client-type": "my-client", "instances": 1}' http://10.140.64.135:9110/subscribe
>
> {"my": [{"ip": "10.140.64.135", "port": 3333}], "ttl": 496}

OK, we subscribed. In 496 seconds we need to come back and subscribe again.

## Rest of HTTP

Besides pub/sub endpoints, there are a few endpoints wich allow to manipulate clients and service (delete them for example), query information of given types (/query/). If you GET endpoint /, you can discover links representing services and clients. Links /services and /clients return HTML, so you can just look at it to see status of subscriptions. /services.json and /clients.json list all entities of given kind. And there are more endpoints.

## Cassandra and Zookeeper

SD can use Cassandra or Zookeeper as a backend database. The file disc_server.py is Cassandra version, disc_server_zk.py is Zookeeper version. There is difference in configuration and functions. For example, we need to configure Cassandra cluster node list for Cassandra version, but do not need to configure Zookeeper node list, and vice versa. 

Cassandra version  it implements re-balance endpoint to re-shuffle subscribers between publishers in a more justified way. Zookeeper version has a simple throttling for subscriptions to really busy services, which Cassandra version does not have.

TTL logic is slightly different in Cassandra and Zookeeper versions.

## Stats

Certain operations, like accepting a connection for example, or choosing a certain policy for deciding what instance of published service will be used to subscribe requesting client, trigger increment (and sometimes decrement -- see cur_pend_* stats) of a certain numbers. All these number are available at /stats endpoint. See table for description of debug flags. These numbers are reset to zero at every restart of SD daemon.

## Policies

When a client subscribes to a server it specifies type. Instance to subscribe is chosen according to policy. Default policy is “load-balance”. It’s possible to specify policy for a service type in config file.

Example:

> [contrail-dns]
>
> policy = fixed

Possible policies: 
* load-balance: balance service by subscription count,
* round-robin: randomly picks instances to subscribe,
* fixed: the sequence of services to choose from is sorted by unix timestamp + hostname.

## Configuration

SD is configured by a normal ini-file. The path to the file and certain values in it can overridden by CLI arguments. See table for description of parameters.

Current configuration can be checked at HTTP endpoint /config.

## Sandesh

SD is a Sandesh generator, it is visible in Contrail UI. We can trace messages as for other components. Default log severity is DEBUG, very verbose.

## Oper-state

Cassandra version of SD has feature of PUTting attribute named “oper-state” to a service. It’s possible to change oper-state to “down”. In this case this service will not be used for new subscriptions. It may be a way to switch clients to another server in a soft way, because in a few minutes (ttl_max) all clients will request a new subscription and migrate to new server. So, failing ifmap-server could excluded with oper-state, then we could check that all clients drained to another ifmap-server, then restart ifmap-server, as an example.

## Future of SD

SD should was deprecated in Contrail v4.

Centralized service discovery was replaced with Distributed Service Resource Allocation. It was done in order to have finite time required to switch fro a failed node to a replacement.

Details are here: https://www.juniper.net/documentation/en_US/contrail4.0/topics/concept/distributed-service-resource-allocation.html

In short: we'll need to provision every module of Contrail with a list of nodes to use.

For example, contrail-vrouter-agent.conf will have [CONTROL-NODE].servers with provisioned list of control-nodes, like "10.1.1.1:5269 10.1.1.12:5269". And so on, every module will have a list of counterparts to interact with. Update of configuration file should be followed with SIGHUP, to force a module to reload configuration.

## Tables

Endpoints

|Endpoint	 | Response Content-Type	 | Accepted Methods | Accepted Content-Types | Description | Cassandra only |
| --- | --- | --- | --- | --- | --- |
/heartbeat | HTML | POST	 | application/xml, application/json(default) | | 
/publish | HTML	| | application/xml, application/json -- no default! | |
/publish/<end_point> | JSON | POST | | |
/subscribe | HTML | | | |
/query | HTML | POST | | |
/services | HTML | GET | | |
/services.json | JSON | GET | | |
/clients	 | HTML | GET | | |
/clients.json | JSON | GET | | |
/config | HTML | | | |
/stats | HTML | | | Stats of running daemon |
/cleanup	 | HTML | GET | | Purge inactive publishers |
/ | HTML	 | | | Discovery endpoint | 
/load-balance/\<service type\> | JSON | | | On-demand re-balance of subscriptions between servers.	 | yes
/service/\<id\> | JSON | | | |
/service/\<id\>/brief | JSON | | | |
/clients/\<service type\>/\<service_id\> | JSON | | | |

Configuration

| Parameter name | CLI | description | Zookeeper | Сassandra |
--- | --- | --- | --- | ---
|| -c, --conf | сonfig file path | |
|| --reset_config | resets service configs on connect to DB | |
|| --listen_ip_addr | | |
|| --listen_port | | |
|| --ttl_{min,max,short} | | |
|| --hc_interval | Heartbeat interval | |
|| --hc_max_miss | Maximum missed heartbeats | |
|| --collectors | List of IP:port pair=ss of Sandesh collectors | |
|| -http_server_port | Port of local HTTP server, effectively the same as --listen_port. Used in Sandesh messages. | |
|| --log_local | | |
|| --log_level | | |
|| --log_category | | |
|| --use_syslog | | |
|| --syslog_facility | | |
|| --worker_id | Instance ID of SD for Sandesh logging | |
|| --sandesh_send_rate_limit | rate of limits for Sandesh messages | |
cass_server_ip | | | yes
cass_server_port	 | | | yes
cass_max_retries	 | | | yes
cass_timeout | | | yes 
zk_server_ip | | yes |
zk_server_port | | yes |

Stats

| Debug Key | Endpoint | Increments when	 | Zookeeper only | Cassandra only |
| --- | --- | --- | --- | --- |
| hb_stray | /heartbeat | The publisher specified by the request is not found | | |
| msg_pubs | /publish | The endpoint accepts request | | |
| msg_subs | /subscribe | The endpoint accepts request | | |
| msg_query | /query | The endpoint accepts request | | |
| msg_hbt | /heartbeat | The endpoint accepts request | | |
| ttl_short | /subscribe	 | Shorter TTL was chosen for new client (when no publishers exist for the client yet). _Short TTL logic is different in ZK and Cassandra versions._
| policy_rr | /subscribe	 | Round-robin policy was used to choose a server instance for the client to subscribe.
| policy_lb | /subscribe	 | Load-balance policy was used to choose a server instance for the client to subscribe.
| policy_fi | /subscribe	 | Fixed policy was used to choose a server instance for the client to subscribe.
| db_upd_hb | No | At startup time. _If entry heartbeet  was not set, the program resets sets it to Unix timestamp on read from db. Migration code for DB entries from old versions of SD._
| throttle_subs | /subscribe | Request is throttled. _Decision is based on 'cur_pend_sb'.  Threshold is 100, not parameterized. In Cassandra there is no throttling, it's always 0._ | yes
503 | All | Not a single Cassandra node is available, or Cassandra client hits maximum retry limit during the request.	 | |yes
count_lb | /load-balance/<service-type> | Client subscription is removed. | | yes
max_pend_pb | /publish | Maximum value of publish requests served at the same time. | yes
max_pend_sb | /subscribe	 | Maximum value of subscribe requests served at the same time.	| yes
max_pend_hb | /heartbeat | Maximum value of heartbeat requests served at the same time.	| yes
cur_pend_pb | /publish | Current number of publish requests served at the same time. | yes
cur_pend_sb | /subscribe	 | Current number of serve requests served at the same time. | yes
сur_pend_hb | /heartbeat	 | Current number of heartbeat requests served at the same time.	 | yes
restarting | All	 | ZK was restarting at the moment of request, HTTP 503 was returned. | yes