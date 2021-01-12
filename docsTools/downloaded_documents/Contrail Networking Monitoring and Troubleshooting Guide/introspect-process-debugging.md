# Debugging Processes Using the Contrail Introspect Feature

 

This topic describes how to use the Sandesh infrastructure and the
Contrail Introspect feature to debug processes.

Introspect is a mechanism for taking a program object and querying
information about it.

Sandesh is the name of a unified infrastructure in the Contrail Virtual
Networking solution.

Sandesh is a way for the Contrail daemons to provide a request-response
mechanism. Requests and responses are defined in Sandesh format and the
Sandesh compiler generates code to process the requests and send
responses.

Sandesh also provides a way to use a Web browser to send Sandesh
requests to a Contrail daemon and get the Sandesh responses. This
feature is used to debug processes by looking into the operational
status of the daemons.

Each Contrail daemon starts an HTTP server, with the following page
types:

-   The main index.html listing all Sandesh modules and the links to
    them.

-   Sandesh module pages that present HTML forms for each Sandesh
    request.

-   XML-based dynamically-generated pages that display Sandesh
    responses.

-   An automatically generated page that shows all code needed for
    rendering and all HTTP server-client interactions.

You can display the HTTP introspect of a Contrail daemon directly by
accessing the following Introspect ports:

-   `<controller-ip>`:8083. This port displays the *contrail-control*
    introspect port.

-   `<compute-ip>`:8085 This port displays the *contrail-vrouter-agent*
    introspect port.

-   `<controller-ip>`:8087 This port displays the *contrail-schema*
    introspect port.

-   `<controller-ip>`:8088 This port displays the *contrail-svc-monitor*
    introspect port.

-   `<controller-ip>`:8092 This port displays the *contrail-dns*
    introspect port.

-   `<controller-ip>`:8084 This port displays the *contrail-api*
    introspect port. (:8084/Snh\_SandeshTraceRequest?x=RestApiTraceBuf)

You can use the config editor to review configured objects.

Another way to launch the Introspect page is by browsing to a particular
node page using the Contrail Web user interface.

[Figure 1](introspect-process-debugging.html#con-node-detail-win) shows
the contrail-control infrastructure page. Notice the Introspect link at
the bottom of the Control Nodes Details tab window.

![Figure 1: Control Nodes Details Tab Window](images/s042485.png)

The following are the Sandesh modules for the Contrail control process
(contrail-control) Introspect port.

-   bgp\_peer.xml

-   control\_node.xml

-   cpuinfo.xml

-   discovery\_client\_stats.xml

-   ifmap\_log.xml

-   ifmap\_server\_show.xml

-   rtarget\_group.xml

-   sandesh\_trace.xml

-   sandesh\_uve.xml

-   service\_chaining.xml

-   static\_route.xml

-   task.xml

-   xmpp\_server.xml

[Figure 2](introspect-process-debugging.html#cont-intro-win) shows the
Controller Introspect window.

![Figure 2: Controller Introspect Window](images/s042488.png)

[Figure 3](introspect-process-debugging.html#bgp-peer-neigh-sum) shows
an example of the BGP Peer (bgp\_peer.xml) Introspect page.

![Figure 3: BGP Peer Introspect Page](images/s042486.png)

[Figure 4](introspect-process-debugging.html#bgp-neigh-sum) shows an
example of the BGP Neighbor Summary Introspect page.

![Figure 4: BGP Neighbor Summary Introspect Page](images/s042487.png)

The following are the Sandesh modules for the Contrail vRouter agent
(`contrail-vrouter-agent`) Introspect port.

-   agent.xml

-   agent\_stats\_interval.xml

-   cfg.xml

-   controller.xml

-   cpuinfo.xml

-   diag.xml

-   discovery\_client\_stats.xml

-   flow\_stats\_interval.xml

-   ifmap\_agent.xml

-   kstate.xml

-   multicast.xml

-   pkt.xml

-   port\_ipc.xml

-   sandesh\_trace.xml

-   sandesh\_uve.xml

-   services.xml

-   stats\_interval.xml

-   task.xml

-   xmpp\_server.xml

[Figure 5](introspect-process-debugging.html#agent-introspect) shows an
example of the Agent (agent.xml) Introspect page.

![Figure 5: Agent Introspect Page](images/s042489.png)

 
