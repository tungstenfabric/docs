Configuring Analytics as a Standalone Solution
==============================================

 

.. raw:: html

   <div id="intro">

.. raw:: html

   <div class="mini-toc-intro">

Starting with Contrail 4.0, it is possible to configure Contrail
Analytics as a standalone solution.

.. raw:: html

   </div>

.. raw:: html

   </div>

Overview: Contrail Analytics as a Standalone Solution
-----------------------------------------------------

Starting with Contrail 4.0 (containerized Contrail), Contrail Analytics
can be configured as a standalone solution.

The following services are necessary for a standalone solution:

-  config

-  webui

-  analytics

-  analyticsdb

A standalone Contrail Analytics solution consists of the following
containers:

-  controller container with only config and webui services enabled

-  analytics container

-  analyticsdb container

Configuration Examples for Standalone
-------------------------------------

.. raw:: html

   <div class="mini-toc-intro">

The following are examples of default inventory file configurations for
the controller container for standalone Contrail analytics.

.. raw:: html

   </div>

-  `Examples: Inventory File Controller
   Components <analytics-standalone-40-vnc.html#jd0e55>`__

-  `JSON Configuration
   Examples <analytics-standalone-40-vnc.html#jd0e76>`__

Examples: Inventory File Controller Components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. raw:: html

   <div class="mini-toc-intro">

The following are example analytics standalone solution inventory file
configurations for Contrail controller container components.

.. raw:: html

   </div>

-  `Single Node Cluster <analytics-standalone-40-vnc.html#jd0e63>`__

-  `Multi-Node Cluster <analytics-standalone-40-vnc.html#jd0e69>`__

Single Node Cluster
^^^^^^^^^^^^^^^^^^^

.. raw:: html

   <div id="jd0e66" class="example" dir="ltr">

::

   [contrail-controllers]
   10.xx.32.10             controller_components=['config','webui']

   [contrail-analyticsdb]
   10.xx.32.10

   [contrail-analytics]
   10.xx.32.10

.. raw:: html

   </div>

Multi-Node Cluster
^^^^^^^^^^^^^^^^^^

.. raw:: html

   <div id="jd0e73" class="example" dir="ltr">

::

   [contrail-controllers]
   10.xx.32.10             controller_components=['config','webui']
   10.xx.32.11             controller_components=['config','webui']
   10.xx.32.12             controller_components=['config','webui']

   [contrail-analyticsdb]
   10.xx.32.10
   10.xx.32.11
   10.xx.32.12

   [contrail-analytics]
   10.xx.32.10
   10.xx.32.11
   10.xx.32.12

.. raw:: html

   </div>

JSON Configuration Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. raw:: html

   <div class="mini-toc-intro">

The following are example JSON file configurations for (server.json) for
Contrail analytics standalone solution.

.. raw:: html

   </div>

-  `Example: JSON Single Node
   Cluster <analytics-standalone-40-vnc.html#jd0e87>`__

-  `Example: JSON Multi-Node
   Cluster <analytics-standalone-40-vnc.html#jd0e93>`__

Example: JSON Single Node Cluster
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. raw:: html

   <div id="jd0e90" class="example" dir="ltr">

::

   {                                                                
       "cluster_id": "cluster1",                                    
       "domain": "sm-domain.com",                                   
       "id": "server1",                                             
       "parameters" : {                                             
           "provision": {                                           
               "contrail_4": {                                      
                  "controller_components": "['config',’webui']"   
               },                  
       …
       …
   }

.. raw:: html

   </div>

Example: JSON Multi-Node Cluster
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. raw:: html

   <div id="jd0e96" class="example" dir="ltr">

::

   {                                                                
       "cluster_id": "cluster1",                                    
       "domain": "sm-domain.com",                                   
       "id": "server1",                                             
       "parameters" : {                                             
           "provision": {                                           
               "contrail_4": {                                      
                  "controller_components": "['config',’webui']"   
               },                  
       …
       …
   },
   {                                                                
       "cluster_id": "cluster1",                                    
       "domain": "sm-domain.com",                                   
       "id": "server2",                                             
       "parameters" : {                                             
           "provision": {                                           
               "contrail_4": {                                      
                  "controller_components": "['config',’webui']"   
               },                  
       …
       …
   },
   {                                                                
       "cluster_id": "cluster1",                                    
       "domain": "sm-domain.com",                                   
       "id": "server3",                                             
       "parameters" : {                                             
           "provision": {                                           
               "contrail_4": {                                      
                  "controller_components": "['config',’webui']"   
               },                  
       …
       …
   }

.. raw:: html

   </div>

 
