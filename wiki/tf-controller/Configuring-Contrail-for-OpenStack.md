## Configuring Contrail for OpenStack

Contrail can be installed and added to any existing OpenStack deployment by making relevant configuration changes on the OpenStack setup and pointing Contrail configuration to the existing OpenStack. The same principle can also be applied to a new contrail and new openstack deployments. 

Lets first start by identifying the hooks and the touch points. 

The OpenStack hooks used by Contrail are:

1. `core_plugin` - This is used in the neutron config to point to ContrailPlugin
2. `libvirt_vif_driver` - This is used in the nova compute config to point to Contrail VRouterVIFDriver
3. MQ broker IP and Port - If existing OpenStack provides RabbitMQ then corresponding IP and port needs to be configured in the neutron and nova config. 

The Contrail touch points are:

1. `api_service.conf` - This file needs to be edited to provide details of existing OpenStack keystone.
2. `plugin.ini` - This file needs proper keystone URL, token and credentials.
3. `neutron.conf` - This file needs auth_host credentials to connect OpenStack keystone.
4. `config.global.js` - This file contains IP and PORT for image (glance), compute (nova), identity (keystone), storage (cinder)
5. OpenStack controller nova config to point to Contrail neutron
6. OpenStack controller neuron service endpoint to point to contrail neutron.

## Lets build one:

Here are the steps to install contrail and connect to OpenStack. For better understanding there are 3 procedures listed. One, which provides details on the Contrail controller configuration and two, which provides details on the Compute node configuration and three, provides details on the OpenStack controller config. 

**_Make sure to remove existing OpenStack OVS installed modules and config._**

### Procedure - 1 (Contrail Config Node)

1. Install Contrail on the target system
2. Once contrail is installed properly, edit the fab file (testbed.py) and provide the details of the existing OpenStack node. In a non fab way of doing the setup, contrail provides puppet manifests and python scripts for contrail setup. 
3. Once the setup is complete, edit the following files. 
* `/etc/contrail/api_server.conf` 
Update the KEYSTONE section to point to the existing OpenStack Keystone and provide the proper credentials.

* Here is an example of the complete api_server config:
```
[DEFAULTS]
ifmap_server_ip=10.1.1.252
ifmap_server_port=8443
ifmap_username=api-server
ifmap_password=api-server
cassandra_server_list=10.1.1.252:9160
listen_ip_addr=0.0.0.0
listen_port=8082
auth=keystone
multi_tenancy=False
log_file=/var/log/contrail/api.log
disc_server_ip=10.1.1.252
disc_server_port=5998
zk_server_ip=10.1.1.252:2181
redis_server_ip=None

[SECURITY]
use_certs=False
keyfile=/etc/contrail/ssl/private_keys/apiserver_key.pem
certfile=/etc/contrail/ssl/certs/apiserver.pem
ca_certs=/etc/contrail/ssl/certs/ca.pem

[KEYSTONE]
auth_host=10.1.1.2
auth_protocol=http
admin_user=admin
admin_password=1a0137e30d2845ee
admin_token=9a6acb8cc6ba43ac847ecc1bea0a7df6
admin_tenant_name=admin
```

> 10.1.1.252 is the contrail controller IP

> 10.1.1.2 is the openstack controller. 

* edit `/etc/neutron/plugin.ini` and provide API server IP and port along with the keystone credentials. 
* Here is a sample configuration:

```
[APISERVER]
api_server_ip = 10.1.1.252
api_server_port = 8082

[KEYSTONE]
;auth_url = http://10.1.1.2:35357/v2.0
;admin_token = 9a6acb8cc6ba43ac847ecc1bea0a7df6
admin_user=admin
admin_password=1a0137e30d2845ee
```

* edit `/etc/neutron/neutron.conf` and provide the auth_host. Also provide the rabbitMQ details
* Here is the sample config:

```
[keystone_authtoken]
auth_host = 10.1.1.2
auth_port = 35357
auth_protocol = http
admin_tenant_name = services
admin_user = neutron
admin_password = 66bd8e29876844aa
signing_dir = $state_path/keystone-signing

rabbit_host=10.1.1.2
rabbit_port=5672
```

* edit `/etc/contrail/config.global.js` and provide the OpenStack IP and port for image, compute, identity and storage.
* Here is an example:
```
config.imageManager = {};
config.imageManager.ip = '10.1.1.2';
config.imageManager.port = '9292';

config.computeManager = {};
config.computeManager.ip = '10.1.1.2';
config.computeManager.port = '8774';

config.identityManager = {};
config.identityManager.ip = '10.1.1.2';
config.identityManager.port = '5000';
config.identityManager.authProtocol = 'http';
config.identityManager.strictSSL = false;
config.identityManager.ca = '';

config.storageManager = {};
config.storageManager.ip = '10.1.1.2';
config.storageManager.port = '8776';
```

### Procedure - 2 (Compute Node)

1. On an existing compute node, ensure bridge kernel modules are uninstalled / disabled. Clean up the OVS packages and config
2. Install and setup vrouter using the scripts provided by Contrail.
3. Make the following config changes:

* edit `/etc/nova/nova.config` on the compute node and provide details of the VRouterVIFDriver and neutron details. 

Here is an example:
```
neutron_url=http://10.1.1.252:9696
neutron_admin_username=neutron
neutron_admin_password=66bd8e29876844aa
neutron_admin_tenant_name=services
neutron_region_name=RegionOne
neutron_admin_auth_url=http://10.1.1.2:35357/v2.0
neutron_auth_strategy=keystone
neutron_extension_sync_interval=600

libvirt_vif_driver=contrail_vif.contrailvif.VRouterVIFDriver

rabbit_host=10.1.1.2
rabbit_port=5672
```

### Procedure - 3 (OpenStack Node)

Ensure that the OVS and bridge configuration is removed. 

1. On an existing OpenStack node, update the nova config to include neutron network.  

* edit `/etc/nova/nova.conf` and provide neutron_url 

Here is an example:
```
neutron_url=http://10.1.1.252:9696

rabbit_host=10.1.1.2
rabbit_port=5672
```

## Verification:

Once all the system is configured, contrail processes should be able to connect to OpenStack. 

Here are some commands to check:

On OpenStack controller run:

neutron net-list. If all the configuration is in place, network list should be displayed. 
```
[root@contnode2 ~(keystone_admin)]# neutron net-list
+--------------------------------------+-------------------------+-----------------------------------------------------+
| id                                   | name                    | subnets                                             |
+--------------------------------------+-------------------------+-----------------------------------------------------+
| 95c2733c-d4d1-4540-89db-474b07c01445 | test-net                | 69b9e27f-33aa-4e64-b131-c7e71a3065a1 10.5.5.0/24    |
| 07b0f300-8aa2-4ca7-af3f-e558d779e957 | intranet                | 4ce5aa95-2a30-4146-a8ca-dd77035d4224 10.102.50.0/27 |
| ebb66f84-fc7b-4298-9d5e-25dfbdde817b | default-virtual-network |                                                     |
| c36ed4c4-c7cc-4f85-ba7c-7e92997824ec | ip-fabric               |                                                     |
| e5a1f057-4523-4cd4-9194-6270e62efbc9 | __link_local__          |                                                     |
+--------------------------------------+-------------------------+-----------------------------------------------------+
```

 


 