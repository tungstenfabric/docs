# Contrail Networking Alarms

 

[Table 1](contrail-networking-alarms.html#alarms-table) lists the
default alarms in Contrail Networking and their severity levels.

An alarm with severity level 0 (zero) is critical, 1 (one) is major, and
2 (two) is minor.

Table 1: Contrail Networking Alarms and Severity Level

<table data-cellspacing="0" style="border-top:thin solid black;" width="99%">
<colgroup>
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
</colgroup>
<thead>
<tr class="header">
<th style="text-align: left;"><p>Alarm Name</p></th>
<th style="text-align: left;"><p>Severity</p></th>
<th style="text-align: left;"><p>Description</p></th>
<th style="text-align: left;"><p>Steps to Resolve This Alarm</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>system-defined-address-mismatch-<br />
compute</p></td>
<td style="text-align: left;"><p>1</p></td>
<td style="text-align: left;"><p>Compute Node IP Address mismatch.</p></td>
<td style="text-align: left;"><p>The compute node IP address provided in the configuration file and the IP address provided as part of creating (provisioning) vrouter-agent do not match.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>system-defined-address-mismatch-<br />
control</p></td>
<td style="text-align: left;"><p>1</p></td>
<td style="text-align: left;"><p>Control Node IP Address mismatch.</p></td>
<td style="text-align: left;"><p>IP address for control node is different in config node and control node.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>system-defined-bgp-connectivity</p></td>
<td style="text-align: left;"><p>1</p></td>
<td style="text-align: left;"><p>BGP peer mismatch. Not enough BGP peers are up.</p></td>
<td style="text-align: left;"><p>Total number of BGP peers is different from the configured number of BGP peers.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>system-defined-bottle-request-<br />
size-limit</p></td>
<td style="text-align: left;"><p>-</p></td>
<td style="text-align: left;"><p>Bottle request size limit exceeded.</p></td>
<td style="text-align: left;"><p>Request Size received by API server is too large.</p>
<p>In most cases, this can be resolved by increasing the value set for the variable <var data-v-pre="">max_request_size </var> in the <code class="filepath">/etc/contrail/contrail-api.conf</code> file in config API Docker container. However, as a good practice, investigate as to why such a huge request is being sent to the Config API server.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>system-defined-conf-incorrect</p></td>
<td style="text-align: left;"><p>1</p></td>
<td style="text-align: left;"><p>ContrailConfig missing or incorrect. Configuration pushed to Ifmap as ContrailConfig is missing or incorrect.</p></td>
<td style="text-align: left;"><p>Config node did not send ContrailConfig for this node. This could be due to name mismatch between the node configured compared to actual node.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>system-defined-disk-usage-high</p></td>
<td style="text-align: left;"><p>1</p></td>
<td style="text-align: left;"><p>Disk usage exceeds high threshold limit.</p></td>
<td style="text-align: left;"><p>Corresponding disk is filled between 70%-90% capacity. Delete some files to create disk space.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>system-defined-disk-usage-critical</p></td>
<td style="text-align: left;"><p>0</p></td>
<td style="text-align: left;"><p>Disk usage crosses critical threshold limit.</p></td>
<td style="text-align: left;"><p>Corresponding disk is filled up &gt; 90%. Delete some files to create disk space.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>system-defined-node-status</p></td>
<td style="text-align: left;"><p>0</p></td>
<td style="text-align: left;"><p>Node Failure. NodeStatus UVE not present.</p></td>
<td style="text-align: left;"><p>NodeStatus UVE is not present or process is non-functional for this node. Verify that the <span class="cli" data-v-pre="">process</span> and <span class="cli" data-v-pre="">nodemgr</span> is up.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>system-defined-partial-sysinfo</p></td>
<td style="text-align: left;"><p>1</p></td>
<td style="text-align: left;"><p>System Info Incomplete.</p></td>
<td style="text-align: left;"><p>build_info is not present in NodeStatus. Cause unknown at this time.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>system-defined-process-connectivity</p></td>
<td style="text-align: left;"><p>0</p></td>
<td style="text-align: left;"><p>Process(es) reporting as non-functional.</p></td>
<td style="text-align: left;"><p>One or more processes have connections missing.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>system-defined-process-status</p></td>
<td style="text-align: left;"><p>0</p></td>
<td style="text-align: left;"><p>Process Failure.</p></td>
<td style="text-align: left;"><p>Review the docker logs to understand the reason for process failure.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>system-defined-prouter-connectivity</p></td>
<td style="text-align: left;"><p>1</p></td>
<td style="text-align: left;"><p>Prouter connectivity to controlling tor agent does not exist. Contrail looks for non-empty value for connected_agent_list</p></td>
<td style="text-align: left;"><p>Check for OVSDB connectivity status on the physical device. Debug for link failures between physical device or OVSDB connection failure between the vrouter-agent and physical router.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>system-defined-prouter-tsn-<br />
connectivity</p></td>
<td style="text-align: left;"><p>1</p></td>
<td style="text-align: left;"><p>Prouter connectivity to controlling TSN agent does not exist. Contrail looks for non-empty value for tsn_agent_list.</p></td>
<td style="text-align: left;"><p>Check for OVSDB connectivity status on the physical device. Debug for link failures between physical device or OVSDB connection failure between the vrouter-agent and physical router.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>system-defined-storage-cluster-state</p></td>
<td style="text-align: left;"><p>1</p></td>
<td style="text-align: left;"><p>Storage Cluster warning or errors.</p></td>
<td style="text-align: left;"><p>Since Contrail is not provisioning storage this alarm is not generated.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>system-defined-vrouter-interface</p></td>
<td style="text-align: left;"><p>1</p></td>
<td style="text-align: left;"><p>vRouter interface(s) down.</p></td>
<td style="text-align: left;"><p>This alarm is raised if forwarding and bridging is disabled or if health check has failed. Other reasons for this alarm include the following:</p>
<ul>
<li><p>no IP or subnet assignment</p></li>
<li><p>admin state is down</p></li>
<li><p>parent interface is down</p></li>
<li><p>VLAN is down</p></li>
<li><p>oper state is down</p></li>
<li><p>config is missing</p></li>
</ul>
<p>Resolve above items based on information available from the introspect page for interface.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>system-defined-xmpp-connectivity</p></td>
<td style="text-align: left;"><p>1</p></td>
<td style="text-align: left;"><p>XMPP peer mismatch.</p></td>
<td style="text-align: left;"><p>Number of XMPP peers is different from configured XMPP peers.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>system-defined-xmpp-close-reason</p></td>
<td style="text-align: left;"><p>1</p></td>
<td style="text-align: left;"><p>XMPP connection closed towards peer. Alarm has reason to close.</p></td>
<td style="text-align: left;"><p>This alarm is deprecated.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>system-defined-core-files</p></td>
<td style="text-align: left;"><p>0</p></td>
<td style="text-align: left;"><p>A core file has been generated on the node.</p></td>
<td style="text-align: left;"><p>There is some core file in the node.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>system-defined-pending-cassandra-<br />
compaction-tasks</p></td>
<td style="text-align: left;"><p>1</p></td>
<td style="text-align: left;"><p>Pending compaction tasks in cassandra crossed the configured threshold.</p></td>
<td style="text-align: left;"><p>This alarm is raised when disk space is insufficient. Check Cassandra system logs to understand the reason for pending compaction.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>system-defined-package-version-<br />
mismatch</p></td>
<td style="text-align: left;"><p>0</p></td>
<td style="text-align: left;"><p>There is a mismatch between installed and running package version.</p></td>
<td style="text-align: left;"><p>Package version for the package mentioned in the alarm is not matching with the required version.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>system-defined-vrouter-limit-<br />
exceeded</p></td>
<td style="text-align: left;"><p>1</p></td>
<td style="text-align: left;"><p>Agent resource usage exceeded configured watermark for resource.</p></td>
<td style="text-align: left;"><p>This alarm is raised when the next hop count or the used mpls label count crosses the high watermark.</p>
<p>The alarm is reset when the next hop count or the used MPLS label count becomes less than the low watermark.</p>
<p>To reset alarm, delete the <span class="cli" data-v-pre="">nexthop</span> and <span class="cli" data-v-pre="">mpls</span> label, which can be achieved by deleting virtual machines on the compute.</p>
<p>Alarm can also be cleared by increasing the default watermark, which is 80 (80% of the maximum number of nexthops configured in vRouter after which alarm is raised).</p>
<p>For this, you need to change the configuration in the <code class="filepath">contrail-vrouter-agent.conf</code> file and restart the vRouter agent.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>system-defined-vrouter-table-limit-<br />
exceeded</p></td>
<td style="text-align: left;"><p>0</p></td>
<td style="text-align: left;"><p>Agent resource usage exceeded table size for resource in vRouter.</p></td>
<td style="text-align: left;"><p>This alarm is raised when the next hop count reaches the <span class="cli" data-v-pre="">nexthop count </span> configured in vRouter, or when the maximum number of MPLS labels on the compute are used.</p>
<p>This alarm is cleared when the next hop count goes below 95% of the next hop count in vRouter, or the number of used MPLS label count becomes 95 % of the maximum labels or less.</p>
<p>To reset the alarm, delete the nexthop and MPLS labels, which can be achieved by deleting virtual machines on the compute for which alarm is raised.</p>
<p>This alarm can also be reset by increasing the maximum number of <span class="cli" data-v-pre="">nexthop</span> and MPLS labels configured in vRouter, if it is not already configured to the maximum supported limit.</p></td>
</tr>
</tbody>
</table>

 
