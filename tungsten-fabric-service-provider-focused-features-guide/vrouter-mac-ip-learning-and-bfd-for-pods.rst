Tungsten Fabric vRouter MAC Address - IP Address Learning and Bidirectional Forwarding and Detection Health Checking for Pods on Virtual Machines
=================================================================================================================================================

:date: 2020-12-11

In Tungsten Fabric Release 2011, the Tungsten Fabric vRouter agent
dynamically learns the MAC address-IP address binding of a pod deployed
on a virtual machine (VM). This enables the vRouter agent to perform an
efficient pod to pod communication in Tungsten Fabric.

In previous releases, the MAC address - IP address of a pod is assigned
by OpenStack. Tungsten Fabric is unable to perform pod to pod
communication as it does not have the reachability information of the
pods hosted by the VMs.

In the Contrail Command user interface (UI), the **Dynamic Address
Learning** checkbox must be enabled while creating a virtual network.
This enables the vRouter agent to learn the MAC address-IP address of
the pods connected to the virtual network.

In release 2011, Tungsten Fabric also supports Bidirectional
Forwarding and Detection (BFD) based health check to verify the
liveliness of a pod. The BFD session is enabled for a list of
target IP addresses. In release 2011, Tungsten Fabric supports IPv4
target IP addresses. The vRouter agent learns these IP addresses through
the MAC address - IP address learning feature. The BFD health check
session is initiated, when the vRouter agent learns the target IP
address assigned to the BFD health check service. The BFD health check
monitors the target list of health check for newly learnt IP addresses.
If the BFD session is detected as DOWN, the vRouter agent deletes the
routes generated for the MAC address - IP address of a pod learned by
the vRouter.

The vRouter agent also sends address resolution protocol (ARP) packets
in regular intervals to newly learnt IP addresses. The vRouter agent
performs this action to check a pod’s liveliness. If a pod responds to
the ARP request sent by the vRouter, the pod is considered as UP. If the
pod does not respond to the ARP packets, the pod is considered as DOWN.
If vRouter identifies a pod as DOWN, it deletes the routes generated for
the respective MAC address-IP address of the pod.

You must perform the following steps to enable the vRouter to
dynamically learn the MAC address - IP address of a pod:

1. Navigate to :menuselection:`Overlay > Virtual Networks` page. Click **Create**
   to create a new virtual network.

   Alternatively, you can also edit the properties of an existing
   virtual network. To edit an existing virtual network, select a
   virtual network from the displayed list and click the **Edit
   (pencil)** icon.

2. Follow the steps given :ref:`Create Virtual
   Network <CreateVN>` to create a virtual network.

3. In the **Create Virtual Network** page, select **Dynamic Address
   Learning** to enable vRouter to learn the MAC address - IP address of
   pods dynamically.

4. Click **Create** to create a VN where the vRouter can learn the MAC
   address - IP address of the pods connected to the VN.

   The **Virtual Networks** page is displayed listing the newly created
   virtual network.

You must perform the following steps to enable BFD based healthcheck for
the pods deployed on a VM:

1. Navigate to :menuselection:`Services > Health Check`. Click **Create** to
   create a new BFD based health check service.

   Alternatively, you can also edit the properties of an existing
   virtual network. To edit an existing virtual network, select a
   virtual network from the displayed list and click the **Edit
   (pencil)** icon.

2. Enter values in the **Create Health Check Service** page according to
   the guidelines provided in Table 1.

3. Click **Create**.

   The **Health Check** tab is displayed listing the newly created
   health check service.

Table 1: Create Health Check Fields

+------------------------------------------+----------------------------------+
| Field                                    | Description                      |
+==========================================+==================================+
| **Name**                                 | Enter a name for the health      |
|                                          | check service you are creating.  |
+------------------------------------------+----------------------------------+
| **Health Check Type**                    | Select **VN IP List** to run     |
|                                          | health check on the IP addresses |
|                                          | of the virtual networks.         |
+------------------------------------------+----------------------------------+
| **Protocol**                             | Protocol is set to **BFD** by    |
|                                          | default when **VN IP List** is   |
|                                          | selected as the\ **Health Check  |
|                                          | Type**. BFD health check enables |
|                                          | you to verify pod liveliness.    |
+------------------------------------------+----------------------------------+
| **Add all option**                       | Select this to run BFD health    |
|                                          | check for all IP addresses       |
|                                          | learned by the vRouter Agent     |
|                                          | from learning the MAC address -  |
|                                          | IP address of a pod.             |
+------------------------------------------+----------------------------------+
| **Target IP List**                       | Select IP addresses from list to |
|                                          | run BFD health check on the      |
|                                          | selected IP addresses.           |
+------------------------------------------+----------------------------------+
| **Desired Min Tx Interval (millisecs)**  | Enter the desired minimum        |
|                                          | transmission (Tx) interval       |
|                                          | before transmitting BFD packets. |
+------------------------------------------+----------------------------------+
| **Required Min Rx Interval (milli secs)**| Enter the minimum interval       |
|                                          | between successive BFD packets   |
|                                          | that is supported by the system. |
+------------------------------------------+----------------------------------+
| **Multiplier**                           | Enter the number of BFD packets  |
|                                          | that must be missed successively |
|                                          | from the remote end to declare   |
|                                          | the BFD session as DOWN.         |
+------------------------------------------+----------------------------------+

.. list-table:: **Release History Table**
      :header-rows: 1

      * - Release
        - Description
      * - 2011
        - In Tungsten Fabric Release 2011, the Tungsten Fabric vRouter agent
          dynamically learns the MAC address-IP address binding of a pod deployed
          on a virtual machine (VM). This enables the vRouter agent to perform an
          efficient pod to pod communication in Tungsten Fabric.
      * - 2011
        - In release 2011, Tungsten Fabric also supports Bidirectional
          Forwarding and Detection (BFD) based health check to verify the
          liveliness of a pod.
 
