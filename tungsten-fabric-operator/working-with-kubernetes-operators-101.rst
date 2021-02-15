Working with Kubernetes Operators 101
=====================================

What is an operator?
--------------------

And operator is an automated software extension that allows to easily manage applications and their components.
It's used to package, deploy and manage applications based on Kubernetes custom resources.

The operator acts as a controller that extends Kubernetes API to manage the lifecycle of dependent application resources.
The controller implements logic that periodically compares desired state of a cluster to it's actual state and applies corrections to meet declared state.

Compared to other methods of managing application deployment on Kubernetes clusters, operator allows to cover the complete lifetime of an application.
Below graph compares operator to Helm and Ansible.
Helm provides only installation process with some mechanisms of upgrade.
Ansible additionaly allows to cover some aspects of managing application resources lifecycle.
However, only operator allows to have full insights into created cluster resources and perform custom operations on them during lifecycle.

.. figure:: figures/operator-compared.png

Custom operator may be written in multiple languages as in fact it's just a piece of code  that acts when triggered by events from the Kubernetes API.
Currently, the most popular language to write operators is the language that was used to write the Kubernetes project itself - Go.
Helpful tool for creating operators is `Operator Framework <https://github.com/operator-framework>`_ which distributes
`Operator-SDK <https://github.com/operator-framework/operator-sdk>`_ commonly used to create operators - for example this operator.

Every custom resource built with operator contains 2 elements.
First element is API which defines how resource is defined and what's it's structure.
This definition is used afterwards by Operator Framework to generate CustomResourceDefinition (CRD in short) manifests that
are applied on a cluster and extend the Kubernetes API. User can follow the schema defined by the CRD to create new custom resources.
Second element is controller which runs on an operator pod and handles logic of custom resource.
Every controller uses Kubernetes watch API to observe state of the cluster and, if necessary, trigger Reconcile method
containing code describing logic of the particular custom resource.
Commonly, it creates, deletes or updates standard Kubernetes resources like pods, sets, secrets etc.

How does it work here?
----------------------

This operator implements custom resources for Tungsten Fabric deployment.
Before tf-operator the `tf-ansible-deployer <https://github.com/tungstenfabric/tf-ansible-deployer>`_ was used, which contained
set of ansible playbooks that setup instances based on a file with configuration.
This method took a lot time and could often fail, because of connection lost between bootstraping instance and cluster or unexpected failure.

With tf-operator all that's required is Kubernetes cluster (or Kubernetes-like cluster e.g. Openshift)
and one manifest in common format similar to definition of simple Pod or Daemonset.
Applying manifest on cluster will create all required resources to deploy Tungsten Fabric succesfullly.
Status of all components is available to check at any time of deployment as well as during lifetime of a cluster.

Tungsten Fabric may be configured in various ways for various infrastructures.
Example infrastructure with 3 master nodes and 3 worker nodes is presented below.

.. figure:: figures/operator-tf-scheme.png

Master node contains Tungsten Fabric controller components.
Rabbitmq, Zookeeper and Cassandra create databases with configuration.
From configuration database, Config components take or store current configuration of cluster.
Configuration may be set with WebUI and it's read and propagated by Control components to vRouters which manage networking on an interface
on remote machines that are managed by Tungsten Fabric.
Controller also contains Kubemanager component which gathers information from Kubernetes cluster and provides it to configuration.
vRouters mounted on every node control networking traffic on an interface with rules defined by agent that gathers rules from control node.
Controller components may also have more than one replica spread across multiple nodes which allows Tungsten Fabric to work in HA (High Availability) mode.

In order to deploy such infrastructure on Kubernetes cluster it's necessary to create manifest which defines the Manager custom resource.
Manager is a single resource which defines Tungsten Fabric cluster.
In its definition user defines which components should be created and with what configuration.

However, Kubernetes cluster by default does not know what is Manager resource how to implement it's deployment.
Because of that it's necessary to beforewards apply all CRDs (Custom Resource Definitions) to cluster which in this repository are located under
`deploy/crds <https://github.com/tungstenfabric/tf-operator/tree/master/deploy/crds>`_ directory.
While Kubernetes cluster will now properly read manifests for Tungsten Fabric custom resources, it does not have logic that
should be used in order to properly control resources.

To fix that problem, operator itself has to be deployed on cluster.
Applied operator will create separate Pod which will act as controller of custom resources in cluster.

Afterwards, when manifest is applied on cluster in namespace *contrail* (*contrail* namespace has to be created beforehand),
status of all pods created by Tungsten Fabric may be observed.
Because operator allows to create custom logic in code, some components wait for other components to be deployed in order to start its'
Pods which protects deployment against race conditions and potential failures.

After example infrastructure is deployed following Pods run in contrail namespace:
```
$ kubectl get pods -n contrail
NAME                                          READY   STATUS             RESTARTS   AGE
cassandra1-cassandra-statefulset-0            1/1     Running            0          39m
cassandra1-cassandra-statefulset-1            1/1     Running            0          39m
cassandra1-cassandra-statefulset-2            1/1     Running            0          39m
config1-config-statefulset-0                  10/10   Running            0          38m
config1-config-statefulset-1                  10/10   Running            0          38m
config1-config-statefulset-2                  10/10   Running            0          39m
tf-operator-dd5bb5c-klqwb                     1/1     Running            0          42m
control1-control-statefulset-0                4/4     Running            0          30m
control1-control-statefulset-1                4/4     Running            0          30m
control1-control-statefulset-2                4/4     Running            0          30m
kubemanager1-kubemanager-statefulset-0        2/2     Running            0          30m
kubemanager1-kubemanager-statefulset-1        2/2     Running            0          30m
kubemanager1-kubemanager-statefulset-2        2/2     Running            0          30m
provmanager1-provisionmanager-statefulset-0   1/1     Running            0          30m
rabbitmq1-rabbitmq-statefulset-0              1/1     Running            0          39m
rabbitmq1-rabbitmq-statefulset-1              1/1     Running            0          39m
rabbitmq1-rabbitmq-statefulset-2              1/1     Running            0          39m
vroutermasternodes-vrouter-daemonset-rgl4t    1/1     Running            0          28m
vroutermasternodes-vrouter-daemonset-ttc7c    1/1     Running            0          28m
vroutermasternodes-vrouter-daemonset-wn6qg    1/1     Running            0          28m
vrouterworkernodes-vrouter-daemonset-gs4bw    1/1     Running            0          5m
vrouterworkernodes-vrouter-daemonset-p7zkw    1/1     Running            0          5m
vrouterworkernodes-vrouter-daemonset-pqfw9    1/1     Running            0          5m
webui1-webui-statefulset-0                    3/3     Running            0          30m
webui1-webui-statefulset-1                    3/3     Running            0          30m
webui1-webui-statefulset-2                    3/3     Running            0          30m
zookeeper1-zookeeper-statefulset-0            1/1     Running            0          8m
zookeeper1-zookeeper-statefulset-1            1/1     Running            0          8m
zookeeper1-zookeeper-statefulset-2            1/1     Running            0          8m
```
That's just one resource type which creates all the custom Tungsten Fabric resources the in cluster during deployment.

Miscellaneous elements of deployment
------------------------------------

Deployment described in previous section is just a core solution of tf-operator.
However, for different platforms, deployment may vary.
Because of that, additional components are defined in this repository. They allow to deploy operatorized Tungsten Fabric
with platforms like Openstack or Openshift.
Depending on specific bussiness problem and environment it's necessary to pick components that will fulfill the needs.
To find out more about Tungsten Fabric architecture watch `this <https://wiki.lfnetworking.org/display/LN/2021-02-02+-+TF+Architecture+Overview>`_
presentation or read `this <https://codilime.com/tungsten-fabric-architecture-an-overview/>`_ blogpost.

Openshift deployment use case example
-------------------------------------

For example, to deploy described above infrastructure on Openshift, it's necessary to apply some additional resources.
Openshift is based on RedHat CoreOS nodes which have generally read-only filesystem and limited system tools for configuration during runtime.
CoreOS is designed to be configured buring boot process with so called ignition configs and then work with persistent configuration.
Because of that `here <https://github.com/tungstenfabric/tf-openshift/tree/master/deploy/openshift>`_ are some ignition configs applied as custom resources managed by operator
delivered by Openshift. For example nftables rules required by Tungsten Fabric are applied with ignition files or an overlay mount
of `/lib/modules` directory is created in order to allow mount of vRouter kernel module.

Openshift deployment process from version 4 is fully based on operators.
It means that every feature of this platform is deployed as set of custom resources managed by operator.
Because of that, tf-operator works great with deploying CNI plugin on cluster during Openshift installation.
Openshift installation process is all defined with manifests similar to manifests created for
Tungsten Fabric created by Openshift just before cluster install which means that Tungsten Fabric `manifests <https://github.com/tungstenfabric/tf-openshift/tree/master/deploy/manifests>`_may just be
added to other install manifests and will be applied on cluster during install process.

More on Openshift install process with Tungsten Fabric as CNI `here <https://github.com/tungstenfabric/tf-openshift>`_.