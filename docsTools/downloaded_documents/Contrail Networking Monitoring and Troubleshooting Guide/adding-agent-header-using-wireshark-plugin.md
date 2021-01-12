# Using the Wireshark Plugin to Analyze Packets Between vRouter and vRouter Agent on pkt0 Interface

 

Wireshark is a an application that analyzes packets from a network and
displays the packet information in detail.

<span id="jd0e12">Contrail Networking Release 2008 and later supports
the Wireshark `agent_header.lua` plugin, which enables you to capture
and analyze the packets exchanged between a vRouter data plane and
vRouter agent.</span> You can capture the packets by executing the <span
class="cli" v-pre="">vifdump -i 2</span> and the <span class="cli"
v-pre="">tcpdump -i pkt0</span> commands in DPDK mode and kernel mode
respectively. In release 2008, the Wireshark agent\_header.lua plugin is
supported on Macintosh OS computers only. .<span id="jd0e24">Starting
from release 2011, the Wireshark `agent_header.lua` plugin is supported
on Macintosh OS as well as Windows OS computers.</span> Wireshark also
enables you to add agent header information to the captured packets.

<span class="kbd user-typing" v-pre="">Before you begin</span>

You must ensure that the Wireshark application is installed on your
computer. You can download Wireshark from the [Download
Wireshark](https://www.wireshark.org/#download) page.

<span class="kbd user-typing" v-pre="">Configuration</span>

Follow these steps to configure the Wireshark plugin and dissect agent
header information in a packet:

1.  <span id="jd0e49">Download the Wireshark plugin from GitHub:
    <https://github.com/tungstenfabric/tf-vrouter/tree/master/utils/agent_hdr_plugin>.</span>

2.  <span id="jd0e55">Copy the plugin in to the following Wireshark
    directory on your Macintosh OS computer:
    `/Applications/Wireshark.app/Contents/PlugIns/wireshark/`.</span>

3.  <span id="jd0e61">Verify that the `agent_hdr.lua` plugin is loaded
    successfully in Wireshark. Relaunch Wireshark and navigate to
    **Wireshark** &gt; **About Wireshark** &gt; **Plugins** to verify
    that the plugin is loaded in the **Plugins** section. See
    [Figure 1](adding-agent-header-using-wireshark-plugin.html#agent-hdr-plugin-loaded).</span>

    ![Figure 1: The Plugin is Loaded in Wireshark](images/s060265.png)

4.  <span id="step-four">Pass the pcap file through editcap to add a
    custom encapsulation type for a packet:</span>

    `editcap -T user0 <pcap-file-to-be-read> <output.pcap>`

5.  <span id="jd0e91">In Wireshark, navigate to **Wireshark** &gt;
    **Preferences** &gt; **Protocols** &gt; **DLT\_USER** &gt; **Edit
    Encapsulation Table**. See
    [Figure 2](adding-agent-header-using-wireshark-plugin.html#encapsulation-table).</span>

    ![Figure 2: Edit Encapsulation Table](images/s060266.png)

6.  <span id="jd0e115">In the **Edit Encapsulation Table**, add the
    `agent_hdr` as a payload protocol for the packet. See
    [Figure 3](adding-agent-header-using-wireshark-plugin.html#add-agent-hdr).</span>

    ![Figure 3: Add Agent Header to a Packet](images/s060267.png)

7.  <span id="jd0e130">Using Wireshark, open the modified pcap file you
    generated in step
    [4](adding-agent-header-using-wireshark-plugin.html#step-four).
    Wireshark displays the parsed packets. See
    [Figure 4](adding-agent-header-using-wireshark-plugin.html#modified-parsed-packets).</span>

    ![Figure 4: Packets Expanded Using the Wireshark
    Plugin](images/s060268.png)

Follow these steps to configure the Wireshark plugin in a Windows OS
computer and dissect agent header information in a packet:

1.  <span id="jd0e145">Download the Wireshark plugin from GitHub:
    <https://github.com/tungstenfabric/tf-vrouter/tree/master/utils/agent_hdr_plugin>.</span>

2.  <span id="jd0e151">If you are using Windows 32-bit OS, copy the
    plugin in to the following Wireshark directory on your computer:
    `C:\Program Files (x86)\Wireshark\`.</span>

    If you are using Windows 64-bit OS, copy the plugin in to the
    following Wireshark directory on your computer:
    `C:\Program Files\Wireshark\plugins\`.

3.  <span id="jd0e162">Verify that the `agent_hdr.lua` plugin is loaded
    successfully in Wireshark. Relaunch Wireshark and navigate to
    **Help** &gt; **About Wireshark** &gt; **Plugins** to verify that
    the plugin is loaded in the **Plugins** section.</span>

4.  <span id="step-four-ms">Open command prompt in <span
    class="kbd user-typing" v-pre="">Run as administrator</span> mode
    and navigate to `C:\Program Files\Wireshark` to use editcap. Pass
    the pcap file through editcap to add a custom encapsulation type for
    a packet:</span>

    `editcap -T user0 <pcap-file-to-be-read> <output.pcap>`

5.  <span id="jd0e192">In Wireshark, navigate to **Edit** &gt;
    **Preferences** &gt; **Protocols** &gt; **DLT\_USER** &gt; **Edit
    Encapsulation Table**.</span>

6.  <span id="jd0e210">In the **Edit Encapsulation Table**, add the
    `agent_hdr` as a payload protocol for the packet. See .</span>

7.  <span id="jd0e219">Using Wireshark, open the modified pcap file you
    generated in step
    [4](adding-agent-header-using-wireshark-plugin.html#step-four-ms).
    Wireshark displays the parsed packets.</span>

The `agent_header.lua` plugin is also available in contrail-tools
container. You must perform the following steps to use the plugin from
the contrail-tools container:

1.  <span id="jd0e230">Log in to vRouter as a root user.</span>

2.  <span id="jd0e233">Use the following command to view the summary of
    eachpacket in the pcap file:</span>

    <span class="cli" v-pre="">tshark3\_2 -nr &lt;pcap file&gt; -o
    "uat:user\_dlts:\\"User
    0(DLT=147)\\",\\"ag\_hdr\\",\\"0\\",\\"\\",\\"0\\",\\"\\"" -t
    ad</span>

3.  <span id="jd0e239">Use the following command to view detailed
    informationof the packets in the pcap file:</span>

    <span class="cli" v-pre=""> tshark3\_2 -nr &lt;pcap file&gt; -o
    "uat:user\_dlts:\\"User0
    (DLT=147)\\",\\"ag\_hdr\\",\\"0\\",\\"\\",\\"0\\",\\"\\"" -T
    pdml</span>

<div class="table">

<div class="caption">

Release History Table

</div>

<div class="table-row table-head">

<div class="table-cell">

Release

</div>

<div class="table-cell">

Description

</div>

</div>

<div class="table-row">

<div class="table-cell">

[2011](#jd0e24)

</div>

<div class="table-cell">

Starting from release 2011, the Wireshark `agent_header.lua` plugin is
supported on Macintosh OS as well as Windows OS computers.

</div>

</div>

<div class="table-row">

<div class="table-cell">

[2008](#jd0e12)

</div>

<div class="table-cell">

Contrail Networking Release 2008 and later supports the Wireshark
`agent_header.lua` plugin, which enables you to capture and analyze the
packets exchanged between a vRouter data plane and vRouter agent.

</div>

</div>

</div>

 
