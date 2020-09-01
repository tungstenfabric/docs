_**WHAT'S NEW:**_

CONTROL_DATA_NET_LIST has been deprecated and has been removed.

The following Kolla parameters are derived automatically:
  - kolla_internal_address and network_interface are derived based on kolla_internal_vip_address if it is provided, otherwise they are derived based on an instance IP  
  - kolla_external_vip_interface  is derived based on kolla_external_vip_address if it is provided, otherwise it is set to kolla_internal_address.

This derivation logic could be overwritten by explicitly setting of values for these variables in the kolla_global section. 

_**NOTE:**_ If you have host-specific parameters, for example, if your interface names are different on each host, you could specify them under each role (see below). The more specific setting will take precedence. For example, if there was no "PHYSICAL_INTERFACE" setting under role "vrouter" for bms7, then it will take "eth2" from the global variable, but since there is a setting under bms7->vrouter section, it will take eno1.


```

global_configuration:
  CONTAINER_REGISTRY: hub.juniper.net/contrail-nightly
  REGISTRY_PRIVATE_INSECURE: False
  CONTAINER_REGISTRY_USERNAME: <RegistryUserName>
  CONTAINER_REGISTRY_PASSWORD: <RegistryPassword>
provider_config:
  bms:
    ssh_pwd: <Pwd>
    ssh_user: root
    ntpserver: <NTP Server>
    domainsuffix: local
instances:
  bms1:
    provider: bms
    ip: 10.0.0.1
    roles:
      openstack:
  bms2:
    provider: bms
    ip: 10.0.0.2
    roles:
      openstack:
  bms3:
    provider: bms
    ip: 10.0.0.3
    roles:
      openstack:
  bms4:
    provider: bms
    ip: 10.0.0.4
    roles:
      config_database:
      config:
      control:
      analytics_database:
      analytics:
      webui:
  bms5:
    provider: bms
    ip: 10.0.0.5
    roles:
      config_database:
      config:
      control:
      analytics_database:
      analytics:
      webui:
  bms6:
    provider: bms
    ip: 10.0.0.6
    roles:
      config_database:
      config:
      control:
      analytics_database:
      analytics:
      webui:
  bms7:
    provider: bms
    ip: 10.0.0.7
    roles:
      openstack_compute:
      vrouter:
        # This should be the gateway on the Ctrl-data Network.
        VROUTER_GATEWAY: 192.168.10.1
  bms8:
    provider: bms
    ip: 10.0.0.8
    roles:
      vrouter:
        # Add following line for TSN Compute Node
        TSN_EVPN_MODE: True
contrail_configuration:
  CLOUD_ORCHESTRATOR: openstack
  OPENSTACK_VERSION: queens
  CONTRAIL_VERSION: 5.0-198
  # Use this to specify the IP addresses on each contrail node where Contrail services are to be hosted.
  # In this instance, all contrail services will run on the control-data subnet (192.168.10.0/24)
  CONTROL_NODES: 192.168.10.4,192.168.10.5,192.168.10.6

  KEYSTONE_AUTH_URL_VERSION: /v3
  # Add following line for TSN Compute Node
  TSN_NODES: 192.168.10.8
  # For EVPN VXLAN TSN
  ENCAP_PRIORITY: "VXLAN,MPLSoUDP,MPLSoGRE"
  VROUTER_GATEWAY: 192.168.10.1
  # Avoid Java apps consuming more space. 1g initial memory 2g maximum memory.
  # 1g and 2g can be changed according memory availability.
  JVM_EXTRA_OPTS: "-Xms1g -Xmx2g"

kolla_config:
  kolla_globals:
    # Virtual IP where Openstack services are accessible (haproxy/keepalived will be used on this IP)
    kolla_internal_vip_address: 10.0.0.100
  kolla_passwords:
    keystone_admin_password: <Keystone Admin Password>
```

For more detailed information on Multi NIC definition, please refer to the following link:

[General description of multinic usage](https://github.com/Juniper/contrail-ansible-deployer/wiki/Contrail%27s-multi-interface-setup-in-general)
