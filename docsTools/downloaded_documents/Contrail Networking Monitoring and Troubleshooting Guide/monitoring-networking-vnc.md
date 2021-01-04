# Monitor &gt; Networking

 

<div id="intro">

<div class="mini-toc-intro">

The **Monitor -&gt; Networking** pages give an overview of the
networking traffic statistics and health of domains, projects within
domains, virtual networks within projects, and virtual machines within
virtual networks.

</div>

</div>

## Monitor &gt; Networking Menu Options

[Figure 1](monitoring-networking-vnc.html#monitor-networking-menu) shows
the menu options available under **Monitor &gt; Networking**.

![Figure 1: Monitor Networking Menu Options](images/64512.gif)

## Monitor &gt; Networking &gt; Dashboard

Select **Monitor &gt; Networking &gt; Dashboard** to gain insight into
usage statistics for domains, virtual networks, projects, and virtual
machines. When you select this option, the Traffic Statistics for Domain
window is displayed as shown in
[Figure 2](monitoring-networking-vnc.html#traf-stat-dom-win).

![Figure 2: Traffic Statistics for Domain Window](images/s041588.gif)

[Table 1](monitoring-networking-vnc.html#prog-sum-tabl) describes the
fields in the Traffic Statistics for Domain window.

Table 1: Projects Summary Fields

| Field                    | Description                                                                                                                                                                                                                    |
|:-------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Total Traffic In**     | The volume of traffic into this domain                                                                                                                                                                                         |
| **Total Traffic Out**    | The volume of traffic out of this domain.                                                                                                                                                                                      |
| **Inter VN Traffic In**  | The volume of inter-virtual network traffic into this domain.                                                                                                                                                                  |
| **Inter VN Traffic Out** | The volume of inter-virtual network traffic out of this domain.                                                                                                                                                                |
| **Projects**             | This chart displays the networks and interfaces for projects with the most throughput over the past 30 minutes. Click **Projects** then select **Monitor &gt; Networking &gt; Projects**, to display more detailed statistics. |
| **Networks**             | This chart displays the networks for projects with the most throughput over the past 30 minutes. Click **Networks** then select **Monitor &gt; Networking &gt; Networks**, to display more detailed statistics.                |

## Monitor &gt; Networking &gt; Projects

Select **Monitor &gt; Networking &gt; Projects** to see information
about projects in the system. See
[Figure 3](monitoring-networking-vnc.html#project-statistics).

![Figure 3: Monitor &gt; Networking &gt; Projects](images/s041589.gif)

See [Table 2](monitoring-networking-vnc.html#monitor-proj-table) for
descriptions of the fields on this screen.

Table 2: Projects Summary Fields

| Field           | Description                                                                                            |
|:----------------|:-------------------------------------------------------------------------------------------------------|
| **Projects**    | The name of the project. You can click the name to access details about connectivity for this project. |
| **Networks**    | The volume of inter-virtual network traffic out of this domain.                                        |
| **Traffic In**  | The volume of traffic into this domain.                                                                |
| **Traffic Out** | The volume of traffic out of this domain.                                                              |

## Monitor Projects Detail

You can click any of the projects listed on the Projects Summary to get
details about connectivity, source and destination port distribution,
and instances. When you click an individual project, the Summary tab for
Connectivity Details is displayed as shown in
[Figure 4](monitoring-networking-vnc.html#mon-proj-con-det). Hover over
any of the connections to get more details.

![Figure 4: Monitor Projects Connectivity Details](images/s041846.gif)

In the Connectivity Details window you can click the links between the
virtual networks to view the traffic statistics between the virtual
networks.

The Traffic Statistics information is also available when you select
**Monitor &gt; Networking &gt; Networks** as shown in
[Figure 5](monitoring-networking-vnc.html#traf-stats-bt-nets).

![Figure 5: Traffic Statistics Between Networks](images/s041590.gif)

In the Connectivity Details window you can click the Instances tab to
get a summary of details for each of the instances in this project.

![Figure 6: Projects Instances Summary](images/s041593.gif)

See Table 3 for a description of the fields on this screen.

Table 3: Projects Instances Summary Fields

| Field                | Description                                                                                                                                                        |
|:---------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Instance**         | The name of the instance. Click the name then select **Monitor &gt; Networking &gt; Instances** to display details about the traffic statistics for this instance. |
| **Virtual Network**  | The virtual network associated with this instance.                                                                                                                 |
| **Interfaces**       | The number of interfaces associated with this instance.                                                                                                            |
| **vRouter**          | The name of the vRouter associated with this instance.                                                                                                             |
| **IP Address**       | Any IP addresses associated with this instance.                                                                                                                    |
| **Floating IP**      | Any floating IP addresses associated with this instance.                                                                                                           |
| **Traffic (In/Out)** | The volume of traffic in KB or MB that is passing in and out of this instance.                                                                                     |

Select **Monitor &gt; Networking &gt; Instances** to display instance
traffic statistics as shown in
[Figure 7](monitoring-networking-vnc.html#inst-traf-stats).

![Figure 7: Instance Traffic Statistics](images/s041595.gif)

## Monitor &gt; Networking &gt; Networks

Select **Monitor &gt; Networking &gt; Networks** to view a summary of
the virtual networks in your system. See
[Figure 8](monitoring-networking-vnc.html#network-summ).

![Figure 8: Network Summary](images/s041873.gif)

Table 4: Network Summary Fields

| Field                   | Description                                                                                                                                                                                                                                                                |
|:------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Network**             | The domain and network name of the virtual network. Click the arrow next to the name to display more information about the network, including the number of ingress and egress flows, the number of ACL rules, the number of interfaces, and the total traffic in and out. |
| **Instances**           | The number of instances launched in this network.                                                                                                                                                                                                                          |
| **Traffic (In/Out)**    | The volume of inter-virtual network traffic in and out of this network.                                                                                                                                                                                                    |
| **Throughput (In/Out)** | The throughput of inter-virtual network traffic in and out of this network.                                                                                                                                                                                                |

At **Monitor &gt; Networking &gt; Networks** you can click on the name
of any of the listed networks to get details about the network
connectivity, traffic statistics, port distribution, instances, and
other details, by clicking the tabs across the top of the page.

[Figure 9](monitoring-networking-vnc.html#connect-summ) shows the
**Summary** tab for an individual network, which displays connectivity
details and traffic statistics for the selected network.

![Figure 9: Individual Network Connectivity Details—Summary
Tab](images/s041874.gif)

[Figure 10](monitoring-networking-vnc.html#port-map) shows the **Port
Map** tab for an individual network, which displays the relative
distribution of traffic for this network by protocol, by port.

![Figure 10: Individual Network-– Port Map Tab](images/s041875.gif)

[Figure 11](monitoring-networking-vnc.html#port-dist) shows the **Port
Distribution** tab for an individual network, which displays the
relative distribution of traffic in and out by source port and
destination port.

![Figure 11: Individual Network-– Port Distribution
Tab](images/s041876.gif)

[Figure 12](monitoring-networking-vnc.html#netw-inst) shows the
**Instances** tab for an individual network, which displays details for
each instance associated with this network, including the number of
interfaces, the associated vRouter, the instance IP address, and the
volume of traffic in and out.

Additionally, you can click the arrow near the instance name to reveal
even more details about the instance—the interfaces and their addresses,
UUID, CPU (usage), and memory used of the total amount available.

![Figure 12: Individual Network Instances Tab](images/s041877.gif)

[Figure 13](monitoring-networking-vnc.html#ind-net-det-tab) shows the
**Details** tab for an individual network, which displays the code used
to define this network -–the User Virtual Environment (UVE) code.

![Figure 13: Individual Network Details Tab](images/s041878.gif)

 
