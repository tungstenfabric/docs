Tungsten Fabric DPDK vRouter Support for Intel DDP Technology in Fortville NICs
===============================================================================

:date: 2020-12-09 

In Tungsten Fabric Release 2011, the Tungsten Fabric DPDK enabled vRouter
uses the Intel dynamic device personalization (DDP) technology. The
Intel DDP technology provides a programmable pipeline, which enables you
to meet specific use cases as per your requirement. Similarly in
Tungsten Fabric, the Intel DDP technology enables you to forward
packets with MPLSoGRE encapsulation. The Intel DDP technology is
supported only by Intel Ethernet 700 Series (Fortville Series) NICs.

In previous releases, Intel Ethernet 500 Series (Niantic Series) NICs
are unable to perform load-balancing for MPLSoGRE packets as they lack
in port information. Due to this, all incoming packets between a pair of
compute nodes start lining up in the same hardware receiving queue (Rx)
of the NIC. The vRouter performs software load-balancing by distributing
the packets to other CPU cores, which processes the packets in the Rx
queue. This reduces the capacity of the vRouter and affects its
performance.

In release 2011, Tungsten Fabric uses the Intel DDP technology,
which enables the Fortville NICs to perform load-balancing for the
MPLSoGRE packets. The Intel DDP technology allows dynamic
re-configuration of the packet processing pipeline in the NIC at
runtime, without rebooting the server. Tungsten Fabric is configured
with an MPLSoGRE profile to process the incoming packets with MPLSoGRE
encapsulation. The MPLSoGRE profile enables the NIC to distribute the
packets evenly across different hardware Rx queues and enables the CPU
cores to perform proportionally. This increases the performance of the
vRouter.

Starting from release 2011, you can use the following commands to
enable, add, delete, or view the list of DDP profiles loaded in a DPDK
enabled vRouter:

-  The Intel DDP profile is not enabled by default in DPDK enabled
   vRouter. You can pass --ddp as a command line argument when the
   system comes up to enable DDP in DPDK enabled vRouters for Fortville
   NICs.

-  Alternatively, during runtime you can execute the dpdkconf –ddp add
   command present in the contrail-tools container to enable DDP in
   vRouter for Fortville NICs.

   ::

      (contrail-tools)[root@cs-scale-02 /]$ dpdkconf --ddp add
      Programming DDP image mplsogreudp - success

-  Use the dpdkconf --ddp delete command on the CLI to remove a DDP
   profile already loaded in the vRouter for Fortville NICs.

   ::

      (contrail-tools)[root@cs-scale-02 /]$ dpdkconf --ddp delete
      vr_dpdk_ddp_del: Removed DDP image mplsogreudp - success

-  Use the dpdkinfo --ddp list command on the CLI to display the list of
   DDP profiles loaded in the vRouter for Fortville NICs.

   ::

      (contrail-tools)[root@cs-scale-02 /]$ dpdkinfo --ddp list
      Profile count is: 1

      Profile 0:
      Track id:     0x8000000c
      Version:      1.0.0.0
      Profile name: L2/L3 over MPLSoGRE/MPLSoUDP
      (contrail-tools)[root@cs-scale-02 /]$


.. list-table:: **Release History Table**
      :header-rows: 1

      * - Release
        - Description
      * - 2011
        - In Tungsten Fabric Release 2011, the Tungsten Fabric DPDK enabled vRouter
          uses the Intel dynamic device personalization (DDP) technology. The
          Intel DDP technology provides a programmable pipeline, which enables you
          to meet specific use cases as per your requirement
 
