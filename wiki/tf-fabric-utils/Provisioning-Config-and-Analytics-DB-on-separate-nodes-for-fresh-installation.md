# Introduction
The recommended best practice for production deployment of Contrail is to separate database for Contrail Config and Contrail Analytics. The Contrail Analytics and  Analytics DB would be installed as separate nodes (physical host or VM) while Contrail Config along with Config DB would be a separate node. 

Below are the recommended roles: 
* Contrail Controller: Contrail Config (Config Cassandra and zookeeper), Control, WebUI
* Contrail Analytics: Contrail Analytics
* Analytics DB (Analytics Cassandra and kafka) 

NOTE: These steps are applicable for Contrail 3.0.3 and later releases. 

## Example testbed.py for such a deployment
``````````````
env.roledefs = {
    'all': [host1, host2, host3, host4, host5, host6, host7, host8, host9, host11, host12, host13],
    'cfgm': [host1, host2, host3],
    'openstack': [host1, host2, host3],
    'control': [host1, host2, host3],
    'compute': [host11, host12, host13],
    'collector': [host4, host5, host6],
    'webui': [host1, host2, host3],
    'database': [host7, host8, host9],
    'build': [host_build],
    #'storage-master': [host1],
    #'storage-compute': [host4, host5, host6, host7, host8, host9, host10],
    #'rally': [host11], # Optional, to enable/setup rally, it can be a separate node from contrail cluster
    # 'vgw': [host4, host5], # Optional, Only to enable VGW. Only compute can support vgw
    # 'tsn': [host1], # Optional, Only to enable TSN. Only compute can support TSN
    # 'toragent': [host1], Optional, Only to enable Tor Agent. Only compute can
    # support Tor Agent
    #   'backup':[backup_node],  # only if the backup_node is defined
}
``````

* cfgm: This role is given to config nodes. Now this role will also include config cassandra DB and zookeeper. 
* control: This role is given to control node
* collector: This is given to analytics node. 
* database: This role now refers to only the Analytics DB.

Once the testbed.py is populated correctly, running the usual fab commands for provisioning cluster would suffice to bring up a brand new setup of Contrail with separate config and analytics databases. The fab commands are: 
* fab install_contrail
* fab setup_all

The following additional steps are done as part of the fab provisioning steps, to achieve the database split: 

1. Install 'contrail-database-common' in the config nodes
2. Provision Cassandra/zookeeper in the config nodes as well
3. Skip provisioning zookeeper in database nodes
4. Direct all config services to use Cassandra provisioned in the config node (currently they use Cassandra in database node)
  * In config.global.js, contrail-api.conf, contrail-device-manager.conf, contrail-discovery.conf, contrail-schema.conf, contrail-svc-monitor.conf
5. Direct all config services to use zookeeper provisioned in the config node (currently they use zookeeper in database node)   
  * In config.global.js, contrail-api.conf, contrail-device-manager.conf, contrail-discovery.conf, contrail-schema.conf, contrail-svc-monitor.conf
6. Direct all analytics services to use zookeeper provisioned in the config node (currently they use zookeeper in database node)
  * In contrail-collector.conf, contrail-snmp-collector.conf, contrail-topology.conf

