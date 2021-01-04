# Creating a Query for Flows

 

Select **Query &gt; Flows** to perform rich and complex SQL-like queries
on flows in the Contrail Controller. You can use the query results for
such things as gaining insight into the operation of applications in a
virtual network, performing historical analysis of flow issues, and
pinpointing problem areas with flows.

## Query Flow Series Table

Select **Query &gt; Flows &gt; Series** to create queries of the flow
series table. The results are in the form of time series data for flow
series. See [Figure 1](query-flows-cc.html#query-flows-series).

![Figure 1: Query Flow Series Window](images/s008307.PNG)

The query fields available on the screen for the **Series** tab are
described in [Table 1](query-flows-cc.html#flow-table). Enter query data
into the fields to create a SQL-like query to display and analyze flows.

Table 1: Query Flow Series Fields

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
<td style="text-align: left;"><p>Select a range of time to display the flow series:</p>
<ul>
<li><p>Last 10 Mins</p></li>
<li><p>Last 30 Mins</p></li>
<li><p>Last 1 Hr</p></li>
<li><p>Last 6 Hrs</p></li>
<li><p>Last 12 Hrs</p></li>
<li><p>Custom</p></li>
</ul>
<p>Click <strong>Custom</strong> to enter a specific custom time range in two fields: <strong>Start Time</strong> and <strong>End Time</strong>.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Select Terms</strong></p></td>
<td style="text-align: left;"><p>Click the edit button (pencil icon) to open a <strong>Select Terms</strong> window (<a href="query-flows-cc.html#select-terms">Figure 2</a>), where you can click one or more fields to display from the flow series, such as <strong>Virtual Router, Source VN, Destination VN, SUM(bytes), SUM(packets)</strong>, and more.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>Direction</strong></p></td>
<td style="text-align: left;"><p>Select the desired flow direction: <strong>Ingress</strong> or <strong>Egress</strong>.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Where</strong></p></td>
<td style="text-align: left;"><p>Click the <strong>+Add</strong> to open a query-writing window, where you can specify query values for variables such as <strong>destvn, protocol, sourcevn, and vrouter</strong>.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>Filter</strong></p></td>
<td style="text-align: left;"><p>Click the edit button (pencil icon) to open a <strong>Filters</strong> window (<a href="query-flows-cc.html#query-flows-series">Figure 1</a>), where you can select filter items to sort by, the sort order, and limits to the number of results returned.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Time Granularity</strong></p></td>
<td style="text-align: left;"><p>When <strong>Time Granularity</strong> is selected, you have the option to view results in graph or flowchart form. Graph buttons appear on the screen above the <strong>Export</strong> button. Click a graph button to transform the tabular results into a graphical chart display.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>Unit</strong></p></td>
<td style="text-align: left;"><p>Select minutes or seconds for unit of measurement.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Run</strong></p></td>
<td style="text-align: left;"><p>Click <strong>Run</strong> to retrieve the flows that match the query you created. The flows are listed on the lower portion of the screen in a box with columns identifying the selected fields for each flow.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>Export</strong></p></td>
<td style="text-align: left;"><p>The Export button is displayed after you click <strong>Run</strong>. This allows you to export the list of flows to a text <code class="inline" data-v-pre="">.csv</code> file.</p></td>
</tr>
</tbody>
</table>

The **Select Terms** window allows you to select one or more attributes
of a flow series by clicking each attribute desired. See
[Figure 2](query-flows-cc.html#select-terms). Select **SUM(Bytes)** or
**SUM(Packets)** to aggregate bytes and packets in intervals.

![Figure 2: Flow Series Select Terms](images/s008305.PNG)

Use the **Filters** window to refine the display of query results for
flows, by defining an attribute by which to sort the results, the sort
order of the results, and any limit needed to restrict the number of
results. See [Figure 3](query-flows-cc.html#flow-series-filter).

![Figure 3: Flows Series Filter](images/s008306.PNG)

## Query Individual Flow Records

Select **Query &gt; Flow &gt; Records** to create queries of individual
flow records for detailed debugging of connectivity issues between
applications and virtual machines. Queries at this level return records
of the active flows within a given time period.

![Figure 4: Flows Records](images/s008308.PNG)

The query fields available on the screen for the **Records** tab are
described in [Table 2](query-flows-cc.html#flow-records-table1). Enter
query data into the fields to create an SQL-like query to display and
analyze flows.

Table 2: Query Flow Records Fields

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
<td style="text-align: left;"><p>Select a range of time for the flow records:</p>
<ul>
<li><p>Last 10 Mins</p></li>
<li><p>Last 30 Mins</p></li>
<li><p>Last 1 Hr</p></li>
<li><p>Last 6 Hrs</p></li>
<li><p>Last 12 Hrs</p></li>
<li><p>Custom</p></li>
</ul>
<p>Click <strong>Custom</strong> to enter a specified custom time range in two fields: <strong>Start Time</strong> and <strong>End Time</strong>.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Select Terms</strong></p></td>
<td style="text-align: left;"><p>Click the edit button (pencil icon) to open a <strong>Select Terms</strong> window (<a href="query-flows-cc.html#select-records-2005">Figure 4</a>), where you can click one or more attributes to display for the flow records, including <strong>vrouter, sourcevn, sourceip, destvn, destip, protocol, dport,</strong> and <strong>action</strong>.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>Direction</strong></p></td>
<td style="text-align: left;"><p>Select the desired flow direction: <strong>Ingress</strong> or <strong>Egress</strong>.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Where</strong></p></td>
<td style="text-align: left;"><p>Click <strong>+Add</strong> to open a query window where you can specify query values for <strong>destvn, protocol, sourcevn,</strong> and <strong>vrouter</strong>.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>Run</strong></p></td>
<td style="text-align: left;"><p>Click <strong>Run</strong> to retrieve the flow records that match the query you created. The records are listed on the lower portion of the screen in a box with columns identifying the fields for each flow.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Export</strong></p></td>
<td style="text-align: left;"><p>The <strong>Export</strong> button is displayed after you click <strong>Run</strong>, allowing you to export the list of flows to a text <code class="filepath">.csv</code> file.</p></td>
</tr>
</tbody>
</table>

The **Select Terms** window allows you to select one or more attributes
to display for the flow records selected. See
[Figure 5](query-flows-cc.html#records-select-terms).

![Figure 5: Flows Records Select Terms](images/s008337.png)

## Using the Query Window

The query window is available by clicking the **+Add** in the **Where**
field. Use the query window to enter query statements. See
[Figure 5](query-flows-cc.html#records-select-terms).

You can restrict the query to a particular source VN and destination VN
combination using the **Select** section.

The **Where** supports logical AND and logical OR operations, and is
modeled as a logical OR of multiple AND terms. For example: ( (term1 AND
term2 AND term3..) OR (term4 AND term5) OR…).

Each term is a single variable expression such as **sourcevn = vn1**.

See [Table 3](query-flows-cc.html#query-window-fields) for descriptions
of the fields in the query window.

Table 3: Query Window Fields and Descriptions

<table data-cellspacing="0" style="border-top:thin solid black;" width="99%">
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="header">
<th style="text-align: left;"><p>Item</p></th>
<th style="text-align: left;"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>—</p></td>
<td style="text-align: left;"><p>Select from a list of available item types the type from which to query.</p>
<ul>
<li><p>destvn</p></li>
<li><p>protocol</p></li>
<li><p>sourcevn</p></li>
<li><p>vrouter</p></li>
</ul></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>(operator)</p></td>
<td style="text-align: left;"><p><strong>=</strong>(equal to) and <strong>Starts with</strong> are available.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>AND +</strong></p></td>
<td style="text-align: left;"><p>Click the <strong>+Add</strong> to add more elements to your query. Repeat to include additional query elements to your query statement.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Apply</strong></p></td>
<td style="text-align: left;"><p>Click to enter the query into the fields on the main screen.</p></td>
</tr>
</tbody>
</table>

The **Where** clause supports logical AND and logical OR operations.

The **Where** can be modeled as logical OR of multiple AND terms. (
(term1 AND term2 AND term3..) OR (term4 AND term5) OR…).

Each term is a single variable expression such as **Source VN = VN1.**

## Display Flows Query Queue

Select **Query &gt; Flows &gt; Query Queue** to display queries that are
in the queue waiting to be performed on the data.

The query fields available on the screen for the **Records** tab are
described in [Table 4](query-flows-cc.html#flow-records-table). Enter
query data into the fields to create an SQL-like query to display and
analyze flows.

Table 4: Query Flow Records Fields

| Field          | Description                                                                                                                                                       |
|:---------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Date**       | The date and time the query was started.                                                                                                                          |
| **Query**      | A display of the parameters set for the query.                                                                                                                    |
| **Progress**   | The percentage completion of the query to date.                                                                                                                   |
| **Records**    | The number of records matching the query to date.                                                                                                                 |
| **Status**     | The status of the query, such as **completed**.                                                                                                                   |
| **Time Taken** | The amount of time in seconds it has taken the query to return the matching records.                                                                              |
| (Action icon)  | Click the **Action** icon and select **View Results** to view a list of the records that match the query, or click **Delete** to remove the query from the queue. |

 
