Kubernetes Updates
==================

 

.. raw:: html

   <div id="intro">

.. raw:: html

   <div class="mini-toc-intro">

This topic describes updates to Kubernetes and supported features in
Contrail.

.. raw:: html

   </div>

.. raw:: html

   </div>

TLS Bootstrapping of Kubernetes Nodes
-------------------------------------

Contrail supports TLS Bootstrapping of Kubernetes Nodes starting in
Contrail Networking Release 5.1. TLS bootstrapping streamlines
Kubernetes’ ability to add and remove nodes from the Contrail cluster.

Priority Based Multitenancy
---------------------------

Contrail supports priority on the various resource quotas through the
ResourceQuotaScopeSelector feature starting in Contrail Networking
Release 5.1.

Improved Autoscaling
--------------------

Contrail Networking supports improved pod autoscaling by creating and
deleting pods based on the load starting in Contrail Networking Release
5.1.

Reachability to Kubernetes Pods Using the IP Fabric Forwarding Feature
----------------------------------------------------------------------

A Kubernetes pod is a group of one or more containers (such as Docker
containers), the shared storage for those containers, and options on how
to run the containers. Since pods are in the overlay network, they
cannot be reached directly from the underlay without a gateway or
vRouter. Starting in Contrail Networking Release 5.0, the IP fabric
forwarding (ip-fabric-forwarding) feature enables virtual networks to be
created as part of the underlay network and eliminates the need for
encapsulation and decapsulation of data. The ip-fabric-forwarding
feature is only applicable for pod networks. If ip-fabric-forwarding is
enabled, pod-networks are associated to ip-fabric-ipam instead of
pod-ipam which is also a flat subnet.

The ip-fabric-forwarding feature is enabled and disabled in the global
and namespace levels. By default, ip-fabric-forwarding is disabled in
the global level. To enable it in global level, you must set
“ip_fabric_forwarding” to “true” in the “[KUBERNETES]” section of the
``/etc/contrail/contrail-kubernetes.conf`` file. To enable or disable
the feature in namespace level, you must set “ip_fabric_forwarding” to
“true” or “false” respectively in namespace annotation. For example,
“opencontrail.org/ip_fabric_forwarding”: “true”. Once the feature is
enabled, it cannot be disabled.

For more information, see `Gateway-less
Forwarding <https://github.com/tungstenfabric/tf-specs/blob/master/gateway-less-forwarding.md>`__.

Service Isolation Through Virtual Networks
------------------------------------------

In namespace isolation mode, services in one namespace are not
accessible from other namespaces, unless security groups or network
policies are explicitly defined to allow access. If any Kubernetes
service is implemented by pods in an isolated namespace, those services
are reachable only to pods in the same namespace through the Kubernetes
service-ip.

The Kubernetes service-ip is allocated from the cluster network despite
being in an isolated namespace. So, by default, service from one
namespace can reach services from another namespace. However, security
groups in isolated namespaces prevent reachability from external
namespace and also prevent reachability from outside of the cluster. In
order to enable access by external namespaces, the security group must
be edited to allow access to all namespaces which defeats the purpose of
isolation.

Contrail Networking—starting in Contrail Networking Release 5.0—enables
service or ingress reachability from external clusters in isolated
namespaces. Two virtual networks are created in isolated namespaces. One
network is dedicated to pods and one is dedicated to services. Contrail
network-policy is created between the pod network and the service
network for reachability between pods and services. Service uses the
same service-ipam which is a flat-subnet like pod-ipam. It is applicable
for default namespace as well.

Contrail ip-fabric-snat Feature
-------------------------------

With the Contrail ip-fabric-snat feature, pods that are in the overlay
can reach the Internet without floating IPs or a logical-router. The
ip-fabric-snat feature uses compute node IP for creating a source NAT to
reach the required services and is applicable only to pod networks. The
kube-manager reserves ports 56000 through 57023 for TCP and 57024
through 58047 for UDP to create a source NAT in global-config during the
initialization.

The ip-fabric-snat feature can be enabled or disabled in the global or
namespace levels. By default, the feature is disabled in the global
level. To enable the ip-fabric-snat feature in the global level, you
must set “ip-fabric-snat” to “true” in the “[KUBERNETES]” section in the
``/etc/contrail/contrail-kubernetes.conf`` file. To enable or disable it
in the namespace level, you must set “ip_fabric_snat” to “true” or
“false” respectively in namespace annotation. For example,
“opencontrail.org/ip_fabric_snat”: “true”. The ip_fabric_snat feature
can be at enabled and disabled any time. To enable or disable the
ip_fabric_snat feature in the default-pod-network, default namespace
must be used. If the ip_fabric_forwarding is enabled, ip_fabric_snat is
ignored.

For more information, see `Distributed
SNAT <https://github.com/tungstenfabric/tf-specs/blob/master/distributed-snat.md>`__.

Third-Party Ingress Controllers
-------------------------------

Multiple ingress controllers can co-exist in Contrail. If
“kubernetes.io/ingress.class” is absent or is “opencontrail” in the
annotations of the Kubernetes ingress resource, the kube-manager creates
a HAProxy loadbalancer. Otherwise it is ignored and the respective
ingress controller handles the ingress resource. Since Contrail ensures
the reachability between pods and services, any ingress controller can
reach the endpoints or pods directly or through services.

Custom Network Support for Ingress Resources
--------------------------------------------

Contrail supports custom networks in namespace level for pods. Starting
with Contrail Release 5.0, custom networks are supported for ingress
resources as well.

Kubernetes Probes and Kubernetes Service Node-Port
--------------------------------------------------

The Kubelet needs reachability to pods for liveness and readiness
probes. Contrail network policy is created between the IP fabric network
and pod network to provide reachability between node and pods. Whenever
the pod network is created, the network policy is attached to the pod
network to provide reachability between node and pods. So, any process
in the node can reach the pods.

Kubernetes Service Node-Port is based on node reachability to pods.
Since Contrail provides connectivity between node and pods through
Contrail the network policy, Node Port is supported.

Kubernetes Network-Policy Support
---------------------------------

Contrail Networking supports the following Kubernetes release 1.12
network policy features:

-  Egress support for network policy—Each NetworkPolicy includes a
   policyTypes list which can include either Ingress, Egress, or both.
   The policyTypes field indicates whether or not the given policy
   applies to ingress traffic to selected pod, egress traffic from the
   selected pod, or both. Contrail Networking—starting in Contrail
   Networking Release 5.1—supports the podSelector&namespaceSelector
   egress specification. Contrail Networking—starting in Contrail
   Networking Release 5.0—supports podSelector, namespaceSelector, and
   egress CIDR egress specifications.

-  Classless Interdomain Routing (CIDR) selector support for egress and
   ingress network policies

-  Contrail-ansible-deployer provisioning—Contrail-ansible-deployer is
   updated to support Kubernetes 1.12.

Contrail Networking supports Kubernetes release 1.9.2 and enables
implementing Kubernetes network policy in Contrail using the Contrail
firewall security policy framework. While Kubernetes network policy can
be implemented using other security objects in Contrail like security
groups and Contrail network policies, the support of tags by Contrail
firewall security policy aids in the simplification and abstraction of
workloads.

For more information, see `Implementation of Kubernetes Network Policy
with Contrail Firewall Policy <k8s-network-policy.html>`__.

 
