.. _monitor--infrastructure--control-nodes:

Monitor > Infrastructure > Control Nodes
========================================

 

.. raw:: html

   <div id="intro">

.. raw:: html

   <div class="mini-toc-intro">

Navigate to **Monitor > Infrastructure > Control Nodes** to gain insight
into usage statistics for control nodes.

.. raw:: html

   </div>

.. raw:: html

   </div>

Monitor Control Nodes Summary
-----------------------------

Select **Monitor > Infrastructure > Control Nodes** to see a graphical
chart of average memory usage versus average CPU percentage usage for
all control nodes in the system. Also on this screen is a list of all
control nodes in the system. See
`Figure 1 <monitoring-infrastructure-vnc.html#control-node-summary>`__.
See
`Table 1 <monitoring-infrastructure-vnc.html#control-nodes-summ-fields>`__
for descriptions of the fields on this screen.

|Figure 1: Control Nodes Summary|

Table 1: Control Nodes Summary Fields

+----------------------------------+----------------------------------+
| Field                            | Description                      |
+==================================+==================================+
| **Host name**                    | The name of the control node.    |
+----------------------------------+----------------------------------+
| **IP Address**                   | The IP address of the control    |
|                                  | node.                            |
+----------------------------------+----------------------------------+
| **Version**                      | The software version number that |
|                                  | is installed on the control      |
|                                  | node.                            |
+----------------------------------+----------------------------------+
| **Status**                       | The current operational status   |
|                                  | of the control node — Up or      |
|                                  | Down.                            |
+----------------------------------+----------------------------------+
| **CPU (%)**                      | The CPU percentage currently in  |
|                                  | use by the selected control      |
|                                  | node.                            |
+----------------------------------+----------------------------------+
| **Memory**                       | The memory in MB currently in    |
|                                  | use and the total memory         |
|                                  | available for this control node. |
+----------------------------------+----------------------------------+
| **Total Peers**                  | The total number of peers for    |
|                                  | this control node.               |
+----------------------------------+----------------------------------+
| **Established in Sync Peers**    | The total number of peers in     |
|                                  | sync for this control node.      |
+----------------------------------+----------------------------------+
| **Established in Sync vRouters** | The total number of vRouters in  |
|                                  | sync for this control node.      |
+----------------------------------+----------------------------------+

Monitor Individual Control Node Details
---------------------------------------

Click the name of any control nodes listed under the **Control Nodes**
titleto view an array of graphical reports of usage and numerous details
about that node. There are several tabs available to help you probe into
more details about the selected control node. The first tab is the
**Details** tab; see
`Figure 2 <monitoring-infrastructure-vnc.html#control-details>`__.

|Figure 2: Individual Control Node—Details Tab|

The Details tab provides a summary of the status and activity on the
selected node, and presents graphical displays of CPU and memory usage.
See
`Table 2 <monitoring-infrastructure-vnc.html#control-node-details-fields>`__
for descriptions of the fields on this tab.

Table 2: Individual Control Node—Details Tab Fields

+----------------------------------+----------------------------------+
| Field                            | Description                      |
+==================================+==================================+
| **Hostname**                     | The host name defined for this   |
|                                  | control node.                    |
+----------------------------------+----------------------------------+
| **IP Address**                   | The IP address of the selected   |
|                                  | node.                            |
+----------------------------------+----------------------------------+
| **Status**                       | The operational status of the    |
|                                  | control node.                    |
+----------------------------------+----------------------------------+
| **Control Node Manager**         | The operational status of the    |
|                                  | control node manager.            |
+----------------------------------+----------------------------------+
| **Config Node**                  | The IP address of the            |
|                                  | configuration node associated    |
|                                  | with this control node.          |
+----------------------------------+----------------------------------+
| **Analytics Node**               | The IP address of the node from  |
|                                  | which analytics (monitor)        |
|                                  | information is derived.          |
+----------------------------------+----------------------------------+
| **Analytics Messages**           | The total number of analytics    |
|                                  | messages in and out from this    |
|                                  | node.                            |
+----------------------------------+----------------------------------+
| **Peers**                        | The total number of peers        |
|                                  | established for this control     |
|                                  | node and how many are in sync    |
|                                  | and of what type.                |
+----------------------------------+----------------------------------+
| **CPU**                          | The average percent of CPU load  |
|                                  | incurred by this control node.   |
+----------------------------------+----------------------------------+
| **Memory**                       | The average memory usage         |
|                                  | incurred by this control node.   |
+----------------------------------+----------------------------------+
| **Last Log**                     | The date and time of the last    |
|                                  | log message issued about this    |
|                                  | control node.                    |
+----------------------------------+----------------------------------+
| **Control Node CPU/Memory        | A graphic display x, y chart of  |
| Utilization**                    | the average CPU load and memory  |
|                                  | usage incurred by this control   |
|                                  | node over time.                  |
+----------------------------------+----------------------------------+

Monitor Individual Control Node Console
---------------------------------------

Click the **Console** tab for an individual control node to display
system logging information for a defined time period, with the last 5
minutes of information as the default display. See
`Figure 3 <monitoring-infrastructure-vnc.html#control-console>`__.

|Figure 3: Individual Control Node—Console Tab|

See `Table 3 <monitoring-infrastructure-vnc.html#console-tab-fields>`__
for descriptions of the fields on the **Console** tab screen.

Table 3: Control Node: Console Tab Fields

.. raw:: html

   <table data-cellspacing="0" style="border-top:thin solid black;" width="99%">
   <colgroup>
   <col style="width: 50%" />
   <col style="width: 50%" />
   </colgroup>
   <thead>
   <tr class="header">
   <th style="text-align: left;"><p>Field</p></th>
   <th style="text-align: left;"><p>Description</p></th>
   </tr>
   </thead>
   <tbody>
   <tr class="odd">
   <td style="text-align: left;"><p><strong>Time Range</strong></p></td>
   <td style="text-align: left;"><p>Select a timeframe for which to review logging information as sent to the console. There are 11 options, ranging from the <strong>Last 5 mins</strong> through to the <strong>Last 24 hrs</strong>. The default display is for the <strong>Last 5 mins</strong>.</p></td>
   </tr>
   <tr class="even">
   <td style="text-align: left;"><p><strong>Log Category</strong></p></td>
   <td style="text-align: left;"><p>Select a log category to display:</p>
   <ul>
   <li><p>All</p></li>
   <li><p>_default_</p></li>
   <li><p>XMPP</p></li>
   <li><p>TCP</p></li>
   </ul></td>
   </tr>
   <tr class="odd">
   <td style="text-align: left;"><p><strong>Log Type</strong></p></td>
   <td style="text-align: left;"><p>Select a log type to display.</p></td>
   </tr>
   <tr class="even">
   <td style="text-align: left;"><p><strong>Log Level</strong></p></td>
   <td style="text-align: left;"><p>Select a log severity level to display:</p>
   <ul>
   <li><p>SYS_EMERG</p></li>
   <li><p>SYS_ALERT</p></li>
   <li><p>SYS_CRIT</p></li>
   <li><p>SYS_ERR</p></li>
   <li><p>SYS_WARN</p></li>
   <li><p>SYS_NOTICE</p></li>
   <li><p>SYS_INFO</p></li>
   <li><p>SYS_DEBUG</p></li>
   </ul></td>
   </tr>
   <tr class="odd">
   <td style="text-align: left;"><p><strong>Search</strong></p></td>
   <td style="text-align: left;"><p>Enter any text string to search and display logs containing that string.</p></td>
   </tr>
   <tr class="even">
   <td style="text-align: left;"><p><strong>Limit</strong></p></td>
   <td style="text-align: left;"><p>Select from a list an amount to limit the number of messages displayed:</p>
   <ul>
   <li><p>No Limit</p></li>
   <li><p>Limit 10 messages</p></li>
   <li><p>Limit 50 messages</p></li>
   <li><p>Limit 100 messages</p></li>
   <li><p>Limit 200 messages</p></li>
   <li><p>Limit 500 messages</p></li>
   </ul></td>
   </tr>
   <tr class="odd">
   <td style="text-align: left;"><p><strong>Auto Refresh</strong></p></td>
   <td style="text-align: left;"><p>Click the check box to automatically refresh the display if more messages occur.</p></td>
   </tr>
   <tr class="even">
   <td style="text-align: left;"><p><strong>Display Logs</strong></p></td>
   <td style="text-align: left;"><p>Click this button to refresh the display if you change the display criteria.</p></td>
   </tr>
   <tr class="odd">
   <td style="text-align: left;"><p><strong>Reset</strong></p></td>
   <td style="text-align: left;"><p>Click this button to clear any selected display criteria and reset all criteria to their default settings.</p></td>
   </tr>
   <tr class="even">
   <td style="text-align: left;"><p><strong>Time</strong></p></td>
   <td style="text-align: left;"><p>This column lists the time received for each log message displayed.</p></td>
   </tr>
   <tr class="odd">
   <td style="text-align: left;"><p><strong>Category</strong></p></td>
   <td style="text-align: left;"><p>This column lists the log category for each log message displayed.</p></td>
   </tr>
   <tr class="even">
   <td style="text-align: left;"><p><strong>Log Type</strong></p></td>
   <td style="text-align: left;"><p>This column lists the log type for each log message displayed.</p></td>
   </tr>
   <tr class="odd">
   <td style="text-align: left;"><p><strong>Log</strong></p></td>
   <td style="text-align: left;"><p>This column lists the log message for each log displayed.</p></td>
   </tr>
   </tbody>
   </table>

Monitor Individual Control Node Peers
-------------------------------------

The **Peers** tab displays the peers for an individual control node and
their peering state. Click the expansion arrow next to the address of
any peer to reveal more details. See
`Figure 4 <monitoring-infrastructure-vnc.html#control-peers>`__.

|Figure 4: Individual Control Node—Peers Tab|

See `Table 4 <monitoring-infrastructure-vnc.html#peers-tab-fields>`__
for descriptions of the fields on the **Peers** tab screen.

Table 4: Control Node: Peers Tab Fields

+--------------------------+------------------------------------------+
| Field                    | Description                              |
+==========================+==========================================+
| **Peer**                 | The hostname of the peer.                |
+--------------------------+------------------------------------------+
| **Peer Type**            | The type of peer.                        |
+--------------------------+------------------------------------------+
| **Peer ASN**             | The autonomous system number of the      |
|                          | peer.                                    |
+--------------------------+------------------------------------------+
| **Status**               | The current status of the peer.          |
+--------------------------+------------------------------------------+
| **Last flap**            | The last flap detected for this peer.    |
+--------------------------+------------------------------------------+
| **Messages (Recv/Sent)** | The number of messages sent and received |
|                          | from this peer.                          |
+--------------------------+------------------------------------------+

Monitor Individual Control Node Routes
--------------------------------------

The **Routes** tab displays active routes for this control node and lets
you query the results. Use horizontal and vertical scroll bars to view
more results. Click the expansion icon next to a routing table name to
reveal more details about the selected route. See
`Figure 5 <monitoring-infrastructure-vnc.html#control-routes>`__.

|Figure 5: Individual Control Node—Routes Tab|

See `Table 5 <monitoring-infrastructure-vnc.html#routes-tab-fields>`__
for descriptions of the fields on the **Routes** tab screen.

Table 5: Control Node: Routes Tab Fields

.. raw:: html

   <table data-cellspacing="0" style="border-top:thin solid black;" width="99%">
   <colgroup>
   <col style="width: 50%" />
   <col style="width: 50%" />
   </colgroup>
   <thead>
   <tr class="header">
   <th style="text-align: left;"><p>Field</p></th>
   <th style="text-align: left;"><p>Description</p></th>
   </tr>
   </thead>
   <tbody>
   <tr class="odd">
   <td style="text-align: left;"><p><strong>Routing Instance</strong></p></td>
   <td style="text-align: left;"><p>You can select a single routing instance from a list of all instances for which to display the active routes.</p></td>
   </tr>
   <tr class="even">
   <td style="text-align: left;"><p><strong>Address Family</strong></p></td>
   <td style="text-align: left;"><p>Select an address family for which to display the active routes:</p>
   <ul>
   <li><p>All (default)</p></li>
   <li><p>l3vpn</p></li>
   <li><p>inet</p></li>
   <li><p>inetmcast</p></li>
   </ul></td>
   </tr>
   <tr class="odd">
   <td style="text-align: left;"><p>(Limit Field)</p></td>
   <td style="text-align: left;"><p>Select to limit the display of active routes:</p>
   <ul>
   <li><p>Limit 10 Routes</p></li>
   <li><p>Limit 50 Routes</p></li>
   <li><p>Limit 100 Routes</p></li>
   <li><p>Limit 200 Routes</p></li>
   </ul></td>
   </tr>
   <tr class="even">
   <td style="text-align: left;"><p><strong>Peer Source</strong></p></td>
   <td style="text-align: left;"><p>Select from a list of available peers the peer for which to display the active routes, or select All.</p></td>
   </tr>
   <tr class="odd">
   <td style="text-align: left;"><p><strong>Prefix</strong></p></td>
   <td style="text-align: left;"><p>Enter a route prefix to limit the display of active routes to only those with the designated prefix.</p></td>
   </tr>
   <tr class="even">
   <td style="text-align: left;"><p><strong>Protocol</strong></p></td>
   <td style="text-align: left;"><p>Select a protocol for which to display the active routes:</p>
   <ul>
   <li><p>All (default)</p></li>
   <li><p>XMPP</p></li>
   <li><p>BGP</p></li>
   <li><p>ServiceChain</p></li>
   <li><p>Static</p></li>
   </ul></td>
   </tr>
   <tr class="odd">
   <td style="text-align: left;"><p><strong>Display Routes</strong></p></td>
   <td style="text-align: left;"><p>Click this button to refresh the display of routes after selecting different display criteria.</p></td>
   </tr>
   <tr class="even">
   <td style="text-align: left;"><p><strong>Reset</strong></p></td>
   <td style="text-align: left;"><p>Click this button to clear any selected criteria and return the display to default values.</p></td>
   </tr>
   <tr class="odd">
   <td style="text-align: left;"><p><em>Column</em></p></td>
   <td style="text-align: left;"><p><em>Description</em></p></td>
   </tr>
   <tr class="even">
   <td style="text-align: left;"><p><strong>Routing Table</strong></p></td>
   <td style="text-align: left;"><p>The name of the routing table that stores this route.</p></td>
   </tr>
   <tr class="odd">
   <td style="text-align: left;"><p><strong>Prefix</strong></p></td>
   <td style="text-align: left;"><p>The route prefix for each active route displayed.</p></td>
   </tr>
   <tr class="even">
   <td style="text-align: left;"><p><strong>Protocol</strong></p></td>
   <td style="text-align: left;"><p>The protocol used by the route.</p></td>
   </tr>
   <tr class="odd">
   <td style="text-align: left;"><p><strong>Source</strong></p></td>
   <td style="text-align: left;"><p>The host source for each active route displayed.</p></td>
   </tr>
   <tr class="even">
   <td style="text-align: left;"><p><strong>Next hop</strong></p></td>
   <td style="text-align: left;"><p>The IP address of the next hop for each active route displayed.</p></td>
   </tr>
   <tr class="odd">
   <td style="text-align: left;"><p><strong>Label</strong></p></td>
   <td style="text-align: left;"><p>The label for each active route displayed.</p></td>
   </tr>
   <tr class="even">
   <td style="text-align: left;"><p><strong>Security</strong></p></td>
   <td style="text-align: left;"><p>The security value for each active route displayed.</p></td>
   </tr>
   <tr class="odd">
   <td style="text-align: left;"><p><strong>Origin VN</strong></p></td>
   <td style="text-align: left;"><p>The virtual network from which the route originates.</p></td>
   </tr>
   <tr class="even">
   <td style="text-align: left;"><p><strong>AS Path</strong></p></td>
   <td style="text-align: left;"><p>The AS path for each active route displayed.</p></td>
   </tr>
   </tbody>
   </table>

 

.. |Figure 1: Control Nodes Summary| image:: images/s041574.gif
.. |Figure 2: Individual Control Node—Details Tab| image:: images/s041577.gif
.. |Figure 3: Individual Control Node—Console Tab| image:: images/s041578.gif
.. |Figure 4: Individual Control Node—Peers Tab| image:: images/s041579.gif
.. |Figure 5: Individual Control Node—Routes Tab| image:: images/s041580.gif
