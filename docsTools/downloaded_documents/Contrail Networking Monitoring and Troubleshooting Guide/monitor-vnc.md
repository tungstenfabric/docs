# Monitoring the System

 

The **Monitor** icon on the Contrail Controller provides numerous
options so you can view and analyze usage and other activity associated
with all nodes of the system, through the use of reports, charts, and
detailed lists of configurations and system activities.

Monitor pages support monitoring of infrastructure components—control
nodes, virtual routers, analytics nodes, and config nodes. Additionally,
users can monitor networking and debug components.

Use the menu options available from the **Monitor** icon to configure
and view the statistics you need for better understanding of the
activities in your system. See
[Figure 1](monitor-vnc.html#monitor-tab-screen)

![Figure 1: Monitor Menu](images/s041506.gif)

See [Table 1](monitor-vnc.html#monitor-tab) for descriptions of the
items available under each of the menu options from the **Monitor**
icon.

Table 1: MonitorMenu Options

<table data-cellspacing="0" style="border-top:thin solid black;" width="99%">
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="header">
<th style="text-align: left;"><p>Option</p></th>
<th style="text-align: left;"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p><strong>Infrastructure &gt; Dashboard</strong></p></td>
<td style="text-align: left;"><p>Shows “at-a-glance” status view of the infrastructure components, including the numbers of virtual routers,control nodes, analytics nodes, and config nodes currently operational, and a bubble chart of virtual routers showing the CPU and memory utilization, log messages, system information, and alerts. See <a href="../task/configuration/monitor-dashboard-vnc.html">Monitor &gt; Infrastructure &gt; Dashboard</a>.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Infrastructure &gt; Control Nodes</strong></p></td>
<td style="text-align: left;"><p>View a summary for all control nodes in the system, and for each control node, view:</p>
<ul>
<li><p>Graphical reports of memory usage and average CPU load.</p></li>
<li><p>Console information for a specified time period.</p></li>
<li><p>A list of all peers with details about type, ASN, and the like.</p></li>
<li><p>A list of all routes, including next hop, source, local preference, and the like.</p></li>
</ul>
<p>See <a href="../task/configuration/monitoring-infrastructure-vnc.html">Monitor &gt; Infrastructure &gt; Control Nodes</a>.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>Infrastructure &gt; Virtual Routers</strong></p></td>
<td style="text-align: left;"><p>View a summary of all vRouters in the system, and for each vRouter, view:</p>
<ul>
<li><p>Graphical reports of memory usage and average CPU load.</p></li>
<li><p>Console information for a specified time period.</p></li>
<li><p>A list of all interfaces with details such as label, status, associated network, IP address, and the like.</p></li>
<li><p>A list of all associated networks with their ACLs and VRFs.</p></li>
<li><p>A list of all active flows with source and destination details, size, and time.</p></li>
</ul>
<p>See <a href="../task/configuration/monitoring-vrouters-vnc.html">Monitor &gt; Infrastructure &gt; Virtual Routers</a>.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Infrastructure &gt; Analytics Nodes</strong></p></td>
<td style="text-align: left;"><p>View activity for the analytics nodes, including memory and CPU usage, analytics host names, IP address, status, and more. See <a href="../task/configuration/monitor-analytics-vnc.html">Monitor &gt; Infrastructure &gt; Analytics Nodes</a>.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>Infrastructure &gt; Config Nodes</strong></p></td>
<td style="text-align: left;"><p>View activity for the config nodes, including memory and CPU usage, config host names, IP address, status, and more. See <a href="../task/configuration/monitor-config-vnc.html">Monitor &gt; Infrastructure &gt; Config Nodes</a>.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Networking &gt; Networks</strong></p></td>
<td style="text-align: left;"><p>For all virtual networks for all projects in the system, view graphical traffic statistics, including:</p>
<ul>
<li><p>Total traffic in and out.</p></li>
<li><p>Inter VN traffic in and out.</p></li>
<li><p>The most active ports, peers, and flows for a specified duration.</p></li>
<li><p>All traffic ingress and egress from connected networks, including their attached policies.</p></li>
</ul>
<p>See <a href="../task/configuration/monitoring-networking-vnc.html">Monitor &gt; Networking</a>.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>Networking &gt; Dashboard</strong></p></td>
<td style="text-align: left;"><p>For all virtual networks for all projects in the system, view graphical traffic statistics, including:</p>
<ul>
<li><p>Total traffic in and out.</p></li>
<li><p>Inter VN traffic in and out.</p></li>
</ul>
<p>You can view the statistics in varying levels of granularity, for example, for a whole project, or for a single network. See <a href="../task/configuration/monitoring-networking-vnc.html">Monitor &gt; Networking</a>.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Networking &gt; Projects</strong></p></td>
<td style="text-align: left;"><p>View essential information about projects in the system including name, associated networks, and traffic in and out.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>Networking &gt; Networks</strong></p></td>
<td style="text-align: left;"><p>View essential information about networks in the system including name and traffic in and out.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Networking &gt; Instances</strong></p></td>
<td style="text-align: left;"><p>View essential information about instances in the system including name, associated networks, interfaces, vRouters, and traffic in and out.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>Debug &gt; Packet Capture</strong></p></td>
<td style="text-align: left;"><ul>
<li><p>Add and manage packet analyzers.</p></li>
<li><p>Attach packet captures and configure their details.</p></li>
<li><p>View a list of all packet analyzers in the system and the details of their configurations, including source and destination networks, ports, and IP addresses.</p></li>
</ul></td>
</tr>
</tbody>
</table>

 
