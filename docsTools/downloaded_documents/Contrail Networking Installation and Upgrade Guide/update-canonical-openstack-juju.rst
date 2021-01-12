Updating Contrail Networking using the Zero Impact Upgrade Procedure in a Canonical Openstack Deployment with Juju Charms
=========================================================================================================================

 

.. raw:: html

   <div id="intro">

.. raw:: html

   <div class="mini-toc-intro">

This document provides the steps needed to update a Contrail Networking
deployment that is using Canonical Openstack as it’s orchestration
platform. The procedure utilizes Juju charms and provides a zero impact
upgrade (ZIU) with minimal disruption to network operations.

.. raw:: html

   </div>

.. raw:: html

   </div>

Prerequisites
-------------

This document makes the following assumptions about your environment:

-  A Contrail Networking deployment using Canonical Openstack as the
   orchestration platform is already operational.

-  Juju charms for Contrail services are active in your environment, and
   the Contrail Networking controller has access to the Juju jumphost
   and the Juju cluster.

When to Use This Procedure
--------------------------

This procedure is used to upgrade Contrail Networking when it is running
in environments using Canonical Openstack.

You can use this procedure to incrementally upgrade to the next main
Contrail Networking release only. This procedure is not validated for
upgrades between releases that are two or more releases apart.

The procedure in this document has been validated for the following
Contrail Networking upgrade scenarios:

Table 1: Contrail Networking with Canonical Openstack Validated Upgrade
Scenarios

+----------------------------------+----------------------------------+
| Starting Contrail Networking     | Target Upgraded Contrail         |
| Release                          | Networking Release               |
+==================================+==================================+
| 1912.L0                          | 1912.L1                          |
+----------------------------------+----------------------------------+
| 1912 or 1912.L0                  | 2003                             |
+----------------------------------+----------------------------------+
| 2003                             | 2005                             |
+----------------------------------+----------------------------------+
| 2005                             | 2008                             |
+----------------------------------+----------------------------------+
| 2008                             | 2011                             |
+----------------------------------+----------------------------------+

Recommendations
---------------

We strongly recommend performing the following tasks before starting
this procedure:

-  Backup your current environment.

-  Enable huge pages for the kernel-mode vRouter.

   Starting in Contrail Networking Release 2005, you can enable huge
   pages in the kernel-mode vRouter to avoid future compute node reboots
   during upgrades. Huge pages in Contrail Networking are used primarily
   to allocate flow and bridge table memory within the vRouter. Huge
   pages for kernel-mode vRouters provide enough flow and bridge table
   memory to avoid compute node reboots to complete future Contrail
   Networking software upgrades.

   We recommend allotting 2GB of memory—either using the default
   1024x2MB huge page size setting or the 2x1GB size setting—for huge
   pages. Other huge page size settings should only be set by expert
   users in specialized circumstances.

   A compute node reboot is required to initially enable huge pages.
   Future compute node upgrades can happen without reboots after huge
   pages are enabled. The 1024x2MB huge page setting is configured by
   default starting in Contrail Networking Release 2005, but is not
   active in any compute node until the compute node is rebooted to
   enable the setting.

   2GB and 1MB huge page size settings cannot be enabled simultaneously
   in environments using Juju.

   The huge page configurations can be changed by entering one of the
   following commands:

   -  Enable 1024 2MB huge pages (Default): juju config contrail-agent
      kernel-hugepages-2m=1024

      Disable 2MB huge pages (empty value): juju config contrail-agent
      kernel-hugepages-2m=““

   -  Enable 2 1GB huge pages: juju config contrail-agent
      kernel-hugepages-1g=2

      Disable 1GB huge pages (default. empty value): juju config
      contrail-agent kernel-hugepages-1g=““

      **Note**

      1GB huge page settings can only be specified at initial
      deployment; you cannot modify the setting in active deployments.
      The 1GB huge page setting can also not be completely disabled
      after being activated on a compute node. Be sure that you want to
      use 1GB huge page settings on your compute node before enabling
      the setting.

Updating Contrail Networking in a Canonical Openstack Deployment Using Juju Charms
----------------------------------------------------------------------------------

To update Contrail Networking in an environment that is using Canonical
Openstack as the orchestration platform:

1. Upgrade all charms. See the `Upgrading
   applications <https://juju.is/docs/upgrading-applications>`__
   document from Juju.

2. From the Juju jumphost, enter the run-action command to place all
   control plane services—Contrail Controller, Contrail Analytics, &
   Contrail AnalyticsDB—into maintenance mode in preparation for the
   upgrade.

   .. raw:: html

      <div id="jd0e156" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      juju run-action --wait contrail-controller/leader upgrade-ziu

   .. raw:: html

      </div>

   .. raw:: html

      </div>

   **Note**

   The --wait option is not required to complete this step, but is
   recommended to ensure this procedure completes without interfering
   with the procedures in the next step.

   Wait for all charms to move to the ``maintenance`` status. You can
   check the status of all charms by entering the juju status command.

3. Update the image tags in Juju for the Contrail Analytics, Contrail
   AnalyticsDB, Contrail Agent, and Contrail Openstack services.

   .. raw:: html

      <div id="jd0e176" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

       juju config contrail-analytics image-tag=master-latest 
       juju config contrail-analyticsdb image-tag=master-latest
       juju config contrail-agent image-tag=master-latest
       juju config contrail-openstack image-tag=master-latest

   .. raw:: html

      </div>

   .. raw:: html

      </div>

   If a Contrail Service node (CSN) is part of the cluster, also update
   the image tags in Juju for the Contrail Service node.

   .. raw:: html

      <div id="jd0e181" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      juju config contrail-agent-csn image-tag=master-latest

   .. raw:: html

      </div>

   .. raw:: html

      </div>

4. Update the image tag in Juju for the Contrail Controller service:

   .. raw:: html

      <div id="jd0e187" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      juju config contrail-controller image-tag=master-latest

   .. raw:: html

      </div>

   .. raw:: html

      </div>

5. After updating the image tags, wait for all services to complete
   stage 5 of the ZIU upgrade process workflow. The wait time for this
   step varies by environment, but often takes 30 to 90 minutes.

   Enter the juju status command and review the **Workload** and
   **Message** field outputs to monitor progress. The update is complete
   when all services are in the maintenance state—the **Workload** field
   output is maintenance—and each individual service has completed stage
   5 of the ZIU upgrade—illustrated by the ziu is in progress -
   stage/done = 5/5 output in the **Message** field.

   A sample output of an in-progress update that has not completed the
   image tag update process. The **Message** field illustrates that the
   ZIU processes have not completed stage 5 of the upgrade.

   **Note**

   Some juju status output fields removed for readability.

   .. raw:: html

      <div id="jd0e227" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      juju status
      Unit                      Workload    Agent     Message
      contrail-analytics/0*     maintenance idle      ziu is in progress - stage/done = 4/4
      contrail-analytics/1      maintenance idle      ziu is in progress - stage/done = 4/4
      contrail-analytics/2      maintenance idle      ziu is in progress - stage/done = 4/4
      contrail-analyticsdb/0*   maintenance idle      ziu is in progress - stage/done = 4/4
      contrail-analyticsdb/1    maintenance idle      ziu is in progress - stage/done = 4/3
      contrail-analyticsdb/2    maintenance idle      ziu is in progress - stage/done = 4/3
      contrail-controller/0*    maintenance idle      ziu is in progress - stage/done = 4/4
        ntp/3                   active      idle      chrony: Ready
      contrail-controller/1     maintenance executing ziu is in progress - stage/done = 4/3
        ntp/2                   active      idle      chrony: Ready
      contrail-controller/2     maintenance idle      ziu is in progress - stage/done = 4/3
        ntp/4                   active      idle      chrony: Ready
      contrail-keystone-auth/0* active      idle      Unit is ready

   .. raw:: html

      </div>

   .. raw:: html

      </div>

   A sample output of an update that has completed the image tag update
   process on all services. The **Workload field** is maintenance for
   all services and the **Message** field explains that stage 5 of the
   ZIU process is done.

   **Note**

   Some juju status output fields removed for readability.

   .. raw:: html

      <div id="jd0e276" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      juju status
      Unit                      Workload     Agent Message
      contrail-analytics/0*     maintenance  idle  ziu is in progress - stage/done = 5/5
      contrail-analytics/1      maintenance  idle  ziu is in progress - stage/done = 5/5
      contrail-analytics/2      maintenance  idle  ziu is in progress - stage/done = 5/5
      contrail-analyticsdb/0*   maintenance  idle  ziu is in progress - stage/done = 5/5
      contrail-analyticsdb/1    maintenance  idle  ziu is in progress - stage/done = 5/5
      contrail-analyticsdb/2    maintenance  idle  ziu is in progress - stage/done = 5/5
      contrail-controller/0*    maintenance  idle  ziu is in progress - stage/done = 5/5
        ntp/3                   active       idle  chrony: Ready
      contrail-controller/1     maintenance  idle  ziu is in progress - stage/done = 5/5
        ntp/2                   active       idle  chrony: Ready
      contrail-controller/2     maintenance  idle  ziu is in progress - stage/done = 5/5
        ntp/4                   active       idle  chrony: Ready
      contrail-keystone-auth/0* active       idle  Unit is ready
      glance/0*                 active       idle  Unit is ready
      haproxy/0*                active       idle  Unit is ready
        keepalived/2            active       idle  VIP ready
      haproxy/1                 active       idle  Unit is ready
        keepalived/0*           active       idle  VIP ready
      haproxy/2                 active       idle  Unit is ready
        keepalived/1            active       idle  VIP ready
      heat/0*                   active       idle  Unit is ready
        contrail-openstack/3    active       idle  Unit is ready
      keystone/0*               active       idle  Unit is ready
      mysql/0*                  active       idle  Unit is ready
      neutron-api/0*            active       idle  Unit is ready
        contrail-openstack/2    active       idle  Unit is ready
      nova-cloud-controller/0*  active       idle  Unit is ready
      nova-compute/0*           active       idle  Unit is ready

   .. raw:: html

      </div>

   .. raw:: html

      </div>

6. Upgrade every Contrail agent on each individual compute node:

   .. raw:: html

      <div id="jd0e338" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      juju run-action contrail-agent/0 upgrade
      juju run-action contrail-agent/1 upgrade
      juju run-action contrail-agent/2 upgrade
      ...

   .. raw:: html

      </div>

   .. raw:: html

      </div>

   If Contrail Service nodes (CSNs) are part of the cluster, also
   upgrade every Contrail CSN agent:

   .. raw:: html

      <div id="jd0e343" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      juju run-action contrail-agent-csn/0 upgrade
      ...

   .. raw:: html

      </div>

   .. raw:: html

      </div>

   Wait for each compute node and CSN node upgrade to finish. The wait
   time for this step varies by environment, but typically takes around
   10 minutes to complete per node.

7. If huge pages are not enabled for your vRouter, log into each
   individual compute node and reboot to complete the
   procedure.\ **Note**\ 

   A compute node reboot is required to initially enable huge pages. If
   huge pages have been configured in Juju without a compute node
   reboot, you can also use this reboot to enable huge pages. You can
   avoid rebooting the compute node during future software upgrades
   after this initial reboot.

   1024x2MB huge page support is configured by default starting in
   Contrail Networking Release 2005, which is also the first Contrail
   Networking release that supports huge pages. If you are upgrading to
   Release 2005 for the first time, a compute node reboot is always
   required because huge pages could not have been previously enabled.

   This reboot also enables the default 1024x2MB huge page configuration
   unless you change the huge page configuration in Release 2005 or
   later.

   .. raw:: html

      <div id="jd0e359" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      sudo reboot

   .. raw:: html

      </div>

   .. raw:: html

      </div>

   This step can be skipped if huge pages are enabled.

 
