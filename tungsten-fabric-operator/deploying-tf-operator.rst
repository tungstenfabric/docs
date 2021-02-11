Deploying TF Operator
=====================

Prerequisities
--------------

In order to sucessfully deploy Tungsten Fabric Operator into Kubernetes cluster you will need:

* kubectl
* jinja2 (if generating manifests from templates)

Preparing Manifests
-------------------

Deployment of TF Operator requires two sets of kustomize manifests -
one of them deploys Kubernetes Operator which provides control for custom resources in the cluster
and another one provides configuration of desired Tungsten Fabric infrastructure

Manifests may be created manually, but it is recommended to generate them using jinja2 CLI tool from templates provided in the code repository.
Templates accept input data which allows to adjust final manifests with custom configuration.

.. csv-table:: **Configuration Input Data**
   :header: Variable name, Description, Example

    CONTRAIL_CONTAINER_TAG, Tag of container images, "``latest``, ``R2011``"
    CONTAINER_REGISTRY, Container registry where Tungsten Fabric images are stored., ``tungstenfabric``
    CONTRAIL_REPLICAS, Number of Tungsten Fabric controllers working in HA mode. Should not be greater than number of nodes in cluster., ``3``
    CONTROLLER_NODES, List of nodes where Tungsten Fabric controller should run. It is ignored when `CONTRAIL_REPLICAS` is provided., "``node1, node2, node3``"

