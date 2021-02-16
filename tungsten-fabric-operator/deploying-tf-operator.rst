Deploying TF Operator
=====================

:Date: 2021-02-16

Prerequisities
--------------

In order to sucessfully deploy Tungsten Fabric Operator into Kubernetes cluster you will need:

* kubectl
* jinja2 (if generating manifests from templates)
* Kubernetes cluster

.. note::

   Before deploying Tungsten Fabric to the Kubernetes cluster, check whether master nodes have labeled ``node-role.kubernetes.io/master: ""``.
   Usually, nodes are labeled automatically on cluster installation, but in some environments, this label may be missing.
   Currently, control plane components of Tungsten Fabric use node selector, which allows to deploy it only on master nodes.

Preparing Manifests
-------------------

Deployment of TF Operator requires two sets of kustomize manifests -
one of them deploys Kubernetes Operator, which provides a control for custom resources in the cluster
and another one provides configuration of desired Tungsten Fabric infrastructure

Manifests may be created manually, but it is recommended to generate them using jinja2 CLI tool from templates provided in the code repository.
Templates accept input data, which allows adjusting final manifests with custom configuration.

.. csv-table:: **Configuration Input Data**
   :header: Variable name, Description, Example

   CONTRAIL_CONTAINER_TAG, Tag of container images, "``latest``, ``R2011``"
   CONTAINER_REGISTRY, Container registry where Tungsten Fabric images are stored., ``tungstenfabric``
   CONTRAIL_REPLICAS, Number of Tungsten Fabric controllers working in HA mode. Should not be greater than number of nodes in cluster., ``3``
   CONTROLLER_NODES, List of nodes where Tungsten Fabric controller should run. It is ignored when `CONTRAIL_REPLICAS` is provided., "``node1, node2, node3``"
   CONTRAIL_DEPLOYER_CONTAINER_TAG, Tag for operator container image. Use it when using different tag for operator than other TF containers. If not specified the same tag as `CONTRAIL_CONTAINER_TAG` will be used, "``latest``, ``R2011``"
   DEPLOYER_CONTAINER_REGISTRY, Container registry to download from operator container image. Use it when container registry is different from other container images of Tungsten Fabric. If not specified the sam registry as `CONTAINER_REGISTRY` will be used, "``tungstenfabric``"

Jinja2 API accepts multiple formats of input data (ini, env, yaml etc.).
Prepare configuration file in chosen format and render templates providing configuration file.
There are multiple jinja2 CLI wrappers that allow rendering templates from terminal.
For example using `this <https://github.com/mattrobenolt/jinja2-cli>`_ Python based tool which may be installed from PyPI with pip.

Applying Manifests
------------------

Assuming that a Kubernetes cluster is up and running, apply manifests.

First, using :command:`kubectl apply -f ./deploy/crds/` apply CRDs (Custom Resource Definitions) to the cluster.
This step create new custom Tungsten Fabric resources in Kubernetes API and allow to recongise them when applying to the cluster.

With :command:`kubectl wait crds --for=condition=Established --timeout=2m managers.contrail.juniper.net` ensure that all CRDs are properly applied and ready to be used.

Afterward, create a new Kubernetes Operator in the cluster applying kustomize manifests with :command:`kubectl apply -k ./deploy/kustomize/operator/templates/`.
This command will create a deployment with pods that run operator code and control behaviour of Tungsten Fabric custom resources applied in the cluster.

Finally, deploy Tungsten Fabric into Kubernetes infrastructure with :command:`kubectl apply -k ./deploy/kustomize/contrail/templates/`.
To ensure that Tungsten Fabric is up and running check pods state in namespace `contrail`.
All pods should be either in `Running` or `Completed` state.
