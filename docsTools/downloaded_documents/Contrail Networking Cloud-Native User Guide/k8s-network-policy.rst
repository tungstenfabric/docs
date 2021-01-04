Implementation of Kubernetes Network Policy with Contrail Firewall Policy
=========================================================================

 

Contrail Networking—starting in Contrail Networking Release 5.0—supports
implementing Kubernetes 1.9.2 network policy in Contrail using the
Contrail firewall security policy framework. While Kubernetes network
policy can be implemented using other security objects in Contrail like
security groups and Contrail network policies, the support of tags by
Contrail firewall security policy aids in the simplification and
abstraction of Kubernetes workloads.

Contrail firewall security policy allows decoupling of routing from
security policies and provides multi-dimension segmentation and policy
portability while significantly enhancing user visibility and analytics
functions. Contrail firewall security policy uses tags to achieve
multi-dimension traffic segmentation among various entities, and with
security features. Tags are key-value pairs associated with different
entities in the deployment. Tags can be pre-defined or custom defined.
Kubernetes network policy is a specification of how groups of Kubernetes
workloads, which are hereafter referred to as pods, are allowed to
communicate with each other and other network endpoints. Network policy
resources use labels to select pods and define rules which specify what
traffic is allowed to the selected pods.

Kubernetes Network Policy Characteristics
-----------------------------------------

Kubernetes network policies have the following characteristics:

-  A network policy is pod specific and applies to a pod or a group of
   pods. If a specified network policy applies to a pod, the traffic to
   the pod is dictated by rules of the network policy.

-  If a network policy is not applied to a pod then the pod accepts
   traffic from all sources.

-  A network policy can define traffic rules for a pod at the ingress,
   egress, or both directions. By default, a network policy is applied
   to the ingress direction, if no direction is explicitly specified.

-  When a network policy is applied to a pod, the policy must have
   explicit rules to specify an allowlist of permitted traffic in the
   ingress and egress directions. All traffic that does not match the
   allowlist rules are denied and dropped.

-  Multiple network policies can be applied on any pod. Traffic matching
   any one of the network policies must be permitted.

-  A network policy acts on connections rather than individual packets.
   For example, if traffic from pod A to pod B is allowed by the
   configured policy, then the return packets for that connection from
   pod B to pod A are also allowed, even if the policy in place does not
   allow pod B to initiate a connection to pod A.

-  Ingress Policy: An ingress rule consists of the identity of the
   source and the protocol:port type of traffic from the source that is
   allowed to be forwarded to a pod.

   The identity of the source can be of the following types:

   -  Classless Interdomain Routing (CIDR) block—If the source IP
      address is from the CIDR block and the traffic matches the
      protocol:port, then traffic is forwarded to the pod.

   -  Kubernetes namespaces—Namespace selectors identify namespaces,
      whose pods can send the defined protocol:port traffic to the
      ingress pod.

   -  Pods—Pod selectors identify the pods in the namespace
      corresponding to the network policy, that can send matching
      protocol:port traffic to the ingress pods.

-  Egress Policy: This specifies an allowlist CIDR to which a particular
   protocol:port type of traffic is permitted from the pods targeted by
   the network policy

   The identity of the destination can be of the following types:

   -  CIDR block—If the destination IP address is from the CIDR block
      and the traffic matches the protocol:port, then traffic is
      forwarded to the destination.

   -  Kubernetes namespaces—Namespace selectors identify namespaces,
      whose pods can send the defined protocol:port traffic to the
      egress pod.

   -  Pods—Pod selectors identify the pods in the namespace
      corresponding to the network policy, that can receive matching
      protocol:port traffic from the egress pods.

Representing Kubernetes Network Policy as Contrail Firewall Security Policy
---------------------------------------------------------------------------

Kubernetes and Contrail firewall policy are different in terms of the
semantics in which network policy is specified in each. The key to
efficient implementation of a Kubernetes network policy through Contrail
firewall policy is in mapping the corresponding configuration constructs
between these two entities.

The constructs are mapped as displayed in
`Table 1 <k8s-network-policy.html#kds-contrail-constructs>`__:

Table 1: Kubernetes Network Policy and Contrail Firewall Policy Mapping

+----------------------------------+----------------------------------+
| Kubernetes Network Policy        | Contrail Firewall Policy         |
| Constructs                       | Constructs                       |
+==================================+==================================+
| Label                            | Custom Tag (one for each label)  |
+----------------------------------+----------------------------------+
| Namespace                        | Custom Tag (one for each         |
|                                  | namespace)                       |
+----------------------------------+----------------------------------+
| Network Policy                   | Firewall Policy (one firewall    |
|                                  | policy per Network Policy)       |
+----------------------------------+----------------------------------+
| Rule                             | Firewall Rule (one firewall rule |
|                                  | per network policy rule)         |
+----------------------------------+----------------------------------+
| CIDR Rules                       | Address Group                    |
+----------------------------------+----------------------------------+
| Cluster                          | Default Application Policy Set   |
+----------------------------------+----------------------------------+

**Note**

The project in which Contrail firewall policy constructs are created is
the one that houses the Kubernetes cluster. For example, the Contrail
firewall policy constructs are created in the global scope, if the
Kubernetes cluster is a standalone cluster and the Contrail firewall
policy constructs are created in the project scope, if the Kubernetes
cluster is a nested cluster.

Resolving Kubernetes Network Policy Labels

The representation of pods in Contrail firewall policy is exactly the
same as in the corresponding Kubernetes network policy. Contrail
firewall policy deals with labels or tags in Contrail terminology.
Contrail does not expand labels to IP addresses.

For example, in the default namespace, if network policy-podSelector
specifies: role=db, then the corresponding firewall rule specifies the
pods as (role=db && namespace=default). No other translations to pod IP
address or otherwise are done.

If the same network-policy also has namespaceSelector as
namespace=myproject, then the corresponding firewall rule represents
that namespace as (namespace=myproject). No other translations or rules
representing pods in “myproject“ namespace is done.

Similarly, each CIDR is represented by one rule. In essence, the
Kubernetes network policy is translated 1:1 to Contrail firewall policy.
There is only one additional firewall rule created for each Kubernetes
network policy. The purpose of that rule is to implement the implicit
deny requirements of the network policy and no other rule is created.

Contrail Firewall Policy Naming Convention
------------------------------------------

Contrail firewall security policies and rules are named as follows:

-  A Contrail firewall security policy created for a Kubernetes network
   policy is named in the following format:

   .. raw:: html

      <div id="jd0e189" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      < Namespace-name >-< Network Policy Name >

   .. raw:: html

      </div>

   .. raw:: html

      </div>

   For example, a network policy "world" in namespace "Hello" is named:

   .. raw:: html

      <div id="jd0e194" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      Hello-world

   .. raw:: html

      </div>

   .. raw:: html

      </div>

-  Contrail firewall rules created for a Kubernetes network policy are
   named in the following format:

   .. raw:: html

      <div id="jd0e200" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      < Namespace-name >-<PolicyType>-< Network Policy Name >-<Index of from/to blocks>-<selector type>-<rule-index>-<svc/port index>

   .. raw:: html

      </div>

   .. raw:: html

      </div>

   .. raw:: html

      <div id="jd0e203" class="sample" dir="ltr">

   For example:

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      apiVersion: networking.k8s.io/v1
      kind: NetworkPolicy
      metadata:
        name: world
        namespace: hello
      spec:
        podSelector:
          matchLabels:
            role: db
        policyTypes:
        - Ingress
        ingress:
        - from:
          - podSelector:
              matchLabels:
                role: frontend

   .. raw:: html

      </div>

   .. raw:: html

      </div>

   A rule corresponding to this policy is named:

   .. raw:: html

      <div id="jd0e210" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      hello-ingress-world-0-podSelector-0-0

   .. raw:: html

      </div>

   .. raw:: html

      </div>

Implementation of Kubernetes Network Policy
-------------------------------------------

The contrail-kube-manager daemon binds Kubernetes and Contrail together.
This daemon connects to the API server of Kubernetes clusters and
coverts Kubernetes events, including network policy events, into
appropriate Contrail objects. With respect to a Kubernetes network
policy, contrail-kube-manager performs the following actions:

-  Creates a Contrail tag for each Kubernetes label

-  Creates a firewall policy for each Kubernetes network policy

-  Creates an Application Policy Set (APS) to represent the cluster. All
   firewall policies created in that cluster are attached to this
   application policy set.

-  Modifications to existing Kubernetes network policies result in the
   corresponding firewall policies being updated.

Example Network Policy Configurations
-------------------------------------

The following examples illustrate various sample network policies and
the corresponding firewall security policies created.

Example 1 - Conditional egress and ingress traffic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following policy specifies a sample network policy with specific
conditions for ingress and egress traffic to and from all pods in a
namespace:

Sample Kubernetes network policy

.. raw:: html

   <div id="jd0e244" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   apiVersion: networking.k8s.io/v1
   kind: NetworkPolicy
   metadata:
     name: test-network-policy
     namespace: default
   spec:
     podSelector:
       matchLabels:
         role: db
     policyTypes:
     - Ingress
     - Egress
     ingress:
     - from:
       - ipBlock:
           cidr: 17x.xx.0.0/16
           except:
           - 17x.xx.1.0/24
       - namespaceSelector:
           matchLabels:
             project: myproject
       - podSelector:
           matchLabels:
             role: frontend
       ports:
       - protocol: TCP
         port: 6379
     egress:
     - to:
       - ipBlock:
           cidr: 10.0.0.0/24
       ports:
       - protocol: TCP
         port: 5978

.. raw:: html

   </div>

.. raw:: html

   </div>

Sample Contrail firewall security policy

The test-network-policy defined in Kubernetes results in the following
objects being created in Contrail.

*Tags*—The following tags are created, if they do not exist. In a
regular workflow, these tags must have been created by the time the
namespace and pods were created.

========= =======
Key       Value
========= =======
role      db
namespace default
========= =======

*Address Groups*

The following address groups are created:

============= =============
Name          Prefix
============= =============
17x.xx.1.0/24 17x.xx.1.0/24
17x.xx.0.0/16 17x.xx.0.0/16
10.0.0.0/24   10.0.0.0/24
============= =============

*Firewall Rules*

The following firewall rules are created:

+----------+--------+----------+----------+-----+----------+----------+
| Rule     | Action | Services | E        | Dir | E        | Match    |
| Name     |        |          | ndpoint1 |     | ndpoint2 | Tags     |
+==========+========+==========+==========+=====+==========+==========+
| default  | deny   | tcp:6379 | Address  | >   | role=db  |          |
| -ingress |        |          | Group:   |     | &&       |          |
| -test-ne |        |          | 17x.x    |     | n        |          |
| twork-po |        |          | x.1.0/24 |     | amespace |          |
| licy-0-i |        |          |          |     | =default |          |
| pBlock-0 |        |          |          |     |          |          |
| -17x.xx. |        |          |          |     |          |          |
| 1.0/24-0 |        |          |          |     |          |          |
+----------+--------+----------+----------+-----+----------+----------+
| defa     | pass   | tcp:6379 | Address  | >   | role=db  |          |
| ult-ingr |        |          | Group:   |     | &&       |          |
| ess-test |        |          | 17x.x    |     | n        |          |
| -network |        |          | x.0.0/16 |     | amespace |          |
| -policy- |        |          |          |     | =default |          |
| 0-ipBloc |        |          |          |     |          |          |
| k-0-cidr |        |          |          |     |          |          |
| -17x.xx. |        |          |          |     |          |          |
| 0.0/16-0 |        |          |          |     |          |          |
+----------+--------+----------+----------+-----+----------+----------+
| def      | pass   | tcp:6379 | p        | >   | role=db  |          |
| ault-ing |        |          | roject=m |     | &&       |          |
| ress-tes |        |          | yproject |     | n        |          |
| t-networ |        |          |          |     | amespace |          |
| k-policy |        |          |          |     | =default |          |
| -0-names |        |          |          |     |          |          |
| paceSele |        |          |          |     |          |          |
| ctor-1-0 |        |          |          |     |          |          |
+----------+--------+----------+----------+-----+----------+----------+
| defau    | pass   | tcp:6379 | n        | >   | role=db  |          |
| lt-ingre |        |          | amespace |     | &&       |          |
| ss-test- |        |          | =default |     | n        |          |
| network- |        |          | &&       |     | amespace |          |
| policy-0 |        |          | role=    |     | =default |          |
| -podSele |        |          | frontend |     |          |          |
| ctor-2-0 |        |          |          |     |          |          |
+----------+--------+----------+----------+-----+----------+----------+
| default  | pass   | tcp:5978 | role=db  | >   | Address  |          |
| -egress- |        |          | &&       |     | Group:   |          |
| test-net |        |          | n        |     | 10.      |          |
| work-pol |        |          | amespace |     | 0.0.0/24 |          |
| icy-ipBl |        |          | =default |     |          |          |
| ock-0-ci |        |          |          |     |          |          |
| dr-10.0. |        |          |          |     |          |          |
| 0.0/24-0 |        |          |          |     |          |          |
+----------+--------+----------+----------+-----+----------+----------+

*Firewall Policy*

The following firewall security policy is created with the following
rules.

.. raw:: html

   <table data-cellspacing="0" style="border-top:thin solid black;" width="99%">
   <colgroup>
   <col style="width: 50%" />
   <col style="width: 50%" />
   </colgroup>
   <thead>
   <tr class="header">
   <th style="text-align: left;"><span class="CellHeading">Name</span></th>
   <th style="text-align: left;"><span class="CellHeading">Rules</span></th>
   </tr>
   </thead>
   <tbody>
   <tr class="odd">
   <td style="text-align: left;"><p>default-test-network-policy</p></td>
   <td style="text-align: left;"><ul>
   <li><p>default-ingress-test-network-policy-0-ipBlock-0-17x.xx.1.0/24-0</p></li>
   <li><p>default-ingress-test-network-policy-0-ipBlock-0-cidr-17x.xx.0.0/16-0</p></li>
   <li><p>default-ingress-test-network-policy-0-namespaceSelector-1-0</p></li>
   <li><p>default-ingress-test-network-policy-0-podSelector-2-0</p></li>
   <li><p>default-egress-test-network-policy-ipBlock-0-cidr-10.0.0.0/24-0</p></li>
   </ul></td>
   </tr>
   </tbody>
   </table>

Example 2 - Allow all Ingress Traffic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following policy explicitly allows all traffic for all pods in a
namespace:

Sample Kubernetes network policy

.. raw:: html

   <div id="jd0e512" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   apiVersion: networking.k8s.io/v1
       kind: NetworkPolicy
       metadata:
         name: allow-all-ingress
       spec:
         podSelector:
         ingress:
         - {}

.. raw:: html

   </div>

.. raw:: html

   </div>

Sample Contrail firewall security policy

*Tags*—The following tags are created, if they do not exist. In a
regular workflow, these tags are created before the namespace and pods
are created.

========= =======
Key       Value
========= =======
namespace default
========= =======

*Address Groups* - None

*Firewall Rules*

The following firewall rule is created:

+----------+--------+----------+----------+-----+----------+----------+
| Rule     | Action | Services | E        | Dir | E        | Match    |
| Name     |        |          | ndpoint1 |     | ndpoint2 | Tags     |
+==========+========+==========+==========+=====+==========+==========+
| default  | pass   | any      | any      | >   | n        |          |
| -ingress |        |          |          |     | amespace |          |
| -allow-a |        |          |          |     | =default |          |
| ll-ingre |        |          |          |     |          |          |
| ss-0-all |        |          |          |     |          |          |
| ow-all-0 |        |          |          |     |          |          |
+----------+--------+----------+----------+-----+----------+----------+

*Firewall Policy*

The following firewall policy are created:

+---------------------------+-------------------------------------------------+
| Name                      | Rules                                           |
+===========================+=================================================+
| default-allow-all-ingress | default-ingress-allow-all-ingress-0-allow-all-0 |
+---------------------------+-------------------------------------------------+

Example 3 - Deny all ingress traffic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following policy explicitly denies all ingress traffic to all pods
in a namespace:

Sample Kubernetes network policy

.. raw:: html

   <div id="jd0e638" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   apiVersion: networking.k8s.io/v1
   kind: NetworkPolicy
   metadata:
     name: deny-ingress
   spec:
     podSelector:
     policyTypes:
     - Ingress

.. raw:: html

   </div>

.. raw:: html

   </div>

Sample Contrail firewall security policy

Tags—The following tags are created, if they do not exist. In a regular
workflow, these tags are created before the namespace and pods are
created.

========= =======
Key       Value
========= =======
namespace default
========= =======

*Address Groups* - None

*Firewall Rules* - None

**Note**

The implicit behavior of any network policy is to deny traffic not
matching explicit allow flows. However in this policy, there are no
explicit allow rules. Hence, no firewall rules are created for this
policy.

*Firewall Policy*

The following firewall policy is created:

==================== =====
Name                 Rules
==================== =====
default-deny-ingress 
==================== =====

Example 4 - Allow all egress traffic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following policy explicitly allows all egress traffic from all pods
in a namespace:

Sample Kubernetes network policy

.. raw:: html

   <div id="jd0e709" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   apiVersion: networking.k8s.io/v1
   kind: NetworkPolicy
   metadata:
     name: allow-all-egress
   spec:
     podSelector:
     egress:
     - {}

.. raw:: html

   </div>

.. raw:: html

   </div>

Sample Contrail firewall security policy

Tags—The following tag is created, if they do not exist. In a regular
workflow, these tags are created before the namespace and pods are
created.

========= =======
Key       Value
========= =======
namespace default
========= =======

*Address Groups* - None

*Firewall Rules*

The following firewall rule is created:

+----------+--------+----------+----------+-----+----------+----------+
| Rule     | Action | Services | E        | Dir | E        | Match    |
| Name     |        |          | ndpoint1 |     | ndpoint2 | Tags     |
+==========+========+==========+==========+=====+==========+==========+
| def      | pass   | any      | n        | >   | any      |          |
| ault-egr |        |          | amespace |     |          |          |
| ess-allo |        |          | =default |     |          |          |
| w-all-eg |        |          |          |     |          |          |
| ress-all |        |          |          |     |          |          |
| ow-all-0 |        |          |          |     |          |          |
+----------+--------+----------+----------+-----+----------+----------+

*Firewall Policy*

The following firewall policy is created:

======================== ===========================================
Name                     Rules
======================== ===========================================
default-allow-all-egress default-egress-allow-all-egress-allow-all-0
======================== ===========================================

Example 5 - Default deny all egress traffic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following policy explicitly denies all egress traffic from all pods
in a namespace:

Sample Kubernetes network policy

.. raw:: html

   <div id="jd0e833" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   apiVersion: networking.k8s.io/v1
   kind: NetworkPolicy
   metadata:
     name: deny-all-egress
   spec:
     podSelector: {}
     policyTypes:
     - Egress

.. raw:: html

   </div>

.. raw:: html

   </div>

Sample Contrail firewall security policy

Tags—The following tag is created, if they do not exist. In a regular
workflow, these tags are created before the namespace and pods are
created.

========= =======
Key       Value
========= =======
namespace default
========= =======

*Address Groups* - None

*Firewall Rules* - None

**Note**

The implicit behavior of any network policy with egress policy type is
to deny egress traffic not matching explicit egress allow flows. In this
policy, there are no explicit egress allow rules. Hence, no firewall
rules are created for this policy.

*Firewall Policy*

The following firewall policy is created:

======================= =====
Name                    Rules
======================= =====
default-deny-all-egress 
======================= =====

Example 6 - Default deny all ingress and egress traffic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following policy explicitly denies all ingress and egress traffic to
and from all pods in that namespace:

Sample Kubernetes network policy

.. raw:: html

   <div id="jd0e904" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   apiVersion: networking.k8s.io/v1
   kind: NetworkPolicy
   metadata:
     name: deny-all-ingress-egress
   spec:
     podSelector:
     policyTypes:
     - Ingress
     - Egress

.. raw:: html

   </div>

.. raw:: html

   </div>

Sample Contrail firewall security policy

Tags—The following tags is created, if they do not exist. In a regular
workflow, these tags are created before the namespace and pods are
created.

========= =======
Key       Value
========= =======
namespace default
========= =======

*Address Groups* - None

*Firewall Rules* - None

**Note**

The implicit behavior of any network policy with ingress/egress policy
type is to deny corresponding traffic not matching explicit allow flows.
In this policy, there are no explicit allow rules. Hence, no firewall
rules are created for this policy.

*Firewall Policy*

The following firewall policy is created:

=============================== =====
Name                            Rules
=============================== =====
default-deny-all-ingress-egress 
=============================== =====

Cluster-wide Policy Action Enforcement
--------------------------------------

The specification and the syntax of network policies allow for maximum
flexibility and varied combinations. However, you must exercise caution
while configuring the network policies.

Consider a case where two network policies are created:

-  Policy 1: Pod A can send to Pod B.

-  Policy 2: Pod B can only receive from Pod C.

From a networking flow perspective, there is an inherent contradiction
between the above policies. Policy 1 states that a flow from Pod A to
Pod B is allowed. Policy 2 implies that flow from Pod A to Pod B is not
allowed. From a networking perspective, Contrail prioritizes flow
behavior as more critical. In the event of inherent contradiction in
network policies, Contrail will honor the flow perspective. One of the
core aspects of this notion is that if a policy matches a flow, the
action is honored cluster-wide.

For instance, if a flow matches a policy at the source, the flow will
match the same policy in the destination as well. Therefore, the flow
behavior in a Contrail-managed Kubernetes cluster is as shown below:

-  Flow from Pod A to Pod B is allowed (due to Policy 1)

-  Flow from Pod C to Pod B is allowed (due to Policy 2)

-  Any other flow to Pod B is disallowed (due to Policy 2)

Example Network Policy Action Enforcement Scenarios
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Consider the following examples of network policy action enforcement:

-  Allow all egress traffic and deny all ingress traffic

   Setup: Namespace NS1 has two pods, Pod A and Pod B.

   Policy: A network policy applied on namespace NS1 states:

   -  Rule 1. Allow all egress traffic from all pods in NS1.

   -  Rule 2. Deny all ingress traffic to all pods in NS1.

   Behavior:

   -  Pod A can send traffic to Pod B (due to rule 1)

   -  Pod B can send traffic to Pod A (due to rule 1)

   -  PodX from a different namespace cannot send traffic to Pod A or
      Pod B (due to rule 2)

-  Allow all ingress traffic and deny all egress traffic

   Setup: Namespace NS1 has two pods, Pod A and Pod B.

   Policy: A network policy applied on namespace NS1 states:

   -  Rule 1. Allow all ingress traffic to all pods in NS1

   -  Rule 2. Deny all egress traffic from all pods in NS1.

   Behavior:

   -  Pod A can send traffic to Pod B (due to rule 1)

   -  Pod B can send traffic to Pod A (due to rule 1)

   -  Pod A and Pod B cannot send traffic to pods in any other
      namespace.

-  Egress CIDR rule

   Setup: Namespace NS1 has two pods, Pod A and Pod B.

   Policy: A network policy applied on namespace NS1 states:

   -  Policy 1: Allow Pod A to send traffic to CIDR of Pod B.

   -  Policy 2: Deny all ingress traffic to all pods in NS1.

   Behavior:

   -  Pod A can send traffic to Pod B (due to Policy 1)

   -  All other traffic to Pod A and Pod B is dropped (due to policy 2)

 
