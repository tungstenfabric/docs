# Understanding Flow Sampling

 

This topic describes how flow records are sampled and exported to the
Contrail collector, flow handling, and flow aging.

## Flow Sampling

The Contrail vRouter agent exports flow records to the Contrail
collector when a flow is created or deleted. It also updates flow
statistics at regular intervals.

If all flow records are exported from the agent, depending on the scale
of flows, some of the exported flows might be dropped due to queue
overflow.

Based on sampling, flow records are sampled and exported to the Contrail
Controller of Contrail Networking. This enables Contrail Networking to
reduce queue overflow.

The flows that are exported are selected based on the following
parameters used in the algorithm:

-   The configured flow export rate. This is configured as part of the
    `global-vrouter-config` object.

-   The actual flow export rate.

-   The sampling threshold. This is a dynamic value calculated
    internally. If the flow statistics in a flow sample are above this
    threshold, the flow record is exported.

Each flow is subjected to the following algorithm at regular intervals.
The algorithm determines whether to export the sample or not.

-   Flows with traffic that is greater than or equal to the sampling
    threshold are always exported. The byte and packet counts are
    reported without modification.

-   Flows with traffic that is less than the sampling threshold are
    exported according to the probability. The byte and packet counts
    are adjusted upwards according to the probability.

    The probability is calculated as
    `(bytes during the interval) / (sampling threshold)`.

-   The system generates a random number less than the sampling
    threshold. If the byte count during the interval is less than the
    random number, then the flow sample is not exported.

-   If none of these conditions are met, the flow sample is exported
    after normalizing the byte count and packet count during the
    interval. Normalization is done by dividing the byte count and
    packet count during the interval by the probability. This
    normalization is used as a heuristic to account for statistics of
    flow samples that are dropped.

The actual flow export rate is close to the configured export rate. If
there is a large deviation, the sampling threshold is adjusted to bring
the actual flow export rate close to the configured flow export rate.

## Flow Handling

When a virtual machine sends or receives IP traffic, forward and reverse
flow entries are set up. When the first packet arrives, a flow key is
used to hash into a flow table (identify a hash bucket). The flow key is
based on five-tuples consisting of source and destination IP addresses,
ports, and the IP protocol.

A flow entry is created and the packet is sent to the Contrail vRouter
agent. Configured policies are applied and the flow action is updated.
The agent also creates a flow entry for the reverse direction where
relevant. Subsequent packets match the established flow entries and are
forwarded, dropped, NAT translated, and so on, based on the flow action.

When the hash bucket is full, entries are created in an overflow table.
Contrail Networking maintains the overflow entries as a list against the
hash bucket.

By default, the maximum number of flow table and overflow table entries
are 512,000 and 8000 respectively. These can be modified by configuring
them as vRouter module parameters, for example: <span class="cli"
v-pre="">vr\_flow\_entries</span> and `vr_oflow_entries`.

For more information about the vRouter module parameters, see
<https://github.com/Juniper/contrail-controller/wiki/Vrouter-Module-Parameters>.

## Flow Aging

Flows are aged out based on inactivity for a specified period of time.
By default, the timeout value is 180 seconds. This can be modified by
configuring the <span class="cli" v-pre="">flow\_cache\_timeout</span>
parameter under the `DEFAULT` section in the <span class="cli"
v-pre="">/etc/contrail/contrail-vrouter-agent.conf</span> file.

## TCP State-Based Flow Handling and Aging

-   [TCP State-Based Flow Handling](flow-sample-overview.html#jd0e106)

-   [Protocol-Based Flow Aging](flow-sample-overview.html#jd0e119)

### TCP State-Based Flow Handling

The Contrail vRouter in Contrail Networking monitors TCP flows to
identify entries that can be reused without going through the standard
aging cycle.

All flow entries that match TCP flows that have experienced a connection
teardown, either through the standard TCP closure cycle
(FIN/ACK-FIN/ACK) or the RST indicator, are torn down by the vRouter and
are immediately available for use by new qualified flows.

The vRouter also keeps track of connection establishment cycles and
exports the necessary information to the vRouter agent, such as SYN/ACK
and a digested established flag. This allows the vRouter agent to tear
down flows that do not experience a full connection cycle.

Flows that the vRouter identifies as reuse candidates, or eviction
candidates, are marked as such in the flow entry. Flows are in the
evicted state when they become available for other new flows to be
reused.

This two-step transition is used so that the flow entry remains valid
until the packet reaches the destination, preventing the flow from
getting remapped to another flow entry in the interim.

### Protocol-Based Flow Aging

Although TCP flows are deleted based on TCP state, you are sometimes
required to age out specific protocol flows more aggressively. One
example is when a DNS server is run in one VM. In this case, multiple
flows are set up for DNS. A pair of flows are set up to serve each
query. Because the flows are no longer required after the query is
served, the timeout can be lower for these flows. To handle these cases,
protocol-based flow aging is used.

With protocol-based flow aging, the aging timeout can be configured per
protocol. All other protocols continue to use the default aging timeout.

Protocol-based flow aging is also supported in Contrail Networking.

The configuration for protocol-based flow aging can be done in the
`global-vrouter-config` object. For example, to have all DNS flows aged
out in five seconds, use the following entry:
`protocol = udp, port = 53 will be set an aging timeout of 5 seconds.`

 
