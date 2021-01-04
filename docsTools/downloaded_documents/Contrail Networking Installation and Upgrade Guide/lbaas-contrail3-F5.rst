Using Load Balancers in Contrail
================================

 

.. raw:: html

   <div id="intro">

.. raw:: html

   <div class="mini-toc-intro">

As of Contrail Release 3.0, load balancer LBaaS features are available.
This topic includes:

.. raw:: html

   </div>

.. raw:: html

   </div>

Invoking LBaaS Drivers
----------------------

The provider field specified in the pool configuration determines which
load balancer drivers are selected. The load balancer driver selected is
responsible for configuring the external hardware or virtual machine
load balancer.

Supported load balancer drivers include:

-  HAProxy

-  A10 Networks

-  F5 Networks

-  Avi Networks

Benefits of Creating Configuration Objects
------------------------------------------

Starting with Contrail 3.0, the Neutron LBaaS plugin creates required
configuration objects (such as pool, VIP, members, and monitor) in the
Contrail API server, instead of within the Neutron plugin context, as in
previous releases.

This method of configuration has the following benefits:

-  Configuration objects can be created in multiple ways: from Neutron,
   from virtual controller APIs, or from the Contrail UI.

-  The load balancer driver can make inline calls, such as REST or SUDS,
   to configure the external load balancer device.

-  The load balancer driver can use Contrail service monitor
   infrastructure, such as database, logging, and API server.

**Note**

The *Neutron* LBaaS plugin is not supported in OpenStack Train release.

`Figure 1 <lbaas-contrail3-F5.html#lbaas-neutron>`__ provides an
overview of the Contrail LBaaS components.

|Figure 1: Contrail LBaaS components with neutron-lbaas|

Using a Service Appliance Set as the LBaaS Provider
---------------------------------------------------

In OpenStack Neutron, the load balancer provider is statically
configured in ``neutron.conf``, which requires restart of the Neutron
server when configuring a new provider. The following is an example of
the service provider configuration in ``neutron.conf``.

.. raw:: html

   <div id="jd0e76" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   [service_providers]
   service_provider = LOADBALANCER:Opencontrail:neutron_plugin_contrail.plugins.opencontrail. loadbalancer.driver.OpencontrailLoadbalancerDriver:default

.. raw:: html

   </div>

.. raw:: html

   </div>

In Contrail Release 3.0 and greater, the Neutron LBaaS provider is
configured by using the object ``service-appliance-set``. All of the
configuration parameters of the LBaaS driver are populated to the
``service-appliance-set`` object and passed to the driver.

During initialization, the service monitor creates a default service
appliance set with a default LBaaS provider, which uses an HAProxy-based
load balancer. The service appliance set consists of individual service
appliances for load balancing the traffic. The service appliances can be
physical devices or virtual machines.

.. raw:: html

   <div id="jd0e89" class="sample" dir="ltr">

**Sample Configuration: Service Appliance Set**

The following is a sample configuration of the service appliance set for
the LBaaS provider:

.. raw:: html

   <div class="output" dir="ltr">

::

   {
     "service-appliance-set": {
       "fq_name": [
         "default-global-system-config",
         "f5"
       ],
       "service_appliance_driver": "svc_monitor.services.loadbalancer.drivers.f5.f5_driver.OpencontrailF5LoadbalancerDriver",
       "parent_type": "global-system-config",
       "service_appliance_set_properties": {
         "key_value_pair": [
           {
             "key": "sync_mode",
             "value": "replication"
           },
          {
             "key": "global_routed_mode",
             "value": "True"
           }
         ]
       },
       "name": "f5"
     }
   }

.. raw:: html

   </div>

.. raw:: html

   </div>

.. raw:: html

   <div id="jd0e96" class="sample" dir="ltr">

**Sample Configuration: Single Service Appliance**

The following is a sample configuration of a single service appliance:

.. raw:: html

   <div class="output" dir="ltr">

::

   {
     "service-appliance": {
       "fq_name": [
         "default-global-system-config",
         "f5",
         "bigip"
       ],
       "parent_type": "service-appliance-set",
       "service_appliance_ip_address": "<ip address>",
       "service_appliance_user_credentials": {
         "username": "admin",
         "password": "<password>"
       },
       "name": "bigip"
     }
   }

.. raw:: html

   </div>

.. raw:: html

   </div>

Understanding the Load Balancer Agent
-------------------------------------

The load balancer agent is a module in the service monitor. The service
monitor listens on the RabbitMQ configuration messaging queue
(``vnc_config.object-update``) to get configuration objects. The
dependency tracker triggers changes to all related objects, based on
configuration updates.

The dependency tracker is informed to notify the pool object whenever
the VIP, member, or health monitor object is modified.

Whenever there is an update to the pool object, either directly due to a
pool update or due to a dependency update, the load balancer agent in
the service monitor is notified.

The load balancer agent module handles the following:

-  Loading and unloading LBaaS driver-based service appliance set
   configuration.

-  Providing the abstract driver class for the load balancer driver.

-  Invoking the LBaaS driver.

-  Load balancer-related configuration.

F5 Networks Load Balancer Integration in Contrail
-------------------------------------------------

.. raw:: html

   <div class="mini-toc-intro">

This section details use of the F5 load balancer driver with Contrail.

.. raw:: html

   </div>

-  `F5 Load Balancer Global Routed
   Mode <lbaas-contrail3-F5.html#jd0e154>`__

-  `Initial Configuration on an F5
   Device <lbaas-contrail3-F5.html#jd0e254>`__

-  `Initial Configuration on an MX Series Device Used as DC
   Gateway <lbaas-contrail3-F5.html#jd0e264>`__

Contrail Release 3.0 implements an LBaaS driver that supports a physical
or virtual F5 Networks load balancer, using the abstract load balancer
driver class, ``ContrailLoadBalancerAbstractDriver``.

This driver is invoked from the load balancer agent of the
``contrail-svc-monitor``. The driver makes a BIG-IP interface call to
configure the F5 Networks device. All of the configuration parameters
used to tune the driver are configured in the ``service-appliance-set``
object and passed to the driver by the load balancer agent while loading
the driver.

The F5 load balancer driver uses the BIG-IP interface version V1.0.6,
which is a Python package extracted from the load balancer plugin
provided by F5 Networks. The driver uses either a SOAP API or a REST
API.

F5 Load Balancer Global Routed Mode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The F5 load balancer driver is programmed in ``global routed`` mode
using a property of the ``service-appliance-set``.

This section describes the features and requirements of the F5 load
balancer driver configured in global routed mode.

The following are features of the global routed mode.

-  All virtual IP addresses (VIPs) are assumed to be routable from
   clients and all members are routable from the F5 device.

-  All access to and from the F5 device is assumed to be globally
   routed, with no segregation between tenant services on the F5 device.
   Consequently, do NOT configure overlapping addresses across tenants
   and networks.

-  The F5 device can be attached to the corporate network or to the IP
   fabric.

The following are requirements to support global routed mode of an F5
device used with LBaaS:

-  The entire configuration of the F5 device for Layer 2 and Layer 3 is
   preprovisioned.

-  All tenant networks and all IP fabrics are in the same namespace as
   the corporate network.

-  All VIPs are in the same namespace as the tenant and corporate
   networks.

Traffic Flow in Global Routed Mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This section describes and illustrates the behavior of traffic flow in
global routed mode.

The information in this section is based on a model that includes the
following network topology:

Corporate Network --- DC Gateway (MX device) --- IP Fabric --- Compute
nodes

The Corporate Network, the IP Fabric and all tenant networks use IP
addresses from a single namespace, there is no overlap of the addresses
in the networks. The F5 devices can be attached to the Corporate Network
or to the IP Fabric, and are configured to use the global routed mode.

The role of the MX Series device is to route post-proxy traffic, coming
from the F5 device in the underlay, to the pool members in the overlay.
In the reverse direction, the MX device takes traffic coming from the
pool members in the overlay and routes it back to the F5 device in the
underlay.

The MX device is preprovisioned with the following:

-  VRF connected to pool network 2

-  ability to route traffic from inet.0 to the pool network

The MX routes the traffic from inet.0 to public VRF and sends traffic to
the compute node where the pool member is instantiated.

The F5 device is preprovisioned with the following:

-  publish route to attract VIP traffic

-  pool network subnet route that points to the MX device

The F5 device is responsible for attracting traffic destined to all the
VIPs, by advertising a subnet route that covers all VIPs using IGP.

The F5 device load balances among different pool members and sends
traffic to the chosen member.

`Figure 2 <lbaas-contrail3-F5.html#lbaas-contrail-2>`__ shows the
traffic flow in global routed mode.

|Figure 2: Global Routed Traffic Flow|

A similar result can also be achieved on the switch to which the F5 is
attached, by publishing the VIP subnet in IGP and using a static route
to point the VIP traffic to the F5 device.

The MX should attract the reverse traffic from the pool members going
back to the F5.

Routing Traffic to Pool Members
'''''''''''''''''''''''''''''''

For post load balancing traffic going from the F5 device to the pool
members, the MX Series device needs to attract traffic for all the
tenant networks.

Routing Reverse Traffic from Pool Members to the F5 Device
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

The MX should attract the reverse traffic from the pool members going
back to the F5.

Initial Configuration on an F5 Device
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  The operator is responsible for ensuring that the F5 device attracts
   traffic to all VIP subnets by injecting the route for the VIP subnet
   into IGP. Alternately, the switch to which F5 is connected can
   advertise the VIP subnet route and use the static route to send VIP
   traffic to the F5 device.

-  In the global routed mode, the F5 uses AutoMap SNAT for all VIP
   traffic.

Initial Configuration on an MX Series Device Used as DC Gateway
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  The operator must identify a super-net that contains all tenant
   network subnets (pool members across multiple pools) and advertise
   its route into corporate and fabric networks, using IGP (preferred)
   or static routes.

-  The operator must add a static route for the super-net into inet.0
   with a next-hop of public.inet.0.

-  The operator must create a public VRF and get its default route
   imported into the VRF. This is to attract the return traffic from
   pool members to the F5 device (VIP destination).

Configuration on MX Device for Each Pool Member
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  For each member virtual network, the operator adds a policy to
   connect the member pool virtual network to the public virtual
   network.

-  As new member virtual networks are connected to the public virtual
   network by policy, corresponding targets are imported by the public
   VRF on MX. The Contrail Device Manager generates the configuration of
   import, export targets for public VRF on the MX device.

-  The operator must ensure that security group rules for the member
   virtual network ports allow traffic coming from the F5 device.

Example: Creating a Load Balancer
---------------------------------

Use the following steps to create a load balancer in Contrail Release
3.0 and greater.

1. To configure a service appliance set, use the script in
   ``/opt/contrail/utils`` to create a load balancer provider. With the
   script, you specify the driver and name of the selected provider.
   Additional configuration can be performed using the key-value pair
   property configuration.

   ``/opt/contrail/utils/service_appliance_set.py --api_server_ip <ip address>--api_server_port 8082 --oper add --admin_user admin --admin_password <password> --admin_tenant_name admin --name f5 --driver "svc_monitor.services.loadbalancer.drivers.f5.f5_driver.OpencontrailF5LoadbalancerDriver" --properties '{"use_snat": "True", "num_snat": "1", "global_routed_mode":"True", "sync_mode": "replication", "vip_vlan": "trial2"}'``

2. Add the actual device information of the load balancer.

   ``/opt/contrail/utils/service_appliance.py --api_server_ip <ip address>--api_server_port 8082 --oper add --admin_user admin --admin_password <password> --admin_tenant_name admin --name bigip --service_appliance_set f5 --device_ip 10.204.216.113 --user_credential '{"user": "admin", "password": "<password>"}'``

3. Refer to the load balancer provider while configuring the pool.

   ``neutron lb-pool-create --lb-method ROUND_ROBIN --name web_service --protocol HTTP --provider "f5" --subnet-id <subnet id>``

4. Add members to the load balancer pool. Both bare metal webserver and
   overlay webserver are allowed as pool members. The F5 device can load
   balance the traffic among all pool members.

   ``neutron lb-member-create --address <ip address>--protocol-port 8080 --weight 3 web_service``

   ``neutron lb-member-create --address <ip address> --protocol-port 8080 --weight 2 web_service``

5. Create a VIP for the load balancer pool.

   ``neutron lb-vip-create --name httpserver --protocol-port 80 --protocol HTTP web_service --subnet-id <subnet id>``

6. Create the health monitor and associate it with the load balancer
   pool.

   ``neutron lb-healthmonitor-create --delay 3 --type HTTP --max-retries 3 --timeout 3``

   ``neutron lb-healthmonitor-associate <nnnnn-nnnnn-nnnn-> web_service``

Using the Avi Networks Load Balancer for Contrail
-------------------------------------------------

If you are using the Avi LBaaS driver in an OpenStack Contrail
environment, there are two possible modes that are mutually-exclusive.
The Avi Vantage cloud configuration is exactly the same in both modes:

-  | Neutron-based Avi LBaaS driver
   | In this mode, the Avi LBaaS driver derives from Neutron and resides
     in the Neutron server process. This mode enables coexistence of
     multiple Neutron LBaaS providers.

-  | Contrail-based Avi LBaaS driver
   | In this mode, the Avi LBaaS driver derives from Contrail and
     resides in the service-monitor process. This mode enables
     coexistence of multiple Contrail LBaaS providers.

   **Note**

   In a Contrail environment, you cannot have a mix of Contrail LBaaS
   and Neutron LBaaS. You must select a mode that is compatible with the
   current environment.

Installing the Avi LBaaS Neutron Driver
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the following procedure to install the Avi Networks LBaaS load
balancer driver for the Neutron server for Contrail.

The following steps are performed on the Neutron server host.

1. Determine the installed version of the Contrail Neutron plugin.

   .. raw:: html

      <div id="jd0e374" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      $ contrail-version neutron-plugin-contrail
      Package Version
      ------------------------- ------------
      neutron-plugin-contrail 3.0.2.0-51

   .. raw:: html

      </div>

   .. raw:: html

      </div>

2. Adjust the ``neutron.conf``\ database connection URL.

   .. raw:: html

      <div id="jd0e383" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      $ vi /etc/neutron/neutron.conf
      # if using mysql
      connection = mysql+pymysql://neutron:c0ntrail123@127.0.0.1/neutron

   .. raw:: html

      </div>

   .. raw:: html

      </div>

3. Populate and upgrade the Neutron database schema.

   .. raw:: html

      <div id="jd0e389" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      # to upgrade to head
      $ neutron-db-manage upgrade head
      # to upgrade to a specific version
      $ neutron-db-manage --config-file /etc/neutron/neutron.conf upgrade liberty

   .. raw:: html

      </div>

   .. raw:: html

      </div>

4. Drop foreign key constraints.

   .. raw:: html

      <div id="jd0e395" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      # obtain current mysql token
      $ cat /etc/contrail/mysql.token
      fabe17d9dd5ae798f7ea

      $ mysql -u root -p
      Enter password: fabe17d9dd5ae798f7ea

      mysql> use neutron;

      mysql> show create table vips;
      # CONSTRAINT `vips_ibfk_1` FOREIGN KEY (`port_id`) REFERENCES `ports` (`id`) - ports table is not used by Contrail
      mysql> alter table vips drop FOREIGN KEY vips_ibfk_1;

      mysql> show create table lbaas_loadbalancers;
      # CONSTRAINT `fk_lbaas_loadbalancers_ports_id` FOREIGN KEY (`vip_port_id`) REFERENCES `ports` (`id`)
      mysql> alter table lbaas_loadbalancers drop FOREIGN KEY fk_lbaas_loadbalancers_ports_id;

   .. raw:: html

      </div>

   .. raw:: html

      </div>

5. To install the Avi LBaaS plugin, continue with steps from the readme
   file that downloads with the Avi LBaaS software. You can perform
   either a local installation or a manual installation. The following
   are sample installation steps.

   -  For a local installation:

      .. raw:: html

         <div id="jd0e405" class="sample" dir="ltr">

      .. raw:: html

         <div class="output" dir="ltr">

      ::

         # LBaaS v1 driver
         $ ./install.sh --aname avi_adc --aip

           <controller_ip|controller_vip>
             --auser
            
              --apass
             
         # LBaaS v2 driver 
         $ ./install.sh --aname avi_adc_v2 --aip
              <controller_ip|controller_vip>
                --auser
               
                 --apass
                
                  --v2

      .. raw:: html

         </div>

      .. raw:: html

         </div>

   -  For a manual installation:

      .. raw:: html

         <div id="jd0e411" class="sample" dir="ltr">

      .. raw:: html

         <div class="output" dir="ltr">

      ::

         # LBaaS v1 driver
         $ vi /etc/neutron/neutron.conf
         #service_plugins = neutron_plugin_contrail.plugins.opencontrail.loadbalancer.plugin.LoadBalancerPlugin
         service_plugins = neutron_lbaas.services.loadbalancer.plugin.LoadBalancerPlugin
         [service_providers]
         service_provider = LOADBALANCER:Avi_ADC:neutron_lbaas.services.loadbalancer.drivers.avi.avi_driver.AviLbaaSDriver

         [avi_adc]
         address=10.1.11.4
         user=admin
         password=avi123
         cloud=jcos

         # LBaaS v2 driver
         $ vi /etc/neutron/neutron.conf
         #service_plugins = neutron_plugin_contrail.plugins.opencontrail.loadbalancer.plugin.LoadBalancerPlugin
         service_plugins = neutron_lbaas.services.loadbalancer.plugin.LoadBalancerPluginv2
         [service_providers]
         service_provider = LOADBALANCERV2:avi_adc_v2:neutron_lbaas.drivers.avi.driver.AviDriver

         [avi_adc_v2]
         controller_ip=10.1.11.3
         username=admin
         password=avi123

         $ service neutron-server restart
         $ neutron service-provider-list

      .. raw:: html

         </div>

      .. raw:: html

         </div>

Installing the Avi LBaaS Contrail Driver
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the following procedure to install the Avi Networks LBaaS load
balancer driver for Contrail.

The following steps are performed on the Contrail ``api-server`` host.

1. Determine the installed version of the Contrail Neutron plugin.

   .. raw:: html

      <div id="jd0e429" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      $ contrail-version neutron-plugin-contrail
      Package Version
      ------------------------- ------------
      neutron-plugin-contrail 3.0.2.0-51

   .. raw:: html

      </div>

   .. raw:: html

      </div>

2. Install the Avi driver.

   .. raw:: html

      <div id="jd0e435" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      # LBaaS v2 driver
      $ ./install.sh --aname ocavi_adc_v2 --aip

        <controller_ip|controller_vip>
          --auser
         
           --apass
          
            --v2 --no-restart --no-confmodify

   .. raw:: html

      </div>

   .. raw:: html

      </div>

3. Set up the service appliance set.\ **Note**\ 

   If ``neutron_lbaas`` doesn’t exist on the ``api-server`` node, adjust
   the driver path to the correct path location for ``neutron_lbaas``.

   ``$ /opt/contrail/utils/service_appliance_set.py --api_server_ip 10.xx.xx.100 --api_server_port 8082 --oper add --admin_user admin --admin_password <password> --admin_tenant_name admin --name ocavi_adc_v2 --driver "neutron_lbaas.drivers.avi.avi_ocdriver.OpencontrailAviLoadbalancerDriver" --properties '{"address": "10.1.xx.3", "user": "admin", "password": "avi123", "cloud": "Default-Cloud"}'``

4. To delete the service appliance set.

   ``$ /opt/contrail/utils/service_appliance_set.py --api_server_ip 10.xx.xx.100 --api_server_port 8082 --oper del --admin_user admin --admin_password <password> --admin_tenant_name admin --name ocavi_adc_v2``

Configuring the Avi Controller
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. If OpenStack endpoints are private IPs and Contrail provides a public
   front-end IP to those endpoints, use iptables to DNAT. On the
   AviController only, perform iptable NAT to reach the private IPs.

   ``$ iptables -t nat -I OUTPUT --dest 17x.xx.xx.50 -j DNAT --to-dest 10.xx.xx.100``

2. To configure the Avi controller during cloud configuration, select
   the “Integration with Contrail” checkbox and provide the endpoint URL
   of the Contrail VNC api-server. Use the Keystone credentials from the
   OpenStack configuration to authenticate with the api-server service.

   .. raw:: html

      <div id="jd0e475" class="sample" dir="ltr">

   **Example Configuration Settings**

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      : > show cloud jcos
          +---------------------------+--------------------------------------------+
          | Field                     | Value                                      |
          +---------------------------+--------------------------------------------+
          | uuid                      | cloud-104bb7e6-a9d2-4b34-a4c5-d94be659bb91 |
          | name                      | jcos                                       |
          | vtype                     | CLOUD_OPENSTACK                            |
          | openstack_configuration   |                                            |
          |   username                | admin                                      |
          |   admin_tenant            | demo                                       |
          |   keystone_host           | 17x.xx.xx.50                               |
          |   mgmt_network_name       | mgmtnw                                     |
          |   privilege               | WRITE_ACCESS                               |
          |   use_keystone_auth       | True                                       |
          |   region                  | RegionOne                                  |
          |   hypervisor              | KVM                                        |
          |   tenant_se               | True                                       |
          |   import_keystone_tenants | True                                       |
          |   anti_affinity           | True                                       |
          |   port_security           | False                                      |
          |   security_groups         | True                                       |
          |   allowed_address_pairs   | True                                       |
          |   free_floatingips        | True                                       |
          |   img_format              | OS_IMG_FMT_AUTO                            |
          |   use_admin_url           | True                                       |
          |   use_internal_endpoints  | False                                      |
          |   config_drive            | True                                       |
          |   insecure                | True                                       |
          |   intf_sec_ips            | False                                      |
          |   external_networks       | False                                      |
          |   neutron_rbac            | True                                       |
          |   nuage_port              | 8443                                       |
          |   contrail_endpoint       | http://10.10.10.100:8082                   |
          | apic_mode                 | False                                      |
          | dhcp_enabled              | True                                       |
          | mtu                       | 1500 bytes                                 |
          | prefer_static_routes      | False                                      |
          | enable_vip_static_routes  | False                                      |
          | license_type              | LIC_CORES                                  |
          | tenant_ref                | admin                                      |
          +---------------------------+--------------------------------------------+

   .. raw:: html

      </div>

   .. raw:: html

      </div>

 

.. |Figure 1: Contrail LBaaS components with neutron-lbaas| image:: documentation/images/g300524.png
.. |Figure 2: Global Routed Traffic Flow| image:: documentation/images/g300525.png
