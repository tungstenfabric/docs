Contrail Integration with Kubernetes
====================================

 

.. raw:: html

   <div id="intro">

.. raw:: html

   <div class="mini-toc-intro">

Starting in Release 4.0, Contrail supports the Container Network
Interface (CNI) for integrating Contrail with the Kubernetes automation
platform.

.. raw:: html

   </div>

.. raw:: html

   </div>

What is Kubernetes?
-------------------

Kubernetes, also called K8s, is an open source platform for automating
deployment, scaling, and operations of application containers across
clusters of hosts, providing container-centric infrastructure. It
provides a portable platform across public and private clouds.
Kubernetes supports deployment, scaling, and auto-healing of
applications.

Kubernetes supports a pluggable framework called Container Network
Interface (CNI) for most of the basic network connectivity, including
container pod addressing, network isolation, policy-based security, a
gateway, SNAT, load-balancer, and service chaining capability for
Kubernetes orchestration. Contrail Release 4.0 provides support for CNI
for Kubernetes.

Kubernetes provides a flat networking model in which all container pods
can talk to each other. Network policy is added to provide security
between the pods. Contrail integrated with Kubernetes adds additional
networking functionality, including multi-tenancy, network isolation,
micro-segmentation with network policies, load-balancing, and more.

`Table 1 <kubernetes-cni-contrail.html#k8s-contrail>`__ lists the
mapping between Kubernetes concepts and Tungsten Fabric resources.

Table 1: Kubernetes to Tungsten Fabric Mapping

============== ===================================================
Kubernetes     Tungsten Fabric Resources
Namespace      Shared or single project
Pod            Virtual-machine, Interface, Instance-ip
Service        ECMP-based native Loadbalancer
Ingress        HAProxy-based L7 Loadbalancer for URL routing
Network policy Security group based on namespace and pod selectors
============== ===================================================

What is a Kubernetes Pod?
~~~~~~~~~~~~~~~~~~~~~~~~~

A Kubernetes pod is a group of one or more containers (such as Docker
containers), the shared storage for those containers, and options on how
to run the containers. Pods are always co-located and co-scheduled, and
run in a shared context. The shared context of a pod is a set of Linux
namespaces, cgroups, and other facets of isolation. Within the context
of a pod, individual applications might have further sub-isolations
applied.

You can find more information about Kubernetes at:
http://kubernetes.io/docs/whatisk8s/.

Configuration Modes for Contrail Integrated with Kubernetes
-----------------------------------------------------------

.. raw:: html

   <div class="mini-toc-intro">

Contrail can be configured in several different modes in Kubernetes.
This section describes the various configuration modes.

.. raw:: html

   </div>

-  `Default Mode <kubernetes-cni-contrail.html#jd0e93>`__

-  `Namespace Isolation Mode <kubernetes-cni-contrail.html#jd0e103>`__

-  `Custom Isolation Mode <kubernetes-cni-contrail.html#jd0e188>`__

-  `Nested Mode <kubernetes-cni-contrail.html#jd0e201>`__

Default Mode
~~~~~~~~~~~~

In Kubernetes, all pods can communicate with all other pods without
using network address translation (NAT). This is the default mode of
Contrail Kubernetes cluster. In the default mode, Contrail creates a
virtual-network that is shared by all namespaces, from which service and
pod IP addresses are allocated.

All pods in all namespaces that are spawned in the Kubernetes cluster
are able to communicate with one another. The IP addresses for all of
the pods are allocated from a pod subnet that is configured in the
Contrail Kubernetes manager.

**Note**

System pods that are spawned in the kube-system namespace are not run in
the Kubernetes cluster; they run in the underlay, and networking for
these pods is not handled by Contrail.

Namespace Isolation Mode
~~~~~~~~~~~~~~~~~~~~~~~~

In addition to the default networking model mandated by Kubernetes,
Contrail supports additional custom networking models that make
available the many rich features of Contrail to the users of the
Kubernetes cluster. One such feature is network isolation for Kubernetes
namespaces.

For namespace isolation mode, the cluster administrator can configure a
namespace annotation to turn on isolation. As a result, services in that
namespace are not accessible from other namespaces, unless security
groups or network policies are explicitly defined to allow access.

A Kubernetes namespace can be configured as isolated by annotating the
Kubernetes namespace metadata:

``opencontrail.org/isolation : true``

Namespace isolation provides network isolation to pods, because the pods
in isolated namespaces are not reachable to pods in other namespaces in
the cluster.

Namespace isolation also provides service isolation to pods. If any
Kubernetes service is implemented by pods in an isolated namespace,
those pods are reachable only to pods in the same namespace through the
Kubernetes service-ip.

To make services remain reachable to other namespaces, service isolation
can be disabled by the following additional annotation on the namespace:

``opencontrail.org/isolation.service : false``

Disabling service isolation makes the services reachable to pods in
other namespaces, however pods in isolated namespaces still remain
unreachable to pods in other namespaces.

A namespace annotated as “isolated” for both pod and service isolation
has the following network behavior:

-  All pods created in an isolated namespace have network reachability
   with each other.

-  Pods in other namespaces in the Kubernetes cluster *cannot* reach
   pods in the isolated namespace.

-  Pods created in isolated namespaces *can* reach pods in non-isolated
   namespaces.

-  Pods in isolated namespaces *can* reach non-isolated services in any
   namespace in the Kubernetes cluster.

-  Pods from other namespaces *cannot* reach services in isolated
   namespaces.

A namespace annotated as “isolated”, with service-isolation disabled and
only pod isolation enabled, has the following network behavior:

-  All pods created in an isolated namespace have network reachability
   with each other.

-  Pods in other namespaces in the Kubernetes cluster *cannot* reach
   pods in the isolated namespace.

-  Pods created in isolated namespaces *can* reach pods in other
   namespaces.

-  Pods in isolated namespaces *can* reach non-isolated services in any
   namespace in the Kubernetes cluster.

-  Pods from other namespaces *can* reach services in isolated
   namespaces.

Custom Isolation Mode
~~~~~~~~~~~~~~~~~~~~~

Administrators and application developers can add annotations to specify
the virtual network in which a pod or all pods in a namespace are to be
provisioned. The annotation to specify this custom virtual network is:

``"opencontrail.org/network: <fq_network_name>"``

If this annotation is configured on a pod spec then the pod is launched
in that network. If the annotation is configured in the namespace spec
then all the pods in the namespace are launched in the provided network.

**Note**

The virtual network must be created using Contrail VNC APIs or
Contrail-UI prior to configuring it in the pod or namespace spec.

Nested Mode
~~~~~~~~~~~

Contrail supports the provisioning of Kubernetes cluster inside an
OpenStack cluster. While this nesting of clusters by itself is not
unique, Contrail provides a *collapsed* control and data plane in which
a single Contrail control plane and a single network stack manage and
service both the OpenStack and Kubernetes clusters. With unified control
and data planes, interworking and configuring these clusters is
seamless, and the lack of replication and duplicity makes this a very
efficient option.

In nested mode, a Kubernetes cluster is provisioned in the virtual
machine of an OpenStack cluster. The CNI-plugin and the
Contrail-kubernetes manager of the Kubernetes cluster interface directly
with Contrail components that manage the OpenStack cluster.

In a nested-mode deployment, all Kubernetes features, functions, and
specifications are supported as is. Nested deployment stretches the
boundaries and limits of Kubernetes by allowing it to operate on the
same plane as underlying OpenStack cluster.

For more information, see `Provisioning of Kubernetes
Clusters <../task/installation/provisioning-k8s-cluster.html>`__.

Kubernetes Services
-------------------

A Kubernetes service is an abstraction that defines a logical set of
pods and the policy used to access the pods. The set of pods
implementing a service are selected based on the **LabelSelector** field
in the service definition. In Contrail, a Kubernetes service is
implemented as an ECMP-native load-balancer.

The Contrail Kubernetes integration supports the following
**ServiceType**\ s:

-  **\`clusterIP\`**: This is the default mode. Choosing this
   **ServiceType** makes the service reachable through the cluster
   network.

-  **\`LoadBalancer\`**: Designating a **ServiceType** as
   **\`LoadBalancer\`** enables the service to be accessed externally.
   The **\`LoadBalancer\` \_Service\_** is assigned both CluserIP and
   ExternalIP addresses. This **ServiceType** assumes that the user has
   configured the public network with a floating-ip pool.

Contrail Kubernetes Service-integration supports TCP and UDP for
protocols. Also, Service can expose more than one port where port and
targetPort are different. For example:

.. raw:: html

   <div id="jd0e259" class="example" dir="ltr">

::

   kind: Service
   apiVersion: v1
   metadata:
     name: my-service
   spec:
       selector:
         app: MyApp
       ports:
         - name: http
           protocol: TCP
           port: 80
           targetPort: 9376
         - name: https
           protocol: TCP
           port: 443
           targetPort: 9377

.. raw:: html

   </div>

Kubernetes users can specify spec.clusterIP and spec.externalIPs for
both **LoadBalancer** and **clusterIP ServiceType**\ s.

If **ServiceType** is **LoadBalancer** and no spec.externalIP is
specified by the user, then contrail-kube-manager allocates a
floating-ip from the public pool and associates it to the ExternalIP
address.

Ingress
-------

Kubernetes services can be exposed externally or exposed outside of the
cluster in many ways. See
https://kubernetes.io/docs/concepts/services-networking/ingress/#alternatives
for a list of all methods of exposing Kubernetes services externally.
Ingress is one such method. Ingress provides Layer 7 load-balancing
whereas the other methods provide Layer 4 load-balancing. Contrail
supports http-based single-service ingress, simple-fanout ingress, and
name-based virtual hosting ingress.

Contrail Kubernetes Solution
----------------------------

.. raw:: html

   <div class="mini-toc-intro">

Contrail Kubernetes solution includes the following elements.

.. raw:: html

   </div>

-  `Contrail Kubernetes
   Manager <kubernetes-cni-contrail.html#jd0e295>`__

-  `ECMP Load-Balancers for Kubernetes
   Services <kubernetes-cni-contrail.html#jd0e302>`__

-  `HAProxy Loadbalancer for Kubernetes
   Ingress <kubernetes-cni-contrail.html#jd0e309>`__

-  `Security Groups for Kubernetes Network
   Policy <kubernetes-cni-contrail.html#jd0e318>`__

-  `Kubernetes Support for Security
   Policy <kubernetes-cni-contrail.html#jd0e333>`__

-  `Domain Name Server (DNS) <kubernetes-cni-contrail.html#jd0e338>`__

-  `Supported Kubernetes
   Annotations <kubernetes-cni-contrail.html#jd0e343>`__

Contrail Kubernetes Manager
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Contrail Kubernetes implementation requires listening to the
Kubernetes API messages and creating corresponding resources in the
Contrail API database.

A new module, contrail-kube-manager, runs in a Docker container to
listen to the messages from the Kubernetes API server.

ECMP Load-Balancers for Kubernetes Services
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each service in Kubernetes is represented by a load-balancer object. The
service IP allocated by Kubernetes is used as the VIP for the
load-balancer. Listeners are created for the port on which the service
is listening. Each pod is added as a member of the listener pool. The
contrail-kube-manager listens for any changes based on service labels or
pod labels, and updates the member pool list with any added, updated, or
deleted pods.

Load-balancing for services is Layer 4 native, non-proxy load-balancing
based on ECMP. The instance-ip (service-ip) is linked to the ports of
each of the pods in the service. This creates an ECMP next-hop in
Contrail and traffic is load-balanced directly from the source pod.

HAProxy Loadbalancer for Kubernetes Ingress
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Kubernetes Ingress is implemented through the HAProxy load-balancer
feature in Contrail. Whenever ingress is configured in Kubernetes,
contrail-kube-manager creates the load-balancer object in
contrail-controller. The Contrail service monitor listens for the
load-balancer objects and launches the HAProxy with appropriate
configuration, based on the ingress specification rules in
active-standby mode.

See `Using Load Balancers in
Contrail <../task/configuration/lbaas-contrail3-F5.html>`__ for more
information on load balancers.

Security Groups for Kubernetes Network Policy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Kubernetes network policy is a specification of how groups of pods are
allowed to communicate with each other and other network endpoints.
**NetworkPolicy** resources use labels to select pods and define allow
list rules which allow traffic to the selected pods in addition to what
is allowed by the isolation policy for a given namespace.

For more information about Kubernetes network policies, see
https://kubernetes.io/docs/concepts/services-networking/networkpolicies/.

The contrail-kube-manager listens to the Kubernetes network policy
events for create, update, and delete, and translates the Kubernetes
network policy to Contrail security group objects applied to virtual
machine interfaces (VMIs). The VMIs are dynamically updated as pods and
labels are added and deleted.

Kubernetes Support for Security Policy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Network policies created in a Kubernetes environment are implemented by
using Contrail Security Policy framework. Labels from the Kubernetes
environment are exposed as tags in Contrail. Starting in Contrail
Release 5.0, you can define tags for a Kubernetes environment. Contrail
security policy uses these tags to implement specified Kubernetes
policies. You can define tags in the UI or upload configurations in JSON
format. The newly-defined tags can be used to create and enforce
policies in Contrail Security.

Domain Name Server (DNS)
~~~~~~~~~~~~~~~~~~~~~~~~

Kubernetes implements DNS using SkyDNS, a small DNS application that
responds to DNS requests for service name resolution from pods. SkyDNS
runs as a pod in Kubernetes.

Supported Kubernetes Annotations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Currently, Contrail Networking supports the following Kubernetes
annotations:

.. raw:: html

   <div id="jd0e348" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   'opencontrail.org/network': '{"domain":"default-domain", "project": "k8s-contrail", "name":"deu"}'
   'opencontrail.org/isolation': 'true'
   'opencontrail.org/fip-pool': '{"domain": "default-domain", "project": "k8s-default", "network": "k8s-default-svc-public", "name": "default"}'

.. raw:: html

   </div>

.. raw:: html

   </div>

For further details, refer to
https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/.

 
