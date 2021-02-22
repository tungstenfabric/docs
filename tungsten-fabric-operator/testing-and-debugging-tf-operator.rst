Testing and Debugging TF Operator
==================================

:Date: 2021-02-22

This article describes how to test or debug running cluster with TF Operator applied as CNI plugin.

Pod-to-Pod ping
---------------

Working Tungsten Fabric as CNI plugin on creation of a new Pod is responsile for assigning IP address.
As well as assigning IP address, TF provides networking between Pods.
In default configuration every Pod (both in the same namespace and different namespaces) should be able to ping each other.

Apply below manifest onto cluster:

.. code-block:: YAML

    apiVersion: v1
    kind: Pod
    metadata:
    name: busy1
    spec:
    containers:
    - name: busy1
        image: busybox
        command: ["/bin/sh","-c", "while true; do echo hello; sleep 10;done"]
    nodeSelector:
        node-role.kubernetes.io/master: ""
    tolerations:
    - effect: NoSchedule
        operator: Exists
    ---
    apiVersion: v1
    kind: Pod
    metadata:
    name: busy2
    spec:
    containers:
    - name: busy2
        image: busybox
        command: ["/bin/sh","-c", "while true; do echo hello; sleep 10;done"]

Above manifest will create 2 Pods.
both are running single busybox container with dummy command.

.. note::

    `busy1` Pod has `nodeSelector` set to nodes with ``node-role.kubernetes.io/master: ""`` label.
    Usually all Kubernetes or Openshift clusters has this label automatically applied to master nodes.
    However, depending on environment it is worth checking whether nodes has this label applied, because otherwise Pod will not be created.

Check when Pods will be created and if they have IP addresses assigned with :command:`kubectl get pods -o wide`.
When Pods are created execute into one of them with :command:`kubectl exec -it busy1 sh`.
Now all commands executed in the shell will be executed in `busy1` Pod.
Check whether `busy1` Pod can ping `busy2` Pod with :command:`ping <busy2 IP address>`.
If Tungsten Fabric provides networking properly then all ping request should be successfull.
To ensure two way communication the same procedure may be repeated executing to `busy2` Pod.

The same procedure may be repeated, but with one Pod placed in a different namespace.

Isolated Namespaces ping
------------------------

Tungsten Fabric supports Kubernetes annotations as an easy way to configure basic networking properties of Kubernetes cluster.
One of them is namespace isolation.

In order to create new namespace that will be isolated (it is not necessary to create new namespace. If there is already a namespace that should be isolated it is possible to annotate it) below manifest should be applied in the cluster:

.. code-block:: YAML

    apiVersion: v1
    kind: Namespace
    metadata:
    name: "test-ns"
    annotations: {
    "opencontrail.org/isolation" : "true"
    }

Afterward, similar to Pod-to-Pod ping test two Pods should be created:

.. code-block:: YAML

    apiVersion: v1
    kind: Pod
    metadata:
    name: busy1
    namespace: test-ns
    spec:
    containers:
    - name: busy1
        image: busybox
        command: ["/bin/sh","-c", "while true; do echo hello; sleep 10;done"]
    tolerations:
    - effect: NoSchedule
        operator: Exists
    ---
    apiVersion: v1
    kind: Pod
    metadata:
    name: busy2
    spec:
    containers:
    - name: busy2
        image: busybox
        command: ["/bin/sh","-c", "while true; do echo hello; sleep 10;done"]

Above manifest will create `busy1` Pod in the isolated namespace while `busy2` Pod will be created in default namespace which should not be able to ping `busy1` Pod.
Check when Pods will be created and if they have IP addresses assigned with :command:`kubectl get pods -o wide` and :command:`kubectl get pods -o wide -n test-ns` for `busy1` Pod.
When Pods are created execute into one of them with :command:`kubectl exec -it busy1 sh`.
Now all commands executed in the shell will be executed in `busy1` Pod.
Check whether `busy1` Pod can ping `busy2` Pod with :command:`ping <busy2 IP address>`.
If Tungsten Fabric provides networking properly then all ping request should be dropped as `busy1` Pod is in isolated namespace which should not communicate with other namespaces.
To ensure two way communication the same procedure may be repeated executing to `busy2` Pod.

Compute Node configuration
--------------------------

Every compute node has applied vRouter module which provides Tungsten Fabric networking rules (more on specific Tungsten Fabric architecture `here <https://codilime.com/tungsten-fabric-architecture-an-overview/>`__ or `here <https://wiki.lfnetworking.org/display/LN/2021-02-02+-+TF+Architecture+Overview>`__).

A series of simple checks may be helpful to ensure that specific compute node is working properly or to perform basic debugging of Tungsten Fabric.

vhost0 Interface
~~~~~~~~~~~~~~~~

vRouter operates via vhost0 interface which is virtual interface that applies Tungsten Fabric rules to a traffic that goes throught the node.
Every node should have vhost0 interface with IP address assigned from physical interface (the one that receives the traffic).
To check whether vhost0 interface exists run :command:`ip address`.
In list of interfaces there should be vhost0 interface with IP address assigned.
It is worth also checking the physical interface to see whether there is no IP address (because vhost0 took it over).

.. code-block:: console

    1:  p1p1 Link encap:Ethernet HWaddr b0:ob:ab:ba:0a:a0
        UP BROADCAST RUNNING MULTICAST MTU:9000 Metric:1
        RX packets:194126327 errors:0 dropped:0 overruns:0 frame:0
        TX packets:125130748 errors:0 dropped:0 overruns:0 carrier:0
        collisions:0 txqueuelen:1000
        RX bytes:286638778868 (286.6 GB) TX bytes:94956347917 (94.9 GB)
        Interrupt:40 Memory:f3000000-f37fffff
    2:  vhost0 Link encap:Ethernet HWaddr b0:ob:ab:ba:0a:a0
        inet addr:172.20.0.23 Bcast:172.20.0.31 Mask:255.255.255.240
        UP BROADCAST RUNNING MULTICAST MTU:9000 Metric:1
        RX packets:84487487 errors:0 dropped:182627 overruns:0 frame:0
        TX packets:82063519 errors:0 dropped:0 overruns:0 carrier:0
        collisions:0 txqueuelen:1000
        RX bytes:253984497954 (253.9 GB) TX bytes:67502412941 (67.5 GB)

Also vhost0 and physical interface shoul dhave the same MAC address.
If you do not know which interface is pysical interface for vhost0 then by default it is `eth0` interface.
However, it may be checked using `vif` CLI tool that comes together with vRouter module.

Command :command:`vif --list` shows all interfaces recognised by Tungsten Fabric.
Here it is also possible to recongise physical interface by comparing MAC address of vhost0 interface with any other interface.

If you need specific information regarding name of the physical interface then vRouter confgiuration contains it written in `ini` format easy to parse with any programming language.
File `/etc/contrail/contrail-vrouter-agent.conf` under section `[VIRTUAL-HOST-INTERFACE]` has field `physical_interface` with value of the interface name.

.. code-block:: console

    cmpt001:~# cat /etc/contrail/contrail-vrouter-agent.conf | grep -A13 -i virtual-host-interface
    [VIRTUAL-HOST-INTERFACE]
    # Everything in this section is mandatory

    # name of virtual host interface
    name=vhost0

    # IP address and prefix in ip/prefix_len format
    ip=172.20.0.23/32

    # Gateway IP address for virtual host
    gateway=172.20.0.1

    # Physical interface name to which virtual host interface maps to
    physical_interface=p1p1

Node Routing
~~~~~~~~~~~~
