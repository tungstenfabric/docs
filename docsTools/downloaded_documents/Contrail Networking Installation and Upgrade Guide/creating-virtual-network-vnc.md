# Creating a Virtual Network with OpenStack Contrail

 

You can create virtual networks in Contrail Networking from the
OpenStack. The following procedure shows how to create a virtual network
when using OpenStack.

1.  <span id="jd0e30">To create a virtual network when using OpenStack
    Contrail, select **Project &gt; Network &gt; Networks**. The
    **Networks** page is displayed. See
    [Figure 1](creating-virtual-network-vnc.html#networks-openstack).</span>

    ![Figure 1: Networks Page](documentation/images/s008528.png)

2.  <span id="jd0e45">Click **Create Network**. The **Create Network**
    window is displayed. See
    [Figure 2](creating-virtual-network-vnc.html#create-network-os) and
    [Figure 3](creating-virtual-network-vnc.html#create-network-tab).</span>

    ![Figure 2: Create Networks](documentation/images/s008529.png)

    ![Figure 3: Subnet and Gateway
    Details](documentation/images/s008530.png)

3.  <span id="jd0e66">Click the **Network** and **Subnet** tabs to
    complete the fields in the **Create Network** window. See field
    descriptions in
    [Table 1](creating-virtual-network-vnc.html#net-field-desc-os).</span>

    Table 1: Create Network Fields

    | Field               | Description                                                                                                                           |
    |:--------------------|:--------------------------------------------------------------------------------------------------------------------------------------|
    | **Network Name**    | Enter a name for the network.                                                                                                         |
    | **Subnet Name**     | Enter a name for the subnetwork.                                                                                                      |
    | **Network Address** | Enter the network address in CIDR format.                                                                                             |
    | **IP Version\***    | Select IPv4 or IPv6.                                                                                                                  |
    | **Gateway IP**      | Optionally, enter an explicit gateway IP address for the IP address block. Check the Disable Gateway box if no gateway is to be used. |

4.  <span id="jd0e135">Click the **Subnet Details** tab to specify the
    Allocation Pool, DNS Name Servers, and Host Routes.</span>

    ![Figure 4: Additional Subnet
    Attributes](documentation/images/s008531.png)

5.  <span id="jd0e145">To save your network, click **Create** , or click
    **Cancel** to discard your work and start over.</span>

 
