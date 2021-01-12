.. _monitor--networking:

Monitor > Networking
====================

 

.. raw:: html

   <div id="intro">

.. raw:: html

   <div class="mini-toc-intro">

The **Monitor -> Networking** pages give an overview of the networking
traffic statistics and health of domains, projects within domains,
virtual networks within projects, and virtual machines within virtual
networks.

.. raw:: html

   </div>

.. raw:: html

   </div>

.. _monitor--networking-menu-options:

Monitor > Networking Menu Options
---------------------------------

`Figure 1 <monitoring-networking-vnc.html#monitor-networking-menu>`__
shows the menu options available under **Monitor > Networking**.

|Figure 1: Monitor Networking Menu Options|

.. _monitor--networking--dashboard:

Monitor > Networking > Dashboard
--------------------------------

Select **Monitor > Networking > Dashboard** to gain insight into usage
statistics for domains, virtual networks, projects, and virtual
machines. When you select this option, the Traffic Statistics for Domain
window is displayed as shown in
`Figure 2 <monitoring-networking-vnc.html#traf-stat-dom-win>`__.

|Figure 2: Traffic Statistics for Domain Window|

`Table 1 <monitoring-networking-vnc.html#prog-sum-tabl>`__ describes the
fields in the Traffic Statistics for Domain window.

Table 1: Projects Summary Fields

+--------------------------+------------------------------------------+
| Field                    | Description                              |
+==========================+==========================================+
| **Total Traffic In**     | The volume of traffic into this domain   |
+--------------------------+------------------------------------------+
| **Total Traffic Out**    | The volume of traffic out of this        |
|                          | domain.                                  |
+--------------------------+------------------------------------------+
| **Inter VN Traffic In**  | The volume of inter-virtual network      |
|                          | traffic into this domain.                |
+--------------------------+------------------------------------------+
| **Inter VN Traffic Out** | The volume of inter-virtual network      |
|                          | traffic out of this domain.              |
+--------------------------+------------------------------------------+
| **Projects**             | This chart displays the networks and     |
|                          | interfaces for projects with the most    |
|                          | throughput over the past 30 minutes.     |
|                          | Click **Projects** then select **Monitor |
|                          | > Networking > Projects**, to display    |
|                          | more detailed statistics.                |
+--------------------------+------------------------------------------+
| **Networks**             | This chart displays the networks for     |
|                          | projects with the most throughput over   |
|                          | the past 30 minutes. Click **Networks**  |
|                          | then select **Monitor > Networking >     |
|                          | Networks**, to display more detailed     |
|                          | statistics.                              |
+--------------------------+------------------------------------------+

.. _monitor--networking--projects:

Monitor > Networking > Projects
-------------------------------

Select **Monitor > Networking > Projects** to see information about
projects in the system. See
`Figure 3 <monitoring-networking-vnc.html#project-statistics>`__.

|Figure 3: Monitor > Networking > Projects|

See `Table 2 <monitoring-networking-vnc.html#monitor-proj-table>`__ for
descriptions of the fields on this screen.

Table 2: Projects Summary Fields

+-----------------+---------------------------------------------------+
| Field           | Description                                       |
+=================+===================================================+
| **Projects**    | The name of the project. You can click the name   |
|                 | to access details about connectivity for this     |
|                 | project.                                          |
+-----------------+---------------------------------------------------+
| **Networks**    | The volume of inter-virtual network traffic out   |
|                 | of this domain.                                   |
+-----------------+---------------------------------------------------+
| **Traffic In**  | The volume of traffic into this domain.           |
+-----------------+---------------------------------------------------+
| **Traffic Out** | The volume of traffic out of this domain.         |
+-----------------+---------------------------------------------------+

Monitor Projects Detail
-----------------------

You can click any of the projects listed on the Projects Summary to get
details about connectivity, source and destination port distribution,
and instances. When you click an individual project, the Summary tab for
Connectivity Details is displayed as shown in
`Figure 4 <monitoring-networking-vnc.html#mon-proj-con-det>`__. Hover
over any of the connections to get more details.

|Figure 4: Monitor Projects Connectivity Details|

In the Connectivity Details window you can click the links between the
virtual networks to view the traffic statistics between the virtual
networks.

The Traffic Statistics information is also available when you select
**Monitor > Networking > Networks** as shown in
`Figure 5 <monitoring-networking-vnc.html#traf-stats-bt-nets>`__.

|Figure 5: Traffic Statistics Between Networks|

In the Connectivity Details window you can click the Instances tab to
get a summary of details for each of the instances in this project.

|Figure 6: Projects Instances Summary|

See Table 3 for a description of the fields on this screen.

Table 3: Projects Instances Summary Fields

+----------------------+----------------------------------------------+
| Field                | Description                                  |
+======================+==============================================+
| **Instance**         | The name of the instance. Click the name     |
|                      | then select **Monitor > Networking >         |
|                      | Instances** to display details about the     |
|                      | traffic statistics for this instance.        |
+----------------------+----------------------------------------------+
| **Virtual Network**  | The virtual network associated with this     |
|                      | instance.                                    |
+----------------------+----------------------------------------------+
| **Interfaces**       | The number of interfaces associated with     |
|                      | this instance.                               |
+----------------------+----------------------------------------------+
| **vRouter**          | The name of the vRouter associated with this |
|                      | instance.                                    |
+----------------------+----------------------------------------------+
| **IP Address**       | Any IP addresses associated with this        |
|                      | instance.                                    |
+----------------------+----------------------------------------------+
| **Floating IP**      | Any floating IP addresses associated with    |
|                      | this instance.                               |
+----------------------+----------------------------------------------+
| **Traffic (In/Out)** | The volume of traffic in KB or MB that is    |
|                      | passing in and out of this instance.         |
+----------------------+----------------------------------------------+

Select **Monitor > Networking > Instances** to display instance traffic
statistics as shown in
`Figure 7 <monitoring-networking-vnc.html#inst-traf-stats>`__.

|Figure 7: Instance Traffic Statistics|

.. _monitor--networking--networks:

Monitor > Networking > Networks
-------------------------------

Select **Monitor > Networking > Networks** to view a summary of the
virtual networks in your system. See
`Figure 8 <monitoring-networking-vnc.html#network-summ>`__.

|Figure 8: Network Summary|

Table 4: Network Summary Fields

+-------------------------+-------------------------------------------+
| Field                   | Description                               |
+=========================+===========================================+
| **Network**             | The domain and network name of the        |
|                         | virtual network. Click the arrow next to  |
|                         | the name to display more information      |
|                         | about the network, including the number   |
|                         | of ingress and egress flows, the number   |
|                         | of ACL rules, the number of interfaces,   |
|                         | and the total traffic in and out.         |
+-------------------------+-------------------------------------------+
| **Instances**           | The number of instances launched in this  |
|                         | network.                                  |
+-------------------------+-------------------------------------------+
| **Traffic (In/Out)**    | The volume of inter-virtual network       |
|                         | traffic in and out of this network.       |
+-------------------------+-------------------------------------------+
| **Throughput (In/Out)** | The throughput of inter-virtual network   |
|                         | traffic in and out of this network.       |
+-------------------------+-------------------------------------------+

At **Monitor > Networking > Networks** you can click on the name of any
of the listed networks to get details about the network connectivity,
traffic statistics, port distribution, instances, and other details, by
clicking the tabs across the top of the page.

`Figure 9 <monitoring-networking-vnc.html#connect-summ>`__ shows the
**Summary** tab for an individual network, which displays connectivity
details and traffic statistics for the selected network.

|Figure 9: Individual Network Connectivity Details—Summary Tab|

`Figure 10 <monitoring-networking-vnc.html#port-map>`__ shows the **Port
Map** tab for an individual network, which displays the relative
distribution of traffic for this network by protocol, by port.

|Figure 10: Individual Network-– Port Map Tab|

`Figure 11 <monitoring-networking-vnc.html#port-dist>`__ shows the
**Port Distribution** tab for an individual network, which displays the
relative distribution of traffic in and out by source port and
destination port.

|Figure 11: Individual Network-– Port Distribution Tab|

`Figure 12 <monitoring-networking-vnc.html#netw-inst>`__ shows the
**Instances** tab for an individual network, which displays details for
each instance associated with this network, including the number of
interfaces, the associated vRouter, the instance IP address, and the
volume of traffic in and out.

Additionally, you can click the arrow near the instance name to reveal
even more details about the instance—the interfaces and their addresses,
UUID, CPU (usage), and memory used of the total amount available.

|Figure 12: Individual Network Instances Tab|

`Figure 13 <monitoring-networking-vnc.html#ind-net-det-tab>`__ shows the
**Details** tab for an individual network, which displays the code used
to define this network -–the User Virtual Environment (UVE) code.

|Figure 13: Individual Network Details Tab|

 

.. |Figure 1: Monitor Networking Menu Options| image:: images/64512.gif
.. |Figure 2: Traffic Statistics for Domain Window| image:: images/s041588.gif
.. |Figure 3: Monitor > Networking > Projects| image:: images/s041589.gif
.. |Figure 4: Monitor Projects Connectivity Details| image:: images/s041846.gif
.. |Figure 5: Traffic Statistics Between Networks| image:: images/s041590.gif
.. |Figure 6: Projects Instances Summary| image:: images/s041593.gif
.. |Figure 7: Instance Traffic Statistics| image:: images/s041595.gif
.. |Figure 8: Network Summary| image:: images/s041873.gif
.. |Figure 9: Individual Network Connectivity Details—Summary Tab| image:: images/s041874.gif
.. |Figure 10: Individual Network-– Port Map Tab| image:: images/s041875.gif
.. |Figure 11: Individual Network-– Port Distribution Tab| image:: images/s041876.gif
.. |Figure 12: Individual Network Instances Tab| image:: images/s041877.gif
.. |Figure 13: Individual Network Details Tab| image:: images/s041878.gif
