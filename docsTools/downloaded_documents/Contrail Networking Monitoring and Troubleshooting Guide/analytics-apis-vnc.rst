Contrail Analytics Application Programming Interfaces (APIs) and User-Visible Entities (UVEs)
=============================================================================================

 

The Contrail **analytics-api** server provides a REST API interface to
extract the operational state of the Contrail system.

APIs are used by the Contrail Web user interface to present the
operational state to users. Other applications might also use the
server's REST APIs for analytics or other uses.

This section describes some of the more common APIs and their uses. To
see all of the available APIs, navigate the URL tree at the REST
interface, starting at the root
\**http://``<ip>``:``<analytics-api-port>`` .**You can also view
Contrail API information at:
http://configuration-schema-documentation.s3-website-us-west-1.amazonaws.com/R3.2/
.

User-Visible Entities
---------------------

In Contrail, a User-Visible Entity (UVE) is an object entity that might
span multiple components in Contrail and might require aggregation
before the complete information of the UVE is presented. Examples of
UVEs in Contrail are virtual network, virtual machine, vRouter, and
similar objects. Complete operational information for a virtual network
might span multiple vRouters, config nodes, control nodes, and the like.
The analytics-api server aggregates all of this information through REST
APIs.

To get information about a UVE, you must have the UVE type and the UVE
key. In Contrail, UVEs are identified by type, such as virtual network,
virtual machine, vRouter, and so on. A system-wide unique key is
associated with each UVE. The key type could be different, based on the
UVE type. For example, perhaps a virtual network uses its name as its
UVE key, and in the same system, a virtual machine uses its UUID as its
key.

The URL ``/analytics/uves`` shows the list of all UVE types available in
the system.

The following is sample output from ``/analytics/uves``:

.. raw:: html

   <div id="jd0e51" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   [
   {
   href: "http://<system IP>:8081/analytics/uves/xmpp-peers",
   name: "xmpp-peers"
   },
   {
   href: "http://<system IP>:8081/analytics/uves/service-instances",
   name: "service-instances"
   },
   {
   href: "http://<system IP>:8081/analytics/uves/config-nodes",
   name: "config-nodes"
   },
   {
   href: "http://<system IP>:8081/analytics/uves/virtual-machines",
   name: "virtual-machines"
   },
   {
   href: "http://<system IP>:8081/analytics/uves/bgp-routers",
   name: "bgp-routers"
   },
   {
   href: "http://<system IP>:8081/analytics/uves/collectors",
   name: "collectors"
   },
   {
   href: "http://<system IP>:8081/analytics/uves/service-chains",
   name: "service-chains"
   },
   {
   href: "http://<system IP>:8081/analytics/uves/generators",
   name: "generators"
   },
   {
   href: "http://<system IP>:8081/analytics/uves/bgp-peers",
   name: "bgp-peers"
   },
   {
   href: "http://<system IP>:8081/analytics/uves/virtual-networks",
   name: "virtual-networks"
   },
   {
   href: "http://<system IP>:8081/analytics/uves/vrouters",
   name: "vrouters"
   },
   {
   href: "http://<system IP>:8081/analytics/uves/dns-nodes",
   name: "dns-nodes"
   }
   ]

.. raw:: html

   </div>

.. raw:: html

   </div>

Common UVEs in Contrail
-----------------------

This section presents descriptions of some common UVEs in Contrail.

Virtual Network UVE
-------------------

This UVE provides information associated with a virtual network, such
as:

-  list of networks connected to this network

-  list of virtual machines spawned in this network

-  list of access control lists (ACLs) associated with this virtual
   network

-  global input and output statistics

-  input and output statistics per virtual network pair

The REST API to get a UVE for a specific virtual network is through HTTP
GET, using the URL:

``/analytics/uves/virtual-network/<key>``

The REST API to get UVEs for all virtual machines is through HTTP GET,
using the URL:

``/analytics/uves/virtual-networks``

Virtual Machine UVE
-------------------

This UVE provides information associated with a virtual machine, such
as:

-  list of interfaces in this virtual machine

-  list of floating IPs associated with each interface

-  input and output statistics

The REST API to get a UVE for a specific virtual machine is through HTTP
GET, using the URL:

``/analytics/uves/virtual-machine/<key>``

The REST API to get UVEs for all virtual machines is through HTTP GET,
using the URL:

``/analytics/uves/virtual-machines``

vRouter UVE
-----------

This UVE provides information associated with a vRouter, such as:

-  virtual networks present on this vRouter

-  virtual machines spawned on the server of this vRouter

-  statistics of the traffic flowing through this vRouter

The REST API to get a UVE for a specific vRouter is through HTTP GET,
using the URL:

``/analytics/uves/vrouter/<key>``

The REST API to get UVEs for all virtual machines is through HTTP GET,
using the URL:

``/analytics/uves/vrouters``

UVEs for Contrail Nodes
-----------------------

There are multiple node types in Contrail (including the node type
vRouter previously described). Other node types include control node,
config node, analytics node, and compute node.

There is a UVE for each node type. The common information associated
with each node UVE includes:

-  the IP address of the node

-  a list of processes running on the node

-  the CPU and memory utilization of the running processes

Each UVE also has node-specific information, such as:

-  the control node UVE has information about its connectivity to the
   vRouter and other control nodes

-  the analytics node UVE has information about the number of generators
   connected

The REST API to get a UVE for a specific config node is through HTTP
GET, using the URL:

``/analytics/uves/config-node/<key>``

The REST API to get UVEs for all config nodes is through HTTP GET, using
the URL:

``/analytics/uves/config-nodes``

**Note**

Use similar syntax to get UVES for each of the different types of nodes,
substituting the node type that you want in place of ``config-node.``

Wild Card Query of UVEs
-----------------------

You can use wildcard queries when you want to get multiple UVEs at the
same time. Example queries are the following:

The following HTTP GET with wildcard retrieves all virtual network UVEs:

``/analytics/uves/virtual-network/*``

The following HTTP GET with wildcard retrieves all virtual network UVEs
with name starting with ``project1``:​

``/analytics/uves/virtual-network/project1*``

Filtering UVE Information
-------------------------

It is possible to retrieve filtered UVE information. The following flags
enable you to retrieve partial, filtered information about UVEs.

Supported filter flags include:

-  ``sfilt`` : filter by source (usually the hostname of the generator)

-  ``mfilt`` : filter by module (the module name of the generator)

-  ``cfilt`` : filter by content, useful when only part of a UVE needs
   to be retrieved

-  ``kfilt`` : filter by UVE keys, useful to get multiple, but not all,
   UVEs of a particular type

.. raw:: html

   <div id="jd0e276" class="example" dir="ltr">

Examples
~~~~~~~~

.. raw:: html

   </div>

The following HTTP GET with filter retrieves information about virtual
network ``vn1`` as provided by the source ``src1``:

``/analytics/uves/virtual-network/vn1?sfilt=src1``

The following HTTP GET with filter retrieves information about virtual
network ``vn1`` as provided by all ``ApiServer`` modules:​

``​/analytics/uves/virtual-network/vn1?mfilt=ApiServer``

.. raw:: html

   <div id="jd0e303" class="example" dir="ltr">

Example Output: Virtual Network UVE
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example output for a virtual network UVE:

::

   [user@host ~]# curl <system IP>:8081/analytics/virtual-network/default-domain:demo:front-end | python -mjson.tool
     % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                    Dload  Upload   Total   Spent    Left  Speed
   100  2576  100  2576    0     0   152k      0 --:--:-- --:--:-- --:--:--  157k
   {
       "UveVirtualNetworkAgent": {
           "acl": [
               [
                   {
                       "@type": "string"
                   },
                   "a3s18:VRouterAgent"
               ]
           ],
           "in_bytes": {
               "#text": "2232972057",
               "@aggtype": "counter",
               "@type": "i64"
           },
           "in_stats": {
               "@aggtype": "append",
               "@type": "list",
               "list": {
                   "@size": "3",
                   "@type": "struct",
                   "UveInterVnStats": [
                       {
                           "bytes": {
                               "#text": "2114516371",
                               "@type": "i64"
                           },
                           "other_vn": {
                               "#text": "default-domain:demo:back-end",
                               "@aggtype": "listkey",
                               "@type": "string"
                           },
                           "tpkts": {
                               "#text": "5122001",
                               "@type": "i64"
                           }
                       },
                       {
                           "bytes": {
                               "#text": "1152123",
                               "@type": "i64"
                           },
                           "other_vn": {
                               "#text": "__FABRIC__",
                               "@aggtype": "listkey",
                               "@type": "string"
                           },
                           "tpkts": {
                               "#text": "11323",
                               "@type": "i64"
                           }
                       },
                       {
                           "bytes": {
                               "#text": "8192",
                               "@type": "i64"
                           },
                           "other_vn": {
                               "#text": "default-domain:demo:front-end",
                               "@aggtype": "listkey",
                                "@type": "string"
                           },
                           "tpkts": {
                               "#text": "50",
                               "@type": "i64"
                           }
                       }
                   ]
               }
           },
           "in_tpkts": {
               "#text": "5156342",
               "@aggtype": "counter",
               "@type": "i64"
           },
           "interface_list": {
               "@aggtype": "union",
               "@type": "list",
               "list": {
                   "@size": "1",
                   "@type": "string",
                   "element": [
                       "tap2158f77c-ec"
                   ]
               }
           },
           "out_bytes": {
               "#text": "2187615961",
               "@aggtype": "counter",
               "@type": "i64"
           },
    "out_stats": {
               "@aggtype": "append",
               "@type": "list",
               "list": {
                   "@size": "4",
                   "@type": "struct",
                   "UveInterVnStats": [
                       {
                           "bytes": {
                               "#text": "2159083215",
                               "@type": "i64"
                           },
                           "other_vn": {
                               "#text": "default-domain:demo:back-end",
                               "@aggtype": "listkey",
                               "@type": "string"
                           },
                           "tpkts": {
                               "#text": "5143693",
                               "@type": "i64"
                           }
                       },
                       {
                           "bytes": {
                               "#text": "1603041",
                               "@type": "i64"
                           },
                           "other_vn": {
                               "#text": "__FABRIC__",
                               "@aggtype": "listkey",
                               "@type": "string"
                           },
                            "tpkts": {
                               "#text": "9595",
                               "@type": "i64"
                           }
                       },
                       {
                           "bytes": {
                               "#text": "24608",
                               "@type": "i64"
                           },
                           "other_vn": {
                               "#text": "__UNKNOWN__",
                               "@aggtype": "listkey",
                               "@type": "string"
                           },
                           "tpkts": {
                               "#text": "408",
                               "@type": "i64"
                           }
                       },
                       {
                           "bytes": {
                               "#text": "8192",
                               "@type": "i64"
                           },
                           "other_vn": {
                               "#text": "default-domain:demo:front-end",
                               "@aggtype": "listkey",
                               "@type": "string"
                           },
                             "tpkts": {
                               "#text": "50",
                               "@type": "i64"
                           }
                       }
                   ]
               }
           },
           "out_tpkts": {
               "#text": "5134830",
               "@aggtype": "counter",
               "@type": "i64"
           },
           "virtualmachine_list": {
               "@aggtype": "union",
               "@type": "list",
               "list": {
                   "@size": "1",
                   "@type": "string",
                   "element": [
                       "dd09f8c3-32a8-456f-b8cc-fab15189f50f"
                   ]
               } }
       },
       "UveVirtualNetworkConfig": {
           "connected_networks": {
               "@aggtype": "union",
               "@type": "list",
               "list": {
                   "@size": "1",
                   "@type": "string",
                   "element": [
                       "default-domain:demo:back-end"
                   ]
               }
           },
           "routing_instance_list": {
               "@aggtype": "union",
               "@type": "list",
               "list": {
                   "@size": "1",
                   "@type": "string",
                   "element": [
                       "front-end"
                   ]
               }
           },
           "total_acl_rules": [
               [
                   { 
                      "#text": "3",
                       "@type": "i32"
                   },
                   ":",
                   "a3s14:Schema"
               ]
           ]
       }
   }

.. raw:: html

   </div>

.. raw:: html

   <div id="jd0e314" class="example" dir="ltr">

Example Output: Virtual Machine UVE
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example output for a virtual machine UVE:

::

   [user@host ~]# curl <system IP>:8081/analytics/virtual-machine/f38eb47e-63d2-4b39-80de-8fe68e6af1e4 | python -mjson.tool
     % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                    Dload  Upload   Total   Spent    Left  Speed
   100   736  100   736    0     0   160k      0 --:--:-- --:--:-- --:--:--  179k
   {
       "UveVirtualMachineAgent": {
           "interface_list": [
               [
                   {
                       "@type": "list",
                       "list": {
                           "@size": "1",
                           "@type": "struct",
                           "VmInterfaceAgent": [
                               {
                                   "in_bytes": {
                                       "#text": "2188895907",
                                       "@aggtype": "counter",
                                       "@type": "i64"
                                   },
                                   "in_pkts": {
                                       "#text": "5130901",
                                       "@aggtype": "counter",
                                       "@type": "i64"
                                   },
                                   "ip_address": {
                                       "#text": "192.168.2.253",
                                       "@type": "string"
                                   },
                                   "name": {
                                       "#text": "f38eb47e-63d2-4b39-80de-8fe68e6af1e4:ccb085a0-c994-4034-be0f-6fd5ad08ce83",
                                       "@type": "string"
                                   },
                                   "out_bytes": {
                                       "#text": "2201821626",
                                       "@aggtype": "counter",
                                       "@type": "i64"
                                   },
                                   "out_pkts": {
                                       "#text": "5153526",
                                       "@aggtype": "counter",
                                       "@type": "i64"
                                   },
                                   "virtual_network": {
                                       "#text": "default-domain:demo:back-end",
                                       "@aggtype": "listkey",
                                       "@type": "string"
                                   }
                               }
                           ]
                       }
                   },
                   "a3s19:VRouterAgent"
               ]
           ]
       }
   }

.. raw:: html

   </div>

.. raw:: html

   <div id="jd0e325" class="example" dir="ltr">

Example Output: vRouter UVE
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example output for a vRouter UVE:

::

   [user@host ~]# curl <system IP>:8081/analytics/vrouter/a3s18 | python -mjson.tool
     % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                    Dload  Upload   Total   Spent    Left  Speed
   100   706  100   706    0     0   142k      0 --:--:-- --:--:-- --:--:--  172k
   {
       "VrouterAgent": {
           "collector": [
               [
                   {
                       "#text": "10.xx.17.1",
                       "@type": "string"
                   },
                   "a3s18:VRouterAgent"
               ]
           ],
           "connected_networks": [
               [
                   {
                       "@type": "list",
                       "list": {
                           "@size": "1",
                           "@type": "string",
                           "element": [
                               "default-domain:demo:front-end"
                           ]
                       }
                   },
                   "a3s18:VRouterAgent"
               ]
           ],
           "interface_list": [
               [
                   {
                       "@type": "list",
                       "list": {
                           "@size": "1",
                           "@type": "string",
                           "element": [
                               "tap2158f77c-ec"
                           ]
                       }
                   },
                   "a3s18:VRouterAgent"
               ]
           ],
           "virtual_machine_list": [
               [
                   {
                       "@type": "list",
                       "list": {
                           "@size": "1",
                           "@type": "string",
                           "element": [
                               "dd09f8c3-32a8-456f-b8cc-fab15189f50f"
                           ]
                       }
                   },
                   "a3s18:VRouterAgent"
               ]
           ],
           "xmpp_peer_list": [
               [
                   {
                       "@type": "list",
                       "list": {
                           "@size": "2",
                           "@type": "string",
                           "element": [
                               "10.xx.17.2",
                               "10.xx.17.3"
                           ]
                       }
                   },
                   "a3s18:VRouterAgent"
               ]
           ]
       }
   }

.. raw:: html

   </div>

 
