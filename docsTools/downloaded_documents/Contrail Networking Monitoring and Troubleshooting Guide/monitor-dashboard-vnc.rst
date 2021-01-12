.. _monitor--infrastructure--dashboard:

Monitor > Infrastructure > Dashboard
====================================

 

.. raw:: html

   <div id="intro">

.. raw:: html

   <div class="mini-toc-intro">

Use **Monitor > Infrastructure > Dashboard** to get an “at-a-glance”
view of the system infrastructure components, including the numbers of
virtual routers, control nodes, analytics nodes, and config nodes
currently operational, a bubble chart of virtualrouters showing the CPU
and memory utilization, log messages, system information, and alerts.

.. raw:: html

   </div>

.. raw:: html

   </div>

Monitor Dashboard
-----------------

Click **Monitor > Infrastructure > Dashboard** on the left to view the
**Dashboard**. See `Figure 1 <monitor-dashboard-vnc.html#dashboard1>`__.

|Figure 1: Monitor > Infrastructure > Dashboard|

Monitor Individual Details from the Dashboard
---------------------------------------------

Across the top of the **Dashboard** screen are summary boxes
representing the components of the system that are shown in the
statistics. See
`Figure 2 <monitor-dashboard-vnc.html#control-details-dash>`__. Any of
the control nodes, virtual routers, analytics nodes, and config nodes
can be monitored individually and in detail from the **Dashboard** by
clicking an associated box, and drilling down for more detail.

|Figure 2: Dashboard Summary Boxes|

Detailed information about monitoring each of the areas represented by
the boxes is provided in the links in
`Table 1 <monitor-dashboard-vnc.html#dash-details-boxes>`__.

Table 1: Dashboard Summary Boxes

+---------------------+-----------------------------------------------+
| Box                 | For More Information                          |
+=====================+===============================================+
| **vRouters**        | `Monitor > Infrastructure > Virtual           |
|                     | Routers <monitoring-vrouters-vnc.html>`__     |
+---------------------+-----------------------------------------------+
| **Control Nodes**   | `Monitor > Infrastructure > Control           |
|                     | Nodes <monitoring-infrastructure-vnc.html>`__ |
+---------------------+-----------------------------------------------+
| **Analytics Nodes** | `Monitor > Infrastructure > Analytics         |
|                     | Nodes <monitor-analytics-vnc.html>`__         |
+---------------------+-----------------------------------------------+
| **Config Nodes**    | `Monitor > Infrastructure > Config            |
|                     | Nodes <monitor-config-vnc.html>`__            |
+---------------------+-----------------------------------------------+

Using Bubble Charts
-------------------

Bubble charts show the CPU and memory utilization of components
contributing to the current analytics display, including vRouters,
control nodes, config nodes, and the likeso on. You can hover over any
bubble to get summary information about the component it represents; see
`Figure 3 <monitor-dashboard-vnc.html#bubble-summ>`__. You can click
through the summary information to get more details about the component.

|Figure 3: Bubble Summary Information|

Color-Coding of Bubble Charts
-----------------------------

Bubble charts use the following color-coding scheme:

*Control Nodes*

-  Blue—working as configured.

-  Red—error, at least one configured peer is down.

*vRouters*

-  Blue—working, but no instance is launched.

-  Green—working with at least one instance launched.

-  Red—error, there is a problem with connectivity or a vRouter is in a
   failed state.

 

.. |Figure 1: Monitor > Infrastructure > Dashboard| image:: images/s041572.gif
.. |Figure 2: Dashboard Summary Boxes| image:: images/s041566.gif
.. |Figure 3: Bubble Summary Information| image:: images/s041898.gif
