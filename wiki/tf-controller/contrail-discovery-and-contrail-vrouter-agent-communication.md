### The below document has a list of frequently asked questions about the communication between contrail-vrouter-agent and contrail-discovery in various scenarios. 

### The following IP addresses are used throughout the document to explain message exchanges:

    vrouter-agent: 10.219.94.10

    DiscoveryServer/ControlNode : 10.219.94.4, 10.219.94.5 and 10.219.94.6


 1. How does vrouter-agent request IP addresses of available xmpp-servers from Discovery?
   
    When vrouter-agent starts up, it subscribes and requests two IP addresses of xmpp-server to the DiscoveryServer. The following packet explains this subscribe request:

    Frame 26: 409 bytes on wire (3272 bits), 409 bytes captured (3272 bits)

    Ethernet II, Src: IntelCor_c9:a8:e0 (90:e2:ba:c9:a8:e0), Dst: HewlettP_31:e3:95 (14:02:ec:31:e3:95)

    Internet Protocol Version 4, Src: 10.219.94.10, Dst: 10.219.94.4

    Transmission Control Protocol, Src Port: 53361, Dst Port: 5998, Seq: 1, Ack: 1, Len: 343

    Hypertext Transfer Protocol

    eXtensible Markup Language
    ```xml
    <xmpp-server>
        <instances>
            0
        </instances>
        <min-instances>
            2
        </min-instances>
        <client-type>
            contrail-vrouter-agent:0
        </client-type>
        <client>
            contrail100:contrail-vrouter-agent:0
        </client>
        <remote-addr>
            10.219.94.10
        </remote-addr>
    </xmpp-server>
    ```
    As seen above, vrouter-agent requests for a list of XMPP servers indicated by “instances = 0” with a minimum of at least 2 instances of XMPP Server service. Other details like the client's IP address, client type etc are self explanatory. 

 2. How discovery server responds to the above subscribe request?

    Upon receiving the request from the client as shown in 1), the DiscoveryServer sends a subscribe response to the vrouter-agent showing all published xmpp-server service. The following packet explains the subscribe response from the DiscoveryServer:

    Frame 28: 575 bytes on wire (4600 bits), 575 bytes captured (4600 bits)

    Ethernet II, Src: HewlettP_31:e3:95 (14:02:ec:31:e3:95), Dst: IntelCor_c9:a8:e0 (90:e2:ba:c9:a8:e0)

    Internet Protocol Version 4, Src: 10.219.94.4, Dst: 10.219.94.10

    Transmission Control Protocol, Src Port: 5998, Dst Port: 53361, Seq: 1, Ack: 344, Len: 509

    Hypertext Transfer Protocol

    eXtensible Markup Language
    ```xml
    <response>
        <xmpp-server
            publisher-id="contrail65">
            <port>
                5269
                </port>
            <ip-address>
                10.219.94.6
                </ip-address>
            </xmpp-server>
        <xmpp-server
            publisher-id="contrail64">
            <port>
                5269
                </port>
            <ip-address>
                10.219.94.5
                </ip-address>
            </xmpp-server>
        <xmpp-server
            publisher-id="contrail60">
            <port>
                5269
                </port>
            <ip-address>
                10.219.94.4
                </ip-address>
            </xmpp-server>
        <ttl>
            915
            </ttl>
        </response>
       ```
       Note: The client picks the first two servers from the list sent by DiscoveryServer. This list is ordered and maintained by DiscoveryServer.


 3. Is there a TTL for every connection response and what is it all about?
   
    TTL is the time we define for the client to cache service information. It is defined in seconds. When   DiscoveryServer sends a response to the client, the packet will also have a random TTL value attached to it. Please see 915 in the above XML output. The minimum and maximum ttl values are defined in /etc/contrail/discovery.conf

    ttl_min=300
    
    ttl_max=1800

    DiscoveryServer randomizes a value between 300 and 1800 and sends it in <ttl> tag of the response to the client.

 4. Is there an introspect for discovery that shows the TTL values that came from the DiscoveryServer?
    
    [[http://discovery_server_ip:5998/clients]]

    In the above introspect, please look for TTL Column for service-type=xmpp-server.

 5. Is there a way with which we can determine the time elapsed for a specific TTL. 
   
    [[http://discovery_server_ip:5998/clients]]

    In the above introspect, please look for "Time Remaining" Column for service-type=xmpp-server.

 6. How to check the xmpp-servers vrouter-agent is connected to?
    
    [[http://vrouter_agent_ip:8085/Snh_AgentXmppConnectionStatusReq?]]

 7. Why vrouter-agent requires two xmpp-server connections?

    XMPP is a protocol that is used between controllers and compute nodes (vrouter-agent in particular). 
    Through XMPP, the following messages are exchanged:

     * Routes
     * Config
     * Multicast Information

    vrouter-agent follows an active-active model with two xmpp-server connections it receives. It is important to  note that route exchanges happen on both xmpp-server connections. However, Config and Multicast gets updated only on the first active(*) channel. 

 8. How do we determine which xmpp-server connection is active for Multicast and Config?

    [[http://vrouter_agent_ip:8085/Snh_AgentXmppConnectionStatusReq?]]
 
    Please look for cfg_controller and mcast_controller in the above introspect. The ones that has "Yes" as the value for this column indicates the active cfg_controller and mcast_controller. The other way to determine this is through Contrail WebUI -> Virtual Routers -> Click on the vRouter in question -> Look for Control Nodes with a (*).  

 9. How vrouter-agent marks one xmpp-server connection as config master/multicast master?

    The XMPP connection that comes up first is choosen to be the config master/multicast Master.

 10. What happens when an active master xmpp-server connection disconnects due to underlay connectivity problem?

     The second active session becomes master. The vrouter-agent requests the discovery server for a pair of XMPP servers again. The subscribe response from the DiscoveryServer looks the same as 2). The only change is Discovery publishes only two xmpp-server now excluding the active that went down due to underlay issues.

     Note: The active connection was on 10.219.94.6 and it was brought down to demonstrate the packet sent by DiscoveryServer.

     Frame 14: 470 bytes on wire (3760 bits), 470 bytes captured (3760 bits)

     Ethernet II, Src: HewlettP_31:e3:95 (14:02:ec:31:e3:95), Dst: IntelCor_c9:a8:e0 (90:e2:ba:c9:a8:e0)

     Internet Protocol Version 4, Src: 10.219.94.4, Dst: 10.219.94.10

     Transmission Control Protocol, Src Port: 5998, Dst Port: 53377, Seq: 1, Ack: 426, Len: 404

     Hypertext Transfer Protocol
     
     eXtensible Markup Language
     ```xml
     <response>
        <xmpp-server
            publisher-id="contrail64">
            <port>
                5269
            </port>
            <ip-address>
                10.219.94.5
            </ip-address>
        </xmpp-server>
        <xmpp-server
            publisher-id="contrail60">
            <port>
                5269
            </port>
            <ip-address>
                10.219.94.4
            </ip-address>
        </xmpp-server>
        <ttl>
            1341
        </ttl>
     </response>
   
 11. What is the impact of traffic when scenario in 10) happens.
    
     Any result in flap of multicast master connection results in re-baking of the multicast tree and the multicast traffic is impacted till we re-bake it completely. Please note this communication impact is only for the VRFs involved on that compute/TSN. Unicast traffic must not be impacted.

 12. What is the impact of traffic when non-cfg/non-mcast xmpp-server connection disconnects due to underlay connectivity problem?

     The vrouter-agent re-subscribes when all servers in the previous list have been tried and max-retries parameter is reached. Once obtained, it marks the new session as backup. No impact on BUM/Unicast traffic should be seen here as we are not re-computing the multicast tree.

 13. What happens when TTL is expired for the master xmpp-server connection?
    
     No change in the existing connections. The xmpp-servers held by the agent before TTL expiry would continue after the TTL is renewed.


 14. What happens when TTL is expired for the backup xmpp-server connection?
   
     No change in the existing connections. The xmpp-servers held by the agent before TTL expiry would continue after the TTL is renewed. 

 15. What happens when vrouter-agent crashes/cores?

     After the vrouter-agent recovers, it again follows the same sequence explained in Q)10 to get a pair of xmpp-server connections. It decides on the active connection part and marks it accordingly. This also results in the following:

        *  Routes, Config and Multicast information has to be downloaded by the agent post the xmpp-server connections are honored.

        *  All existing flows on the compute are evicted and the flow table has to be re-computed. 

        *  The multicast tree needs to be re-baked.
     
     Due to this, all kind of communication (unicast, bum etc) are impacted on the involved VRFs. 

 16. What is the impact on traffic if a control node involved in the active session is restarted?
    
     Same answer as that of Q)10

 17. What is the impact on traffic if a control node involved in the backup session is restarted?
    
     Same answer as that of Q)12

 18. How XMPP connections are rebalanced when a control node involved in active XMPP sessions for few computes are restarted in a three-node controller scenario?
    
     All active XMPP sessions on the restarted controller node is closed. The corresponding agents will determine the loss in connection and requests discovery for a new set of xmpp-server connections. DiscoveryServer will send the ordered list of xmpp-server to be used based on an internal load balancing algorithm.