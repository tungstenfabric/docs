Security Policy Features in OpenStack
=====================================

 

Overview of Existing Network Policy and Security Groups in OpenStack
--------------------------------------------------------------------

Contrail virtual networks are isolated by default. Workloads in a
virtual network cannot communicate with workloads in other virtual
networks, by default. A neutron router or a Contrail network policy may
be used to connect two virtual networks. In addition, Contrail network
policy also provides security between two virtual networks by allowing
or denying specified traffic.

OpenStack security groups allow access between workloads and instances
for specified traffic types and any other types are denied.

A security policy model for any given customer first needs to map to the
OpenStack network policy framework and security group constructs.

In modern cloud environments, workloads are moving from one server to
another, one rack to another and so on. Therefore, users must rely less
on using IP addresses or other network coordinates to identify the
endpoints to be protected. Instead users must leverage application
attributes to author policies, so that the policies don't need to be
updated on account of workload mobility.

You might want to segregate traffic based on the different categories of
data origination, such as:

-  Protecting the application itself

-  Segregating traffic for specific component tiers within the
   application

-  Segregating traffic based on the deployment environment for the
   application instance

-  Segregating traffic based on the specific geographic location where
   the application is deployed

There are many other possible scenarios where traffic needs to be
segregated.

Additionally, you might need to group workloads based on combinations of
tags. These intents are hard to express with existing network policy
constructs or Security Group constructs. Besides, existing policy
constructs leveraging the network coordinates, must continually be
rewritten or updated each time workloads move and their associated
network coordinates change.

Security Policy Enhancements
----------------------------

As the Contrail environment has grown and become more complex, it has
become harder to achieve desired security results with the existing
network policy and security group constructs. The Contrail network
policies have been tied to routing, making it difficult to express
security policies for environments such as cross sectioning between
categories, or having a multi-tier application supporting development
and production environment workloads with no cross environment traffic.

Starting with Release 5.1, Contrail Networking supports the OpenStack
Neutron Firewall version 2 API extension known as Neutron FWaaS
(Firewall as a Service). The Neutron API enhancements make the existing
FWaaS more granular by giving you the ability to apply the firewall
rules at the port level rather than at the router level, and to have
different firewall policies with different rules applied to inbound
versus outbound connections. Support is extended to various types of
Neutron ports, including VM ports and SFC ports as well as router ports.
It also provides better grouping mechanisms (firewall groups, address
groups and service groups). Finally, the Firewall Group enables firewall
policies to be bound to Neutron ports.

Related enhancements to the OpenStack Neutron and Contrail security
groups API include:

-  Firewall rules support deny, reject, description, and admin status
   attributes

-  A share attribute for firewall rules allow them to be shared between
   different projects

-  Filtering based on the source and destination address prefix and port
   rather than just the remote destination

-  Firewall groups reference firewall rules through a firewall policy,
   allowing reuse of shareable firewall policies that are referenced by
   multiple firewall groups

Configuration Objects
---------------------

The following are the configuration objects for the new security
features.

-  firewall-policy

-  firewall-rule

-  policy-management

-  application-policy

-  service-group

-  address-group

-  tag

-  global-application-policy

For more information on security policies in Contrail, see `Security
Policy Features <security-policy-enhancements.html>`__.

 
