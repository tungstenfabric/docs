Using Contrail Tools
====================

 

Contrail-tools container provides centralized location for all the
available tools and CLI commands in one place.

Starting with Contrail Networking Release 2008, contrail-tools command
will be installed by default.

contrail-tools command enables you to log in to the contrail-tools
container and execute the tool. Additionally, the command will kill the
container on exit.

`Table 1 <contrail-tools.html#AvailableTools>`__ provides a list of
available tools and CLI options in the *contrail-tools* package.

Table 1: Available Tools and CLI options

+------------------------+--------------------------------------------+
| Tools and CLI commands | Description                                |
+========================+============================================+
| dpdkinfo               | Adds support to display bond, lacp, Nic,   |
|                        | mempool, core, and app information.        |
+------------------------+--------------------------------------------+
| dpdkvifstats.py        | Display the PPS statistics of DPDK         |
|                        | vRouter.                                   |
+------------------------+--------------------------------------------+
| dropstats​             | Inspects packet drop counters in the       |
|                        | vRouter.                                   |
+------------------------+--------------------------------------------+
| flow                   | Displays active flows in the system.       |
+------------------------+--------------------------------------------+
| mirror                 | Displays the mirror table entries.         |
+------------------------+--------------------------------------------+
| mpls                   | Displays the input label map programmed    |
|                        | into the vRouter.                          |
+------------------------+--------------------------------------------+
| nh                     | Displays the next hops that the vRouter    |
|                        | knows.                                     |
+------------------------+--------------------------------------------+
| qosmap                 | Retrieves and sets QoS mappings.           |
+------------------------+--------------------------------------------+
| rt                     | Displays routes in virtual routing and     |
|                        | forwarding (VRF).                          |
+------------------------+--------------------------------------------+
| sandump                | Captures the Sandesh messages from the     |
|                        | netlink connection between Agent and       |
|                        | vRouter.                                   |
+------------------------+--------------------------------------------+
| vif                    | Inspects vRouter interfaces associated     |
|                        | with the vRouter module.                   |
+------------------------+--------------------------------------------+
| vifdump                | Captures and analyzes packets from DPDK    |
|                        | interface.                                 |
+------------------------+--------------------------------------------+
| vrfstats​              | Displays the next hop statistics for the   |
|                        | VRF.                                       |
+------------------------+--------------------------------------------+
| vrftable               | Displays the interface mapping for each    |
|                        | VRF for a host-based firewall feature.     |
+------------------------+--------------------------------------------+
| vrinfo                 | Displays internal state of DPDK/Kernel     |
|                        | vRouter.                                   |
+------------------------+--------------------------------------------+
| vrmemstats             | Displays the vRouter memory usage          |
|                        | statistics.                                |
+------------------------+--------------------------------------------+
| vrouter                | Display the vRouter information.           |
+------------------------+--------------------------------------------+
| vxlan                  | Displays the vxlan table entries.          |
+------------------------+--------------------------------------------+

There are 2 ways to execute the contrail-tools command:

-  Execute contrail-tools command to login to the container.

   .. raw:: html

      <div id="jd0e180" class="sample" dir="ltr">

   For example:

   .. raw:: html

      <div id="jd0e183" dir="ltr">

   ``[root]# contrail-tools``

   .. raw:: html

      </div>

   .. raw:: html

      <div id="jd0e185" dir="ltr">

   ``(contrail-tools)[root /]$ vif​``

   .. raw:: html

      </div>

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      Usage: vif [--create <intf_name> --mac <mac>]​
         [--add <intf_name> --mac <mac> --vrf <vrf>​
         --type [vhost|agent|physical|virtual|monitoring]​
         --transport [eth|pmd|virtual|socket]​
         --xconnect <physical interface name>​
         --policy, --vhost-phys, --dhcp-enable]​
         --vif <vif ID> --id <intf_id> --pmd --pci]​
         [--delete <intf_id>|<intf_name>]​
         [--get <intf_id>][--kernel][--core <core number>][--rate] [--get-drop-stats]​
         [--set <intf_id> --vlan <vlan_id> --vrf <vrf_id>]​
         [--list][--core <core number>][--rate]​
         [--sock-dir <sock dir>]​
         [--help]

   .. raw:: html

      </div>

   .. raw:: html

      </div>

-  Execute contrail-tools command with the CLI as argument.

   .. raw:: html

      <div id="jd0e195" class="sample" dir="ltr">

   For example:

   .. raw:: html

      <div id="jd0e198" dir="ltr">

   ``[root]# contrail-tools vif``

   .. raw:: html

      </div>

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      Usage: vif [--create <intf_name> --mac <mac>]​
         [--add <intf_name> --mac <mac> --vrf <vrf>​
         --type [vhost|agent|physical|virtual|monitoring]​
         --transport [eth|pmd|virtual|socket]​
         --xconnect <physical interface name>​
         --policy, --vhost-phys, --dhcp-enable]​
         --vif <vif ID> --id <intf_id> --pmd --pci]​
         [--delete <intf_id>|<intf_name>]​
         [--get <intf_id>][--kernel][--core <core number>][--rate] [--get-drop-stats]​
         [--set <intf_id> --vlan <vlan_id> --vrf <vrf_id>]​
         [--list][--core <core number>][--rate]​
         [--sock-dir <sock dir>]​
         [--help]

   .. raw:: html

      </div>

   .. raw:: html

      </div>

.. raw:: html

   <div class="table">

.. raw:: html

   <div class="caption">

Release History Table

.. raw:: html

   </div>

.. raw:: html

   <div class="table-row table-head">

.. raw:: html

   <div class="table-cell">

Release

.. raw:: html

   </div>

.. raw:: html

   <div class="table-cell">

Description

.. raw:: html

   </div>

.. raw:: html

   </div>

.. raw:: html

   <div class="table-row">

.. raw:: html

   <div class="table-cell">

`2008 <#jd0e12>`__

.. raw:: html

   </div>

.. raw:: html

   <div class="table-cell">

Starting with Contrail Networking Release 2008, contrail-tools command
will be installed by default.

.. raw:: html

   </div>

.. raw:: html

   </div>

.. raw:: html

   </div>

 
