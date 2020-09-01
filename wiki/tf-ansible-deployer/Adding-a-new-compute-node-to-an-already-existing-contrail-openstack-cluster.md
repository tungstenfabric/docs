For the sake of this exercise, assume that a contrail cluster has been successfully provisioned using the instances.yaml given below and following the steps given [in this Wiki](https://github.com/Juniper/contrail-ansible-deployer/wiki/Contrail-with-Openstack-Kolla).

```
provider_config:                                                                                
  bms:
    ssh_pwd: c0ntrail123
    ssh_user: root
    ntpserver: 10.84.5.100
    domainsuffix: local
instances:
  srvr1:
    provider: bms
    ip: 192.168.1.51
    roles:
      config_database:
      config:
      control:
      analytics_database:
      analytics:
      webui:
      openstack:
  srvr2:
    provider: bms
    ip: 192.168.1.52
    roles:
      config_database:
      config:
      control:
      analytics_database:
      analytics:
      webui:
      openstack:
  srvr3:
    provider: bms
    ip: 192.168.1.53
    roles:
      config_database:
      config:
      control:
      analytics_database:
      analytics:
      webui:
      openstack:
  srvr4:                                                       
    provider: bms
    ip: 192.168.1.54
    roles:
      vrouter:
      openstack_compute:
contrail_configuration:
  CONTRAIL_VERSION: 5.0.0-0.40-ocata
  CONTROL_DATA_NET_LIST: 192.168.10.0/24
  RABBITMQ_NODE_PORT: 5673
  VROUTER_GATEWAY: 192.168.10.1
  IPFABRIC_SERVICE_HOST: 192.168.10.150
  KEYSTONE_AUTH_URL_VERSION: /v3
kolla_config:
  kolla_globals:
    kolla_internal_vip_address: 192.168.10.150
    kolla_external_vip_address: 192.168.1.150
```

Now, we will try to add a new compute named `srvr5`:

```
provider_config:                                                                                 
  bms:
    ssh_pwd: c0ntrail123
    ssh_user: root
    ntpserver: 10.84.5.100
    domainsuffix: local
instances:
  srvr1:
    provider: bms
    ip: 192.168.1.51
    roles:
      config_database:
      config:
      control:
      analytics_database:
      analytics:
      webui:
      openstack:
  srvr2:
    provider: bms
    ip: 192.168.1.52
    roles:
      config_database:
      config:
      control:
      analytics_database:
      analytics:
      webui:
      openstack:
  srvr3:
    provider: bms
    ip: 192.168.1.53
    roles:
      config_database:
      config:
      control:
      analytics_database:
      analytics:
      webui:
      openstack:
  srvr4:                                                       
    provider: bms
    ip: 192.168.1.54
    roles:
      vrouter:
      openstack_compute:
  srvr5:                                                       
    provider: bms
    ip: 192.168.1.55
    roles:
      vrouter:
      openstack_compute:

contrail_configuration:
  CONTRAIL_VERSION: 5.0.0-0.40-ocata
  CONTROL_DATA_NET_LIST: 192.168.10.0/24
  RABBITMQ_NODE_PORT: 5673
  VROUTER_GATEWAY: 192.168.10.1
  IPFABRIC_SERVICE_HOST: 192.168.10.150
  KEYSTONE_AUTH_URL_VERSION: /v3
kolla_config:
  kolla_globals:
    kolla_internal_vip_address: 192.168.10.150
    kolla_external_vip_address: 192.168.1.150
```

With this new instances.yaml, run the `configure_instances.yml` playbook as below:

```
ansible-playbook -i inventory/ -e orchestrator=openstack playbooks/configure_instances.yml 
```

This will now install the necessary software and prepare the new node for running the relevant containers

Now playbooks can now be run in next way:

```
ansible-playbook  -i inventory/ -e orchestrator=openstack --tags nova playbooks/install_openstack.yml
ansible-playbook  -i inventory/ -e orchestrator=openstack playbooks/install_contrail.yml
```

The `--tags nova` option tells the kolla playbooks to run only the nova role so that the other containers are more or less undisturbed. This is very important because if this option is omitted (especially when multiple open stack nodes are running with HA), the mariadb galera cluster will go out of sync and will never converge. The only option in that case is to destroy the whole openstack cluster.

## Removing a compute

Removing a compute is a similar exercise. Make sure the entry for the compute node exists in the instances.yaml but with empty list of roles. Also add the following section if it does not exists with the `ENABLE_DESTROY` variable. Like so:

```
global_configuration:
    ENABLE_DESTROY: True
...
...
instances:
...
...
  srvr5:                                                       
    provider: bms
    ip: 192.168.1.55
    roles:
...
...
```

Now run the following playbooks to remove the compute from Openstack and contrail config_api:

```
ansible-playbook  -i inventory/ -e orchestrator=openstack --tags nova playbooks/install_openstack.yml
ansible-playbook  -i inventory/ -e orchestrator=openstack playbooks/install_contrail.yml
```

_Known Issues:_ The following scenarios do not work for the deletion of computes yet and will be fixed asap:
1. When keystone v3 is used. Note that default for Queens and Rocky deployments is v3.
2. When `SSL_ENABLE` is set to `yes`