# Deploying SRIOV compute using helm charts

### Preparing multinode-inventory.yaml and multinode-vars.yaml

In `multinode-inventory.yaml`, make sure that you have `contrail-vrouter-sriov` group. 

Sample `multinode-inventory.yaml` file. Refer to `${OSH_INFRA_PATH}/tools/gate/devel/sample-contrail-multinode-inventory.yaml` for much more options

```yaml
all:
  children:
    primary:
      hosts:
        node1:
          ansible_port: 22
          ansible_host: 10.10.10.13
          ansible_user: ubuntu
          ansible_ssh_private_key_file: /home/ubuntu/.ssh/insecure.pem
          ansible_ssh_extra_args: -o StrictHostKeyChecking=no
    nodes:
      children:
        openstack-compute:
           children:
             contrail-vrouter-sriov:
               hosts:
                 node7:
                   ansible_port: 22
                   ansible_host: 10.10.10.19
                   ansible_user: ubuntu
                   ansible_ssh_private_key_file: /home/ubuntu/.ssh/insecure.pem
                   ansible_ssh_extra_args: -o StrictHostKeyChecking=no
```

Sample `multinode-vars.yaml`. Refer to `${OSH_INFRA_PATH}/tools/gate/devel/sample-contrail-multinode-inventory.yaml` for much more options

```yaml
version:
 kubernetes: v1.9.3
 helm: v2.7.2
 cni: v0.6.0

docker:
 insecure_registries:
   - "10.84.5.81:5000"
nodes:
  labels:
    primary:
    - name: openstack-helm-node-class
      value: primary
    - name: openstack-control-plane
      value: enabled
    - name: ceph-mon
      value: enabled
    - name: ceph-osd
      value: enabled
    - name: ceph-mds
      value: enabled
    - name: ceph-rgw
      value: enabled
    - name: ceph-mgr
      value: enabled
    - name: opencontrail.org/controller
      value: enabled
    all:
    - name: openstack-helm-node-class
      value: general
    openstack-compute:
    - name: openstack-compute-node
      value: enabled
    contrial-vrouter-kernel:
    - name: opencontrail.org/vrouter-kernel
      value: enabled
    contrail-vrouter-dpdk:
    - name: opencontrail.org/vrouter-dpdk
      value: enabled
    contrail-vrouter-sriov:
    - name: vrouter-sriov
      value: enabled
```

### Deploy kubernetes 
Deploy kubernetes as mentioned in [multinode-doc](https://github.com/Juniper/contrail-helm-deployer/blob/master/doc/contrail-osh-multinode-install.md#pre-requisites)

### Deploy openstack-helm charts 
Deploy openstack-helm charts as mentioned in this [link](https://github.com/Juniper/contrail-helm-deployer/blob/master/doc/contrail-osh-multinode-install.md#installation-of-openstack-helm-charts)

### Preparing nova config for SRIOV nodes

After deploying openstack-helm charts, edit `${OSH_PATH}/tools/deployment/multinode/144-sriov-compute-kit-opencontrail.sh` path, according to your setup. Make sure to change SRIOV_DEV1 and SRIOV_DEV2 interface name. By default. label level configuration is set. To set node level configuration, please refer to [this doc](https://github.com/Juniper/openstack-helm/blob/master/doc/source/devref/node-and-label-specific-configurations.rst#node-and-label-specific-configurations)

### Deploying contrail-sriov pods using vrouter chart

Sample environment specific values needed by SRIOV, you can have more nodes and respective env variables under the per_compute_info

```yaml
global:
  contrail_env:
    CONTROLLER_NODES: 10.87.64.112
    CONTROL_NODES: 172.16.10.22
    VROUTER_GATEWAY: 172.16.10.5
    BGP_PORT: 1179
  contrail_env_vrouter_sriov:
    SRIOV: true
    per_compute_info:
      - node_name: "5b3s1-node3.englab.juniper.net"
        SRIOV_VF:  10
        SRIOV_PHYSICAL_INTERFACE: "p2p2"
        SRIOV_PHYS_NET: "physnet1"
```

Now deploy contrail charts as mentioned in this [doc](https://github.com/Juniper/contrail-helm-deployer/blob/master/doc/contrail-osh-multinode-install.md#installation-of-contrail-helm-charts)