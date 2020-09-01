GracefulRestart feature test plan is described in this document. More details about the feature itself are in [GracefulRestart Functional Specifications](https://github.com/Juniper/contrail-controller/wiki/Graceful-Restart).

### Release: 3.2

GracefulRestart (GR) has two pieces embedded in it. One is **Graceful Restart Helper mode** where in controller keeps routes of all of its bgp peers and xmpp agents even if the session goes down (for certain period). If and when the session comes back up, routes are cleaned up using the standard mark and sweep approach. In this scenario, the control-node itself does not undergo any restart per se.

Second piece is where in control-node itself restarts. In this scenario, called **GracefulRestart mode** with proper advertisements to bgp peers (before restart), one would like to avail the GR helper mode functionality provided by the peer (such as JUNOS-MX).

[Test Status](https://github.com/Juniper/contrail-test/wiki/Graceful-Restart-Test-Status)

### Reference
* [GracefulRestart wiki](https://github.com/Juniper/contrail-controller/wiki/Graceful-Restart)
* GracefulRestart for BGP (and XMPP) follows [RFC4724](https://tools.ietf.org/html/rfc4724) specifications
* LongLivedGracefulRestart feature follows [draft-uttaro-idr-bgp-persistence](https://tools.ietf.org/html/draft-uttaro-idr-bgp-persistence-03) specifications
* [Unit Test](https://github.com/Juniper/contrail-controller/blob/master/src/bgp/test/graceful_restart_test.cc#L1180)

###GracefulRestart Mode
Configure GracefulRestart timer interval via web-ui/api in vnc_cfg.xsd schema under global-system-config
Bring up the controller, peers and agents, and learn the routes

Stop the control-node (service supervisor-control stop)

The routes advertised from the control-node towards its peers such as MX-JUNOS should continue to remain in the peers as 'STALE'. Once the control-node comes back up, routes should get re-advertised and no longer should remain as stale in the bgp peers

**Events to test and verify**

1. Only GR time intervals configured only in DUT, the restarting contrail-control node
1. Only LLGR time intervals configured only in DUT, the restarting contrail-control node
1. Both GR and LLGR time intervals configured only in DUT, the restarting contrail-control node

1. Only GR time intervals configured only in MX Peer, the non restarting GR helper node
1. Only LLGR time intervals configured only in MX Peer, the non restarting GR helper node
1. Both GR and LLGR time intervals configured MX Peer, the non restarting GR helper node

1. Only GR time intervals configured only in both GR Helper MX node and restarting contrail-control node
1. Only LLGR time intervals configured only in both GR Helper MX node and restarting contrail-control node
1. Both GR and LLGR time intervals configured in both GR Helper MX node and restarting contrail-control node
1. GR/LLGR is configured selectively for certain address families (or all address families) in MX JUNOS peer.
1. Session reset due to cold reboots, warm reboots, process restarts, config changes, etc.

In all the above scenarios,

1. GR and LLGR functionality must be verified
1. Routes should remain in the table until GR timer (and LLGR timer) expires as negotiated
1. EndOfRib must be sent out by the restarting contrail-control node only _after_ at least BgpPeer::kMinEndOfRibSendTimeUsecs duration and at most BgpPeer::kMaxEndOfRibSendTimeUsecs duration.
1. If number of updates to be sent out by the restarting node is not large, then EoR can be expected to be sent out pretty much after BgpPeer::kMinEndOfRibSendTimeUsecs duration. Otherwise, only after output queue is fully drained (Can be checked in introspect)
1. GR and/or LLGR comes into effect only if GR is negotiated for all address families carried over the session
1. Changes to negotiated list of families in GR should result in session closure (non-graceful)

###GracefulRestart Helper Mode

This is the more complicated mode of the two. In this mode, if GR is negotiated in a session, then routes received by a peer are kept intact even after a session goes down. The routes are managed using the standard mark and sweep approach.

**Events to test and verify**

1. All scenarios listed above are applicable with restart step applied to the peer (not DUT control-node)
1. When GR/LLGR is in effect, routes must be verified to for proper flags and path attributes (e.g. LLGR_STALE attribute)
1. Best path selection must be verified for LLGR_STALE paths which are to be less preferred
1. Nested closure where in sessions flap before they reach stable state (before GR and/or LLGR timers expire). Goal is to retain the routes as long as applicable in order to minimize impact to the traffic flow
1. Configuration changes while GR in effect (in DUT and/or in Peers) such as admin-down, families negotiated, GR configuration itself, etc.
1. control-node restart while in the midst of GR helper mode for one or more bgp and/or xmpp peers (There should be no crash and restart should happen quickly and gracefully)
1. Agents subscribe to overlapping and non-overlapping subset of networks after restart
1. Agents send overlapping and non-overlapping subset of routes after restart
1. Routing Instance deletion or modification in the midst of GR helper mode (when agent is down or just coming up)
1. Route Target configuration changes before, during and after GR helper mode is in effect 
1. GR Helper mode disable/enable for BGP and/or XMPP

**[UnitTest](https://github.com/Juniper/contrail-controller/blob/master/src/bgp/test/graceful_restart_test.cc#L1180)**

graceful_restart_test attempts to test many of the following scenarios in [UT](https://github.com/Juniper/contrail-controller/blob/master/src/bgp/test/graceful_restart_test.cc#L970). But those tests are equally applicable to systest environment as well


Bring up n_agents and n_peers in n_instances_ and advertise n_routes (v4 and v6) in each connection
Verify that (n_agents + n_peers) * n_instances_ * n_routes_ routes are received in peer in each instance

* Subset of agents/peers support GR
* Subset of routing-instances are deleted before, during and after GR
* Subset of agents/peers go down permanently (Triggered from agents)
* Subset of agents/peers flip (go down and come back up) (Triggered from agents)
* Subset of agents/peers go down permanently (Triggered from control-node)
* Subset of agents flip/peers (Triggered from control-node)
*   Subset of subscriptions after restart
*   Subset of routes are [re]advertised after restart
*   Subset of routing-instances are deleted (during GR)

**Misc tasks**

* Profile contrail-control using gprof and get performance data
* Profile contrail-control using Valgrind and get info about memory leaks, corruptions, etc.
* Run code-coverage against contrail-control daemon to get coverage data