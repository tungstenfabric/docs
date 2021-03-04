How to Enable Virtualization with KubeVirt in Environments Using Kubernetes with a TF cluster
===================================================================================================

:date: 2020-12-16 

KubeVirt is a virtualization add-on to Kubernetes that allows virtual
machines (VMs) to run alongside the application containers present in a
Kubernetes environment. KubeVirt provides a unified development platform
where developers can build, modify, and deploy applications residing in
both application containers and VMs within a common, shared environment.
For additional information on KubeVirt and it’s benefits, see the
`KubeVirt <https://kubevirt.io/>`__ homepage.

Starting in Tungsten Fabric Release 2011, you can use KubeVirt to
allow VMs to run in any Kubernetes-orchestrated environments that use
TF as the Container Networking Interface (CNI).

This document provides the instructions for installing KubeVirt in any
Kubernetes environment that is using Tungsten Fabric. This document
also includes a section specifically on using KubeVirt to enable
OpenShift Virtualization in environments using Red Hat Openshift.

This document includes the following sections:

.. _how-to-enable-virtualization-with-kubevirt-in-environments-using-kubernetes-with-a-tf-cluster-1:

How to Enable Virtualization with KubeVirt in Environments Using Kubernetes with a TF cluster
---------------------------------------------------------------------------------------------

This section provides the instructions for enabling VM support in
Kubernetes-orchestrated environments that are using Tungsten Fabric
as the CNI.

When to Use This Procedure
~~~~~~~~~~~~~~~~~~~~~~~~~~

A Kubernetes environment is containerized but might have to support VMs.
Common reasons for supporting VMs include maintaining VM-based workloads
that are challenging to containerize or to more gracefully migrate from
a VM-based environment to Kubernetes.

The procedure in this document was validated for Tungsten Fabric
2011.

Prerequisites
~~~~~~~~~~~~~

This procedure makes the following assumptions about your environment:

-  A Kubernetes environment using Tungsten Fabric as the CNI is
   operational.

How to Install KubeVirt
~~~~~~~~~~~~~~~~~~~~~~~

To enable VMs in a Kubernetes environments with KubeVirt:

1. Verify the pods and nodes in your Kubernetes cluster.

   In this representative example, the kubectl get nodes and kubectl get
   pods commands are used to view the nodes and pods in the environment.

   ::

      $ kubectl get nodes -o wide
      NAME          STATUS   ROLES    AGE   VERSION   INTERNAL-IP      EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION       CONTAINER-RUNTIME
      k8s-master1   Ready    master   63d   v1.18.9   172.16.125.115   <none>        Ubuntu 18.04.5 LTS   4.15.0-118-generic   docker://18.9.9
      k8s-master2   Ready    master   63d   v1.18.9   172.16.125.116   <none>        Ubuntu 18.04.5 LTS   4.15.0-118-generic   docker://18.9.9
      k8s-master3   Ready    master   63d   v1.18.9   172.16.125.117   <none>        Ubuntu 18.04.5 LTS   4.15.0-118-generic   docker://18.9.9
      k8s-node1     Ready    <none>   63d   v1.18.9   172.16.125.118   <none>        Ubuntu 18.04.5 LTS   4.15.0-112-generic   docker://18.9.9
      k8s-node2     Ready    <none>   63d   v1.18.9   172.16.125.119   <none>        Ubuntu 18.04.5 LTS   4.15.0-112-generic   docker://18.9.9

      kubectl get pods -n kube-system
      NAME                                          READY   STATUS    RESTARTS   AGE
      config-zookeeper-4klts                        1/1     Running   0          63d
      config-zookeeper-cs2fk                        1/1     Running   0          63d
      config-zookeeper-wgrtb                        1/1     Running   0          63d
      contrail-agent-ch8kv                          3/3     Running   3          63d
      contrail-agent-kh9cf                          3/3     Running   1          63d
      contrail-agent-kqtmz                          3/3     Running   0          63d
      contrail-agent-m6nrz                          3/3     Running   1          63d
      contrail-agent-qgzxt                          3/3     Running   0          63d
      contrail-analytics-6666s                      4/4     Running   1          63d
      contrail-analytics-jrl5x                      4/4     Running   4          63d
      contrail-analytics-x756g                      4/4     Running   4          63d
      contrail-configdb-2h7kd                       3/3     Running   4          63d
      contrail-configdb-d57tb                       3/3     Running   4          63d
      contrail-configdb-zpmsq                       3/3     Running   4          63d
      contrail-controller-config-c2226              6/6     Running   9          63d
      contrail-controller-config-pbbmz              6/6     Running   5          63d
      contrail-controller-config-zqkm6              6/6     Running   4          63d
      contrail-controller-control-2kz4c             5/5     Running   2          63d
      contrail-controller-control-k522d             5/5     Running   0          63d
      contrail-controller-control-nr54m             5/5     Running   2          63d
      contrail-controller-webui-5vxl7               2/2     Running   0          63d
      contrail-controller-webui-mzpdv               2/2     Running   1          63d
      contrail-controller-webui-p8rc2               2/2     Running   1          63d
      contrail-kube-manager-88c4f                   1/1     Running   0          63d
      contrail-kube-manager-fsz2z                   1/1     Running   0          63d
      contrail-kube-manager-qc27b                   1/1     Running   0          63d
      ...

   The Contrail containers running in the pods confirm that Contrail is
   running in this Kubernetes environment.

2. Export the latest KubeVirt version.

   You can check for the latest KubeVirt version using the `Release
   Blogs <https://kubevirt.io/blogs/releases.html>`__ from KubeVirt.

   In this representative example, KubeVirt v0.35.0 is exported.

   ::

      $ export KUBEVIRT_VERSION="v0.35.0"

3. Install the KubeVirt operator. The KubeVirt operator manages the
   lifecycle of all KubeVirt core components and will be used in this
   procedure to enable virtualization.

   ::

      $ kubectl create -f https://github.com/kubevirt/kubevirt/releases/download/${KUBEVIRT_VERSION}/kubevirt-operator.yaml
      $ kubectl get pods -n kubevirt
      NAME                               READY   STATUS    RESTARTS   AGE
      virt-operator-78fbcdfdf4-ghxhg     1/1     Running   2          5m
      virt-operator-78fbcdfdf4-pgsfw     1/1     Running   0          3m

4. After the KubeVirt operator is deployed, deploy the KubeVirt custom
   resource definitions (CRDs):

   ::

      $ kubectl create -f https://github.com/kubevirt/kubevirt/releases/download/${KUBEVIRT_VERSION}/kubevirt-cr.yaml
      $ kubectl get pods -n kubevirt
      NAME                               READY   STATUS    RESTARTS   AGE
      virt-api-64999f7bf5-k48g6          1/1     Running   0          26m
      virt-api-64999f7bf5-ql5fm          1/1     Running   0          26m
      virt-controller-8696ccdf44-w9nd8   1/1     Running   2          25m
      virt-controller-8696ccdf44-znvdk   1/1     Running   0          25m
      virt-handler-c866z                 1/1     Running   0          25m
      virt-handler-ns5xg                 1/1     Running   0          25m
      virt-handler-sr6sj                 1/1     Running   0          25m
      virt-handler-v5gz7                 1/1     Running   0          25m
      virt-handler-w274q                 1/1     Running   0          25m
      virt-operator-78fbcdfdf4-ghxhg     1/1     Running   2          31m
      virt-operator-78fbcdfdf4-pgsfw     1/1     Running   0          29m

5. Create a kubevirt-config ConfigMap.

   The ConfigMap must be updated to support software emulation.

   To create this ConfigMap:

   1. Create a KubeVirt config map:

      ::

         $ kubectl create cm kubevirt-config -n kubevirt

   2. Add the following configuration to the config map and confirm the
      configuration.

      ::

         data:
           debug.useEmulation: "true"

         $ kubectl edit cm kubevirt-config -n kubevirt

         apiVersion: v1
         kind: ConfigMap
         metadata:
           name: kubevirt-config
           namespace: kubevirt
         data:
           debug.useEmulation: "true"

   3. Restart the ``virt-handler`` pods:

      ::

         $ kubectl -n kubevirt delete pod -l k8s-app=virt-handler

How to Create a Virtual Machine on KubeVirt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After KubeVirt is installed, you can create VMs that are fully
integrated into Kubernetes using Virtual Machine Instance (VMI) custom
resources.

To configure these VMs:

1. We will illustrate this procedure within it’s own namespace.

   To create a namespace called ``kubevirt-demo`` for this procedure:

   ::

      $ kubectl create ns kubevirt-demo

2. Create the VM.

   In this representative example, a VM instance running CentOS 7 is
   created and applied using a YAML file named ``kubevirt-centos.yaml``.

   ::

      cat <<EOF > kubevirt-centos.yaml
      apiVersion: kubevirt.io/v1alpha3
      kind: VirtualMachineInstance
      metadata:
        labels:
          special: vmi-centos7
        name: vmi-centos7
        namespace: kubevirt-demo
      spec:
        domain:
          devices:
            disks:
            - disk:
                bus: virtio
              name: containerdisk
            - disk:
                bus: virtio
              name: cloudinitdisk
            interfaces:
            - name: default
              bridge: {}
          resources:
            requests:
              memory: 1024M
        networks:
        - name: default
          pod: {}
        volumes:
        - containerDisk:
            image: ovaleanu/centos:latest
          name: containerdisk
        - cloudInitNoCloud:
            userData: |-
              #cloud-config
              password: centos
              ssh_pwauth: True
              chpasswd: { expire: False }
          name: cloudinitdisk
      EOF

      $ kubectl apply -f kubevirt-centos.yaml
      virtualmachineinstance.kubevirt.io/vmi-centos7 created

3. Confirm that the Virtual Machine instance was created:

   ::

      kubectl get pods -n kubevirt-demo
      NAME                              READY   STATUS    RESTARTS   AGE
      virt-launcher-vmi-centos7-xfw2p   2/2     Running   0          100s

      kubectl get vmi -n kubevirt-demo
      NAME          AGE     PHASE     IP                 NODENAME
      vmi-centos7   5m48s   Running   10.47.255.218/12   k8s-node1

4. Create a service for the VM that allows the VM to establish SSH
   connections through NodePort using node IP.

   In this representative example, the service is created and applied
   using the ``kubevirt-centos-svc.yaml`` file. The get svc command is
   also entered to verify that the service is running.

   ::

      cat <<EOF > kubevirt-centos-svc.yaml
      apiVersion: v1
      kind: Service
      metadata:
        name: vmi-centos-ssh-svc
        namespace: kubevirt-demo
      spec:
        ports:
        - name: centos-ssh-svc
          nodePort: 30000
          port: 27017
          protocol: TCP
          targetPort: 22
        selector:
          special: vmi-centos7
        type: NodePort
      EOF

      $ kubectl apply -f kubevirt-centos-svc.yaml

      $ kubectl get svc -n kubevirt-demo
      NAME                 TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)           AGE
      vmi-centos-ssh-svc   NodePort   10.97.172.252   <none>        27017:30000/TCP   13s

5. Connect to the VM using the service that was created in the previous
   step.

   ::

      ssh centos@172.16.125.118 -p 30000
      The authenticity of host '[172.16.125.118]:30000 ([172.16.125.118]:30000)' can't be established.
      ECDSA key fingerprint is SHA256:1ELZpIiqyBaUEN4EUkskTvGzB+2GyJmkvT7d+FiXfL8.
      Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
      Warning: Permanently added '[172.16.125.118]:30000' (ECDSA) to the list of known hosts.
      centos@172.16.125.118's password:

      [centos@vmi-centos7 ~]$ uname -sr
      Linux 3.10.0-957.12.2.el7.x86_64

      [centos@vmi-centos7 ~]$ ip a
      1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
          link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
          inet 127.0.0.1/8 scope host lo
             valid_lft forever preferred_lft forever
          inet6 ::1/128 scope host
             valid_lft forever preferred_lft forever
      2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
          link/ether 02:bb:7b:93:16:2e brd ff:ff:ff:ff:ff:ff
          inet 10.47.255.218/12 brd 10.47.255.255 scope global dynamic eth0
             valid_lft 86313353sec preferred_lft 86313353sec
          inet6 fe80::bb:7bff:fe93:162e/64 scope link
             valid_lft forever preferred_lft forever

      [centos@vmi-centos7 ~]$ ping www.google.com
      PING www.google.com (216.58.194.164) 56(84) bytes of data.
      64 bytes from sfo07s13-in-f164.1e100.net (216.58.194.164): icmp_seq=1 ttl=113 time=5.06 ms
      64 bytes from sfo07s13-in-f164.1e100.net (216.58.194.164): icmp_seq=2 ttl=113 time=4.30 ms
      ^C
      --- www.google.com ping statistics ---
      2 packets transmitted, 2 received, 0% packet loss, time 1004ms
      rtt min/avg/max/mdev = 4.304/4.686/5.069/0.388 ms

How to Test VM to Pod Connectivity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In these instructions, VM connectivity to a pod is tested.

To test VM to pod connectivity:

1. Create a pod running Ubuntu.

   A small pod named ``ubuntuapp`` is created in this example.

   ::

      cat <<EOF > ubuntu.yaml
      apiVersion: v1
      kind: Pod
      metadata:
        name: ubuntuapp
        labels:
          app: ubuntuapp
      spec:
        containers:
          - name: ubuntuapp
            image: ubuntu-upstart
      EOF

      $ kubectl create -f ubuntu.yaml

      $ kubectl get pods
      NAME                              READY   STATUS    RESTARTS   AGE     IP              NODE                       NOMINATED NODE   READINESS GATES
      ubuntuapp                         1/1     Running   0          3h52m   10.254.255.89   worker1.ocp4.example.com   <none>           <none>
      virt-launcher-vmi-centos7-ttngl   2/2     Running   0          3h57m   10.254.255.90   worker0.ocp4.example.com   <none>           <none>

2. Create a service that allows the CentOS VM to use SSH through
   NodePort using Node IP for outside connectivity.

   ::

      cat <<EOF > kubevirt-centos-svc.yaml
      apiVersion: v1
      kind: Service
      metadata:
        name: vmi-centos-ssh-svc
        namespace: cnv-demo
      spec:
        ports:
        - name: centos-ssh-svc
          nodePort: 30000
          port: 27017
          protocol: TCP
          targetPort: 22
        selector:
          special: vmi-centos7
        type: NodePort
      EOF

      $ kubectl apply -f kubevirt-centos-svc.yaml

      $ kubectl get svc
      NAME                 TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)           AGE
      vmi-centos-ssh-svc   NodePort   172.30.115.77    <none>        27017:30000/TCP   4h2m

3. SSH to the CentOS VM with the NodePort service using an IP address of
   a worker node:

   ::

      $ ssh centos@192.168.7.11 -p 30000
      The authenticity of host '[192.168.7.11]:30000 ([192.168.7.11]:30000)' can't be established.
      ECDSA key fingerprint is SHA256:kk+9dbMqzpXDoPucnxiYozBgDt75IBSNS8Y4hUcEEmI.
      ECDSA key fingerprint is MD5:86:b6:e9:3b:f0:55:ee:e7:fd:56:96:c3:4a:c6:fd:e0.
      Are you sure you want to continue connecting (yes/no)? yes
      Warning: Permanently added '[192.168.7.11]:30000' (ECDSA) to the list of known hosts.
      centos@192.168.7.11's password:

      [centos@vmi-centos7 ~]$ uname -sr
      Linux 3.10.0-957.12.2.el7.x86_64

4. Confirm that the VM has access to the Internet:

   ::

      [centos@vmi-centos7 ~]$ ping www.google.com
      PING www.google.com (142.250.73.196) 56(84) bytes of data.
      64 bytes from iad23s87-in-f4.1e100.net (142.250.73.196): icmp_seq=1 ttl=108 time=13.1 ms
      64 bytes from iad23s87-in-f4.1e100.net (142.250.73.196): icmp_seq=2 ttl=108 time=11.9 ms
      ^C
      --- www.google.com ping statistics ---
      2 packets transmitted, 2 received, 0% packet loss, time 1003ms
      rtt min/avg/max/mdev = 11.990/12.547/13.104/0.557 ms

5. Ping the Ubuntu pod:

   ::

      [centos@vmi-centos7 ~]$ ping 10.254.255.89
      PING 10.254.255.89 (10.254.255.89) 56(84) bytes of data.
      64 bytes from 10.254.255.89: icmp_seq=1 ttl=63 time=3.83 ms
      64 bytes from 10.254.255.89: icmp_seq=2 ttl=63 time=2.26 ms
      ^C
      --- 10.254.255.89 ping statistics ---
      2 packets transmitted, 2 received, 0% packet loss, time 1003ms
      rtt min/avg/max/mdev = 2.263/3.047/3.831/0.784 ms

How to Create a Tungsten Fabric to Isolate a Virtual Machine Within a NameSpace
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After installing OpenShift Virtualization, you may need to isolate a
virtual machine within it’s namespace.

In the following procedure, a virtual machine is isolated in a namespace
by only allowing SSH for ingress connections and setting all egress
connections into ``podNetwork``.

To isolate a VM within it’s namespace:

1. Create a network security policy using the
   ``kubevirt-centos-netpol.yaml`` file, and apply the configuration
   file:

   ::

      cat <<EOF > kubevirt-centos-netpol.yaml
      apiVersion: networking.k8s.io/v1
      kind: NetworkPolicy
      metadata:
       name: netpol
       namespace: cnv-demo
      spec:
       podSelector:
         matchLabels:
          special: vmi-centos7
       policyTypes:
       - Ingress
       - Egress
       ingress:
       - from:
         ports:
         - port: 22
       egress:
       - to:
         - ipBlock:
             cidr: 10.254.255.0/16
      EOF

      $ oc apply -f kubevirt-centos-netpol.yaml
      networkpolicy.networking.k8s.io/netpol

2. Reconnect to the CentOS VM.

   Confirm connectivity to the Ubuntu pod by pinging the Ubuntu pod IP
   address.

   Confirm that connectivity to an internet site—in this example,
   \ `www.google.com <http://www.google.com>`__\ —is not possible.

   ::

      [root@helper ocp4]# ssh centos@192.168.7.11 -p 30000
      centos@192.168.7.11's password:
      [centos@vmi-centos7 ~]$ ping 10.254.255.89
      PING 10.254.255.89 (10.254.255.89) 56(84) bytes of data.
      64 bytes from 10.254.255.89: icmp_seq=1 ttl=63 time=2.58 ms
      64 bytes from 10.254.255.89: icmp_seq=2 ttl=63 time=2.39 ms
      ^C
      --- 10.254.255.89 ping statistics ---
      2 packets transmitted, 2 received, 0% packet loss, time 1003ms
      rtt min/avg/max/mdev = 2.394/2.490/2.587/0.108 ms

      [centos@vmi-centos7 ~]$ ping www.google.com
      ^C
      [centos@vmi-centos7 ~]$

How to Enable OpenShift Virtualization with KubeVirt in Environments Using OpenShift with a TF cluster
------------------------------------------------------------------------------------------------------------
KubeVirt is a virtualization add-on to Kubernetes that allows virtual
machines (VMs) to run alongside the application containers present in a
Kubernetes environment. KubeVirt provides a unified development platform
in Red Hat Openshift—called OpenShift Virtualization—where developers
can build, modify, and deploy applications residing in both application
containers and VMs within a common, shared environment. For additional
information on KubeVirt and it’s benefits, see the
`KubeVirt <https://kubevirt.io/>`__ homepage.

Starting in Tungsten Fabric Release 2011, Red Hat OpenShift
environments—which foundationally use Kubernetes orchestration—that
include TF clusters can support OpenShift Virtualization by
installing the KubeVirt add-on.
.. _when-to-use-this-procedure-1:

When to Use This Procedure
~~~~~~~~~~~~~~~~~~~~~~~~~~

A Kubernetes environment is containerized but might have to support VMs.
Common reasons for supporting VMs include maintaining VM-based workloads
that are challenging to containerize or to more gracefully migrate from
a VM-based environment to Kubernetes. Any environment that needs to
support VMs alongside Kubernetes containers can create an OpenShift
Virtualization environment using KubeVirt.

The procedure in this document was validated for Tungsten Fabric
2011.

.. _prerequisites-1:

Prerequisites
~~~~~~~~~~~~~

This procedure makes the following assumptions about your environment:

-  A Red Hat OpenShift 4.5 or later environment using Tungsten Fabric is operational.

-  Your installing a version of OpenShift Virtualization that is
   supported with your version of Red Hat OpenShift. For information on
   the OpenShift Virtualization versions supported with Red Hat
   OpenShift 4.5, see `About OpenShift
   Virtualization <https://docs.openshift.com/container-platform/4.5/virt/about-virt.html>`__
   from OpenShift.

How to Install OpenShift Virtualization using KubeVirt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To enable OpenShift Virtualization using KubeVirt in a Red Hat OpenShift
environment that is using Tungsten Fabric:

1. Install the OpenShift Virtualization operator:
 
   .. note:: 

      This procedure is based on the official OpenShift Virtualization
      documentation. If you need to reference the official procedure, see
      `Installing OpenShift Virtualization using the
      CLI <https://docs.openshift.com/container-platform/4.5/virt/install/installing-virt-cli.html>`__
      from OpenShift.

   1. Login as a user with ``cluster-admin`` privileges.

   2. Create a YAML file containing the following configuration:

      ::

         $ cat <<EOF > cnv.yaml
         apiVersion: v1
         kind: Namespace
         metadata:
           name: openshift-cnv
         ---
         apiVersion: operators.coreos.com/v1
         kind: OperatorGroup
         metadata:
           name: kubevirt-hyperconverged-group
           namespace: openshift-cnv
         spec:
           targetNamespaces:
             - openshift-cnv
         ---
         apiVersion: operators.coreos.com/v1alpha1
         kind: Subscription
         metadata:
           name: hco-operatorhub
           namespace: openshift-cnv
         spec:
           source: redhat-operators
           sourceNamespace: openshift-marketplace
           name: kubevirt-hyperconverged
           startingCSV: kubevirt-hyperconverged-operator.v2.4.1
           channel: "2.4"
         EOF

   3. Apply the YAML file.

      ::

         $ oc apply -f cnv.yaml

      A ``Namespace``, ``OperatorGroup``, and ``Subscription``—which are
      required elements for OpenShift Virtualization—are created when
      this YAML file is applied.

   4. Deploy the OpenShift Virtualization operator:

      1. Create the following YAML file:

         ::

            $ cat <<EOF > kubevirt-hyperconverged.yaml
            apiVersion: hco.kubevirt.io/v1alpha1
            kind: HyperConverged
            metadata:
              name: kubevirt-hyperconverged
              namespace: openshift-cnv
            spec:
              BareMetalPlatform: true
            EOF

      2. Apply the YAML file to deploy the operator:

         ::

            $ oc apply -f kubevirt-hyperconverged.yaml

      3. Confirm that the pods are running in the ``openshift-cnv``
         namespace:

         ::

            $ oc get pods -n openshift-cnv
            NAME                                                  READY   STATUS    RESTARTS   AGE
            bridge-marker-5tndk                                   1/1     Running   0          22h
            bridge-marker-d2gff                                   1/1     Running   0          22h
            bridge-marker-d8cgd                                   1/1     Running   0          22h
            bridge-marker-r6glh                                   1/1     Running   0          22h
            bridge-marker-rt5lb                                   1/1     Running   0          22h
            cdi-apiserver-7c4566c98c-z89qz                        1/1     Running   0          22h
            cdi-deployment-79fdcfdccb-xmphs                       1/1     Running   0          22h
            cdi-operator-7785b655bb-7q5k6                         1/1     Running   0          22h
            cdi-uploadproxy-5d4cc54b4c-g2ztz                      1/1     Running   0          22h
            cluster-network-addons-operator-67d7f76cbd-8kl6l      1/1     Running   0          22h
            hco-operator-854f5988c8-v2qbm                         1/1     Running   0          22h
            hostpath-provisioner-operator-595b955c9d-zxngg        1/1     Running   0          22h
            kube-cni-linux-bridge-plugin-5w67f                    1/1     Running   0          22h
            kube-cni-linux-bridge-plugin-kjm8b                    1/1     Running   0          22h
            kube-cni-linux-bridge-plugin-rgrn8                    1/1     Running   0          22h
            kube-cni-linux-bridge-plugin-s6xkz                    1/1     Running   0          22h
            kube-cni-linux-bridge-plugin-ssw29                    1/1     Running   0          22h
            kubemacpool-mac-controller-manager-6f9c447bbd-phd5n   1/1     Running   0          22h
            kubevirt-node-labeller-297nh                          1/1     Running   0          22h
            kubevirt-node-labeller-cbjnl                          1/1     Running   0          22h
            kubevirt-ssp-operator-75d54556b9-zq2kb                1/1     Running   0          22h
            nmstate-handler-9prp8                                 1/1     Running   1          22h
            nmstate-handler-dk4ht                                 1/1     Running   0          22h
            nmstate-handler-fzjmk                                 1/1     Running   0          22h
            nmstate-handler-rqwmq                                 1/1     Running   1          22h
            nmstate-handler-spx7w                                 1/1     Running   0          22h
            node-maintenance-operator-6486bcbfcd-rhn4l            1/1     Running   0          22h
            ovs-cni-amd64-4t9ld                                   1/1     Running   0          22h
            ovs-cni-amd64-5mdmq                                   1/1     Running   0          22h
            ovs-cni-amd64-bz5d9                                   1/1     Running   0          22h
            ovs-cni-amd64-h9j6j                                   1/1     Running   0          22h
            ovs-cni-amd64-k8hwf                                   1/1     Running   0          22h
            virt-api-7686f978db-ngwn2                             1/1     Running   0          22h
            virt-api-7686f978db-nkl4d                             1/1     Running   0          22h
            virt-controller-7d567db8c6-bbdjk                      1/1     Running   0          22h
            virt-controller-7d567db8c6-n2vgk                      1/1     Running   0          22h
            virt-handler-lkpsq                                    1/1     Running   0          5h30m
            virt-handler-vfcbd                                    1/1     Running   0          5h30m
            virt-operator-7995d994c4-9bxw9                        1/1     Running   0          22h
            virt-operator-7995d994c4-q8wnv                        1/1     Running   0          22h
            virt-template-validator-5d9bbfbcc7-g2zph              1/1     Running   0          22h
            virt-template-validator-5d9bbfbcc7-lhhrw              1/1     Running   0          22h
            vm-import-controller-58469cdfcf-kwkgb                 1/1     Running   0          22h
            vm-import-operator-9495bd74c-dkw2h                    1/1     Running   0          22h

      4. Confirm that the operator has succeeded.

         ::

            $ oc get csv -n openshift-cnv
            NAME                                      DISPLAY                    VERSION   REPLACES   PHASE
            kubevirt-hyperconverged-operator.v2.4.1   OpenShift Virtualization   2.4.1                Succeeded

      5. Add the ConfigMap to kubevirt-config:

         ::

            data:
              debug.useEmulation: "true"

            $ oc edit cm kubevirt-config -n openshift-cnv

            apiVersion: v1
            kind: ConfigMap
            metadata:
              name: kubevirt-config
              namespace: openshift-cnv
            data:
              debug.useEmulation: "true"

         Restart the ``virt-handler`` pods to complete the configuration
         update.

How to Create a Virtual Machine Using OpenShift Virtualization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

OpenShift Virtualization was installed because your environment needed
to support virtual machines. You can use the Virtual Machine Instance
(VMI) custom resource to create virtual machines that are fully
integrated into Red Hat OpenShift.

To create a virtual machine after installing OpenShift Virtualization:

1. Create a new project with it’s own namespace for the virtual machine:

   ::

      $ oc new-project cnv-demo

2. Create a virtual machine apply the configuration:

   In this sample configuration, a virtual machine running CentOS 7 is
   created using the kubevirt-centos.yaml file.

   ::

      cat <<EOF > kubevirt-centos.yaml
      apiVersion: kubevirt.io/v1alpha3
      kind: VirtualMachineInstance
      metadata:
        labels:
          special: vmi-centos7
        name: vmi-centos7
        namespace: cnv-demo
      spec:
        domain:
          devices:
            disks:
            - disk:
                bus: virtio
              name: containerdisk
            - disk:
                bus: virtio
              name: cloudinitdisk
            interfaces:
            - name: default
              bridge: {}
          resources:
            requests:
              memory: 1024M
        networks:
        - name: default
          pod: {}
        volumes:
        - containerDisk:
            image: ovaleanu/centos:latest
          name: containerdisk
        - cloudInitNoCloud:
            userData: |-
              #cloud-config
              password: centos
              ssh_pwauth: True
              chpasswd: { expire: False }
          name: cloudinitdisk
      EOF

      $ oc apply -f kubevirt-centos.yaml
      virtualmachineinstance.kubevirt.io/vmi-centos7 created

3. Confirm that the pod and the VM instance were created:

   ::

      $ oc get pods
      NAME                              READY   STATUS    RESTARTS   AGE     IP              NODE                       NOMINATED NODE   READINESS GATES
      virt-launcher-vmi-centos7-ttngl   2/2     Running   0          3h57m   10.254.255.90   worker0.ocp4.example.com   <none>           <none>

      $ oc get vmi
      NAME          AGE    PHASE     IP                 NODENAME
      vmi-centos7   4h1m   Running   10.254.255.90/16   worker0.ocp4.example.com

.. _how-to-test-vm-to-pod-connectivity-1:

How to Test VM to Pod Connectivity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In these instructions, VM connectivity to a pod is tested.

To test VM to pod connectivity:

1. Create a pod running Ubuntu.

   A small pod named ``ubuntuapp`` is created in this example.

   ::

      cat <<EOF > ubuntu.yaml
      apiVersion: v1
      kind: Pod
      metadata:
        name: ubuntuapp
        labels:
          app: ubuntuapp
      spec:
        containers:
          - name: ubuntuapp
            image: ubuntu-upstart
      EOF

      $ oc create -f ubuntu.yaml

      $ oc get pods
      NAME                              READY   STATUS    RESTARTS   AGE     IP              NODE                       NOMINATED NODE   READINESS GATES
      ubuntuapp                         1/1     Running   0          3h52m   10.254.255.89   worker1.ocp4.example.com   <none>           <none>
      virt-launcher-vmi-centos7-ttngl   2/2     Running   0          3h57m   10.254.255.90   worker0.ocp4.example.com   <none>           <none>

2. Create a service that allows the CentOS VM to use SSH through
   NodePort using Node IP for outside connectivity.

   ::

      cat <<EOF > kubevirt-centos-svc.yaml
      apiVersion: v1
      kind: Service
      metadata:
        name: vmi-centos-ssh-svc
        namespace: cnv-demo
      spec:
        ports:
        - name: centos-ssh-svc
          nodePort: 30000
          port: 27017
          protocol: TCP
          targetPort: 22
        selector:
          special: vmi-centos7
        type: NodePort
      EOF

      $ oc apply -f kubevirt-centos-svc.yaml

      $ oc get svc
      NAME                 TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)           AGE
      vmi-centos-ssh-svc   NodePort   172.30.115.77    <none>        27017:30000/TCP   4h2m

3. SSH to the CentOS VM with the NodePort service using an IP address of
   a worker node:

   ::

      $ ssh centos@192.168.7.11 -p 30000
      The authenticity of host '[192.168.7.11]:30000 ([192.168.7.11]:30000)' can't be established.
      ECDSA key fingerprint is SHA256:kk+9dbMqzpXDoPucnxiYozBgDt75IBSNS8Y4hUcEEmI.
      ECDSA key fingerprint is MD5:86:b6:e9:3b:f0:55:ee:e7:fd:56:96:c3:4a:c6:fd:e0.
      Are you sure you want to continue connecting (yes/no)? yes
      Warning: Permanently added '[192.168.7.11]:30000' (ECDSA) to the list of known hosts.
      centos@192.168.7.11's password:

      [centos@vmi-centos7 ~]$ uname -sr
      Linux 3.10.0-957.12.2.el7.x86_64

4. Confirm that the VM has access to the Internet:

   ::

      [centos@vmi-centos7 ~]$ ping www.google.com
      PING www.google.com (142.250.73.196) 56(84) bytes of data.
      64 bytes from iad23s87-in-f4.1e100.net (142.250.73.196): icmp_seq=1 ttl=108 time=13.1 ms
      64 bytes from iad23s87-in-f4.1e100.net (142.250.73.196): icmp_seq=2 ttl=108 time=11.9 ms
      ^C
      --- www.google.com ping statistics ---
      2 packets transmitted, 2 received, 0% packet loss, time 1003ms
      rtt min/avg/max/mdev = 11.990/12.547/13.104/0.557 ms

5. Ping the Ubuntu pod:

   ::

      [centos@vmi-centos7 ~]$ ping 10.254.255.89
      PING 10.254.255.89 (10.254.255.89) 56(84) bytes of data.
      64 bytes from 10.254.255.89: icmp_seq=1 ttl=63 time=3.83 ms
      64 bytes from 10.254.255.89: icmp_seq=2 ttl=63 time=2.26 ms
      ^C
      --- 10.254.255.89 ping statistics ---
      2 packets transmitted, 2 received, 0% packet loss, time 1003ms
      rtt min/avg/max/mdev = 2.263/3.047/3.831/0.784 ms

.. _how-to-create-a-tf-security-policy-to-isolate-a-virtual-machine-within-a-namespace-1:

How to Create a Tungsten Fabric to Isolate a Virtual Machine Within a NameSpace
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After installing OpenShift Virtualization, you may need to isolate a
virtual machine within it’s namespace.

In the following procedure, a virtual machine is isolated in a namespace
by only allowing SSH for ingress connections and setting all egress
connections into ``podNetwork``.

To isolate a VM within it’s namespace:

1. Create a network security policy using the
   ``kubevirt-centos-netpol.yaml`` file, and apply the configuration
   file:

   ::

      cat <<EOF > kubevirt-centos-netpol.yaml
      apiVersion: networking.k8s.io/v1
      kind: NetworkPolicy
      metadata:
       name: netpol
       namespace: cnv-demo
      spec:
       podSelector:
         matchLabels:
          special: vmi-centos7
       policyTypes:
       - Ingress
       - Egress
       ingress:
       - from:
         ports:
         - port: 22
       egress:
       - to:
         - ipBlock:
             cidr: 10.254.255.0/16
      EOF

      $ oc apply -f kubevirt-centos-netpol.yaml
      networkpolicy.networking.k8s.io/netpol

2. Reconnect to the CentOS VM.

   Confirm connectivity to the Ubuntu pod by pinging the Ubuntu pod IP
   address.

   Confirm that connectivity to an internet site—in this example,
   \ `www.google.com <http://www.google.com>`__\ —is not possible.

   ::

      [root@helper ocp4]# ssh centos@192.168.7.11 -p 30000
      centos@192.168.7.11's password:
      [centos@vmi-centos7 ~]$ ping 10.254.255.89
      PING 10.254.255.89 (10.254.255.89) 56(84) bytes of data.
      64 bytes from 10.254.255.89: icmp_seq=1 ttl=63 time=2.58 ms
      64 bytes from 10.254.255.89: icmp_seq=2 ttl=63 time=2.39 ms
      ^C
      --- 10.254.255.89 ping statistics ---
      2 packets transmitted, 2 received, 0% packet loss, time 1003ms
      rtt min/avg/max/mdev = 2.394/2.490/2.587/0.108 ms

      [centos@vmi-centos7 ~]$ ping www.google.com
      ^C
      [centos@vmi-centos7 ~]$

How to Create a Virtual Machine with Multiple Interfaces
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can configure a virtual machine with multiple interfaces into
multiple virtual networks when using Tungsten Fabric as the CNI in a
Kubernetes environment.

In the following procedure, a virtual machine uses different interfaces
to connect into two virtual networks, ``neta`` and ``netb``.

To configure a virtual machine with multiple interfaces:

1. Create the virtual networks.

   In this example, two virtual networks—``neta`` and ``netb``—are
   created using the ``netab.yaml`` file.

   ::

      $ cat <<EOF > netab.yaml
      apiVersion: "k8s.cni.cncf.io/v1"
      kind: NetworkAttachmentDefinition
      metadata:
       name: neta
       annotations: {
         "opencontrail.org/cidr" : "10.10.10.0/24",
         "opencontrail.org/ip_fabric_snat": "true"
        }
      spec:
       config: '{
         "cniVersion": "0.3.1",
         "type": "contrail-k8s-cni"
      }'

      ---
      apiVersion: "k8s.cni.cncf.io/v1"
      kind: NetworkAttachmentDefinition
      metadata:
       name: netb
       annotations: {
         "opencontrail.org/cidr" : "20.20.20.0/24",
         "opencontrail.org/ip_fabric_snat": "true"
        }
      spec:
       config: '{
         "cniVersion": "0.3.1",
         "type": "contrail-k8s-cni"
      }'
      EOF

      $ oc apply -f netab.yaml

2. Create a virtual machine with interfaces in multiple virtual
   networks.

   In this example, a virtual machine named ``vmi-fedora`` is created
   with interfaces in both of the virtual networks—``neta`` and
   ``netb``— that were created earlier in this procedure.

   ::

      cat <<EOF > kubevirt-fedora.yaml
      apiVersion: kubevirt.io/v1alpha3
      kind: VirtualMachineInstance
      metadata:
        labels:
          special: vmi-fedora
        name: vmi-fedora
      spec:
        domain:
          devices:
            disks:
            - disk:
                bus: virtio
              name: containerdisk
            - disk:
                bus: virtio
              name: cloudinitdisk
            interfaces:
            - name: default
              bridge: {}
            - name: neta
              bridge: {}
            - name: netb
              bridge: {}
          resources:
            requests:
              memory: 1024M
        networks:
        - name: default
          pod: {}
        - name: neta
          multus:
            networkName: neta
        - name: netb
          multus:
            networkName: netb
        volumes:
        - containerDisk:
            image: kubevirt/fedora-cloud-registry-disk-demo
          name: containerdisk
        - cloudInitNoCloud:
            userData: |-
              #cloud-config
              password: fedora
              ssh_pwauth: True
              chpasswd: { expire: False }
          name: cloudinitdisk
      EOF

      $ oc apply -f kubevirt-fedora.yaml

3. Confirm that the pod and the VM instances were created.

   ::

      $ oc get pods
      NAME                              READY   STATUS    RESTARTS   AGE
      ubuntuapp                         1/1     Running   0          5h11m
      virt-launcher-vmi-centos7-ttngl   2/2     Running   0          5h16m
      virt-launcher-vmi-fedora-czwhx    2/2     Running   0          102m

      $ oc get vmi
      NAME          AGE     PHASE     IP                 NODENAME
      vmi-centos7   5h17m   Running   10.254.255.90/16   worker0.ocp4.example.com
      vmi-fedora    103m    Running   10.254.255.88      worker1.ocp4.example.com

4. Create a service to connect the VM with SSH using Nodeport. Confirm
   that the service was created and is being used by the VM.

   ::

      cat <<EOF > kubevirt-fedora-svc.yaml
      apiVersion: v1
      kind: Service
      metadata:
        name: vmi-fedora-ssh-svc
        namespace: cnv-demo
      spec:
        ports:
        - name: fedora-ssh-svc
          nodePort: 31000
          port: 25025
          protocol: TCP
          targetPort: 22
        selector:
          special: vmi-fedora
        type: NodePort
      EOF

      $ oc apply -f kubevirt-fedora-svc.yaml
      service/vmi-fedora-ssh-svc created

      $ oc get svc -n cnv-demo
      NAME                 TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)           AGE
      vmi-centos-ssh-svc   NodePort   172.30.115.77    <none>        27017:30000/TCP   5h16m
      vmi-fedora-ssh-svc   NodePort   172.30.247.145   <none>        25025:31000/TCP   98m

5. Connect to the Fedora VM with SSH using a worker node IP address,
   then manually enable the network interfaces in the custom ``neta``
   and ``netb`` virtual networks.

   ::

      $ ssh fedora@192.168.7.12 -p 31000
      The authenticity of host '[192.168.7.12]:31000 ([192.168.7.12]:31000)' can't be established.
      ECDSA key fingerprint is SHA256:JlhysyH0XiHXszLLqu8GmuSHB4msOYWPAJjZhv5j3FM.
      ECDSA key fingerprint is MD5:62:ca:0b:b9:21:c9:2b:73:db:b6:09:e2:b0:b4:81:60.
      Are you sure you want to continue connecting (yes/no)? yes
      Warning: Permanently added '[192.168.7.12]:31000' (ECDSA) to the list of known hosts.
      fedora@192.168.7.12's password:

      [fedora@vmi-fedora ~]$ uname -sr
      Linux 4.13.9-300.fc27.x86_64

      [fedora@vmi-fedora ~]$ cat /etc/sysconfig/network-scripts/ifcfg-eth0
      # Created by cloud-init on instance boot automatically, do not edit.
      #
      BOOTPROTO=dhcp
      DEVICE=eth0
      HWADDR=02:dd:00:37:08:0d
      ONBOOT=yes
      TYPE=Ethernet
      USERCTL=no

      [fedora@vmi-fedora ~]$ cat /etc/sysconfig/network-scripts/ifcfg-eth1
      # Created by cloud-init on instance boot automatically, do not edit.
      #
      BOOTPROTO=dhcp
      DEVICE=eth1
      HWADDR=02:dd:3a:e6:dc:0d
      ONBOOT=yes
      TYPE=Ethernet
      USERCTL=no

      [fedora@vmi-fedora ~]$ cat /etc/sysconfig/network-scripts/ifcfg-eth2
      # Created by cloud-init on instance boot automatically, do not edit.
      #
      BOOTPROTO=dhcp
      DEVICE=eth2
      HWADDR=02:dd:71:6e:fa:0d
      ONBOOT=yes
      TYPE=Ethernet
      USERCTL=no

      $ sudo systemctl restart network

      [fedora@vmi-fedora ~]$ ip a
      1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
          link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
          inet 127.0.0.1/8 scope host lo
             valid_lft forever preferred_lft forever
          inet6 ::1/128 scope host
             valid_lft forever preferred_lft forever
      2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
          link/ether 02:dd:00:37:08:0d brd ff:ff:ff:ff:ff:ff
          inet 10.254.255.88/16 brd 10.254.255.255 scope global dynamic eth0
             valid_lft 86307318sec preferred_lft 86307318sec
          inet6 fe80::dd:ff:fe37:80d/64 scope link
             valid_lft forever preferred_lft forever
      3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
          link/ether 02:dd:3a:e6:dc:0d brd ff:ff:ff:ff:ff:ff
          inet 10.10.10.252/24 brd 10.10.10.255 scope global dynamic eth1
             valid_lft 86307327sec preferred_lft 86307327sec
          inet6 fe80::dd:3aff:fee6:dc0d/64 scope link
             valid_lft forever preferred_lft forever
      4: eth2: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
          link/ether 02:dd:71:6e:fa:0d brd ff:ff:ff:ff:ff:ff
          inet 20.20.20.252/24 brd 20.20.20.255 scope global dynamic eth2
             valid_lft 86307336sec preferred_lft 86307336sec
          inet6 fe80::dd:71ff:fe6e:fa0d/64 scope link
             valid_lft forever preferred_lft forever

 
