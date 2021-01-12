# Configuring Graceful Restart and Long-lived Graceful Restart

 

<div id="intro">

<div class="mini-toc-intro">

Graceful restart and long-lived graceful restart BGP helper modes are
supported for the Contrail control node and XMPP helper mode.

</div>

</div>

## Application of Graceful Restart and Long-lived Graceful Restart

Whenever a BGP peer session is detected as down, all routes learned from
the peer are deleted and immediately withdrawn from advertised peers.
This causes instantaneous disruption to traffic flowing end-to-end, even
when routes kept in the vrouter kernel in the data plane remain intact.

Graceful restart and long-lived graceful restart features can be used to
alleviate traffic disruption caused by downs.

When configured, graceful restart features enable existing network
traffic to be unaffected if Contrail controller processes go down. The
Contrail implementation ensures that if a Contrail control module
restarts, it can use graceful restart functionality provided by its BGP
peers. Or when the BGP peers restart, Contrail provides a graceful
restart helper mode to minimize the impact to the network. The graceful
restart features can be used to ensure that traffic is not affected by
temporary outage of processes.

Graceful restart is not enabled by default.

With graceful restart features enabled, learned routes are not deleted
when sessions go down, and the routes are not withdrawn from the
advertised peers. Instead, the routes are kept and marked as 'stale'.
Consequently, if sessions come back up and routes are relearned, the
overall impact to the network is minimized.

After a certain duration, if a downed session does not come back up, all
remaining stale routes are deleted and withdrawn from advertised peers.

The graceful restart and long-lived graceful restart features can be
enabled only for BGP peers in Contrail 3.2.

## BGP Graceful Restart Helper Mode

The BGP helper mode can be used to minimize routing churn whenever a BGP
session flaps. This is especially helpful if the SDN gateway router goes
down gracefully, as in an rpd crash or restart on an MX Series Junos
device. In that case, the contrail-control can act as a graceful restart
helper to the gateway, by retaining the routes learned from the gateway
and advertising them to the rest of the network as applicable. In order
for this to work, the restarting router (the SDN gateway in this case)
must support and be configured with graceful restart for all of the
address families used.

The graceful restart helper mode is also supported for BGP-as-a-Service
(BGPaaS) clients. When configured, contrail-control can provide a
graceful restart or long-lived graceful restart helper mode to a
restarting BGPaaS client.

## Feature Highlights

The following are highlights of the graceful restart and long-lived
graceful restart features.

-   Configuring a non-zero restart time enables the ability to advertise
    graceful restart and long-lived graceful restart capabilities in
    BGP.

-   Configuring helper mode enables the ability for graceful restart and
    long-lived graceful restart helper modes to retain routes even after
    sessions go down.

-   With graceful restart configured, whenever a session down event is
    detected and a closing process is triggered, all routes, across all
    address families, are marked stale. The stale routes are eligible
    for best-path election for the configured graceful restart time
    duration.

-   When long-lived graceful restart is in effect, stale routes can be
    retained for a much longer time than that allowed by graceful
    restart alone. With long-lived graceful restart, route preference is
    retained and best paths are recomputed. The community marked
    LLGR\_STALE is tagged for stale paths and re-advertised. However, if
    no long-lived graceful restart community is associated with any
    received stale route, those routes are not kept, instead, they are
    deleted.

-   After a certain time, if a session comes back up, any remaining
    stale routes are deleted. If the session does not come back up, all
    retained stale routes are permanently deleted and withdrawn from the
    advertised peer.

## XMPP Helper Mode

Contrail supports for long-lived graceful restart (LLGR) with XMPP
helper mode. Graceful restart and long lived graceful restart can be
enabled using the Contrail web UI or by using the provision\_control
script.

The helper modes can also be enabled via schema, and can be disabled
selectively in a contrail-control node for BGP or XMPP sessions by
configuring `gr_helper_disable` in the
`/etc/contrail/contrail-control.conf` configuration file.

## Configuration Parameters

Graceful restart parameters are configured in the `global-system-config`
of the schema. They can be configured by means of a provisioning script
or by using the Contrail Web UI.

Configure a non-zero restart time to advertise for graceful restart and
long-lived graceful restart capabilities from peers.

Configure helper mode for graceful restart and long-lived graceful
restart to retain routes even after sessions go down.

Configuration parameters include:

-   `enable` or `disable` for all graceful restart parameters:

    -   `restart-time`

    -   `long-lived-restart-time`

    -   `end-of-rib-timeout`

-   `bgp-helper-enable` to enable graceful restart helper mode for BGP
    peers in contrail-control

-   `xmpp-helper-enable` to enable graceful restart helper mode for XMPP
    peers (agents) in contrail-control

<div id="jd0e117" class="sample" dir="ltr">

The following shows configuration by a provision script.

<div class="output" dir="ltr">

    /opt/contrail/utils/provision_control.py 
                --api_server_ip 10.xx.xx.20 
                --api_server_port 8082 
                --router_asn 64512             
                --admin_user admin
                --admin_password <password> 
                --admin_tenant_name admin 
                --set_graceful_restart_parameters 
                --graceful_restart_time 60 
                --long_lived_graceful_restart_time 300 
                --end_of_rib_timeout 30 
                --graceful_restart_enable 
                --graceful_restart_bgp_helper_enable

</div>

</div>

The following are sample parameters:

<div id="jd0e124" class="sample" dir="ltr">

<div class="output" dir="ltr">

    -set_graceful_restart_parameters 
                --graceful_restart_time 300 
                --long_lived_graceful_restart_time 60000 
                --end_of_rib_timeout 30 
                --graceful_restart_enable 
                --graceful_restart_bgp_helper_enable 

</div>

</div>

When BGP peering with Juniper Networks devices, Junos must also be
explicitly configured for graceful restart/long-lived graceful restart,
as shown in the following example:

<div id="jd0e129" class="sample" dir="ltr">

<div class="output" dir="ltr">

    set routing-options graceful-restart
    set protocols bgp group <a1234> type internal
    set protocols bgp group <a1234> local-address 10.xx.xxx.181
    set protocols bgp group <a1234> keep all
    set protocols bgp group <a1234> family inet-vpn unicast graceful-restart long-lived restarter stale-time 20
    set protocols bgp group <a1234> family route-target graceful-restart long-lived restarter stale-time 20
    set protocols bgp group <a1234> graceful-restart restart-time 600
    set protocols bgp group <a1234> neighbor 10.xx.xx.20 peer-as 64512

</div>

</div>

The graceful restart helper modes can be enabled in the schema. The
helper modes can be disabled selectively in the `contrail-control.conf`
for BGP sessions by configuring `gr_helper_disable` in the
`/etc/contrail/contrail-control.conf `file.

The following are examples:

`/usr/bin/openstack-config /etc/contrail/contrail-control.conf DEFAULT gr_helper_bgp_disable 1 `

`/usr/bin/openstack-config /etc/contrail/contrail-control.conf DEFAULT gr_helper_xmpp_disable 1 `

`service contrail-control restart `

For more details about graceful restart configuration, see
<https://github.com/Juniper/contrail-controller/wiki/Graceful-Restart> .

## Cautions for Graceful Restart

Be aware of the following caveats when configuring and using graceful
restart.

-   Using the graceful restart/long-lived graceful restart feature with
    a peer is effective either to all negotiated address families or to
    none. If a peer signals support for graceful restart/long-lived
    graceful restart for only a subset of the negotiated address
    families, the graceful restart helper mode does not come into effect
    for any family in the set of negotiated address families.

-   Because graceful restart is not yet supported for
    contrail-vrouter-agent, the parameter should *not* be set for
    `graceful_restart_xmpp_helper_enable`. If the vrouter agent
    restarts, the data plane is reset and the routes and flows are
    reprogrammed anew, which typically results in traffic loss for
    several seconds for new and /existing flows.

-   Graceful restart/long-lived graceful restart is not supported for
    multicast routes.

-   Graceful restart/long-lived graceful restart helper mode may not
    work correctly for EVPN routes, if the restarting node does not
    preserve forwarding state for EVPN routes.

## Configuring Graceful Restart using Contrail Command

To configure graceful restart in Contrail Command, navigate to
**Infrastructure &gt; Cluster &gt; Advanced Options** and select the
Edit icon near the top right corner of the screen.

![Figure 1: Global Config System Configuration
Screen](images/s060275.png)

The **Edit System Configuration** window opens. Click the box for
**Graceful Restart** to enable graceful restart, and enter a non-zero
number to define the **Restart Time** in seconds. You can also specify
the times for the long-lived graceful restart (LLGR) and the end of RIB
timers from this window.

![Figure 2: Edit System Configuration Window](images/s060276.png)

 
