Here is example of HA deployment on single interface.

```
provider_config:
  bms:
    ssh_pwd: <password>
    ssh_user: root
    ntpserver: 10.84.5.100
    domainsuffix: local
instances:
  server1:
    provider: bms
    ip: 10.0.0.1
    roles:
      openstack:
  server2:
    provider: bms
    ip: 10.0.0.2
    roles:
      openstack:
  server3:
    provider: bms
    ip: 10.0.0.3
    roles:
      openstack:
  server4:                                                       
    provider: bms
    ip: 10.0.0.4
    roles:
      config_database:
      config:
      control:
      analytics_database:
      analytics:
      webui:
  server5:
    provider: bms
    ip: 10.0.0.5
    roles:
      config_database:
      config:
      control:
      analytics_database:
      analytics:
      webui:
  server6:
    provider: bms
    ip: 10.0.0.6
    roles:
      config_database:
      config:
      control:
      analytics_database:
      analytics:
      webui:
  server7:
    provider: bms
    ip: 10.0.0.7
    roles:
      vrouter:
      openstack_compute:
  server8:
    provider: bms
    ip: 10.0.0.8
    roles:
      vrouter:
      openstack_compute:
contrail_configuration:
  CONTRAIL_VERSION: <Build number>
  # Optional: Will be derived to mgmt IP list if not specified
  CONTROLLER_NODES: 10.0.0.4,10.0.0.5,10.0.0.6
  CLOUD_ORCHESTRATOR: openstack
  # Optinal: default gw will be used
  VROUTER_GATEWAY: 10.0.0.254
  # Optional: The IP where the nova api service is running. Derived to be same as kolla_internal_vip_address
  IPFABRIC_SERVICE_HOST: <Service Host IP>
  # Optional: The IP where Keystone Service is running. Derived to be same as kolla_internal_vip_address
  KEYSTONE_AUTH_HOST: <Keystone Node IP>
  KEYSTONE_AUTH_URL_VERSION: /v3
  # Avoid Java apps consuming more space. 1g initial memory 2g maximum memory.
  # 1g and 2g can be changed according memory availability. Not mandatory, can be removed if more memory available.
  JVM_EXTRA_OPTS: "-Xms1g -Xmx2g"
kolla_config:
  kolla_globals:
    # This needs to be a virtual IP where openstack services will be accessible on.
    # Refer to the kolla documentation for more info.
    # (https://github.com/openstack/kolla-ansible/blob/stable/ocata/etc/kolla/globals.yml#L26)
    kolla_internal_vip_address: 10.0.0.100
  kolla_passwords:
    keystone_admin_password: <Keystone Admin Password>

```