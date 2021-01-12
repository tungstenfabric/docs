contrail-status (Viewing Node Status)
=====================================

 

Syntax
------

.. raw:: html

   <div id="jd0e12" class="example" dir="ltr">

.. raw:: html

   <div class="statement" style="display:block;">

[root@host ~]# contrail-status

.. raw:: html

   </div>

.. raw:: html

   </div>

Release Information
-------------------

Command introduced in Contrail Release 1.0.

Description
-----------

Display a list of all components of a Contrail server node (such as
control, configuration, database, Web-UI, analytics, or vrouter) and
report their current status of active or inactive.

Required Privilege Level
------------------------

admin

Sample Output
-------------

.. raw:: html

   <div id="jd0e24">

The following example usage displays on a server that is configured for
the roles of vrouter, controller, analytics, configuration, web-ui, and
database.

**Sample Output**

.. raw:: html

   <div class="output" dir="ltr">

::

   root@host:~# contrail-status
   == Contrail vRouter ==
   supervisor-vrouter:           active
   contrail-vrouter-agent        active
   contrail-vrouter-nodemgr      active

   == Contrail Control ==
   supervisor-control:           active
   contrail-control              active
   contrail-control-nodemgr      active
   contrail-dns                  active
   contrail-named                active

   == Contrail Analytics ==
   supervisor-analytics:         active
   contrail-analytics-api        active
   contrail-analytics-nodemgr    active
   contrail-collector            active
   contrail-query-engine         active

   == Contrail Config ==
   supervisor-config:            active
   contrail-api:0                active
   contrail-config-nodemgr       active
   contrail-discovery:0          active
   contrail-schema               active
   contrail-svc-monitor          active
   ifmap                         active
   rabbitmq-server               active

   == Contrail Web UI ==
   supervisor-webui:             active
   contrail-webui                active
   contrail-webui-middleware     active
   redis-webui                   active

   == Contrail Database ==
   supervisord-contrail-database:active
   contrail-database             active
   contrail-database-nodemgr     active

.. raw:: html

   </div>

.. raw:: html

   </div>

 
