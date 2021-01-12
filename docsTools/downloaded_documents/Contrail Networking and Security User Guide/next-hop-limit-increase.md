# Contrail vRouter Next Hop Configuration

 

<span id="jd0e10">In Contrail Networking Release 1911, the next hop
value in the vRouter is increased to 32 bits. By default, the vRouter
can now create 512K next hops and supports up to 1 million next hops.
Also, in release 1911 you can assign a high watermark limit in vRouter
agent configuration file. If the number of next hops or Multiprotocol
Label Switching (MPLS) labels exceed the watermark limit, the vRouter
agent generates alarms.</span> These alarms are generated based on the
usage of next hops and MPLS labels against the watermark limit and
maximum limit of next hops and MPLS labels.

In releases prior to release 1911, Contrail supported 16 bits next hop
value in the vRouter. As the next hop value was assigned a 16 bit value,
the vRouter could create a maximum of 65,536 next hops. The vRouter
agent did not generate alarms when the number of next hops increased.
When the number of next hops exceeded the maximum limit, the vRouter
agent failed to perform another next hop, which led to loss of traffic.

In the vRouter agent configuration file, `contrail-vrouter-agent.conf`,
you can configure a high watermark limit according to your requirement.
The watermark limit specifies the maximum percentage of next hops or
MPLS labels that you can use. The vRouter agent generates alarms when
the next hop usage or the MPLS labels usage exceeds the watermark limit.
For example, the default watermark limit is set to 80 (80% of the
maximum next hops or MPLS labels vRouter can create). If the maximum
number of next hops possible on the compute node is 100, an alarm is
raised after 80 next hops are created. If the maximum number of MPLS
labels that can be created on the compute node is 50, the alarm is
raised after 40 MPLS labels are created.

**Note**

The low watermark limit is calculated to be 95% of the high watermark
limit.

To configure vRouter object watermark limit in a cluster at the time of
provisioning, you must assign a value to
`VROUTER_AGENT__DEFAULT__vr_object_high_watermark` parameter either in
the `roles: vrouter: ` section or in the `contrail_configuration`
section of the `instances.yml` file. You must assign a watermark limit
in the range of 50–95 to the
`VROUTER_AGENT__DEFAULT__vr_object_high_watermark` parameter.

<div id="jd0e49" class="example" dir="ltr">

For example, to configure watermark limit to 60%, you must assign a
value 60 to the `VROUTER_AGENT__DEFAULT__vr_object_high_watermark`
parameter under the following sections:

    roles:
           vrouter:
              VROUTER_AGENT__DEFAULT__vr_object_high_watermark: 60

</div>

<div id="jd0e64" class="example" dir="ltr">

    contrail_configuration:
                VROUTER_AGENT__DEFAULT__vr_object_high_watermark: 60

</div>

**Note**

If you assign a value to
`VROUTER_AGENT__DEFAULT__vr_object_high_watermark` in the
`contrail_configuration` section, the watermark limit for all vRouters
that are configured using `instances.yml` file will be the same. To
assign a different watermark limit to a vRouter, you have to assign the
watermark limit to the
`VROUTER_AGENT__DEFAULT__vr_object_high_watermark` parameter under the
`roles:  vrouter: ` section of a vRouter.

To change the watermark limit later, you must modify the
`vr_object_high_watermark` parameter present in the `[DEFAULT]` section
of the `entrypoint.sh` file. After you assign a watermark value to the
`vr_object_high_watermark` parameter in the `entrypoint.sh` file, the
`contrail-vrouter-agent.conf` configuration file is now updated with the
`vr_object_high_watermark` parameter, which denotes the watermark limit.

<div id="jd0e119" class="example" dir="ltr">

For example, to configure watermark limit to 75%, you must assign a
value 75 to the `vr_object_high_watermark` parameter under the
`[DEFAULT]` section:

    [DEFAULT]
         vr_object_high_watermark

</div>

Based on the next hops or MPLS labels usage, the vRouter agent generates
system defined alarms with various severity. See
[Table 1](next-hop-limit-increase.html#nh-usage-table).

Table 1: Alarms Generated by vRouter Agent

| Next Hop and MPLS Label Usage Against the Watermark Limit and Maximum Limit | Severity Level of Alarm                                                |
|:----------------------------------------------------------------------------|:-----------------------------------------------------------------------|
| Next hop or MPLS labels usage exceeds the high watermark limit              | Major alarm is generated.                                              |
| Next hop or MPLS labels usage equals 100% of the maximum limit              | Critical alarm is generated, and high watermark alarm is also present. |
| Next hop or MPLS labels usage reduces to 95% of the maximum limit           | Critical alarm is cleared, and high watermark alarm is present.        |
| Next hop or MPLS labels usage reduces to 95% of the high watermark limit    | High watermark alarm is cleared.                                       |

## Benefits of Increasing Next Hop Limit

-   Increase in next hop limit allows Contrail to scale more next hops
    than in earlier releases.

-   The alarms generated by vRouter agent enables you to monitor the
    usage and availability of next hops and MPLS labels.

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

[1911](#jd0e10)

</div>

<div class="table-cell">

In Contrail Networking Release 1911, the next hop value in the vRouter
is increased to 32 bits. By default, the vRouter can now create 512K
next hops and supports up to 1 million next hops. Also, in release 1911
you can assign a high watermark limit in vRouter agent configuration
file. If the number of next hops or Multiprotocol Label Switching (MPLS)
labels exceed the watermark limit, the vRouter agent generates alarms.

</div>

</div>

</div>

 