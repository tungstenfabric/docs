# Deploying DPDK with contrail helm charts

#### System requirements on compute node for dpdk

* OS: Ubuntu 16.04.2
* Linux version: 4.4.0-62-generic
* CPU's: 32
* Socket(s): 2
* NUMA node(s): 2
* RAM: 132GB
* 10GB physical NIC (Niantic NIC)

#### Instructions for openstack-helm charts

Before installing compute-kit.sh, `export HUGE_PAGES_DIR="/dev/hugepages"`

#### Instructions to bring up vrouter dpdk

* Label your node as "opencontrail.org/vrouter-dpdk=enabled"
  ```bash
  kubectl label node <node-name> opencontrail.org/vrouter-dpdk=enabled
  ```

* For DPDK compute you have to enable following manifests and please check [contrail-vrouter/values.yaml](https://github.com/Juniper/contrail-helm-deployer/blob/master/contrail-vrouter/values.yaml), which is by default set to false:

```yaml
manifests:
  configmap_vrouter_dpdk: true
  daemonset_dpdk: true
```

#### Sample contrail-vrouter/values.yaml file which has sample user config needed for dpdk and kernel computes in a single cluster
```yaml
global:
  images:
    tags:
      nodemgr: "docker.io/opencontrailnightly/contrail-nodemgr:ocata-master-43"
      build_driver_init: "docker.io/opencontrailnightly/contrail-vrouter-kernel-build-init:ocata-master-43"
      vrouter_agent: "docker.io/opencontrailnightly/contrail-vrouter-agent:ocata-master-43"
      vrouter_init_kernel: "docker.io/opencontrailnightly/contrail-vrouter-kernel-init:ocata-master-43"
      vrouter_dpdk: "docker.io/opencontrailnightly/contrail-vrouter-agent-dpdk:ocata-master-43"
      vrouter_init_dpdk: "docker.io/opencontrailnightly/contrail-vrouter-kernel-init-dpdk:ocata-master-43"
      dpdk_watchdog: "docker.io/opencontrailnightly/contrail-vrouter-net-watchdog:ocata-master-43"
      dep_check: quay.io/stackanetes/kubernetes-entrypoint:v0.2.1
    imagePullPolicy: "IfNotPresent"

  # common section for all vrouter variants
  # this section is commonized with other Contrails' services
  contrail_env:
    CONTROLLER_NODES: 10.87.140.154
    CONTROL_NODES: 8.0.0.1
    LOG_LEVEL: SYS_NOTICE
    CLOUD_ORCHESTRATOR: openstack
    AAA_MODE: cloud-admin
    # this value should be the same as nova/conf.nova.neutron.metadata_proxy_shared_secret
    METADATA_PROXY_SECRET: password
    CONTROL_DATA_NET_LIST: 8.0.0.0/24
    VROUTER_GATEWAY: 8.0.0.254
  # section of vrouter template for kernel mode
  contrail_env_vrouter_kernel:
    AGENT_MODE: nic

  # section of vrouter template for dpdk mode
  contrail_env_vrouter_dpdk:
    PHYSICAL_INTERFACE: bond0.2003
    CPU_CORE_MASK: "0xff"
    DPDK_UIO_DRIVER: uio_pci_generic
    HUGE_PAGES: 48000
    AGENT_MODE: dpdk
  node:
    host_os: ubuntu

labels:
  vrouter_agent_kernel:
    node_selector_key: "opencontrail.org/vrouter-kernel"
    node_selector_value: "enabled"
  vrouter_agent_dpdk:
    node_selector_key: "opencontrail.org/vrouter-dpdk"
    node_selector_value: "enabled"

dependencies:
  vrouter_agent_kernel:
    daemonset:
    - contrail-config
    - contrail-control
  vrouter_agent_dpdk:
    daemonset:
    - contrail-config
    - contrail-control
endpoints:
  cluster_domain_suffix: cluster.local
  keystone:
    auth:
      username: admin
      password: password
      project_name: admin
      user_domain_name: default
      project_domain_name: default
      region_name: RegionOne
    hosts:
      default: keystone-api
    path:
      default: /v3
    port:
      admin:
        default: 35357
      api:
        default: 80
    scheme:
      default: http
    host_fqdn_override:
       default: null
    namespace: openstack

manifests:
  configmap_vrouter_kernel: true
  configmap_vrouter_keystone: true
  configmap_vrouter_dpdk: true
  daemonset_kernel: true
  daemonset_dpdk: true
```

Note: Re-run compute-kit.sh script after installing contrail charts 
