Installing Tungsten Fabric with Kubernetes in Nested Mode by Using Juju Charms
==============================================================================

Tungsten Fabric Release 1909 and later support provisioning of a
Kubernetes cluster inside an OpenStack cluster. Tungsten Fabric
offers a nested control and data plane where a single TF control
plane and a single network stack can manage and service both the
OpenStack and Kubernetes clusters.

In nested mode, a Kubernetes cluster is provisioned in virtual machines
of an OpenStack cluster. The CNI plugin and the TF-Kubernetes
manager of the Kubernetes cluster interface directly with TF
components that manage the OpenStack cluster.

All Kubernetes features, functions and specifications are supported when
used in nested mode.

.. note::

   Nested mode deployment is only supported for TF with OpenStack
   cluster.

Before you begin:

-  Deploy TF with OpenStack either on bare metal server or virtual
   machines.

   **Best Practice**

   Public cloud deployment is not recommended because of slow nested
   virtualization.

-  The VMs must have internet connectivity.

-  TF in underlay network must be configured to support nested
   mode.

   You must select an unused IP in the cluster to configure
   ``link-local``.
   For example:

   10.10.10.5 is the selected service IP.
   ================ ========== ============ ========= ===========
   LL Service Name  Service IP Service Port Fabric IP Fabric Port
   ================ ========== ============ ========= ===========
   K8s-cni-to-agent 10.10.10.5 9091         127.0.0.1 9091
   ================ ========== ============ ========= ===========

Follow these steps to deploy Juju Charms with Kubernetes in nested mode
using bundle deployment:

Use this method if you want to use the existing machines.

1. Create a Juju controller.

   ``juju bootstrap --bootstrap-series=xenial <cloud name> <controller name>``

   You can use OpenStack Cloud provider or manually spun-up VMs. For
   details, refer to :ref:`Installing TF with Kubernetes by Using Juju Charms`.

2. Deploy bundle.

   ``juju deploy --series xenial cs:~containers/kubernetes-worker-550 --to:0 \     --config channel="1.14/stable" \     --config docker_runtime="custom" \``

   If the machines for the setup are already provisioned, run the
   following command to deploy bundle:

   | ``juju deploy --map-machines=existing,0=0,5=1 ./bundle.yaml``
   | where ``bundle-id=existing-id``

   For details, refer to
   https://jaas.ai/u/juniper-os-software/contrail-k8s-nested/bundle.

or

Follow these steps to deploy Juju Charms with Kubernetes in nested mode
manually:

1. Create a Juju controller.

   ``juju bootstrap --bootstrap-series=xenial <cloud name> <controller name>``

   You can use OpenStack Cloud provider or manually spun-up VMs. For
   details, refer to :ref:`Installing TF with Kubernetes by Using Juju Charms`.

2. Create machine instances for TF components, Kubernetes master
   and Kubernetes workers.
   Sample constraints for minimal deployment:

   All-In-One deployment:

   ``juju add-machine --constraints mem=32G cores=8 root-disk=150G --series=xenial # for all-in-one machine``

   or

   Multinode deployment:

   ``juju add-machine --constraints mem=8G cores=2 root-disk=50G --series=xenial # kubernetes workersjuju add-machine --constraints mem=8G cores=2 root-disk=50G --series=xenial # kubernetes mastersjuju add-machine --constraints mem=4G cores=4 root-disk=50G --series=xenial # TF components``
   You can use any series—``xenial`` or ``bionic``.

3. Add machines to the cloud.

   For details, refer to `Using
   Constraints-Juju <https://jaas.ai/docs/constraints>`__.

4. Deploy the Kubernetes services.

   Some of the applications may need additional configuration.

   You can deploy Kubernetes services using any one of the following
   methods:

   -  By specifying the Kubernetes parameters in a YAML file.

   -  By passing options/values directly on the command line.

   **Note**

   You must use the same docker version for TF and Kubernetes.

   For more details, refer to `Juju Application
   Configuration <https://old-docs.jujucharms.com/2.4/en/charms-config>`__.

5. Deploy and configure ntp, easyrsa, etcd, kubernetes-master,
   kubernetes-worker.

   ::

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

6. Deploy and configure TF services.

   Deploy contrail-kubernetes-master, contrail-kubernetes-node,
   contrail-agent from the directory where you have downloaded the
   charms.

   ::

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

   ::

      juju deploy --series xenial cs:~juniper-os-software/contrail-kubernetes-master \
          --config ./path-to-config.yaml

      juju deploy --series xenial cs:~juniper-os-software/contrail-kubernetes-node

7. Add the necessary relations.

   ::

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

8. Apply SSL, if needed.

   You must provide the same certificates to the
   ``contrail-kubernetes-master`` node if TF in underlay cluster
   has SSL enabled.

.. list-table:: Release History Table
   :header-rows: 1

   * - Release
     - Description
   * - 2011
     - Tungsten Fabric Release 2011 and later support provisioning of a
       Kubernetes cluster inside an OpenStack cluster. Tungsten Fabric
       offers a nested control and data plane where a single TF control
       plane and a single network stack can manage and service both the
       OpenStack and Kubernetes clusters.


 
