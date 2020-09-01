##  Minor upgrades of pods deployed using contrail-helm-deployer

### Get release name of contrail charts which are deployed

```bash
helm ls --all | grep contrail
contrail-analytics      1               Wed Apr 25 20:05:17 2018        DEPLOYED        contrail-analytics-0.1.0        contrail
contrail-controller     1               Wed Apr 25 20:05:12 2018        DEPLOYED        contrail-controller-0.1.0       contrail
contrail-thirdparty     1               Wed Apr 25 20:05:08 2018        DEPLOYED        contrail-thirdparty-0.1.0       contrail
contrail-vrouter        1               Wed Apr 25 20:05:22 2018        DEPLOYED        contrail-vrouter-0.1.0          contrail
```
In this output contrail-analytics, contrail-controller, contrail-thirdparty and contrail-vrouter are release name of the charts

### Export the environment variables and generate the override file

```bash
#new container tag, to which you want to upgrade
export CONTRAIL_TAG="5.0.0.1-ocata"
export CONTRAIL_REGISTRY="REGISTRY_NAME"

export CHD_PATH=/path/to/contrail-helm-deployer

# [Optional] only if you are pulling images from a private docker registry
export CONTRAIL_REG_USERNAME="abc@abc.com"
export CONTRAIL_REG_PASSWORD="password"

tee /tmp/contrail-imagesv2.yaml << EOF
global:
  images:
    tags:
      kafka: "${CONTRAIL_REGISTRY:-opencontrailnightly}/contrail-external-kafka:${CONTRAIL_TAG:-latest}"
      cassandra: "${CONTRAIL_REGISTRY:-opencontrailnightly}/contrail-external-cassandra:${CONTRAIL_TAG:-latest}"
      redis: "redis:4.0.2"
      zookeeper: "${CONTRAIL_REGISTRY:-opencontrailnightly}/contrail-external-zookeeper:${CONTRAIL_TAG:-latest}"
      contrail_control: "${CONTRAIL_REGISTRY:-opencontrailnightly}/contrail-controller-control-control:${CONTRAIL_TAG:-latest}"
      control_dns: "${CONTRAIL_REGISTRY:-opencontrailnightly}/contrail-controller-control-dns:${CONTRAIL_TAG:-latest}"
      control_named: "${CONTRAIL_REGISTRY:-opencontrailnightly}/contrail-controller-control-named:${CONTRAIL_TAG:-latest}"
      config_api: "${CONTRAIL_REGISTRY:-opencontrailnightly}/contrail-controller-config-api:${CONTRAIL_TAG:-latest}"
      config_devicemgr: "${CONTRAIL_REGISTRY:-opencontrailnightly}/contrail-controller-config-devicemgr:${CONTRAIL_TAG:-latest}"
      config_schema_transformer: "${CONTRAIL_REGISTRY:-opencontrailnightly}/contrail-controller-config-schema:${CONTRAIL_TAG:-latest}"
      config_svcmonitor: "${CONTRAIL_REGISTRY:-opencontrailnightly}/contrail-controller-config-svcmonitor:${CONTRAIL_TAG:-latest}"
      webui_middleware: "${CONTRAIL_REGISTRY:-opencontrailnightly}/contrail-controller-webui-job:${CONTRAIL_TAG:-latest}"
      webui: "${CONTRAIL_REGISTRY:-opencontrailnightly}/contrail-controller-webui-web:${CONTRAIL_TAG:-latest}"
      analytics_api: "${CONTRAIL_REGISTRY:-opencontrailnightly}/contrail-analytics-api:${CONTRAIL_TAG:-latest}"
      contrail_collector: "${CONTRAIL_REGISTRY:-opencontrailnightly}/contrail-analytics-collector:${CONTRAIL_TAG:-latest}"
      analytics_alarm_gen: "${CONTRAIL_REGISTRY:-opencontrailnightly}/contrail-analytics-alarm-gen:${CONTRAIL_TAG:-latest}"
      analytics_query_engine: "${CONTRAIL_REGISTRY:-opencontrailnightly}/contrail-analytics-query-engine:${CONTRAIL_TAG:-latest}"
      analytics_snmp_collector: "${CONTRAIL_REGISTRY:-opencontrailnightly}/contrail-analytics-snmp-collector:${CONTRAIL_TAG:-latest}"
      contrail_topology: "${CONTRAIL_REGISTRY:-opencontrailnightly}/contrail-analytics-topology:${CONTRAIL_TAG:-latest}"
      build_driver_init: "${CONTRAIL_REGISTRY:-opencontrailnightly}/contrail-vrouter-kernel-build-init:${CONTRAIL_TAG:-latest}"
      vrouter_agent: "${CONTRAIL_REGISTRY:-opencontrailnightly}/contrail-vrouter-agent:${CONTRAIL_TAG:-latest}"
      vrouter_init_kernel: "${CONTRAIL_REGISTRY:-opencontrailnightly}/contrail-vrouter-kernel-init:${CONTRAIL_TAG:-latest}"
      vrouter_dpdk: "${CONTRAIL_REGISTRY:-opencontrailnightly}/contrail-vrouter-agent-dpdk:${CONTRAIL_TAG:-latest}"
      vrouter_init_dpdk: "${CONTRAIL_REGISTRY:-opencontrailnightly}/contrail-vrouter-kernel-init-dpdk:${CONTRAIL_TAG:-latest}"
      nodemgr: "${CONTRAIL_REGISTRY:-opencontrailnightly}/contrail-nodemgr:${CONTRAIL_TAG:-latest}"
      contrail_status: "${CONTRAIL_REGISTRY:-opencontrailnightly}/contrail-status:${CONTRAIL_TAG:-latest}"
      node_init: "${CONTRAIL_REGISTRY:-opencontrailnightly}/contrail-node-init:${CONTRAIL_TAG:-latest}"
      dep_check: quay.io/stackanetes/kubernetes-entrypoint:v0.2.1
EOF

# [Optional] only if you are pulling contrail images from a private registry
tee /tmp/contrail-registry-auth.yaml << EOF
global:
images:
  imageCredentials:
    registry: ${CONTRAIL_REGISTRY:-opencontrailnightly}
    username: ${CONTRAIL_REG_USERNAME}
    password: ${CONTRAIL_REG_PASSWORD}
EOF

# [Optional] only if you are pulling images from a private registry
export CONTRAIL_REGISTRY_ARG="--values=/tmp/contrail-registry-auth.yaml "
```

**Note:** Its suggested to have your env variables global.contrail_env stored in a separate file
Sample contrail env file
```yaml
global:
  contrail_env:
    CONTROLLER_NODES: 192.168.1.10
    CONTROL_NODES: 192.168.1.10
    LOG_LEVEL: SYS_NOTICE
    CLOUD_ORCHESTRATOR: openstack
    AAA_MODE: cloud-admin
    CONTROL_DATA_NET_LIST: 192.168.1.0/24
    VROUTER_GATEWAY: 192.168.1.1
```

### Upgrading contrail helm charts

```bash
helm upgrade <release-name> ${CHD_PATH}/<contrail-chart-name> \
--values=/tmp/contrail-imagesv2.yaml \
--values=/path/to/contrail_env/file \
${CONTRAIL_REGISTRY_ARG}
```

Sample upgrade command for contrail-controller chart 
```bash
helm upgrade contrail-controller ${CHD_PATH}/contrail-controller \
--values=/tmp/contrail-imagesv2.yaml \
--values=/tmp/contrail-env.yaml \
${CONTRAIL_REGISTRY_ARG}
```

