Example: Creating an In-Network-NAT Service Chain
=================================================

 

.. raw:: html

   <div id="intro">

.. raw:: html

   <div class="mini-toc-intro">

This example provides instructions to create an in-network-nat service
chain by using the Contrail Command user interface (UI).

.. raw:: html

   </div>

.. raw:: html

   </div>

Prerequisites
-------------

-  **Hardware and Software Requirements**

   Hardware

   -  Processor: 4 core x86

   -  Memory: 32GB RAM

   -  Storage: at least 128GB hard disk

   Software

   -  Contrail Release 3.2 or later

      **Note**

      For Contrail Networking Release 3.2 through Release 4.1, you use
      the Contrail Web UI. For more information, see `Example: Creating
      a In-Network-NAT Service Chain by Using Contrail Web
      UI </documentation/en_US/contrail4.1/topics/example/example-create-innetwork-nat-service-chain.html>`__.

-  **Create Network IPAM (IP Address Management)**

   1. Click **Overlay**>\ **IPAM**.

      The IP Address Management page is displayed.

   2. Click **Create** to create a new network IPAM.

   3. Enter a name for the IPAM in the name field.

   4. Select **Default** from the DNS list.

   5. Enter valid IP address in the NTP Server IP field.

   6. Enter domain name in the Domain Name field.

   7. Click **Create**.

      The IP Address Management page is displayed.

Overview
--------

A service chain is a set of services that are connected across networks.
A service chain consists of service instances, left and right virtual
networks, and a service policy attached to the networks. A service chain
can have in-network services, in-network-nat services, and transparent
services.

In an in-network-nat service chain, packets are routed between service
instance interfaces. In-network-nat service chain does not require
return traffic to be routed to the source network. When a packet is
routed through the service chain, the source address of the packet
entering the left interface of the service chain is updated and is not
the same as the source address of the packet exiting the right
interface. For more information, see `Service
Chaining <../task/configuration/service-chaining-vnc.html>`__.

Configuration
-------------

.. raw:: html

   <div class="mini-toc-intro">

These topics provide instructions to create an in-network-nat service
chain.

.. raw:: html

   </div>

-  `Create Virtual
   Network <example-create-innetwork-nat-service-chain.html#jd0e114>`__

-  `Create Virtual
   Machine <example-create-innetwork-nat-service-chain.html#create_virtual_machine>`__

-  `Configure Service
   Template <example-create-innetwork-nat-service-chain.html#jd0e339>`__

-  `Add Service
   Instance <example-create-innetwork-nat-service-chain.html#jd0e457>`__

-  `Create Service
   Policy <example-create-innetwork-nat-service-chain.html#jd0e572>`__

-  `Attach Service
   Policy <example-create-innetwork-nat-service-chain.html#jd0e703>`__

-  `Launch Virtual
   Machine <example-create-innetwork-nat-service-chain.html#jd0e756>`__

Create Virtual Network
~~~~~~~~~~~~~~~~~~~~~~

Step-by-Step Procedure
~~~~~~~~~~~~~~~~~~~~~~

Use the Contrail Command UI to create a left virtual network, right
virtual network, and management virtual network.

To create a left virtual network:

1. Click **Overlay**>\ **Virtual Networks**.

   The All Networks page is displayed.

2. Click **Create** to create a network.

   The Create Virtual Network page is displayed.

3. In the **Name** field enter test-left-VN for the left virtual
   network.

4. Select **(Default) User defined subnet only** from the **Allocation
   Mode** list.

5. Click **+Add** in the Subnets section to add subnets.

   In the row that is displayed,

   1. Select an IPAM for the virtual network from the Network IPAM list.
   2. Enter 192.0.2.0/24 in the **CIDR** field.

6. Click **Create**.

   The All Networks page is displayed. All virtual networks that you
   created are displayed in this page.

   **Note**

   Management network is not used to route packets. This network is used
   to help debug issues with the virtual machine.

Repeat steps
`2 <example-create-innetwork-nat-service-chain.html#create-vn-2>`__
through
`6 <example-create-innetwork-nat-service-chain.html#create-vn-10>`__ to
create the right virtual network (test-right-VN) and management virtual
network (test-mgmt-VN).

Create Virtual Machine
~~~~~~~~~~~~~~~~~~~~~~

.. _step-by-step-procedure-1:

Step-by-Step Procedure
~~~~~~~~~~~~~~~~~~~~~~

Follow these steps to create a left virtual machine by using the
Contrail Command UI.

1.  Click **Workloads** > **Instances**.

    The Instances page is displayed.

2.  Click **Create**.

    The Create Instance page is displayed.

3.  Select **Virtual Machine** option button as the serve type.

4.  Enter test-left-VM for the left virtual machine in the **Instance
    Name** field.

5.  Select **Image** as the boot source from the **Select Boot Source**
    list.\ **Note**\ 

    vSRX image with M1.large flavor is recommended for in-network-nat
    virtual machine.

6.  Select vSRX image file from the **Select Image** list.

7.  Select M1.large flavor from the **Select Flavor** list.

8.  Select the network you want to associate with the left virtual
    machine by clicking **>** next to the name of the virtual machine
    listed in the Available Networks table.

    For the left virtual machine, select **test-left-VN**. For the right
    virtual machine, select **test-right-VN**. For the management
    virtual machine, select **test-mgmt-VN**.

    The network is added to the Allocated Networks table.

9.  Select nova from the **Availability Zone** list.\ **Note**\ 

    You can choose any other availability zone.

10. Select 5 from the **Count (1-10)** list.\ **Note**\ 

    You can choose any value from 1 through 10.

11. Click **Create** to launch the left virtual machine instance.

    The Instances page is displayed. The virtual machine instances that
    you created are listed on the Instances page.

Repeat steps
`2 <example-create-innetwork-nat-service-chain.html#create-vm-cc-2>`__
through
`11 <example-create-innetwork-nat-service-chain.html#create-vm-cc-9>`__
to create right virtual machine instance (test-right-VM) and management
virtual machine instance (**test-mgmt-VM**).

Configure Service Template
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _step-by-step-procedure-2:

Step-by-Step Procedure
~~~~~~~~~~~~~~~~~~~~~~

Follow these steps to create a service template by using the Contrail
Command UI:

1. Click **Services**>\ **Catalog**.

   The VNF Service Templates page is displayed.

2. Click **Create**.

   The Create VNF Service Template page is displayed.

3. Enter test-service-template in the **Name** field.

4. Select **v2** as the version type.\ **Note**\ 

   Starting with Release 3.2, Contrail supports only *Service Chain
   Version 2* (**v2**).

5. Select **Virtual Machine** as the virtualization type.

6. Select **In-Network Nat** as the service mode.

7. Select **Firewall** as the service type.

8. From the Interface section,

   -  Select **left** as the interface type from the **Interface Type**
      list.

   -  Click **+ Add**.

      The Interface Type list is added to the table.

      Select **right** as the interface type.

   -  Click **+ Add** again.

      Another Interface Type list is added to the table.

      Select **management** as the interface type.

   **Note**

   The interfaces created on the virtual machine must follow the same
   sequence as that of the interfaces in the service template.

9. Click **Create** to create the service template.

   The VNF Service Templates page is displayed. The service template
   that you created is displayed in the VNF Service Templates page.

Add Service Instance
~~~~~~~~~~~~~~~~~~~~

.. _step-by-step-procedure-3:

Step-by-Step Procedure
~~~~~~~~~~~~~~~~~~~~~~

Follow these steps to add a service instance by using the Contrail
Command UI:

1. Click **Services**>\ **Deployments**.

   The VNF Service Instances page is displayed.

2. Click **Create**.

   The Create VNF Service Instance page is displayed.

3. Enter test-service-instance in the **Name** field.

4. Select **test-service-template - [in-network-nat, (left, right,
   management)] - v2** from the **Service Template** list.

   The **Interface Type** and **Virtual Network** fields are displayed.

5. Select the virtual network for each interface type as given below.

   -  **left**—Select the left virtual network (**test-left-VN**) that
      you created.

   -  **right**—Select the right virtual network (**test-right-VN**)
      that you created.

   -  **management**—Select the management virtual network
      (**test-management-VN**) that you created.

6. Click the **Port Tuples** section and click **+Add**.

   Select the virtual machine instance for each interface type as given
   below.

   -  **left**—Select the left virtual machine instance that you
      created.

   -  **right**—Select the right virtual machine instance that you
      created.

   -  **management**—Select the management virtual machine instance that
      you created.

7. Click **Create** to create the service instance.

   The VNF Service Instances page is displayed. The service instance
   that you created is displayed in the VNF Service Instances page.

Create Service Policy
~~~~~~~~~~~~~~~~~~~~~

.. _step-by-step-procedure-4:

Step-by-Step Procedure
~~~~~~~~~~~~~~~~~~~~~~

Follow these steps to create a service policy by using the Contrail
Command UI.

1. Click **Overlay** > **Network Policies**.

   The Network Policies page is displayed.

2. Click **Create**.

   The Network Policy tab of the Create Network Policy page is
   displayed.

3. Enter test-network-policy in the **Policy Name** field.

4. In the **Policy Rule(s)** section,

   -  Select **pass** from the **Action** list.

   -  Select **ANY** from the **Protocol** list.

   -  Select **Network** from the **Source Type** list.

   -  Select the **test-left-VN** from the **Source** list.

   -  In the **Source Port** field, leave the default option, **Any**,
      as is.

   -  Select **< >** from the **Direction** list.

   -  Select **Network** from the **Destination Type** list.

   -  Select the **test-right-VN** from the **Destination** list.

   -  In the **Destination Ports** field, leave the default option,
      **Any**, as is.

5. Click **Create** to create the service policy.

   The Network Policies page is displayed. All policies that you created
   are displayed in the Network Policies page.

Attach Service Policy
~~~~~~~~~~~~~~~~~~~~~

.. _step-by-step-procedure-5:

Step-by-Step Procedure
~~~~~~~~~~~~~~~~~~~~~~

Follow these steps to attach a service policy:

1. Click **Overlay**>\ **Virtual Networks**.

   The All networks page is displayed.

2. Attach service policy to the left virtual network (**test-left-VN**)
   and right virtual network (**test-right-VN**) that you created.

   To attach service policy,

   1. Select the check box next to the name of the virtual network.

   2. Hover over to the end of the selected row and click the **Edit**
      icon.

      The Edit Virtual Network page is displayed.

   3. Select the network policy from the Network Policies list.

3. Click **Save** to save the changes.

   The Virtual Networks page is displayed.

Launch Virtual Machine
~~~~~~~~~~~~~~~~~~~~~~

.. _step-by-step-procedure-6:

Step-by-Step Procedure
~~~~~~~~~~~~~~~~~~~~~~

You can launch virtual machines from Contrail Command and test the
traffic through the service chain by doing the following:

1. Launch the left virtual machine in left virtual network. See `Create
   Virtual
   Machine <example-create-innetwork-nat-service-chain.html#create_virtual_machine>`__.

2. Launch the right virtual machine in right virtual network. See
   `Create Virtual
   Machine <example-create-innetwork-nat-service-chain.html#create_virtual_machine>`__.

3. Ping the left virtual machine IP address from the right virtual
   machine.

   Follow these steps to ping a virtual machine:

   1. Click **Workloads**>\ **Instances**.

      The Instances page is displayed.

   2. Click the open console icon next to **test-right-VM**.

      The Console page is displayed.

   3. Log in using root user credentials.

   4. Ping the left virtual machine IP address (**190.0.2.3**) from the
      Console.

 
