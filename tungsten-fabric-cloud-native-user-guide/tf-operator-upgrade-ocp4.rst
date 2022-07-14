How to Upgrade Tungsten Fabric Through Kubernetes and/or Red Hat OpenShift
==============================================================================

Starting in Tungsten Fabric Release R21.12, you can update Tungsten Fabric through Kubernetes and/or Red Hat OpenShift.

You can use this procedure to update Tungsten Fabric deployed by the Tungsten Fabric (TF) Operator.

To update Tungsten Fabric:

1. Update manifests with the new container tag.

.. code-block:: shell

    export CONTRAIL_CONTAINER_TAG=<new tag>
    ./tf-operator/contrib/render_manifests.sh

Note: Only CONTRAIL_CONTAINER_TAG must have a new tag. The render manifest must be done with all the same exported environment variables used during the initial deployment.

2. Update the tf-operator deployment.

.. code-block:: shell

    kubectl apply -k ./tf-operator/deploy/kustomize/operator/templates/

3. Wait and ensure that the tf-operator deployment is updated.

.. code-block:: shell

    kubectl –n tf get pods -w | grep tf-operator

4. Update Tungsten Fabric resources.

.. code-block:: shell


    kubectl apply -k ./tf-operator/deploy/kustomize/contrail/templates/

5. Wait and ensure that the TF Control plane pods are updated.

.. code-block:: shell

    kubectl –n tf get pods -w

6. Use the contrail-status tool to check the Tungsten Fabric status on all the master nodes.

.. code-block:: shell

    $ contrail-status
    Must show that all services are active:
    == Contrail control ==
    control: active
    nodemgr: active
    named: active
    dns: active

    == Contrail analytics-alarm ==
    nodemgr: active
    kafka: active
    alarm-gen: active

    == Contrail kubernetes ==
    kube-manager: backup

    == Contrail database ==
    nodemgr: active
    query-engine: active
    cassandra: active

    == Contrail analytics ==
    nodemgr: active
    api: active
    collector: active

    == Contrail config-database ==
    nodemgr: active
    zookeeper: active
    rabbitmq: active
    cassandra: active

    == Contrail webui ==
    web: active
    job: active

    == Contrail vrouter ==
    nodemgr: active
    agent: active

    == Contrail analytics-snmp ==
    snmp-collector: active
    nodemgr: active
    topology: active

    == Contrail config ==
    svc-monitor: backup
    nodemgr: active
    device-manager: backup
    api: active
    schema: backup

7. Upgrade the TF vRouter components (one-by-one or by groups).

* Choose a node to upgrade and obtain the vRouter daemon name for the node.

::
    kubectl describe node <node name>

* Delete the vRouter pod resource by specifying the name of the pod you want to delete.

::
    kubectl –n tf delete pod <vrouter1-vrouter-daemonset-xxxxx>

* Wait until the new daemon set is run by kubernetes on a node.

Use kubectl get pods < > commad.

.. code-block:: shell


    kubectl get pods -n tf | grep "vrouter1-vrouter-daemonset"
    vrouter1-vrouter-daemonset-77cnz   3/3     Running   0    51m
    vrouter1-vrouter-daemonset-7rlvf   3/3     Running   0    87m
    vrouter1-vrouter-daemonset-jrzfm   3/3     Running   0    82m
    vrouter1-vrouter-daemonset-jvhmj   3/3     Running   0    85m
    vrouter1-vrouter-daemonset-v4brl   3/3     Running   0    52m

The status is showing Running for all the vRouter daemon sets. The number of daemon set entries depends on the cluster size (that is number of master nodes and worker nodes).

You can also verify the status of a particular daemon set. Obtain the new vrouter-daemonset from the kubectl describe node <node name> command. Check the status of that particular daemon set using the kubectl get pods -n tf | grep "vrouter1-vrouter-daemonset-XXX" command.

8. Verify the vRouter agent status by using the contrail-status command on the node.

Control/Master nodes

.. code-block:: shell


    $ contrail-status
    Must show that all services are active:
    == Contrail control ==
    control: active
    nodemgr: active
    named: active
    dns: active

    == Contrail analytics-alarm ==
    nodemgr: active
    kafka: active
    alarm-gen: active

    == Contrail kubernetes ==
    kube-manager: backup

    == Contrail database ==
    nodemgr: active
    query-engine: active
    cassandra: active

    == Contrail analytics ==
    nodemgr: active
    api: active
    collector: active

    == Contrail config-database ==
    nodemgr: active
    zookeeper: active
    rabbitmq: active
    cassandra: active

    == Contrail webui ==
    web: active
    job: active

    == Contrail vrouter ==
    nodemgr: active
    agent: active

    == Contrail analytics-snmp ==
    snmp-collector: active
    nodemgr: active
    topology: active

    == Contrail config ==
    svc-monitor: backup
    nodemgr: active
    device-manager: backup
    api: active
    schema: backup

Worker Nodes

.. code-block:: shell

    vrouter kernel module is PRESENT
    == Contrail vrouter ==
    nodemgr: active
    agent: active