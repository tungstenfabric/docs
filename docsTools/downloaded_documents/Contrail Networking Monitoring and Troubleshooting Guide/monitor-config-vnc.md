# Monitor &gt; Infrastructure &gt; Config Nodes

 

<div id="intro">

<div class="mini-toc-intro">

Select **Monitor &gt; Infrastructure &gt; Config Nodes** to view the
information about the system config nodes.

</div>

</div>

## Monitor Config Nodes

Select **Monitor &gt; Infrastructure &gt; Config Nodes** to view a
summary of activities for the analytics nodes. See
[Figure 1](monitor-config-vnc.html#config-nodes-summary).

![Figure 1: Config Nodes Summary](images/s041557.gif)

[Table 1](monitor-config-vnc.html#config-nodes-summary-fields) describes
the fields in the Config Nodes summary.

Table 1: Config Nodes Summary Fields

| Field          | Description                                                                                           |
|:---------------|:------------------------------------------------------------------------------------------------------|
| **Host name**  | The name of this node.                                                                                |
| **IP address** | The IP address of this node.                                                                          |
| **Version**    | The version of software installed on the system.                                                      |
| **Status**     | The current operational status of the node — Up or Down — and the length of time it is in that state. |
| **CPU (%)**    | The average CPU percentage usage for this node.                                                       |
| **Memory**     | The average memory usage for this node.                                                               |

## Monitor Individual Config Node Details

Click the name of any config node displayed on the config nodes summary
to view the **Details** tab for that node; see
[Figure 2](monitor-config-vnc.html#config-nodes-details).

![Figure 2: Individual Config Nodes— Details Tab](images/s041558.gif)

[Table 2](monitor-config-vnc.html#config-nodes-details-fields) describes
the fields on the Details screen.

Table 2: Individual Config Nodes— Details Tab Fields

| Field                   | Description                                                                                                                                              |
|:------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Hostname**            | The name of the config node.                                                                                                                             |
| **IP Address**          | The IP address of this node.                                                                                                                             |
| **Version**             | The installed version of the software.                                                                                                                   |
| **Overall Node Status** | The current operational status of the node — Up or Down — and the length of time it is in this state.                                                    |
| **Processes**           | The current operational status of the processes associated with the config node, including AI Server, Schema Transformer, Service Monitor, and the like. |
| **Analytics Node**      | The analytics node associated with this node.                                                                                                            |
| **CPU (%)**             | The average CPU percentage usage for this node.                                                                                                          |
| **Memory**              | The average memory usage by this node.                                                                                                                   |

## Monitor Individual Config Node Console

Click the **Console** tab for an individual config node to display
system logging information for a defined time period. See
[Figure 3](monitor-config-vnc.html#config-nodes-console).

![Figure 3: Individual Config Node—Console Tab](images/s041565.gif)

See [Table 3](monitor-config-vnc.html#config-nodes-console-tab-fields)
for descriptions of the fields on the **Console** tab screen.

Table 3: Individual Config Node-Console Tab Fields

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
<td style="text-align: left;"><p>Select a timeframe for which to review logging information as sent to the console. Use the drop down calendar in the fields From Time and To Time to select the date and times to include in the time range for viewing.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Log Category</strong></p></td>
<td style="text-align: left;"><p>Select from the drop down menu a log category to display. The option to view All is also available.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>Log Type</strong></p></td>
<td style="text-align: left;"><p>Select a log type to display.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Log Level</strong></p></td>
<td style="text-align: left;"><p>Select a log severity level to display:</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>Limit</strong></p></td>
<td style="text-align: left;"><p>Select from a list an amount to limit the number of messages displayed:</p>
<ul>
<li><p>All</p></li>
<li><p>Limit 10 messages</p></li>
<li><p>Limit 50 messages</p></li>
<li><p>Limit 100 messages</p></li>
<li><p>Limit 200 messages</p></li>
<li><p>Limit 500 messages</p></li>
</ul></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Keywords</strong></p></td>
<td style="text-align: left;"><p>Enter any key words by which to filter the log messages displayed.</p></td>
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
</tbody>
</table>

 
