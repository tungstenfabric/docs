# Installing Contrail with Kubernetes in Nested Mode by Using Juju Charms

 

<span id="jd0e10">Contrail Networking Release 1909 and later support
provisioning of a Kubernetes cluster inside an OpenStack cluster.
Contrail Networking offers a nested control and data plane where a
single Contrail control plane and a single network stack can manage and
service both the OpenStack and Kubernetes clusters.</span>

In nested mode, a Kubernetes cluster is provisioned in virtual machines
of an OpenStack cluster. The CNI plugin and the Contrail-Kubernetes
manager of the Kubernetes cluster interface directly with Contrail
components that manage the OpenStack cluster.

All Kubernetes features, functions and specifications are supported when
used in nested mode.

**Note**

Nested mode deployment is only supported for Contrail with OpenStack
cluster.

Before you begin:

-   Deploy Contrail with OpenStack either on bare metal server or
    virtual machines.

    **Best Practice**

    Public cloud deployment is not recommended because of slow nested
    virtualization.

-   The VMs must have internet connectivity.

-   Contrail in underlay network must be configured to support nested
    mode.

    You must select an unused IP in the cluster to configure
    `link-local`.

    <div id="jd0e41" class="sample" dir="ltr">

    For example:

    10.10.10.5 is the selected service IP.

    </div>

    | LL Service Name  | Service IP | Service Port | Fabric IP | Fabric Port |
    |:-----------------|:-----------|:-------------|:----------|:------------|
    | K8s-cni-to-agent | 10.10.10.5 | 9091         | 127.0.0.1 | 9091        |

Follow these steps to deploy Juju Charms with Kubernetes in nested mode
using bundle deployment:

Use this method if you want to use the existing machines.

1.  <span id="jd0e93">Create a Juju controller.</span>

    `juju bootstrap --bootstrap-series=xenial <cloud name> <controller name>`

    You can use OpenStack Cloud provider or manually spun-up VMs. For
    details, refer to [Preparing to Deploy Contrail with Kubernetes by
    Using Juju
    Charms](/documentation/en_US/contrail19/topics/topic-map/deploying-contrail-using-juju-charms-kubernetes.html#PreparingToDeployContrailk8s).

2.  <span id="jd0e106">Deploy bundle.</span>

    `juju deploy --series xenial cs:~containers/kubernetes-worker-550 --to:0 \     --config channel="1.14/stable" \     --config docker_runtime="custom" \`

    If the machines for the setup are already provisioned, run the
    following command to deploy bundle:

    `juju deploy --map-machines=existing,0=0,5=1 ./bundle.yaml`  
    where `bundle-id=existing-id`

    For details, refer to
    <https://jaas.ai/u/juniper-os-software/contrail-k8s-nested/bundle>.

  

or

  

Follow these steps to deploy Juju Charms with Kubernetes in nested mode
manually:

1.  <span id="jd0e138">Create a Juju controller.</span>

    `juju bootstrap --bootstrap-series=xenial <cloud name> <controller name>`

    You can use OpenStack Cloud provider or manually spun-up VMs. For
    details, refer to [Preparing to Deploy Contrail with Kubernetes by
    Using Juju
    Charms](/documentation/en_US/contrail19/topics/topic-map/deploying-contrail-using-juju-charms-kubernetes.html#PreparingToDeployContrailk8s).

2.  <span id="jd0e151">Create machine instances for Contrail components,
    Kubernetes master and Kubernetes workers.</span>

    <div id="jd0e154" class="sample" dir="ltr">

    Sample constraints for minimal deployment:

    All-In-One deployment:

    `juju add-machine --constraints mem=32G cores=8 root-disk=150G --series=xenial # for all-in-one machine`

    or

    Multinode deployment:

    `juju add-machine --constraints mem=8G cores=2 root-disk=50G --series=xenial # kubernetes workersjuju add-machine --constraints mem=8G cores=2 root-disk=50G --series=xenial # kubernetes mastersjuju add-machine --constraints mem=4G cores=4 root-disk=50G --series=xenial # contrail components`

    </div>

    You can use any series—`xenial` or `bionic`.

3.  <span id="jd0e181">Add machines to the cloud.</span>

    For details, refer to [Using
    Constraints-Juju](https://jaas.ai/docs/constraints).

4.  <span id="jd0e189">Deploy the Kubernetes services.</span>

    Some of the applications may need additional configuration.

    You can deploy Kubernetes services using any one of the following
    methods:

    -   By specifying the Kubernetes parameters in a YAML file.

    -   By passing options/values directly on the command line.

    **Note**

    You must use the same docker version for Contrail and Kubernetes.

    For more details, refer to [Juju Application
    Configuration](https://old-docs.jujucharms.com/2.4/en/charms-config).

5.  <span id="jd0e211">Deploy and configure <span class="cli"
    v-pre="">ntp, easyrsa, etcd, kubernetes-master,
    kubernetes-worker</span>.</span>
    <div id="jd0e217" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        juju deploy --series xenial cs:ntp ntp

        juju deploy --series xenial cs:~containers/easyrsa --to lxd:0

        juju deploy --series xenial cs:~containers/etcd --to:0 --config channel="3.2/stable"

        juju deploy --series xenial cs:~containers/kubernetes-master-696 --to:0 \
            --config channel="1.14/stable" \
            --config docker_runtime="custom" \
            --config docker_runtime_repo="deb [arch={ARCH}] https://download.docker.com/linux/ubuntu {CODE} stable" \
            --config docker_runtime_key_url="https://download.docker.com/linux/ubuntu/gpg" \
            --config docker_runtime_package="docker-ce"

        juju deploy --series xenial cs:~containers/kubernetes-worker-550 --to:0 \
            --config channel="1.14/stable" \
            --config ingress="false" \
            --config docker_runtime="custom" \
            --config docker_runtime_repo="deb [arch={ARCH}] https://download.docker.com/linux/ubuntu {CODE} stable" \
            --config docker_runtime_key_url="https://download.docker.com/linux/ubuntu/gpg" \
            --config docker_runtime_package="docker-ce"

    </div>

    </div>

6.  <span id="jd0e220">Deploy and configure Contrail services.</span>

    Deploy <span class="cli" v-pre="">contrail-kubernetes-master,
    contrail-kubernetes-node, contrail-agent</span> from the directory
    where you have downloaded the charms.

    <div id="jd0e228" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        contrail-kubernetes-master:
            nested_mode: true
            cluster_project: "{'domain':'default-domain','project':'admin'}"
            cluster_network: "{'domain':'default-domain','project':'admin','name':'juju-net'}"
            service_subnets: '10.96.0.0/12'
            nested_mode_config: |
                {
                "CONTROLLER_NODES": "10.0.12.20",
                "AUTH_MODE": "keystone",
                "KEYSTONE_AUTH_ADMIN_TENANT": "admin",
                "KEYSTONE_AUTH_ADMIN_USER": "admin",
                "KEYSTONE_AUTH_ADMIN_PASSWORD": "password",
                "KEYSTONE_AUTH_URL_VERSION": "/v2.0",
                "KEYSTONE_AUTH_HOST": "10.0.12.122",
                "KEYSTONE_AUTH_PROTO": "http",
                "KEYSTONE_AUTH_PUBLIC_PORT":"5000",
                "KEYSTONE_AUTH_REGION_NAME": "RegionOne",
                "KEYSTONE_AUTH_INSECURE": "True",
                "KUBERNESTES_NESTED_VROUTER_VIP": "10.10.10.5"
                }

    </div>

    <div class="output" dir="ltr">

        juju deploy --series xenial cs:~juniper-os-software/contrail-kubernetes-master \
            --config ./path-to-config.yaml

        juju deploy --series xenial cs:~juniper-os-software/contrail-kubernetes-node

    </div>

    </div>

7.  <span id="jd0e233">Add the necessary relations.</span>
    <div id="jd0e236" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        juju add-relation "kubernetes-master:juju-info" "ntp:juju-info"
        juju add-relation "kubernetes-worker:juju-info" "ntp:juju-info"

        juju add-relation "kubernetes-master:kube-api-endpoint" "kubernetes-worker:kube-api-endpoint"
        juju add-relation "kubernetes-master:kube-control" "kubernetes-worker:kube-control"
        juju add-relation "kubernetes-master:certificates" "easyrsa:client"
        juju add-relation "kubernetes-master:etcd" "etcd:db"
        juju add-relation "kubernetes-worker:certificates" "easyrsa:client"
        juju add-relation "etcd:certificates" "easyrsa:client"

        juju add-relation "contrail-kubernetes-node:cni" "kubernetes-master:cni"
        juju add-relation "contrail-kubernetes-node:cni" "kubernetes-worker:cni"
        juju add-relation "contrail-kubernetes-master:kube-api-endpoint" "kubernetes-master:kube-api-endpoint"
        juju add-relation "contrail-kubernetes-master:contrail-kubernetes-config" "contrail-kubernetes-node:contrail-kubernetes-config"

    </div>

    </div>

8.  <span id="jd0e239">Apply SSL, if needed.</span>

    You must provide the same certificates to the
    `contrail-kubernetes-master` node if Contrail in underlay cluster
    has SSL enabled.

<div class="table">

<div class="caption">

Release History Table

</div>

<div class="table-row table-head">

<div class="table-cell">

Release

</div>

<div class="table-cell">

Description

</div>

</div>

<div class="table-row">

<div class="table-cell">

[1909](#jd0e10)

</div>

<div class="table-cell">

Contrail Networking Release 1909 and later support provisioning of a
Kubernetes cluster inside an OpenStack cluster. Contrail Networking
offers a nested control and data plane where a single Contrail control
plane and a single network stack can manage and service both the
OpenStack and Kubernetes clusters.

</div>

</div>

</div>

 
