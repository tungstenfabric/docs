# Controller
## Step 1: Create contrailctl configuration and start controller container on new node
* Configure contrailctl configuraions in /etc/contrailctl/controller.conf Refer [Contrailctl Example configurations](https://github.com/Juniper/contrail-docker/tree/master/tools/python-contrailctl/examples/configs/controller.conf)
* Start controller container - [Refer wiki](https://github.com/Juniper/contrail-docker/wiki/How-to-run-contrail-docker-containers)
* Wait for new containers up completely

## Step 2: Configure existing cluster nodes with new nodes


This step will reconfigure existing cluster application configurations to add newly added servers and restart them to accommodate the configuration changes. 

One may use any one of below methods.

### Use contrailctl to add node configuration on existing containers
One have to run below steps on all existing containers on all cluster nodes

NOTE: one should run this step on all (zookeeper) follower nodes first and then on leader node
* Findout which node is leader. [Follow wiki.](https://github.com/Juniper/contrail-ansible/wiki/Findout-which-node-is-leader-in-zookeeper-cluster)
* run contrailctl on all the existing containers in all cluster nodes (leader node as last in case of controller container)

```
$ contrailctl config node add -h 
usage: contrailctl config node add [-h] -t {controller,analyticsdb,analytics}
                                   -n NODE_ADDRESSES [-s SEED_LIST]
                                   [-f CONFIG_FILE] -c
                                   {controller,analyticsdb,analytics,agent,lb,kubemanager,mesosmanager}
                                   [--config-list CONFIG_LIST]

optional arguments:
  -h, --help            show this help message and exit
  -t {controller,analyticsdb,analytics}, --type {controller,analyticsdb,analytics}
                        Type of node
  -n NODE_ADDRESSES, --node-addresses NODE_ADDRESSES
                        Comma separated list of node addresses
  -s SEED_LIST, --seed-list SEED_LIST
                        Comma separated list of seed nodes to be used
  -f CONFIG_FILE, --config-file CONFIG_FILE
                        Master config file path
  -c {controller,analyticsdb,analytics,agent,lb,kubemanager,mesosmanager}, --component {controller,analyticsdb,analytics,agent,lb,kubemanager,mesosmanager}
                        contrail role to be configured
  --config-list CONFIG_LIST
                        comma separated list of config nodes. Optional it is
                        needed only when the new controller nodes added are
                        config service disabled

# Add new controllers in analytics container
$ contrailctl config node add -t controller -n 192.168.0.10,192.168.0.11 -s 192.168.0.102,192.168.0.99 -c analytics

# Add new controllers in analyticsdb container
$ contrailctl config node add -t controller -n 192.168.0.10,192.168.0.11 -s 192.168.0.102,192.168.0.99 -c analyticsdb

# Add new controllers in other controller containers
$ contrailctl config node add -t controller -n 192.168.0.10,192.168.0.11 -s 192.168.0.102,192.168.0.99 -c controller

```

### Manually configure contrailctl of all containers and sync the configs
One have to run below steps on all existing containers on all cluster nodes

NOTE: one should run this step on all (zookeeper) follower nodes first and then on leader node

* Findout which node is leader. [Follow wiki.](https://github.com/Juniper/contrail-ansible/wiki/Findout-which-node-is-leader-in-zookeeper-cluster)

* Manually configure /etc/contrailctl/controller.conf with new nodes for various *._list configurations and config_seed_list (Refer contrailctl configuration examples in the link mentioned in the Reference section

* Run contrailctl within the containers

```
$ docker exec <container name> contrailctl config sync -c <component name>

$ docker exec controller contrailctl config sync -c controller
```

#### Note:
Removal of contrail nodes require lot more coordination to provide scripts to do it automatically. This is work in progress. Pl contact JTAC if this is needed.

# Reference
* [contrailctl configurations](https://github.com/Juniper/contrail-docker/tree/master/tools/python-contrailctl/examples/configs)