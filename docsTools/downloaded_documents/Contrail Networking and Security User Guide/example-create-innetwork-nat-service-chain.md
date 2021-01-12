# Example: Creating an In-Network-NAT Service Chain

 

<div id="intro">

<div class="mini-toc-intro">

This example provides instructions to create an in-network-nat service
chain by using the Contrail Command user interface (UI).

</div>

</div>

### Prerequisites

-   **Hardware and Software Requirements**

    <span class="kbd user-typing" v-pre="">Hardware</span>

    -   Processor: 4 core x86

    -   Memory: 32GB RAM

    -   Storage: at least 128GB hard disk

    <span class="kbd user-typing" v-pre="">Software</span>

    -   Contrail Release 3.2 or later

        **Note**

        For Contrail Networking Release 3.2 through Release 4.1, you use
        the Contrail Web UI. For more information, see [Example:
        Creating a In-Network-NAT Service Chain by Using Contrail Web
        UI](/documentation/en_US/contrail4.1/topics/example/example-create-innetwork-nat-service-chain.html).

-   **Create Network IPAM (IP Address Management)**

    1.  <span id="jd0e57">Click **Overlay**&gt;**IPAM**.</span>

        The IP Address Management page is displayed.

    2.  <span id="jd0e68">Click **Create** to create a new network
        IPAM.</span>

    3.  <span id="jd0e74">Enter a name for the IPAM in the name
        field.</span>

    4.  <span id="jd0e77">Select **Default** from the DNS list.</span>

    5.  <span id="jd0e83">Enter valid IP address in the NTP Server IP
        field.</span>

    6.  <span id="jd0e86">Enter domain name in the Domain Name
        field.</span>

    7.  <span id="jd0e89">Click **Create**.</span>

        The IP Address Management page is displayed.

### Overview

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
interface. For more information, see [Service
Chaining](../task/configuration/service-chaining-vnc.html).

### Configuration

<div class="mini-toc-intro">

These topics provide instructions to create an in-network-nat service
chain.

</div>

-   [Create Virtual
    Network](example-create-innetwork-nat-service-chain.html#jd0e114)

-   [Create Virtual
    Machine](example-create-innetwork-nat-service-chain.html#create_virtual_machine)

-   [Configure Service
    Template](example-create-innetwork-nat-service-chain.html#jd0e339)

-   [Add Service
    Instance](example-create-innetwork-nat-service-chain.html#jd0e457)

-   [Create Service
    Policy](example-create-innetwork-nat-service-chain.html#jd0e572)

-   [Attach Service
    Policy](example-create-innetwork-nat-service-chain.html#jd0e703)

-   [Launch Virtual
    Machine](example-create-innetwork-nat-service-chain.html#jd0e756)

#### Create Virtual Network

#### Step-by-Step Procedure

Use the Contrail Command UI to create a left virtual network, right
virtual network, and management virtual network.

To create a left virtual network:

1.  <span id="jd0e123">Click **Overlay**&gt;**Virtual Networks**.</span>

    The All Networks page is displayed.

2.  <span id="create-vn-2">Click **Create** to create a network.</span>

    The Create Virtual Network page is displayed.

3.  <span id="jd0e142">In the **Name** field enter <span
    class="kbd user-typing" v-pre="">test-left-VN</span> for the left
    virtual network.</span>

4.  <span id="jd0e151">Select **(Default) User defined subnet only**
    from the **Allocation Mode** list.</span>

5.  <span id="jd0e160">Click **+Add** in the Subnets section to add
    subnets.</span>

    In the row that is displayed,

    1.  <span id="jd0e170">Select an IPAM for the virtual network from
        the Network IPAM list.</span>
    2.  <span id="jd0e173">Enter <span class="kbd user-typing"
        v-pre="">192.0.2.0/24</span> in the **CIDR** field.</span>

6.  <span id="create-vn-10">Click **Create**.</span>

    The All Networks page is displayed. All virtual networks that you
    created are displayed in this page.

    **Note**

    Management network is not used to route packets. This network is
    used to help debug issues with the virtual machine.

Repeat steps
[2](example-create-innetwork-nat-service-chain.html#create-vn-2) through
[6](example-create-innetwork-nat-service-chain.html#create-vn-10) to
create the right virtual network (<span class="kbd user-typing"
v-pre="">test-right-VN</span>) and management virtual network (<span
class="kbd user-typing" v-pre="">test-mgmt-VN</span>).

#### Create Virtual Machine

#### Step-by-Step Procedure

Follow these steps to create a left virtual machine by using the
Contrail Command UI.

1.  <span id="jd0e212">Click **Workloads** &gt; **Instances**.</span>

    The Instances page is displayed.

2.  <span id="create-vm-cc-2">Click **Create**.</span>

    The Create Instance page is displayed.

3.  <span id="jd0e231">Select **Virtual Machine** option button as the
    serve type.</span>

4.  <span id="jd0e237">Enter <span class="kbd user-typing"
    v-pre="">test-left-VM</span> for the left virtual machine in the
    **Instance Name** field.</span>

5.  <span id="jd0e246">Select **Image** as the boot source from the
    **Select Boot Source** list.**Note**</span>

    vSRX image with M1.large flavor is recommended for in-network-nat
    virtual machine.

6.  <span id="jd0e258">Select <span class="kbd user-typing"
    v-pre="">vSRX image</span> file from the **Select Image**
    list.</span>

7.  <span id="jd0e267">Select <span class="kbd user-typing"
    v-pre="">M1.large</span> flavor from the **Select Flavor**
    list.</span>

8.  <span id="jd0e276">Select the network you want to associate with the
    left virtual machine by clicking **&gt;** next to the name of the
    virtual machine listed in the Available Networks table.</span>

    For the left virtual machine, select **test-left-VN**. For the right
    virtual machine, select **test-right-VN**. For the management
    virtual machine, select **test-mgmt-VN**.

    The network is added to the Allocated Networks table.

9.  <span id="jd0e295">Select <span class="kbd user-typing"
    v-pre="">nova</span> from the **Availability Zone**
    list.**Note**</span>

    You can choose any other availability zone.

10. <span id="jd0e307">Select <span class="kbd user-typing"
    v-pre="">5</span> from the **Count (1-10)** list.**Note**</span>

    You can choose any value from 1 through 10.

11. <span id="create-vm-cc-9">Click **Create** to launch the left
    virtual machine instance.</span>

    The Instances page is displayed. The virtual machine instances that
    you created are listed on the Instances page.

Repeat steps
[2](example-create-innetwork-nat-service-chain.html#create-vm-cc-2)
through
[11](example-create-innetwork-nat-service-chain.html#create-vm-cc-9) to
create right virtual machine instance (<span class="kbd user-typing"
v-pre="">test-right-VM</span>) and management virtual machine instance
(**test-mgmt-VM**).

#### Configure Service Template

#### Step-by-Step Procedure

Follow these steps to create a service template by using the Contrail
Command UI:

1.  <span id="jd0e346">Click **Services**&gt;**Catalog**.</span>

    The VNF Service Templates page is displayed.

2.  <span id="jd0e357">Click **Create**.</span>

    The Create VNF Service Template page is displayed.

3.  <span id="jd0e365">Enter <span class="kbd user-typing"
    v-pre="">test-service-template</span> in the **Name** field.</span>

4.  <span id="jd0e374">Select **v2** as the version type.**Note**</span>

    Starting with Release 3.2, Contrail supports only *Service Chain
    Version 2* (**v2**).

5.  <span id="jd0e389">Select **Virtual Machine** as the virtualization
    type.</span>

6.  <span id="jd0e395">Select **In-Network Nat** as the service
    mode.</span>

7.  <span id="jd0e401">Select **Firewall** as the service type.</span>

8.  <span id="jd0e407">From the Interface section,</span>

    -   Select **left** as the interface type from the **Interface
        Type** list.

    -   Click **+ Add**.

        The Interface Type list is added to the table.

        Select **right** as the interface type.

    -   Click **+ Add** again.

        Another Interface Type list is added to the table.

        Select **management** as the interface type.

    **Note**

    The interfaces created on the virtual machine must follow the same
    sequence as that of the interfaces in the service template.

9.  <span id="jd0e449">Click **Create** to create the service
    template.</span>

    The VNF Service Templates page is displayed. The service template
    that you created is displayed in the VNF Service Templates page.

#### Add Service Instance

#### Step-by-Step Procedure

Follow these steps to add a service instance by using the Contrail
Command UI:

1.  <span id="jd0e464">Click **Services**&gt;**Deployments**.</span>

    The VNF Service Instances page is displayed.

2.  <span id="jd0e475">Click **Create**.</span>

    The Create VNF Service Instance page is displayed.

3.  <span id="jd0e483">Enter <span class="kbd user-typing"
    v-pre="">test-service-instance</span> in the **Name** field.</span>

4.  <span id="jd0e492">Select **test-service-template -
    \[in-network-nat, (left, right, management)\] - v2** from the
    **Service Template** list.</span>

    The **Interface Type** and **Virtual Network** fields are displayed.

5.  <span id="jd0e509">Select the virtual network for each interface
    type as given below.</span>
    -   **left**—Select the left virtual network (**test-left-VN**) that
        you created.

    -   **right**—Select the right virtual network (**test-right-VN**)
        that you created.

    -   **management**—Select the management virtual network
        (**test-management-VN**) that you created.

6.  <span id="jd0e537">Click the **Port Tuples** section and click
    **+Add**.</span>

    Select the virtual machine instance for each interface type as given
    below.

    -   **left**—Select the left virtual machine instance that you
        created.

    -   **right**—Select the right virtual machine instance that you
        created.

    -   **management**—Select the management virtual machine instance
        that you created.

7.  <span id="jd0e564">Click **Create** to create the service
    instance.</span>

    The VNF Service Instances page is displayed. The service instance
    that you created is displayed in the VNF Service Instances page.

#### Create Service Policy

#### Step-by-Step Procedure

Follow these steps to create a service policy by using the Contrail
Command UI.

1.  <span id="jd0e579">Click **Overlay** &gt; **Network
    Policies**.</span>

    The Network Policies page is displayed.

2.  <span id="jd0e590">Click **Create**.</span>

    The Network Policy tab of the Create Network Policy page is
    displayed.

3.  <span id="jd0e598">Enter <span class="kbd user-typing"
    v-pre="">test-network-policy</span> in the **Policy Name**
    field.</span>

4.  <span id="jd0e607">In the **Policy Rule(s)** section,</span>
    -   Select **pass** from the **Action** list.

    -   Select **ANY** from the **Protocol** list.

    -   Select **Network** from the **Source Type** list.

    -   Select the **test-left-VN** from the **Source** list.

    -   In the **Source Port** field, leave the default option, **Any**,
        as is.

    -   Select **&lt; &gt;** from the **Direction** list.

    -   Select **Network** from the **Destination Type** list.

    -   Select the **test-right-VN** from the **Destination** list.

    -   In the **Destination Ports** field, leave the default option,
        **Any**, as is.

5.  <span id="jd0e695">Click **Create** to create the service
    policy.</span>

    The Network Policies page is displayed. All policies that you
    created are displayed in the Network Policies page.

#### Attach Service Policy

#### Step-by-Step Procedure

Follow these steps to attach a service policy:

1.  <span id="jd0e710">Click **Overlay**&gt;**Virtual Networks**.</span>

    The All networks page is displayed.

2.  <span id="jd0e721">Attach service policy to the left virtual network
    (**test-left-VN**) and right virtual network (**test-right-VN**)
    that you created.</span>

    To attach service policy,

    1.  <span id="jd0e734">Select the check box next to the name of the
        virtual network.</span>

    2.  <span id="jd0e737">Hover over to the end of the selected row and
        click the **Edit** icon.</span>

        The Edit Virtual Network page is displayed.

    3.  <span id="jd0e745">Select the network policy from the Network
        Policies list.</span>

3.  <span id="jd0e748">Click **Save** to save the changes.</span>

    The Virtual Networks page is displayed.

#### Launch Virtual Machine

#### Step-by-Step Procedure

You can launch virtual machines from Contrail Command and test the
traffic through the service chain by doing the following:

1.  <span id="jd0e763">Launch the left virtual machine in left virtual
    network. See [Create Virtual
    Machine](example-create-innetwork-nat-service-chain.html#create_virtual_machine).</span>

2.  <span id="jd0e768">Launch the right virtual machine in right virtual
    network. See [Create Virtual
    Machine](example-create-innetwork-nat-service-chain.html#create_virtual_machine).</span>

3.  <span id="jd0e773">Ping the left virtual machine IP address from the
    right virtual machine.</span>

    Follow these steps to ping a virtual machine:

    1.  <span id="jd0e779">Click **Workloads**&gt;**Instances**.</span>

        The Instances page is displayed.

    2.  <span id="jd0e790">Click the open console icon next to
        **test-right-VM**.</span>

        The Console page is displayed.

    3.  <span id="jd0e798">Log in using root user credentials.</span>

    4.  <span id="jd0e801">Ping the left virtual machine IP address
        (**190.0.2.3**) from the Console.</span>

 
