The contrail software consists of multiple modules:
* configuration
* analytics
* control plane
* compute node
* web-ui

Binaries built from source packages are available on
https://launchpad.net/~opencontrail/+archive/ppa

## Configuration

### Services
* zookeeper
* cassandra
* rabbitmq
* ntp

Zookeeper: recommend odd number of nodes.

Cassandra: recommend a multi-node cluster configuration.

If rabbitmq is being used for openstack, we recommend that one uses the same service with a "vhost" for open contrail.

Servers running control-node components should be time synchronized.

#### OpenStack APIs using SSL
If the OpenStack API services that Contrail uses are wrapped in SSL, you will need to ensure that the CA certificate is installed on the contrail node(s). This can be done by adding the certificate to the `python-certifi` module's `cacert.pem` file, which on Ubuntu 12.04 is located at `/usr/lib/python2.7/dist-packages/certifi/cacert.pem`.

### Processes
#### ifmap-server
##### Install
```
apt-get install ifmap-server
```
##### Config
- The ifmap-server works with default config when running on all the nodes that api-server runs; the config examples above assume that.
- Authentication is defined in /etc/ifmap-server/basicauthusers.properties
Each ifmap client requires a different username; typically api-server connects to local ifmap-server but control-nodes default to connecting to ifmap-server via discovery; in this case all control-nodes should have unique if map client ids.

##### Running
```
service ifmap-server start
```
----
#### api-server
##### Install
```
apt-get install contrail-config
```

##### Config
Example: /etc/contrail/contrail-api.conf
```
[DEFAULTS]
log_file = /var/log/contrail/contrail-api.log
ifmap_server_ip = x.x.x.x 
ifmap_username = api-server
ifmap_password = api-server
cassandra_server_list = x.x.x.x:9160
auth = keystone
multi_tenancy = True
disc_server_ip = x.x.x.x
disc_server_port = 5998
zk_server_ip = x.x.x.x:2181
rabbit_server = x.x.x.x
rabbit_password = xxxxxxxxxxxxxxxxxxxx

[KEYSTONE]
auth_host = x.x.x.x
auth_port = 35357
auth_protocol = http
admin_user = neutron
admin_password = xxxxxxxxxxxxxxxxxxxx
admin_token = 
admin_tenant_name = service

```

- disc_server_ip should be the load balancer address. The LB should front-end port 5998 which is served by the discovery process. Only a single discovery server answers requires (master election via zookeeper); defaults to localhost.
- cassandra_server_list is a space separated list in the form: "x.x.x.x:9160 y.y.y.y:9160".
- zk_server_ip is a comma separated list in the form "x.x.x.x:2181,y.y.y.y:2181" and defaults to localhost.
- ifmap_server_ip is the IP where the ifmap-server is running (might be localhost)

##### Running
```
service contrail-api start
```

##### Diagnostics/Verification
Before contrail-api will listen on 8082 it has to be able to connect to rabbitmq, cassandra, zookeeper and the ifmap-server.
You can check by
```
netstat -ntop|grep $(ps auxw|grep [c]ontrail-api|awk '{print $2}')
```
There you can see if the contrail-api process actually connects to those services. The log might not always say that it cannot connect.

When multi_tenancy is enabled the http request to the api server requires a keystone auth_token.
The command should return a list of several projects, including the project that contrail creates internally as well as all projects currently visible in keystone tenant-list.

If contrail-api is listening on TCP/8082 you can verfiy the service by

```
curl -s -H "X-Auth-Token: $(keystone token-get | awk '/ id / {print $4}')" api-server-ip:8082/projects | python -mjson.tool
```
The result will be something like this
```
{
    "projects": [
        {
            "fq_name": [
                "default-domain", 
                "admin"
            ], 
            "href": "http://localhost:8082/project/61e4177f-d495-4a99-a5da-773dbb7769bf", 
            "uuid": "61e4177f-d495-4a99-a5da-773dbb7769bf"
        }, 
        {
            "fq_name": [
                "default-domain", 
                "default-project"
            ], 
            "href": "http://localhost:8082/project/66823993-6175-4318-b9d2-77e3cbf8b069", 
            "uuid": "66823993-6175-4318-b9d2-77e3cbf8b069"
        }, 
        {
            "fq_name": [
                "default-domain", 
                "services"
            ], 
            "href": "http://localhost:8082/project/7ca8dc77-b965-44c1-b7ae-e1580286cbb5", 
            "uuid": "7ca8dc77-b965-44c1-b7ae-e1580286cbb5"
        }
    ]
}
```
----
#### schema-transformer
##### Install
```
apt-get install contrail-config
```
##### Config
- Example: /etc/contrail/contrail-schema.conf
```
[DEFAULTS]
log_file = /var/log/contrail/contrail-schema.log
cassandra_server_list = x.x.x.x:9160
zk_server_ip = x.x.x.x
disc_server_ip = x.x.x.x

[KEYSTONE]
admin_user = neutron
admin_password = xxxxxxxxxxxxxxxxxxxx
admin_tenant_name = service
```

Parameters should be the same as api-server.conf.

- Example: /etc/contrail/vnc_api_lib.ini
```
[auth]
AUTHN_TYPE = keystone
AUTHN_SERVER=x.x.x.x
AUTHN_PORT = 35357
AUTHN_URL = /v2.0/tokens
```

vnc_api_lib.ini is required in the systems that run schema-transformer and neutron-server plugin. It is accessed from the neutron process.
##### Running
```
service contrail-schema start
```
----
#### discovery
- Example: /etc/contrail/contrail-discovery.conf
```
[DEFAULTS]
zk_server_ip = x.x.x.x
```
##### Diagnostics/Verification

```
curl http://x.x.x.x:5998/services
```

Displays the services registered in the discovery server. Only one of the discovery servers will answer API requests in a multi node configuration. The others are in standby mode.
The output should show one or more entries for: ApiServer, IfmapServer, Collector and xmpp-server.

----
#### Load balanced services
- api-server (port 8082).
- discovery (port 5998).


## Analytics

### Services
#### cassandra
Cassandra cluster addresses can be provided as space separated list of <ip>:<port>, e.g '10.10.10.10:9160 10.10.10.11:9160', to the analytics processes through the respective dot conf file.

#### redis (>= 2.6.13)
The redis-server version should be (>= 2.6.13). 
By default, the default redis port (6379) is used.
We do not rely on the redis DB being persisted to disk.

### Processes
#### contrail-collector
contrail collector **collects** information across the system through sandesh protocol and stores them in
analytics database

- Example /etc/contrail/contrail-collector.conf
```
[DEFAULT]
# analytics_data_ttl=48
# cassandra_server_list=127.0.0.1:9160
# dup=0
# hostip= # Resolved IP of `hostname`
# hostname= # Retrieved as `hostname`
# http_server_port=8089
# log_category=
# log_disable=0
# log_file=<stdout>
# log_files_count=10
# log_file_size=1048576 # 1MB
# log_level=SYS_NOTICE
# log_local=0
# syslog_port=0
# test_mode=0

[COLLECTOR]
# port=8086
# server=0.0.0.0

[DISCOVERY]
# port=5998
# server=0.0.0.0

[REDIS]
port=6379
server=127.0.0.1
```

#### contrail-query-engine
contrail-query-engine is the helper process in the analytics node to do queries in an optimized way and return the results to contrail-analytics-api process

- Example: /etc/contrail/contrail-query-engine.conf
```
[DEFAULT]
# analytics_data_ttl=48
# cassandra_server_list=127.0.0.1:9160
# collectors= # Provided by discovery server
# hostip= # Resolved IP of `hostname`
# hostname= # Retrieved as `hostname`
# http_server_port=8089
# log_category=
# log_disable=0
# log_file=<stdout>
# log_files_count=10
# log_file_size=1048576 # 1MB
# log_level=SYS_NOTICE
# log_local=0
# max_slice=100
# max_tasks=16
# start_time=0
# test_mode=0

[DISCOVERY]
# port=5998
# server=127.0.0.1 # discovery_server IP address

[REDIS]
  port=6379
  server=127.0.0.1
```
#### contrail-analytics-api
contrail-analytics-api is the operation REST API server and provides operational state and the historic data through REST API

- Example: /etc/contrail/contrail-analytics-api.conf
```
[DEFAULTS]
#host_ip = 127.0.0.1
#collectors = 127.0.0.1:8086
#http_server_port = 8090
#rest_api_port = 8081
#rest_api_ip = 0.0.0.0
#log_local = 0
#log_level = SYS_DEBUG
#log_category =
#log_file = stdout

[DISCOVERY]
#disc_server_ip =
#disc_server_port = 5998

[REDIS]
#server=127.0.0.1
redis_server_port = 6379
redis_query_port = 6379
```

### Diagnostics
* Use "contrail-logs" to query the analytics api and verify that it answers correctly.
* contrail-webui gets much of the info from contrail-analytics-api and hence can be
used to verify analytics functionality

## Contrail WebUI

### Services

#### redis
It is expected an instance of redis-server is instantiated on the local node that is used by webui processes [this is done by creating redis-webui.conf with appropriate parameters]. The ports are configurable through the webui conf file - /etc/contrail/config.global.js, with default being 6383.

### Processes
#### contrail-webui and contrail-webui-middleware
The configurable parameters for the webui processes are given through /etc/contrail/config.global.js
And by default, the webui console is accessible through <ip>:8080

- Example: /etc/contrail/config.global.js
```
var config = {};

config.orchestration = {};
config.orchestration.Manager = 'openstack'

...

config.networkManager = {};
config.networkManager.ip = '10.84.13.45';
config.networkManager.port = '9696'
config.networkManager.authProtocol = 'http';

...

/* Configure level of logs, supported log levels are:
   debug, info, notice, warning, error, crit, alert, emerg
 */
config.logs = {};
config.logs.level = 'debug';

// Export this as a module.
module.exports = config;
```

## Control plane

### control-node
#### Install
```
apt-get install contrail-control
```

#### Config
Example: /etc/contrail/control-node.conf
```
[DISCOVERY]
server = x.x.x.x

[IFMAP]
user=control-node-<N>
password=control-node-<N>
```

* N should be the instance-id (e.g. 1, 2, ...)
* Each username/password has to be defined in in /etc/ifmap-server/basicauthusers.properties and ifmap-server restarted
* Each control-node must have a unique username when it connects to the ifmap-server as an ifmap-client; control-nodes default to connecting to ifmap-server via discovery; in this case all control-nodes should have unique ifmap client ids.

#### Running
```
service ifmap-server restart
```

#### Verification/Diagnostics
For diagnostics check whether the control-node process has an established TCP session to port 8443 using "netstat -ntap".

* dns deamon

Recommendation: 2 control-nodes.

=====
## Compute node
### Install
* vrouter agent
* vrouter kernel module
* nova contrail driver
```
apt-get install contrail-vrouter-agent contrail-nova-driver 
```
* load the vrouter module
```
modprobe vrouter
# autoload vrouter on boot (Ubuntu)
echo vrouter >> /etc/modules
```
* for CentOS /etc/modprobe.conf (otherwise kernel panic)
```
alias bridge off
```

### Config
- /etc/nova/nova.conf (<= icehouse)
```
[DEFAULT]
network_api_class = nova.network.neutronv2.api.API
libvirt_vif_driver = nova_contrail_vif.contrailvif.VRouterVIFDriver
```
- /etc/nova/nova.conf (>= juno)
```
[DEFAULT]
network_api_class = nova_contrail_vif.contrailvif.ContrailNetworkAPI
```

- Example /etc/network/interfaces (<= R1.06)
```
auto eth1
iface eth1 inet static
      address 0.0.0.0
      up ifconfig $IFACE up
      down ifconfig $IFACE down

auto vhost0
iface vhost0 inet static
        pre-up vif --create vhost0 --mac $(cat /sys/class/net/eth1/address)
        pre-up vif --add vhost0 --mac $(cat /sys/class/net/eth1/address) --vrf 0 --mode x --type vhost
        pre-up vif --add eth1 --mac $(cat /sys/class/net/eth1/address) --vrf 0 --mode x --type physical
        address 192.168.2.252
        netmask 255.255.254.0
```
In the example above eth1 is used as VM data interface.

- Example /etc/network/interfaces.d/vhost0.cfg (>= R1.1/master)
```
auto eth1
iface eth1 inet static
    address 0.0.0.0
    up ifconfig $IFACE up
    down ifconfig $IFACE down

auto vhost0
iface vhost0 inet static
    pre-up ip link add type vhost
    pre-up vif --add eth1 --mac $(cat /sys/class/net/eth1/address) --vrf 0 --vhost-phys --type physical
    pre-up vif --add vhost0 --mac $(cat /sys/class/net/eth1/address) --vrf 0 --type vhost --xconnect eth1
    address 192.168.99.253
    netmask 255.255.254.0
    post-down vif --list | awk '/^vif.*OS: vhost0/ {split($1, arr, "\/"); print arr[2];}' | xargs vif --delete
    post-down vif --list | awk '/^vif.*OS: eth1/ {split($1, arr, "\/"); print arr[2];}' | xargs vif --delete
    post-down ip link delete vhost0
```

- /etc/contrail/contrail-vrouter-agent.conf
```
??? FIXME
```

* for CentOS /etc/contrail/agent.conf
```
<config>
    <agent>
        
        <vhost>
            <name>vhost0</name>
            <ip-address>192.168.2.252/23</ip-address><gateway>192.168.2.1</gateway></vhost>
        <eth-port>
            <name>eth1</name></eth-port>
        <metadata-proxy>
            <shared-secret />
        </metadata-proxy>
    <control><ip-address>192.168.2.252</ip-address></control><discovery-server><ip-address>192.168.2.253</ip-address><control-instances>1</control-instances></discovery-server></agent>
```

* known Ubuntu-12.04 LTS qemu issue and workaround
```
http://wiki.libvirt.org/page/Guest_won%27t_start_-_warning:_could_not_open_/dev/net/tun_%28%27generic_ethernet%27_interface%29
```
### Running
``` 
service nova-compute restart
service contrail-vrouter-agent start
```

====
## Neutron Server
### Install
* neutron opencontrail plugin
```
apt-get install neutron-plugin-contrail
```
### Config
- neutron.conf (<= R1.06)
```
core_plugin = neutron_plugin_contrail.plugins.opencontrail.contrailplugin.ContrailPlugin
api_extensions_path = /usr/lib/python2.7/dist-packages/neutron_plugin_contrail/extensions
```

- neutron.conf (>= R1.2/master)
```
core_plugin = neutron_plugin_contrail.plugins.opencontrail.contrail_plugin.NeutronPluginContrailCoreV2
api_extensions_path = /usr/lib/python2.7/dist-packages/neutron_plugin_contrail/extensions
```
- /etc/neutron/plugins/opencontrail/ContrailPlugin.ini
```
[APISERVER]
multi_tenancy = True
[KEYSTONE]
admin_user = neutron
admin_password = 
admin_tenant_name = service
auth_url = http://x.x.x.x:35357/v2.0
```
### Running
```
service neutron-server restart
```