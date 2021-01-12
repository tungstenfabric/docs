contrail-version (Viewing Version Information)
==============================================

 

Syntax
------

.. raw:: html

   <div id="jd0e12" class="example" dir="ltr">

.. raw:: html

   <div class="statement" style="display:block;">

[root@host]# contrail-version

.. raw:: html

   </div>

.. raw:: html

   </div>

Release Information
-------------------

Command introduced in Contrail Release 1.0.

Description
-----------

Display a list of all installed components with their version and build
numbers.

Required Privilege Level
------------------------

admin

Sample Output
-------------

.. raw:: html

   <div id="jd0e24">

The following example shows version and build information for all
installed components.

**Sample Output**

``root@host> contrail-version``

.. raw:: html

   <div class="output" dir="ltr">

::

   Package                                Version                 Build-ID | Repo | RPM Name
   -------------------------------------- ----------------------- ----------------------------------
   contrail-analytics                     1-1309090026.el6        141
   contrail-analytics-venv                0.1-1309062310.el6      141
   contrail-api                           0.1-1309090026.el6      141
   contrail-api-lib                       0.1-1309090026.el6      141
   contrail-api-venv                      0.1-1309080539.el6      141
   contrail-control                       2012.0-1309090026.el6   141
   contrail-database                      0.1-1309050028          141
   contrail-dns                           1-1309090026.el6        141
   contrail-fabric-utils                  1-1309090026            141
   contrail-libs                          1-1309090026.el6        141
   contrail-nodejs                        0.8.15-1309090026.el6   141
   contrail-openstack-analytics           0.1-1309090026.el6      141
   contrail-openstack-cfgm                0.1-1309090026.el6      141
   contrail-openstack-control             0.1-1309090026.el6      141

.. raw:: html

   </div>

.. raw:: html

   </div>

.. _sample-output-1:

Sample Output
-------------

.. raw:: html

   <div id="jd0e36">

The following example shows version and build information for only the
installed contrail components.

**Sample Output**

``root@host> contrail-version | grep contrail``

.. raw:: html

   <div class="output" dir="ltr">

::

   Package                                Version                 Build-ID | Repo | RPM Name
   -------------------------------------- ----------------------- ----------------------------------
   contrail-analytics                     1-1309090026.el6        141                 
   contrail-analytics-venv                0.1-1309062310.el6      141                 
   contrail-api                           0.1-1309090026.el6      141                 
   contrail-api-lib                       0.1-1309090026.el6      141                 
   contrail-api-venv                      0.1-1309080539.el6      141                 
   contrail-control                       2012.0-1309090026.el6   141                 
   contrail-database                      0.1-1309050028          141                 
   contrail-dns                           1-1309090026.el6        141                 
   contrail-fabric-utils                  1-1309090026            141                 
   contrail-libs                          1-1309090026.el6        141                 
   contrail-nodejs                        0.8.15-1309090026.el6   141                 
   contrail-openstack-analytics           0.1-1309090026.el6      141                 
   contrail-openstack-cfgm                0.1-1309090026.el6      141                 
   contrail-openstack-control             0.1-1309090026.el6      141                 
   contrail-openstack-database            0.1-1309090026.el6      141                 
   contrail-openstack-webui               0.1-1309090026.el6      141                 
   contrail-setup                         1-1309090026.el6        141                 
   contrail-webui                         1-1309090026            141                 
   openstack-quantum-contrail             2013.2-1309090026       141                 

.. raw:: html

   </div>

.. raw:: html

   </div>

 
