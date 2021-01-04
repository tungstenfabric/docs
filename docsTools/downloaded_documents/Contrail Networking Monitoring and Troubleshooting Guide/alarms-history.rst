Alarms History
==============

 

.. raw:: html

   <div id="intro">

.. raw:: html

   <div class="mini-toc-intro">

Contrail allows you to view a history of alarms that were raised or
reset. You can also view a history of user-visible entities (UVEs) that
have been changed.

.. raw:: html

   </div>

.. raw:: html

   </div>

Viewing Alarms History
----------------------

In the Contrail Web user interface, new fields at **Monitor > Alarms >
Dashboard > Alarms History** now display alarms history, including
alarms that were set or reset. `Figure 1 <alarms-history.html#ah1>`__
shows the alarms history, identifying the volume and types of alarms by
time and the node types in which events are occurring. The right side
panel lists by name the nodes in which active events are occurring.

You can also use a ``contrail-status`` query to view the alarms history.
Additionally, the ``contrail-status`` displays a history of added,
updated, and removed information for UVEs in Contrail.

|Figure 1: Alarms History Page|

Tooltips are available on the Alarms History page. In the Events area,
you can click on any node type listed to display a tooltip showing
details of the events that have been added and cleared in that node, see
`Figure 2 <alarms-history.html#ah2>`__.

|Figure 2: Events Log Tooltip|

You can expand the event log in the right side panel to display a
detailed event log. Click the name of any node in the list in the right
panel, and the details of the current alarms are visible in the expanded
view, see `Figure 3 <alarms-history.html#ah3>`__.

|Figure 3: Detailed Event Log|

 

.. |Figure 1: Alarms History Page| image:: documentation/images/s019896.png
.. |Figure 2: Events Log Tooltip| image:: documentation/images/s019897.png
.. |Figure 3: Detailed Event Log| image:: documentation/images/s019898.png
