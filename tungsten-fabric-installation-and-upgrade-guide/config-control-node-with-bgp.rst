Configuring the Control Node with BGP
=====================================

 

.. raw:: html

   <div id="intro">

.. raw:: html

   <div class="mini-toc-intro">

An important task after a successful installation is to configure the
control node with BGP. This procedure shows how to configure basic BGP
peering between one or more virtual network controller control nodes and
any external BGP speakers. External BGP speakers, such as Juniper
Networks MX80 routers, are needed for connectivity to instances on the
virtual network from an external infrastructure or a public network.

Before you begin, ensure that the following tasks are completed:

-  The Contrail Controller base system image has been installed on all
   servers.

-  The role-based services have been assigned and provisioned.

-  IP connectivity has been verified between all nodes of the Contrail
   Controller.

-  You have access to Contrail Web User Interface (UI) or Contrail
   Command User Interface (UI). You can access the user interface at
   **http://``nn.nn.nn.nn``:8143**, where **``nn.nn.nn.nn``** is the IP
   address of the configuration node server that is running the contrail
   service.

These topics provide instructions to configure the Control Node with
BGP.

.. raw:: html

   </div>

.. raw:: html

   </div>

Configuring the Control Node from Contrail Web UI
-------------------------------------------------

To configure BGP peering in the control node:

1. From the Contrail Controller module control node
   (**http://``nn.nn.nn.nn``:8143**), select **Configure >
   Infrastructure > BGP Routers**; see
   `Figure 1 <config-control-node-with-bgp.html#config-bgp-peers>`__.

   |Figure 1: Configure> Infrastructure > BGP Routers|

   A summary screen of the control nodes and BGP routers is displayed;
   see
   `Figure 2 <config-control-node-with-bgp.html#control-nodes-summary>`__.

   |Figure 2: BGP Routers Summary|

2. (Optional) The global AS number is 64512 by default. To change the AS
   number, on the **BGP Router** summary screen click the gear wheel and
   select **Edit**. In the Edit BGP Router window enter the new number.

3. To create control nodes and BGP routers, on the **BGP Routers**
   summary screen, click the |image1|  icon. The **Create BGP
   Router** window is displayed; see
   `Figure 3 <config-control-node-with-bgp.html#add-bgp-peer>`__.

   |Figure 3: Create BGP Router|

4. In the **Create BGP Router** window, click **BGP Router** to add a
   new BGP router or click **Control Node** to add control nodes.

   For each node you want to add, populate the fields with values for
   your system. See
   `Table 1 <config-control-node-with-bgp.html#bgp-peers>`__.

   Table 1: Create BGP Router Fields

   +-------------------------+-------------------------------------------+
   | Field                   | Description                               |
   +=========================+===========================================+
   | **Hostname**            | Enter a name for the node being added.    |
   +-------------------------+-------------------------------------------+
   | **Vendor ID**           | Required for external peers. Populate     |
   |                         | with a text identifier, for example,      |
   |                         | “MX-0”. (BGP peer only)                   |
   +-------------------------+-------------------------------------------+
   | **IP Address**          | The IP address of the node.               |
   +-------------------------+-------------------------------------------+
   | **Router ID**           | Enter the router ID.                      |
   +-------------------------+-------------------------------------------+
   | **Autonomous System**   | Enter the AS number in the range 1-65535  |
   |                         | for the node. (BGP peer only)             |
   +-------------------------+-------------------------------------------+
   | **Address Families**    | Enter the address family, for example,    |
   |                         | **inet-vpn**                              |
   +-------------------------+-------------------------------------------+
   | **Hold Time**           | BGP session hold time. The default is 90  |
   |                         | seconds; change if needed.                |
   +-------------------------+-------------------------------------------+
   | **BGP Port**            | The default is 179; change if needed.     |
   +-------------------------+-------------------------------------------+
   | **Authentication Mode** | Enable MD5 authentication if desired.     |
   +-------------------------+-------------------------------------------+
   | **Authentication key**  | Enter the Authentication Key value.       |
   +-------------------------+-------------------------------------------+
   | **Physical Router**     | The type of the physical router.          |
   +-------------------------+-------------------------------------------+
   | **Available Peers**     | Displays peers currently available.       |
   +-------------------------+-------------------------------------------+
   | **Configured Peers**    | Displays peers currently configured.      |
   +-------------------------+-------------------------------------------+

5. Click **Save** to add each node that you create.

6. To configure an existing node as a peer, select it from the list in
   the **Available Peers** box, then click **>>** to move it into the
   **Configured Peers** box.

   Click **<<** to remove a node from the **Configured Peers** box.

7. You can check for peers by selecting **Monitor > Infrastructure >
   Control Nodes**; see
   `Figure 4 <config-control-node-with-bgp.html#control-node-summ>`__.

   |Figure 4: Control Nodes|

   In the **Control Nodes** window, click any hostname in the memory map
   to view its details; see
   `Figure 5 <config-control-node-with-bgp.html#control-node-details>`__.

   |Figure 5: Control Node Details|

8. Click the **Peers** tab to view the peers of a control node; see
   `Figure 6 <config-control-node-with-bgp.html#peer-details>`__.

   |Figure 6: Control Node Peers Tab|

Configuring the Control Node with BGP from Contrail Command
-----------------------------------------------------------

To configure BGP peering in the control node:

1. From Contrail Command UI select **Infrastructure > Cluster >
   Advanced** page.

   Click the **BGP Routers** tab. A list of control nodes and BGP
   routers is displayed. See
   `Figure 7 <config-control-node-with-bgp.html#config-bgp>`__.

   |Figure 7: Infrastructure > Cluster > Advanced > BGP Routers|

2. (Optional) The global AS number is 64512 by default. You can change
   the AS number according to your requirement on the **BGP Router**
   tab, by clicking the **Edit** icon. In the **Edit BGP Router** tab
   enter AS number in the range of 1-65,535. You can also enter the AS
   number in the range of 1-4,294,967,295, when **4 Byte ASN** is
   enabled in **Global Config**.

3. Click the **Create** button on the **BGP Routers** tab. The **Create
   BGP Router** window is displayed. See
   `Figure 8 <config-control-node-with-bgp.html#bgp-create>`__.

   |Figure 8: Create BGP Router|

4. In the **Create BGP Router** page, populate the fields with values to
   create your system. See
   `Table 2 <config-control-node-with-bgp.html#controlnodebgp>`__.

   Table 2: Create BGP Router

   .. raw:: html

      <table data-cellspacing="0" style="border-top:thin solid black;" width="99%">
      <colgroup>
      <col style="width: 50%" />
      <col style="width: 50%" />
      </colgroup>
      <thead>
      <tr class="header">
      <th style="text-align: left;"><p>Fields</p></th>
      <th style="text-align: left;"><p>Description</p></th>
      </tr>
      </thead>
      <tbody>
      <tr class="odd">
      <td style="text-align: left;"><p><strong>Router Type</strong></p></td>
      <td style="text-align: left;"><p>Select the type of router you want create</p></td>
      </tr>
      <tr class="even">
      <td style="text-align: left;"><p><strong>Hostname</strong></p></td>
      <td style="text-align: left;"><p>Enter a name for the node being added.</p></td>
      </tr>
      <tr class="odd">
      <td style="text-align: left;"><p><strong>Vendor ID</strong></p></td>
      <td style="text-align: left;"><p>Required for external peers. Populate with a text identifier, for example, “MX-0”. (BGP peer only)</p></td>
      </tr>
      <tr class="even">
      <td style="text-align: left;"><p><strong>IP Address</strong></p></td>
      <td style="text-align: left;"><p>The IP address of the node.</p></td>
      </tr>
      <tr class="odd">
      <td style="text-align: left;"><p><strong>Router ID</strong></p></td>
      <td style="text-align: left;"><p>Enter the router ID.</p></td>
      </tr>
      <tr class="even">
      <td style="text-align: left;"><p><strong>Autonomous System (AS)</strong></p></td>
      <td style="text-align: left;"><p>Enter autonomous system (AS) number in the range of 1-65,535.</p>
      <p>If you enable <strong>4 Byte ASN</strong> in <strong>Global Config</strong>, you can enter 4-byte AS number in the range of 1-4,294,967,295.</p></td>
      </tr>
      <tr class="odd">
      <td style="text-align: left;"><p><strong>BGP Router ASN</strong></p></td>
      <td style="text-align: left;"><p>Enter the Local-AS number, specific to the associated peers.</p></td>
      </tr>
      <tr class="even">
      <td style="text-align: left;"><p><strong>Address Families</strong></p></td>
      <td style="text-align: left;"><p>Select the Internet Address Family from the list, for example, <strong>inet-vpn</strong>, <strong>inet6-vpn</strong>, and so on.</p></td>
      </tr>
      <tr class="odd">
      <td style="text-align: left;"><p><strong>Cluster ID</strong></p></td>
      <td style="text-align: left;"><p>Enter the cluster ID, for example, 0.0.0.100.</p></td>
      </tr>
      <tr class="even">
      <td style="text-align: left;"><p><kbd class="user-typing" data-v-pre="">Associate Peers</kbd></p></td>
      <td style="text-align: left;"> </td>
      </tr>
      <tr class="odd">
      <td style="text-align: left;"><p><strong>Peer</strong></p></td>
      <td style="text-align: left;"><p>Select the configured peers from the list.</p></td>
      </tr>
      <tr class="even">
      <td style="text-align: left;"><p><strong>Hold Time</strong></p></td>
      <td style="text-align: left;"><p>Enter the maximum time a BGP session remains active if no Keepalives are received.</p></td>
      </tr>
      <tr class="odd">
      <td style="text-align: left;"><p><strong>Loop Count</strong></p></td>
      <td style="text-align: left;"><p>Enter the number of times the same ASN can be seen in a route-update. The route is discarded when the loop count is exceeded.</p></td>
      </tr>
      <tr class="even">
      <td style="text-align: left;"><p><strong>MD5 Auth Key</strong></p></td>
      <td style="text-align: left;"><p>Enter the MD5 authentication key value.</p></td>
      </tr>
      <tr class="odd">
      <td style="text-align: left;"><p><strong>State</strong></p></td>
      <td style="text-align: left;"><p>Select the <strong>state</strong> box when you are associating BGP peers.</p></td>
      </tr>
      <tr class="even">
      <td style="text-align: left;"><p><strong>Passive</strong></p></td>
      <td style="text-align: left;"><p>Select the <strong>passive</strong> box to disable the BGP router from advertising any routes. The BGP router can only receive updates from other peers in this state.</p></td>
      </tr>
      <tr class="odd">
      <td style="text-align: left;"><p><kbd class="user-typing" data-v-pre="">Advanced Options</kbd></p></td>
      <td style="text-align: left;"> </td>
      </tr>
      <tr class="even">
      <td style="text-align: left;"><p><strong>BGP Port</strong></p></td>
      <td style="text-align: left;"><p>Enter BGP Port number. The default is 179; change if needed.</p></td>
      </tr>
      <tr class="odd">
      <td style="text-align: left;"><p><strong>Source Port</strong></p></td>
      <td style="text-align: left;"><p>Enter source port number for client side connection.</p></td>
      </tr>
      <tr class="even">
      <td style="text-align: left;"><p><strong>Hold Time (seconds)</strong></p></td>
      <td style="text-align: left;"><p>BGP session hold time. The default is 90 seconds; change if needed.</p></td>
      </tr>
      <tr class="odd">
      <td style="text-align: left;"><p><strong>Admin State</strong></p></td>
      <td style="text-align: left;"><p>Select the <strong>Admin state</strong> box to enable the state as UP and deselect the box to disable the state to DOWN.</p></td>
      </tr>
      <tr class="even">
      <td style="text-align: left;"><p><strong>Authentication Mode</strong></p></td>
      <td style="text-align: left;"><p>Select MD5 from list if required.</p></td>
      </tr>
      <tr class="odd">
      <td style="text-align: left;"><p><strong>Authentication key</strong></p></td>
      <td style="text-align: left;"><p>Enter the Authentication Key value.</p></td>
      </tr>
      <tr class="even">
      <td style="text-align: left;"><p><strong>Control Node Zone</strong></p></td>
      <td style="text-align: left;"><p>Select the required control node zone from the list.</p></td>
      </tr>
      <tr class="odd">
      <td style="text-align: left;"><p><strong>Physical Router</strong></p></td>
      <td style="text-align: left;"><p>Select the the physical router from the list.</p></td>
      </tr>
      </tbody>
      </table>

5. Click **Create** to complete add each node.

6. You can check for peers and details about the control nodes by
   selecting **Infrastructure > Cluster > Control Nodes**. Click the
   desired node to check the details on **Summary** and **Detailed
   Stats** page.

 

.. |Figure 1: Configure> Infrastructure > BGP Routers| image:: images/s042497.png
.. |Figure 2: BGP Routers Summary| image:: images/s042498.png
.. |image1| image:: images/s042494.png
.. |Figure 3: Create BGP Router| image:: images/s042496.png
.. |Figure 4: Control Nodes| image:: images/s042499.png
.. |Figure 5: Control Node Details| image:: images/s042500.png
.. |Figure 6: Control Node Peers Tab| image:: images/s042501.png
.. |Figure 7: Infrastructure > Cluster > Advanced > BGP Routers| image:: images/s009220.png
.. |Figure 8: Create BGP Router| image:: images/s009221.png
