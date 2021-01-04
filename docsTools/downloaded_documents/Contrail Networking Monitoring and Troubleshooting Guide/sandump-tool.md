# Using Sandump Tool​

 

<span id="jd0e10">Starting with Contrail Networking Release 2008,
*Sandump* tool is available in contrail-tools container. You can use the
*Sandump* tool on macOS machines.</span>

Sandump tool captures the Sandesh messages from netlink connection
between Agent and vRouter (only DPDK mode) and provides interpretation
of all the captured bytes.​

<span id="jd0e21">Starting with Contrail Networking Release 2011, you
can use *Sandump* tool on Windows machines.</span>

Sandesh is a southbound interface protocol based on Apache Thrift, to
send analytics data such as system logs, object logs, UVEs, flow logs,
and the like, to the collector service in the Contrail Insights node.

You can analyze the captured bytes in Wireshark. The Wireshark plugin
parses the hex dumps of all Sandesh objects. You must use Wireshark
Release 3.2 and later.

You must have Wireshark application installed on your machine. You can
download Wireshark from the [Download
Wireshark](https://www.wireshark.org/#download) page.

For more details on Wireshark, see <https://www.wireshark.org/docs/>.

Follow the procedure to use Sandump tool:

1.  <span id="jd0e44">Run the `sandump` command. It gives summary of
    each message which is being transferred between the agent and the
    vRouter.​</span>
    <div id="jd0e50" class="sample" dir="ltr">

    <div id="jd0e51" dir="ltr">

    ` (vrouter-agent-dpdk)[root]$ ./sandump -h `

    </div>

    <div class="output" dir="ltr">

        Sandump - Sandesh dump utility
        Usage:
               ./sandump -w <filename> [filename to write the sandesh packets]
               ./sandump -c <filename> [force cleanup]
        (vrouter-agent-dpdk)[root]$                                 

    </div>

    </div>

2.  <span id="jd0e55">Copy the output into a file.</span>

    <div id="jd0e58" class="sample" dir="ltr">

    <div id="jd0e59" dir="ltr">

    `(vrouter-agent-dpdk)[root]$ ./sandump -w <filename>.pcap `

    </div>

    <div class="output" dir="ltr">

        Dumping into <filename>.pcap
        Running as user "root" and group "root". This could be dangerous.
        Capturing on 'lo'
        12 ^C
        ./sandump: closing...
        (vrouter-agent-dpdk)[root]$

    </div>

    </div>

    The command generates a file which contains sniffed bytes converted
    in to the pcap format.

3.  <span id="jd0e65">Analyze the captured packets transferred between
    the agent and the vRouter.</span>
    <div id="jd0e68" class="sample" dir="ltr">

    <div id="jd0e69" dir="ltr">

    `(vrouter-agent-dpdk)[root]$ ./sandump`

    </div>

    <div class="output" dir="ltr">

        Running as user "root" and group "root". This could be dangerous.
        Capturing on 'lo'
            1 2020-08-04 09:51:01.233639252        Agent → Vrouter      Vif 790  Operation: Dump  Type: Host  ID: 0 
            2 2020-08-04 09:51:01.251279611      Vrouter → Agent        Response, Vif 3966  Response: 0x0000000, Multiple  vr_interface_req
            3 2020-08-04 09:51:33.290323560        Agent → Vrouter      Mem Stats 869  Operation: Get 
            4 2020-08-04 09:51:33.290964111      Vrouter → Agent        Response, Mem Stats 899  Response: 0x00000000  
            5 2020-08-04 09:51:46.175797696        Agent → Vrouter      Info 137  ID: 0 Operation: Dump 
            6 2020-08-04 09:51:46.176494123      Vrouter → Agent        Response, Info 1949  Response: 0x00000001  ID: 0 
            7 2020-08-04 09:51:58.920197081        Agent → Vrouter      Nexthop 280   Nexthop ID: 0 Operation: Dump 
            8 2020-08-04 09:51:58.920905495      Vrouter → Agent        Response, Nexthop 3898  Response: 0x4000001, Multiple  vr_nexthop_req
            9 2020-08-04 09:51:58.922297667        Agent → Vrouter      Nexthop 280   Nexthop ID: 0 Operation: Dump 
           10 2020-08-04 09:51:58.922425514      Vrouter → Agent        Response, Nexthop 3930  Response: 0x4000001, Multiple  vr_nexthop_req
           11 2020-08-04 09:51:58.923525453        Agent → Vrouter      Nexthop 280   Nexthop ID: 0 Operation: Dump 
           12 2020-08-04 09:51:58.926925821      Vrouter → Agent        Response, Nexthop 792  Response: 0x0000000, Multiple  vr_nexthop_req
        ^C12 packets captured
        ./sandump: closing...
        (vrouter-agent-dpdk)[root]$ 

    </div>

    </div>

4.  <span id="jd0e73">Analyze the pcap file in WireShark.</span>
    -   Follow the procedure to analyze the packets in Wireshark for
        Windows OS.

        1.  <span id="jd0e82">Download the `sandump_wireshark_plugin`
            folder from the
            <https://github.com/tungstenfabric/tf-vrouter/tree/master/utils/sandump>
            repository.</span>

        2.  <span id="jd0e91">Copy the
            `sandump_wireshark_plugin/main.lua` file in
            `C:\Program Files\Wireshark\plugins\` folder.</span>

            Create new <span class="kbd user-typing" v-pre="">lua</span>
            folder in `C:\Program Files\Wireshark\` and copy the rest of
            the lua files present in `sandump_wireshark_plugin` folder
            to the newly created <span class="kbd user-typing"
            v-pre="">lua</span> folder.

            **Note**

            Wireshark installation directory for 32-bit Windows is
            present in `C:\Program Files (x86)\Wireshark\`and for 64-bit
            Windows is present in `C:\Program Files\Wireshark\`.

        3.  <span id="jd0e123">Run Notepad as administrator and open
            `C:/Windows/System32/drivers/etc/hosts` file.</span>

        4.  <span id="jd0e129">​​​​​​​Add the host names with the
            following details:</span>

            -   Agent IP address—0.0.0.0

            -   vRouter IP address—1.1.1.1

            [Figure 1](sandump-tool.html#HostFile_win) shows the host
            file with the required IP addresses.

            ![Figure 1: host file](images/s009683.png)

        5.  <span id="jd0e146">Open the pcap file generated from Sandump
            tool for further debugging in Wireshark.</span>

            ![Figure 2: File debugging in Wireshark](images/s060107.png)

    -   Follow the procedure to analyze the packets in Wireshark for
        macOS.

        1.  <span id="jd0e158">Download the `sandump_wireshark_plugin`
            folder from the
            <https://github.com/tungstenfabric/tf-vrouter/tree/master/utils/sandump>
            repository.</span>

        2.  <span id="jd0e167">Copy the `sandump_wireshark_plugin`
            folder in
            `/Applications/Wireshark.app/Contents/PlugIns/wireshark`
            directory which is also know as *Global Lua Plugins*
            directory.</span>

        3.  <span id="jd0e179">Un-comment the `package.prepend_path(…)`
            line in main.lua, common.lua and helpers.lua files found in
            `sandump_wireshark_plugin` folder.</span>

        4.  <span id="jd0e188">Navigate to **Wireshark** &gt; **About
            Wireshark** &gt; **Folders** &gt; **Personal configuration**
            to edit the configuration.</span>

        5.  <span id="jd0e203">​​​​​​​Create hosts file in the
            **Personal configuration** directory and add the host names
            with the following details:</span>

            -   Agent IP address—0.0.0.0

            -   vRouter IP address—1.1.1.1

            [Figure 3](sandump-tool.html#HostFile) shows the host file
            with the required IP addresses.

            ![Figure 3: host file](images/s009683.png)

        6.  <span id="jd0e223">Navigate to **Wireshark &gt;
            Preferences &gt; Name Resolution** and check **Resolve
            network (IP) addresses** option.</span>

            ![Figure 4: Wireshark—Preferences](images/s060106.png)

        7.  <span id="jd0e236">Open the pcap file generated from Sandump
            tool for further debugging in Wireshark.</span>

            ![Figure 5: File debugging in Wireshark](images/s060107.png)

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

[2011](#jd0e21)

</div>

<div class="table-cell">

Starting with Contrail Networking Release 2011, you can use *Sandump*
tool on Windows machines.

</div>

</div>

<div class="table-row">

<div class="table-cell">

[2008](#jd0e10)

</div>

<div class="table-cell">

Starting with Contrail Networking Release 2008, *Sandump* tool is
available in contrail-tools container. You can use the *Sandump* tool on
macOS machines.

</div>

</div>

</div>

 
