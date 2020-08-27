# Install and Configure OpenContrail 1.06

This installation of OpenContrail is based on Ubuntu host installed from **ubuntu-12.04.3-server-amd64.iso**. Installation option is OpenSSH server. Kernel version is 3.8.0-29-generic #42~precise1-Ubuntu.

Host name with interface IP has to be properly set in /etc/hosts before start installing OpenContrail.

## 1 Configuration Node

### 1.1 Install Packages
```
$ echo "deb http://ppa.launchpad.net/opencontrail/ppa/ubuntu precise main" | sudo tee -a /etc/apt/sources.list.d/opencontrail.list
$ sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 16BD83506839FE77
$ echo "deb http://debian.datastax.com/community stable main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
$ curl -L http://debian.datastax.com/debian/repo_key | sudo apt-key add -
$ sudo apt-get update
$
$ sudo apt-get install cassandra=1.2.18 zookeeperd rabbitmq-server ifmap-server
$ sudo apt-get install contrail-config
```

### 1.2 Configure Services

* Cassandra  
  No additional configuration is required. By default, Cassandra listens to 127.0.0.1:9160 only.

* Zookeeper  
  No additional Configuration is required.

* RabbitMQ  
  No additional Configuration is required.

* IP-MAP Server  
  Add username and password for the user of control.
  ```
  $ echo "control:control" | sudo tee -a /etc/ifmap-server/basicauthusers.properties
  $ sudo service ifmap-server restart
  ```

* Configuration API Server  
  No additional Configuration is required.

* Schema Transformer  
  No additional Configuration is required.

* Service Monitor  
  No additional Configuration is required.

* Discovery  
  No additional Configuration is required.

### 1.3 Diagnosis

* Configuration API Server  
  This shall show the list of projects (tenants).
  ```
  $ curl http://127.0.0.1:8082/projects | python -mjson.tool
  ```

* Discovery  
  This shall show the list of registered services and the list of clients asking for service info.
  ```
  $ curl http://127.0.0.1:5998/services
  $ curl http://127.0.0.1:5998/clients
  ```


## 2 Analytics Node

### 2.1 Install Packages
```
$ wget http://mirrors.kernel.org/ubuntu/pool/universe/r/redis/redis-server_2.6.13-1_amd64.deb
$ sudo apt-get install libjemalloc1
$ sudo dpkg -i redis-server_2.6.13-1_amd64.deb
$
$ echo "deb http://ppa.launchpad.net/opencontrail/ppa/ubuntu precise main" | sudo tee -a /etc/apt/sources.list.d/opencontrail.list
$ sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 16BD83506839FE77
$ sudo apt-get update
$
$ sudo apt-get install contrail-analytics
```

### 2.2 Configure Services

* Redis

  Update port setting in /etc/redis/redis.conf.
  ```
  -port 6379
  +port 6381
  ```

  Restart Redis server.
  ```
  $ sudo service redis-server restart
  ```

* Collector

  Update discovery and Redis settings in /etc/contrail/contrail-collector.conf.
  ```
  [DISCOVERY]
  port=5998
  server=127.0.0.1

  [REDIS]
  port=6381
  server=127.0.0.1
  ```

  Restart collector.
  ```
  $ sudo service contrail-collector restart
  ```

* Query Engine

  Update discovery and Redis settings in /etc/contrail/contrail-query-engine.conf.
  ```
  [DISCOVERY]
  port=5998
  server=127.0.0.1

  [REDIS]
  port=6381
  server=127.0.0.1
  ```

  Restart query engine.
  ```
  $ sudo service contrail-query-engine restart
  ```

* Analytics API Server

  Update Redis settings in /etc/contrail/contrail-analytics-api.conf.
  ```
  [REDIS]
  server=127.0.0.1
  redis_server_port=6381
  redis_query_port=6381
  ```

  Restart analytics API server.
  ```
  $ sudo service contrail-analytics-api restart
  ```

### 2.3 Diagnosis

* Analytics API Server

  The introspec port for analytics API server is 8090.  

  This shall show the list of generators.
  ```
  $ curl http://127.0.0.1:8081/analytics/generators | python -mjson.tool
  ```

  This shall show some logs.
  ```
  $ contrail-logs
  ```

* Collector

  The introspec port for collector is 8089.


## 3 Control Node

### 3.1 Install Packages
```
$ echo "deb http://ppa.launchpad.net/opencontrail/ppa/ubuntu precise main" | sudo tee -a /etc/apt/sources.list.d/opencontrail.list
$ sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 16BD83506839FE77
$ sudo apt-get update

$ sudo apt-get install contrail-control
```

### 3.2 Configure Services

* Control (BGP)

  Update [DISCOVERY] and [IFMAP] settings in /etc/contrail/control-node.conf.
  ```
  [DISCOVERY]
  port=5998
  server=127.0.0.1 # discovery_server IP address

  [IFMAP]
  password=control
  user=control
  ```

  Restart control.
  ```
  $ sudo service contrail-control restart
  ```

### 3.3 Diagnosis

* Control

  The introspec port for analytics API server is 8090.  
  This shall show the registration of control (xmpp-server) in discovery.
  ```
  $ curl http://127.0.0.1:5998/services
  ```

  This shall show control as a generator in analytics.
  ```
  curl http://127.0.0.1:8081/analytics/uves/generators | python -mjson.tool
  ```


## 4 Compute Node

### 4.1 Install Packages
```
$ echo "deb http://ppa.launchpad.net/opencontrail/ppa/ubuntu precise main" | sudo tee -a /etc/apt/sources.list.d/opencontrail.list
$ sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 16BD83506839FE77
$ sudo apt-get update
$
$ sudo apt-get install contrail-vrouter-agent
$
$ sudo modprobe vrouter
$ echo "vrouter" | sudo tee -a /etc/modules
```

### 4.2 Configure Services

* vRouter Agent

  Update /etc/contrail/contrail-vrouter-agent.conf.
  ```
  # IP address of discovery server
  server=10.8.1.10

  [VIRTUAL-HOST-INTERFACE]
  # Everything in this section is mandatory

  # name of virtual host interface
  name=vhost0

  # IP address and prefix in ip/prefix_len format
  ip=10.8.1.11/24

  # Gateway IP address for virtual host
  gateway=10.8.1.254

  # Physical interface name to which virtual host interface maps to
  physical_interface=eth1
  ```

  Update /etc/network/interfaces.
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
          address 10.8.1.11
          netmask 255.255.255.0
          #network 10.8.1.0
          #broadcast 10.8.1.255
          #gateway 10.8.1.254
          # dns-* options are implemented by the resolvconf package, if installed
          dns-nameservers 8.8.8.8
  ```

  Restart networking and vRouter agent.
  ```
  $ sudo service networking restart
  $ sudo service contrail-vrouter-agent restart
  ```

  Reboot compute node!
  ```
  $ sudo reboot now
  ```

### 4.3 Diagnosis

* vRouter Agent

  The introspec port for vRouter agent is 8085.
