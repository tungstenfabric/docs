# Service Chaining MX Series Configuration

 

This topic shows how to extend service chaining to the MX Series
routers.

To configure service chaining for MX Series routers, extend the virtual
networks to the MX Series router and program routes so that traffic
generated from a host connected to the router can be routed through the
service.

1.  <span id="jd0e16">The following configuration snippet for an MX
    Series router has a left virtual network called `enterprise` and a
    right virtual network called `public`. The configuration creates two
    routing instances with loopback interfaces and route targets.</span>
    <div id="jd0e25" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        routing-instances {
             enterprise {
                 instance-type vrf;
                 interface lo0.1;
                 vrf-target target:100:20000;
             }
             public {
                 instance-type vrf;
                 interface lo0.2;
                 vrf-target target:100:10000; 
        routing-options {
             static {
         route 0.0.0.0/0 next-hop 10.84.20.1
             }
         }
         interface xe-0/0/0.0;
             }
         }  

    </div>

    </div>
2.  <span id="jd0e28">The following configuration snippet shows the
    configuration for the loopback interfaces.</span>
    <div id="jd0e31" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        interfaces {
            lo0 {
                unit 1 {
                    family inet {
                        address 2.1.1.100/32;
                    }
                }
                unit 2 {
                    family inet {
                        address 200.1.1.1/32;
                    }
                }
            }
        }

    </div>

    </div>
3.  <span id="jd0e34">The following configuration snippet shows the
    configuration to enable BGP. The `neighbor 10.84.20.39` and
    `neighbor 10.84.20.40` are control nodes.</span>
    <div id="jd0e43" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        protocols {
            bgp {
                group demo_contrail {
                    type internal;
                    description "To Contrail Control Nodes & other MX";
                    local-address 10.84.20.252;
                    keep all;
                    family inet-vpn {
                        unicast;
                    }
                    neighbor 10.84.20.39;
                    neighbor 10.84.20.40;
                }
        } 

    </div>

    </div>
4.  <span id="jd0e46">The final step is to add `target:100:10000` to the
    public virtual network and `target:100:20000 `to the enterprise
    virtual network, using the Contrail Juniper Networks
    interface.</span>

A full MX Series router configuration for Contrail can be seen in
[Sample Network Configuration for Devices for Simple Tiered Web
Application](../../reference/code-example-vnc.html).

 
