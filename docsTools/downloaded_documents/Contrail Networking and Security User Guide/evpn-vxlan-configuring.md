# Configuring EVPN and VXLAN

 

Contrail supports Ethernet VPNs (EVPN) and Virtual Extensible Local Area
Networks (VXLAN).

EVPN is a flexible solution that uses Layer 2 overlays to interconnect
multiple edges (virtual machines) within a data center. Traditionally,
the data center is built as a flat Layer 2 network with issues such as
flooding, limitations in redundancy and provisioning, and high volumes
of MAC address learning, which cause churn during node failures. EVPNs
are designed to address these issues without disturbing flat MAC
connectivity.

In EVPNs, MAC address learning is driven by the control plane, rather
than by the data plane, which helps control learned MAC addresses across
virtual forwarders, thus avoiding flooding. The forwarders advertise
locally learned MAC addresses to the controllers. The controllers use
MP-BGP to communicate with peers. The peering of controllers using BGP
for EVPN results in better and faster convergence.

With EVPN, MAC learning is confined to the virtual networks to which the
virtual machine belongs, thus isolating traffic between multiple virtual
networks. In this manner, virtual networks can share the same MAC
addresses without any traffic crossover.

*Unicast in EVPNs*

Unicast forwarding is based on MAC addresses where traffic can terminate
on a local endpoint or is encapsulated to reach the remote endpoint.
Encapsulation can be MPLS/UDP, MPLS/GRE, or VXLAN.

*BUM Traffic in EVPN*

Multicast and broadcast traffic is flooded in a virtual network. The
replication tree is built by the control plane, based on the
advertisements of end nodes (virtual machines) sent by forwarders. Each
virtual network has one distribution tree, a method that avoids
maintaining multicast states at fabric nodes, so the nodes are
unaffected by multicast. The replication happens at the edge forwarders.
Per-group subscription is not provided. Broadcast, unknown unicast, and
multicast (BUM) traffic is handled the same way, and gets flooded in the
virtual network to which the virtual machine belongs.

*VXLAN*

VXLAN is an overlay technology that encapsulates MAC frames into a UDP
header at Layer 2. Communication is established between two virtual
tunnel endpoints (VTEPs). VTEPs encapsulate the virtual machine traffic
into a VXLAN header, as well as strip off the encapsulation. Virtual
machines can only communicate with each other when they belong to the
same VXLAN segment. A 24-bit virtual network identifier (VNID) uniquely
identifies the VXLAN segment. This enables having the same MAC frames
across multiple VXLAN segments without traffic crossover. Multicast in
VXLAN is implemented as Layer 3 multicast, in which endpoints subscribe
to groups.

*Design Details of EVPN and VXLAN*

In Contrail Release 1.03 and later, EVPN is enabled by default. The
supported forwarding modes include:

-   Fallback bridging—IPv4 traffic lookup is performed using the IP FIB.
    All non-IPv4 traffic is directed to a MAC FIB.

-   Layer 2-only— All traffic is forwarded using a MAC FIB lookup.

You can configure the forwarding mode individually on each virtual
network.

EVPN is used to share MAC addresses across different control planes in
both forwarding models. The result of a MAC address lookup is a next
hop, which, similar to IP forwarding, points to a local virtual machine
or a tunnel to reach the virtual machine on a remote server. The tunnel
encapsulation methods supported for EVPN are MPLSoGRE, MPLSoUDP, and
VXLAN. The encapsulation method selected is based on a user-configured
priority.

In VXLAN, the VNID is assigned uniquely for every virtual network
carried in the VXLAN header. The VNID uniquely identifies a virtual
network. When the VXLAN header is received from the fabric at a remote
server, the VNID lookup provides the VRF of the virtual machine. This
VRF is used for the MAC lookup from the inner header, which then
provides the destination virtual machine.

Non-IP multicast traffic uses the same multicast tree as for IP
multicast (255.255.255.255). The multicast is matched against the
all-broadcast prefix in the bridging table (FF:FF:FF:FF:FF:FF). VXLAN is
not supported for IP/non-IP multicast traffic.

The following table summarizes the traffic and encapsulation types
supported for EVPN.

 

**Encapsulation**

**MPLS-GRE**

**MPLS-UDP**

**VXLAN**

**Traffic Type**

**IP unicast**

Yes

Yes

No

**IP-BUM**

Yes

Yes

No

**non IP unicast**

Yes

Yes

Yes

**non IP-BUM**

Yes

Yes

No

## Configuring the VXLAN Identifier Mode

You can configure the global VXLAN identifier mode to select an
auto-generated VNID or a user-generated VXLAN ID, either through the
Contrail Web UI or by modifying a python file.

To configure the global VXLAN identifier mode:

1.  <span id="jd0e165">From the Contrail Web UI, select **Configure &gt;
    Infrastucture &gt; Global Config**.</span>

    The Global Config options and values are displayed in the Global
    Config window.

    ![Figure 1: Global Config Window for VXLAN ID](images/s018533.png)

2.  <span id="jd0e177">Click the edit icon <span
    class="graphic">![](images/s018510.png)</span>.</span>

    The Edit Global Config window is displayed as shown in
    [Figure 2](evpn-vxlan-configuring.html#edit-global-config-vxmode).

    ![Figure 2: Edit Global Config Window for VXLAN Identifier
    Mode](images/s018508.png)

3.  <div id="jd0e190">

    Select one of the following:

    -   **Auto Configured**— The VXLAN identifier is automatically
        assigned for the virtual network.

    -   **User Configured**– You must provide the VXLAN identifier for
        the virtual network.

    **Note**
    When **User Configured** is selected, if you do not provide an
    identifier, then VXLAN encapsulation *is not used* and the mode
    falls back to MPLS.

    </div>

Alternatively, you can set the VXLAN identifier mode by using Python to
modify the `/opt/contrail/utils/encap.py` file as follows:

`python encap.py <add | update | delete > <username > < password > < tenant_name > < config_node_ip >`

## Configuring Forwarding

In Contrail, the default forwarding mode is enabled for fallback
bridging (IP FIB and MAC FIB). The mode can be changed, either through
the Contrail Web UI or by using python provisioning commands.

To change the forwarding mode:

1.  <span id="jd0e242">From the Contrail Web UI, select **Configure &gt;
    Networking &gt; Networks**.</span>

2.  <span id="jd0e248">Select the virtual network that you want to
    change the forwarding mode for.</span>

3.  <span id="jd0e251">Click the gear icon <span
    class="graphic">![](images/s018509.png)</span> and select
    **Edit**.</span>

    The Edit Network window is displayed as shown in
    [Figure 3](evpn-vxlan-configuring.html#edit-network-window).

    ![Figure 3: Edit Network Window](images/s042518.png)

    Under the Advanced Options select the forwarding mode from the
    following choices:

    -   Select **Default** to enable the default forwarding mode.

    -   Select **L2 and L3** to enable IP and MAC FIB (fallback
        bridging).

    -   Select **L2 Only** to enable only MAC FIB.

    -   Select **L3 Only** to enable only IP.

**Note**

The full list of forwarding modes are only displayed if you change
entries in the
`/usr/src/contrail/contrail-web-core/config/config.global.js` file. For
example:

1.  <span id="jd0e303">To make the **L2** selection available locate the
    following:</span>
    <div id="jd0e309" class="example" dir="ltr">

        config.network = {};
        config.network.L2_enable = false;

    </div>
2.  <span id="jd0e312">Change the entry to the following:</span>
    <div id="jd0e315" class="example" dir="ltr">

        config.network = {};
        config.network.L2_enable = true;

    </div>
3.  <span id="jd0e318">To make the other selections available, modify
    the corresponding entries.</span>
4.  <span id="jd0e321">Save the file and quit the editor.</span>
5.  <span id="jd0e324">Restart the Contrail Web user interface process
    (webui).</span>

Alternatively, you can use the following python provisioning command to
change the forwarding mode:

`python provisioning_forwarding_mode --project_fq_name 'defaultdomain: admin' --vn_name vn1 --forwarding_mode < l2_l3| l2 >`

Options:

`l2_l3` = Enable IP FIB and MAC FIB (fallback bridging)

`l2` = Enable MAC FIB only (Layer 2 only)

## Configuring the VXLAN Identifier

The VXLAN identifier can be set only if the VXLAN network identifier
mode has been set to User Configured. You can then set the VXLAN ID by
either using the Contrail Web UI or by using Python commands.

To configure the global VXLAN identifier:

1.  <span id="jd0e359">From the Contrail Web UI, select **Configure &gt;
    Networking &gt; Networks**.</span>

2.  <span id="jd0e365">Select the virtual network that you want to
    change the forwarding mode for.</span>

3.  <span id="jd0e368">Click the gear icon <span
    class="graphic">![](images/s018509.png)</span> and select
    **Edit**.</span>

    The Edit Network window is displayed. Select the **Advanced
    Options** as shown in
    [Figure 4](evpn-vxlan-configuring.html#edit-global-config-vxid).

    ![Figure 4: Edit Network Window for VXLAN
    Identifier](images/s018534.png)

4.  <span id="jd0e387">Type the VXLAN identifier.</span>

5.  <span id="jd0e390">Click **Save**.</span>

Alternatively, you can use the following Python provisioning command to
configure the VXLAN identifier:

`python provisioning_forwarding_mode --project_fq_name 'defaultdomain: admin' --vn_name vn1 --forwarding_mode < vxlan_id >`

## Configuring Encapsulation Methods

The default encapsulation mode for EVPN is MPLS over UDP. All packets on
the fabric are encapsulated with the label allocated for the virtual
machine interface. The label encoding and decoding is the same as for IP
forwarding. Additional encapsulation methods supported for EVPN include
MPLS over GRE and VXLAN. MPLS over UDP is different from MPLS over GRE
only in the method of tunnel header encapsulation.

VXLAN has its own header and uses a VNID label to carry the traffic over
the fabric. A VNID is assigned with every virtual network and is shared
by all virtual machines in the virtual network. The VNID is mapped to
the VRF of the virtual network to which it belongs.

The priority order in which to apply encapsulation methods is determined
by the sequence of methods set either from the Contrail Web UI or in the
`encap.py` file.

To configure the global VXLAN identifier mode:

-   From the Contrail Web UI, select **Configure &gt; Infrastucture &gt;
    Global Config**.

-   The Global Config options are displayed.

-   Click the edit icon <span
    class="graphic">![](images/s018510.png)</span>.

The Edit Global Config window is displayed as shown in
[Figure 5](evpn-vxlan-configuring.html#edit-global-config-encapriority).

![Figure 5: Edit Global Config Window for Encapsulation Priority
Order](images/s018508.png)

Under Encapsulation Priority Order select one of the following:

-   **MPLS over UDP**

-   **MPLS over GRE**

-   **VxLAN**

Click the + plus symbol to the right of the first priority to add a
second priority or third priority.

Use the following procedure to change the default encapsulation method
to VXLAN by editing the `encap.py` file.

**Note**

VXLAN is *only* supported for EVPN unicast. It is not supported for IP
traffic or multicast traffic. VXLAN priority and presence in the
`encap.py` file or configured in the Web UI is ignored for traffic not
supported by VXLAN.

To set the priority of encapsulation methods to VXLAN:

1.  <span id="jd0e483">Modify the `encap.py` file found in the
    `/opt/contrail/utils/` directory.</span>

    The default encapsulation line is:

    `encap_obj=EncapsulationPrioritiesType(encapsulation=['MPLSoUDP','M PLSoGRE'])`

    Modify the line to:

    `encap_obj=EncapsulationPrioritiesType(encapsulation=['VXLAN', 'MPLSoUDP','MPLSoGRE'])`

2.  <span id="jd0e502">After the status is modified, execute the
    following script:</span>

    `python encap_set.py <add|update|delete> <username> <password> <tenant_name> <config_node_ip>`

    The configuration is applied globally for all virtual networks.

 
