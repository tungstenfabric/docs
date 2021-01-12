Configuring Traffic Analyzers and Packet Capture for Mirroring
==============================================================

 

Contrail provides traffic mirroring so you can mirror specified traffic
to a traffic analyzer where you can perform deep traffic inspection.
Traffic mirroring enables you to designate certain traffic flows to be
mirrored to a traffic analyzer, where you can view traffic flows in
great detail.

.. raw:: html

   <div id="intro">

.. raw:: html

   <div class="mini-toc-intro">

This section describes how to set up packet capture to mirror traffic
packets to an analyzer.

.. raw:: html

   </div>

.. raw:: html

   </div>

Traffic Analyzer Images
-----------------------

Before using the Contrail interface to configure traffic analyzers and
packet capture for mirroring, make sure that the following analyzer
images are available in the VM image list for your system. The traffic
analyzer images are enhanced for viewing details of captured packets in
Wireshark. When creating a policy for the traffic analyzer, the traffic
analyzer instance should always have the **Mirror to** field selected in
the policy, do not select the **Apply Service** field for a traffic
analyzer.

-  **analyzer-vm-console-qcow2**—Standard traffic analyzer; should be
   named **analyzer** in the image list. This type of traffic analyzer
   is always configured with a single interface, and the interface
   should be a **Left** interface.

-  **analyzer-vm-console-two-if qcow2**—This type of traffic analyzer
   has two interfaces, **Left** and **Management**. This traffic
   analyzer can have any name except the name **analyzer**, which is
   reserved for the single interface analyzer.

**Note**

The ``analyzer-vm`` images are valid for all versions of Contrail.
Download the images from the Contrail 1.0 software download page:
https://www.juniper.net/support/downloads/?p=contrail#sw .

Configuring Traffic Analyzers
-----------------------------

Contrail Controller enables you to mirror captured packet traffic to a
traffic analyzer. Follow these steps to mirror captured packet traffic:

1. Configure analyzer(s) on the host.

2. Set up rules for packet capture.

You can set up traffic mirroring using **Configure > Networking >
Services**. For more information, see `Setting Up Traffic Mirroring
Using Configure > Networking >
Services <configure-traffic-analyzer-vnc.html#set-up-traffic-mirrioring>`__.

.. _setting-up-traffic-mirroring-using-configure--networking--services:

Setting Up Traffic Mirroring Using Configure > Networking > Services
--------------------------------------------------------------------

Follow these steps to set up traffic mirroring using **Configure >
Networking > Services**.

1.  Access **Configure > Services > Service Templates**.

    The **Service Templates** screen appears; see
    `Figure 1 <configure-traffic-analyzer-vnc.html#config-svc-templ>`__.

    |Figure 1: Service Templates|

2.  To create a new service template, click the **+** icon.

    The **Create** window appears. Select the Service Template tab; see
    `Figure 2 <configure-traffic-analyzer-vnc.html#add-svc-templ>`__.

    |Figure 2: Create Service Template|

3.  Complete the fields by using the guidelines in
    `Table 1 <configure-traffic-analyzer-vnc.html#svc-templ-fields-analyzer>`__.

    Table 1: Create Service Template Fields

    .. raw:: html

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
       <td style="text-align: left;"><p><strong>Name</strong></p></td>
       <td style="text-align: left;"><p>Enter a descriptive text name for this service template.</p></td>
       </tr>
       <tr class="even">
       <td style="text-align: left;"><p><strong>Version</strong></p></td>
       <td style="text-align: left;"><p>Select <strong>v2</strong> from the drop-down list to indicate that this service template is based on templates version 2, valid for Contrail 3.0 and later.</p></td>
       </tr>
       <tr class="odd">
       <td style="text-align: left;"><p><strong>Virtualization Type</strong></p></td>
       <td style="text-align: left;"><p>Select <strong>Virtual Machine</strong> from the drop-down list to indicate the virtualization type for mirroring for this template.</p></td>
       </tr>
       <tr class="even">
       <td style="text-align: left;"><p><strong>Service Mode</strong></p></td>
       <td style="text-align: left;"><p>Select <strong>Transparent</strong> from the drop-down list to indicate that this service template is for transparent mirroring.</p></td>
       </tr>
       <tr class="odd">
       <td style="text-align: left;"><p><strong>Service Type</strong></p></td>
       <td style="text-align: left;"><p>Select <strong>Analyzer</strong> from the drop-down list to indicate that this service template is for a traffic analyzer.</p></td>
       </tr>
       <tr class="even">
       <td style="text-align: left;"><p><strong>Interface(s)</strong></p></td>
       <td style="text-align: left;"><p>From the drop-down list, click the check boxes to indicate which interface types are used for this analyzer service template:</p>
       <ul>
       <li><p>Left</p></li>
       <li><p>Right</p></li>
       <li><p>Management</p></li>
       </ul></td>
       </tr>
       <tr class="odd">
       <td style="text-align: left;"><p><strong>Save</strong></p></td>
       <td style="text-align: left;"><p>When finished, click <strong>OK</strong> to commit the changes</p></td>
       </tr>
       <tr class="even">
       <td style="text-align: left;"><p><strong>Cancel</strong></p></td>
       <td style="text-align: left;"><p>Click <strong>Cancel</strong> to clear the fields and start over.</p></td>
       </tr>
       </tbody>
       </table>

4.  Create a service instance by clicking the **Service Instances** link
    and clicking the **+** icon.

    The **Create** window appears; make sure the Service Instance tab is
    selected. See
    `Figure 3 <configure-traffic-analyzer-vnc.html#add-serv-inst>`__.

    |Figure 3: Create Service Instances|

5.  Complete the fields by using the guidelines in
    `Table 2 <configure-traffic-analyzer-vnc.html#add-svc-inst-fields>`__.

    Table 2: Create Service Instances Fields

    +----------------------+----------------------------------------------+
    | Field                | Description                                  |
    +======================+==============================================+
    | **Name**             | Enter a text name for this service instance. |
    +----------------------+----------------------------------------------+
    | **Service Template** | Select from a drop-down list of available    |
    |                      | service templates the template to use for    |
    |                      | this service instance,                       |
    |                      | analyzer-service-template in this example.   |
    +----------------------+----------------------------------------------+
    | **Interface Type**   | Each interface configured in the service     |
    |                      | template for this instance appears in a      |
    |                      | list.                                        |
    +----------------------+----------------------------------------------+
    | **Virtual Network**  | Select from a drop-down list of available    |
    |                      | virtual networks the network for each        |
    |                      | interface that is configured for the         |
    |                      | instance.                                    |
    +----------------------+----------------------------------------------+
    | **Save**             | Click **Save** to commit your changes.       |
    +----------------------+----------------------------------------------+
    | **Cancel**           | Click **Cancel** to clear your changes and   |
    |                      | start over.                                  |
    +----------------------+----------------------------------------------+

6.  To create a network policy rule for this service instance, click
    **Configure > Networking > Policies**. The **Policies** window
    appears. Click the **+** icon to get to the **Create** window; see
    `Figure 4 <configure-traffic-analyzer-vnc.html#config-netw-pol>`__.

    |Figure 4: Create Policy|

7.  Enter a name for the policy, then click the + icon in the lower
    portion of the screen to configure rules for the policy, see
    `Figure 5 <configure-traffic-analyzer-vnc.html#add-rule-svc-inst>`__.

    |Figure 5: Create Policy Rules|

8.  To add policy rules, complete the fields, using the guidelines in
    `Table 3 <configure-traffic-analyzer-vnc.html#add-rule-svc-inst-fields>`__.
    **Note**\ 

    When there is a network policy attached to the virtual network, any
    conflicting rules configured for the analyzer will not take effect.

    Table 3: Add Rule Fields

    .. raw:: html

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
       <td style="text-align: left;"><p><strong>Action</strong></p></td>
       <td style="text-align: left;"><p>Select PASS or DENY as the rule action.</p></td>
       </tr>
       <tr class="even">
       <td style="text-align: left;"><p><strong>Protocol</strong></p></td>
       <td style="text-align: left;"><p>Select the protocol for the policy rule, or select ANY.</p></td>
       </tr>
       <tr class="odd">
       <td style="text-align: left;"><p><strong>Source</strong></p></td>
       <td style="text-align: left;"><p>Select from multiple drop-down lists the source for this rule, including options under CIDR, Network, Policy, or Security Group.</p></td>
       </tr>
       <tr class="even">
       <td style="text-align: left;"><p><strong>Ports</strong></p></td>
       <td style="text-align: left;"><p>Select from a drop-down list the source ports for the rule.</p></td>
       </tr>
       <tr class="odd">
       <td style="text-align: left;"><p><strong>Direction</strong></p></td>
       <td style="text-align: left;"><p>Select the direction of flow for the packets to be captured:</p>
       <ul>
       <li><p>&lt;&gt; (bidirectional)</p></li>
       <li><p>&gt; (unidirectional)</p></li>
       </ul></td>
       </tr>
       <tr class="even">
       <td style="text-align: left;"><p><strong>Destination</strong></p></td>
       <td style="text-align: left;"><p>Select from multiple drop-down lists the destination for this rule, including options under CIDR, Network, Policy, or Security Group.</p></td>
       </tr>
       <tr class="odd">
       <td style="text-align: left;"><p><strong>Ports</strong></p></td>
       <td style="text-align: left;"><p>Select from a list the destination ports for the packets to be captured.</p></td>
       </tr>
       <tr class="even">
       <td style="text-align: left;"><p><strong>check boxes</strong></p></td>
       <td style="text-align: left;"><p>Check any box that applies to this rule: Log, Services, Mirror, QoS.</p></td>
       </tr>
       <tr class="odd">
       <td style="text-align: left;"><p><strong>Save</strong></p></td>
       <td style="text-align: left;"><p>Click <strong>Save</strong> to commit your changes.</p></td>
       </tr>
       <tr class="even">
       <td style="text-align: left;"><p><strong>Cancel</strong></p></td>
       <td style="text-align: left;"><p>Click <strong>Cancel</strong> to clear your changes and start over.</p></td>
       </tr>
       </tbody>
       </table>

9.  When finished, click **Save**.

10. To verify packet capture, at **Configure > Services > Service
    Instances**, select the analyzer service instance and click **View
    Console**.

    The packet capture displays; see
    `Figure 6 <configure-traffic-analyzer-vnc.html#view-console-analyzer>`__.
    The analyzer service VM launches the Contrail-enhanced Wireshark as
    it starts and captures the mirrored packets destined to this
    service.

    |Figure 6: Service Instances View Console|

 

.. |Figure 1: Service Templates| image:: images/s041612.gif
.. |Figure 2: Create Service Template| image:: images/s041613.gif
.. |Figure 3: Create Service Instances| image:: images/s041858.gif
.. |Figure 4: Create Policy| image:: images/s041859.gif
.. |Figure 5: Create Policy Rules| image:: images/s041833.gif
.. |Figure 6: Service Instances View Console| image:: images/s041869.gif
