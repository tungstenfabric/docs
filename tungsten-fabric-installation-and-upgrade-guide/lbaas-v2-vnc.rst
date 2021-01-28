Support for OpenStack LBaaS
===========================

.. raw:: html

   <div id="intro">

.. raw:: html

   <div class="mini-toc-intro">

Starting with Release 3.1, Contrail provides support for the OpenStack
Load Balancer as a Service (LBaaS) Version 2.0 APIs in the Liberty
release of OpenStack.

.. raw:: html

   </div>

.. raw:: html

   </div>

.. _openstack-neutron-lbaas-version-20:

OpenStack Neutron LBaaS Version 2.0
-----------------------------------

Platform Support
~~~~~~~~~~~~~~~~

Table 1 shows which Contrail with OpenStack release combinations support
which version of OpenStack LBaaS APIs.

Table 1: Contrail OpenStack Platform Support for LBaaS Versions

+----------------------------------+----------------------------------+
| Contrail OpenStack Platform      | LBaaS Support                    |
+==================================+==================================+
| Contrail-3.1-Liberty (and        | Only LBaaS v2 is supported.      |
| subsequent OS releases)          |                                  |
+----------------------------------+----------------------------------+
| Contrail-3.0-Liberty (and        | LBaaS v1 is default. LBaaS v2 is |
| subsequent OS releases)          | Beta.                            |
+----------------------------------+----------------------------------+
| ``<Contrail-any-release>``-Kilo  | Only LBaaS v1 is supported.      |
| (and previous OS releases)       |                                  |
+----------------------------------+----------------------------------+

.. _using-openstack-lbaas-version-20:

Using OpenStack LBaaS Version 2.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The OpenStack LBaaS Version 2.0 extension enables tenants to manage load
balancers for VMs, for example, load-balancing client traffic from a
network to application services, such as VMs, on the same network. The
LBaaS Version 2.0 extension is used to create and manage load balancers,
listeners, pools, members of a pool, and health monitors, and to view
the status of a resource.

For LBaaS v2.0, the Contrail controller aggregates the configuration by
provider. For example, if ``haproxy`` is the provider, the controller
generates the configuration for ``haproxy`` and eliminates the need to
send all of the load-balancer resources to the ``vrouter-agent``; only
the generated configuration is sent, as part of the service instance.

For more information about OpenStack v2.0 APIs, refer to the section
LBaaS 2.0 (STABLE) (lbaas, loadbalancers, listeners, health_monitors,
pools, members), at
http://developer.openstack.org/api-ref-networking-v2-ext.html.

LBaaS v2.0 also allows users to listen to multiple ports for the same
virtual IP, by decoupling the virtual IP address from the port.

The object model has the following resources:

-  Load balancer—Holds the virtual IP address

-  Listeners—One or many listeners with different ports, protocols, and
   so on

-  Pools

-  Members

-  Health monitors

Support for Multiple Certificates per Listener
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Multiple certificates per listener are supported, with OpenStack
Barbican as the storage for certificates. OpenStack Barbican is a REST
API designed for the secure storage, provisioning, and management of
secrets such as passwords, encryption keys, and X.509 certificates.

The following is an example CLI to store certificates in Barbican:

``- barbican --os-identity-api-version 2.0 secret store --payload-content-type='text/plain' --name='certificate' --payload="$(cat server.crt)"``

For more information about OpenStack Barbican, see:
https://wiki.openstack.org/wiki/Barbican.

Neutron Load-Balancer Creation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

   The *Neutron* LBaaS plugin is not supported in OpenStack Train release.
   From OpenStack Train release, *neutron-lbaas* is replaced by *Octavia*.

The following is an example of Neutron load-balancer creation:

.. raw:: html

   <div id="jd0e140" class="example" dir="ltr">

::

   - neutron net-create private-net

   - neutron subnet-create --name private-subnet private-net 10.30.30.0/24

   - neutron lbaas-loadbalancer-create $(neutron subnet-list | awk '/ private-subnet / {print $2}') --name lb1

   - neutron lbaas-listener-create --loadbalancer lb1 --protocol-port 443 --protocol TERMINATED_HTTPS --name listener1 --default-tls-container=$(barbican --os-identity-api-version 2.0 container list | awk '/ tls_container / {print $2}')

   - neutron lbaas-pool-create --name pool1 --protocol HTTP --listener listener1 --lb-algorithm ROUND_ROBIN

   - neutron lbaas-member-create --subnet private-subnet --address 30.30.30.10 --protocol-port 80 mypool

   - neutron lbaas-member-create --subnet private-subnet --address 30.30.30.11 --protocol-port 80 mypool

.. raw:: html

   </div>

OpenStack Octavia LBaaS
-----------------------


Using Octavia Load-Balancer
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Contrail Networking Release 2005 supports Octavia as LBaaS. The
deployment supports RHOSP and Juju platforms.

With Octavia as LBaaS, Contrail Networking is only maintaining network
connectivity and is not involved in any load balancing functions.

For each OpenStack load balancer creation, Octavia launches a VM known
as *amphora VM*. The VM starts the HAPROXY when listener is created for
the load balancer in OpenStack. Whenever the load balancer gets updated
in OpenStack, *amphora VM* updates the running HAPROXY configuration.
The *amphora VM* is deleted on deleting the load balancer.

Contrail Networking provides connectivity to *amphora VM* interfaces.
*Amphora VM* has two interfaces; one for management and the other for
data. The management interface is used by the Octavia services for the
management communication. Since, Octavia services are running in the
underlay network and *amphora VM* is running in the overlay network, SDN
gateway is needed to reach the overlay network. The data interface is
used for load balancing the traffic.

If the load balancer service is exposed to public, you must create the
load balancer VIP in the public subnet. The load balancer members can be
in the public or private subnet.

You must create network policy between public network and private
network if the load balancer members are in the private network.

Octavia Load-Balancer Creation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following is an example of Octavia load-balancer creation:

.. raw:: html

   <div id="jd0e188" class="example" dir="ltr">

::

   openstack loadbalancer listener create --protocol HTTP --protocol-port 80 --name listener1 lb1
   openstack loadbalancer show lb1 # Wait for the provisioning_status to be ACTIVE.
   openstack loadbalancer pool create --lb-algorithm ROUND_ROBIN --listener listener1 --protocol HTTP --name pool1
   openstack loadbalancer healthmonitor create --delay 5 --timeout 2 --max-retries 1 --type HTTP pool1
   openstack loadbalancer member create --subnet-id private --address 10.10.10.50 --protocol-port 80 pool1
   openstack loadbalancer member create --subnet-id private --address 10.10.10.51 --protocol-port 80 pool1

.. raw:: html

   </div>

.. raw:: html

   <div class="table">

.. raw:: html

   <div class="caption">

 .. list-table:: Release History Table
   :header-rows: 1

   * - Release
     - Description
   * - 2011
     - Tungsten Fabric Release 2011 supports Octavia as LBaaS.
