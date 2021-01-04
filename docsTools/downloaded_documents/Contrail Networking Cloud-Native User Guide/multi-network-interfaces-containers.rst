Multiple Network Interfaces for Containers
==========================================

 

Starting in Release 4.0, Contrail provides networking support for
containers using Kubernetes Orchestration. You can allocate a network
interface to every container that you create using standard Container
Networking Interface (CNI plugin). For more information on Contrail
Containers Networking, see `Contrail Integration with
Kubernetes <../../concept/kubernetes-cni-contrail.html>`__.

Starting in Contrail Release 5.1, you can allocate multiple network
interfaces (multi-net) to a container to enable the container to connect
to multiple networks. You can specify the networks the container can
connect to. A network interface is either a physical interface or a
virtual interface and is connected to the Linux network namespace. A
network namespace is the network stack in the Linux kernel. More than
one container can share the same network namespace.

Contrail multi-net support is based on the Kubernetes multi-net model.
Kubernetes multi-net model has a specific design and construct, and can
be extended to non-kubernetes models like Contrail multi-net. Contrail
multi-net model does not require changes to the Kubernetes API and
Kubernetes CNI driver. Contrail multi-net model, as in the case of
Kubernetes multi-net model, does not change the existing cluster-wide
network behavior.

The following limitations and caveats apply when you create multi-net
interfaces:

-  You cannot add or remove sidecar networks while the pod is still
   running.

-  The administrator is responsible for removing corresponding Contrail
   pods before deleting the network attachment definition from the
   Kubernetes API server.

-  Contrail creates a default cluster-wide-network in addition to custom
   networks.

-  Contrail CNI plugin is not a delegating plugin. It does not support
   specifications for delegating plugins that are provided in the
   Kubernetes Network Custom Resource Definition De Facto Standard
   Version 1. For more information, view
   ``[v1] Kubernetes Network Custom Resource Definition De-facto Standard.md``
   from the https://github.com/K8sNetworkPlumbingWG/multi-net-spec page.

Creating Multi-Net Interfaces

Follow these steps to create multi-net interfaces.

1. Create Network Object Model.

   You create the network object model if the cluster does not support
   the model.

   The object model of the container orchestration platform represents
   the network and attaches the network to a container. If the model
   does not support network objects by default, you can use extensions
   to represent the network.

   .. raw:: html

      <div id="jd0e60" class="sample" dir="ltr">

   **Creating Network Object Model by using Kubernetes
   NetworkAttachmentDefinition CRD object**

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      apiVersion: apiextensions.k8s.io/v1beta1
      kind: CustomResourceDefinition
      metadata:
        # name must match the spec fields below, and be in the form: <plural>.<group>
        name: network-attachment-definitions.k8s.cni.cncf.io
      spec:
        # group name to use for REST API: /apis/<group>/<version>
        group: k8s.cni.cncf.io
        # version name to use for REST API: /apis/<group>/<version>
        version: v1
        # either Namespaced or Cluster
        scope: Namespaced
        names:
          # plural name to be used in the URL: /apis/<group>/<version>/<plural>
          plural: network-attachment-definitions
          # singular name to be used as an alias on the CLI and for display
          singular: network-attachment-definition
          # kind is normally the CamelCased singular type. Your resource manifests use this.
          kind: NetworkAttachmentDefinition
          # shortNames allow shorter string to match your resource on the CLI
          shortNames:
          - net-attach-def
        validation:
          openAPIV3Schema:
            properties:
              spec:
                properties:
                  config:
                    type: string

   .. raw:: html

      </div>

   .. raw:: html

      </div>

   Kubernetes uses custom extensions to represent networks in its object
   model. CustomResourceDefinition(CRD) feature of Kubernetes helps
   support custom extensions.

   **Note**

   A CRD is created automatically when you install Contrail. Networks
   specified by CRD are sidecars that are not recognized by Kubernetes.
   The interaction of additional pod network attachments with Kubernetes
   API and its objects, such as services, endpoints, proxies, etc. are
   not specified. Kubernetes does not recognize the association of these
   objects to any pod.

2. Create networks.

   You create networks in the cluster:

   -  Through the API server.

      .. raw:: html

         <div id="jd0e79" class="sample" dir="ltr">

      .. raw:: html

         <div class="output" dir="ltr">

      ::

         apiVersion: k8s.cni.cncf.io/v1
         kind: NetworkAttachmentDefinition
         metadata:
           annotations:
             opencontrail.org/cidr: "<ip address>/24"
             opencontrail.org/ip_fabric_forwarding: "false"
             opencontrail.org/ip_fabric_snat: "false"
           name: right-network
           namespace: default
         spec:
           config: '{ "cniVersion": "0.3.0", "type": "contrail-k8s-cni" }' 

      .. raw:: html

         </div>

      .. raw:: html

         </div>

      Create a ``right-network.yaml`` file.

   -  By mapping to an existing network created from the Contrail Web
      user interface or from the Contrail Command user interface.

      .. raw:: html

         <div id="jd0e93" class="sample" dir="ltr">

      .. raw:: html

         <div class="output" dir="ltr">

      ::

         apiVersion: "k8s.cni.cncf.io/v1"
         kind: NetworkAttachmentDefinition
         metadata:
           name: extns-network
           annotations:
             "opencontrail.org/network" : '{"domain":"default-domain", "project": "k8s-extns", "name":"k8s-extns-pod-network"}'
         spec:
           config: '{
             "cniVersion": "0.3.1",
             "type": "contrail-k8s-cni"
         }'

      .. raw:: html

         </div>

      .. raw:: html

         </div>

   Command to create the network:

   .. raw:: html

      <div id="jd0e98" class="sample" dir="ltr">

   .. raw:: html

      <div id="jd0e99" dir="ltr">

   ``kubectl apply -f right-network.yaml``

   .. raw:: html

      </div>

   .. raw:: html

      </div>

3. Assign networks to pods.

   You assign the networks that you created in Step
   `2 <multi-network-interfaces-containers.html#step-2>`__ to pods. Each
   pod also has a default network assigned to it. Therefore, each pod
   will have the following networks assigned:

   -  default network (assigned by Kubernetes)

      **Note**

      Contrail internally creates a default network called
      ``cluster-wide-network``. This interface is the default interface
      for the pod

   -  network that you created in Step
      `2 <multi-network-interfaces-containers.html#step-2>`__

   Assigning networks to pods by using *k8s-semantics*:

   Option 1

   .. raw:: html

      <div id="jd0e131" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      apiVersion: v1
      kind: Pod
      metadata:
        name: multiNetworkPod
        annotations:
          k8s.v1.cni.cncf.io/networks: '[
            { "name": "network-a" },
            { "name": "network-b" }
          ]'
      spec:
        containers:
        - image: busybox
          command:
            - sleep
            - "3600"
          imagePullPolicy: IfNotPresent
          name: busybox
          stdin: true
          tty: true
        restartPolicy: Always

   .. raw:: html

      </div>

   .. raw:: html

      </div>

   Option 2

   .. raw:: html

      <div id="jd0e137" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      apiVersion: v1
      kind: Pod
      metadata:
        name: ubuntu-pod-3
        annotations:
          k8s.v1.cni.cncf.io/networks: left-network,blue-network,right-network,extns/data-network
      spec:
        containers:
        - name: ubuntuapp
          image: ubuntu-upstart
          securityContext:
            capabilities:
              add:
              - NET_ADMIN

   .. raw:: html

      </div>

   .. raw:: html

      </div>

 
