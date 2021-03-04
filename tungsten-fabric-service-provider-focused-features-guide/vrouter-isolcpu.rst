Optimizing DPDK vRouter Performance Through Full CPU Partitioning and Isolation
===============================================================================

:date: 2020-03-19

Tungsten Fabric Release 2011 supports full CPU partitioning. CPU
isolation is an RHEL method to partition and isolate the CPU cores on a
compute node from the symmetric multiprocessing (SMP) balancing and
scheduler algorithms. The full CPU isolation feature optimizes the
performance of DPDK vRouter when deployed with the DPDK settings
recommended for RHOSP.

CPU isolation helps isolate forwarding cores, VNF cores, and service
cores so that VNF threads and service threads do not send processing
requests to forwarding cores. By applying CPU isolation, you can
allocate dedicated forwarding cores to the DPDK VM and ensure that other
processes do not send processing requests to the cores allocated to DPDK
vRouter, which in turn improves the performance of vRouter to a large
extent.

For CPU isolation and partitioning, RedHat recommends two methods. The
first method is by using a utility called tuned, which partitions the
CPU to virtual network functions (VNFs) and isolates these cores from
the host OS. The tuned method removes isolated CPUs from the common CPU
list that is used to process all tasks and perform CPU isolation after
the system boot, by using the systemd process.

The second is isolcpus, a kernel parameter that keeps CPUs away from the
Linux scheduler. Similar to tuned, the isolcpus method also removes
isolated CPUs from the common CPU list that is used to process all
tasks, and performs CPU isolation at system startup. To enable isolcpus,
you need to modify the GRUB configuration in ``/etc/default/grub`` so
that a new set of isolated CPU is considered. The node needs to be
restarted for the changes to take effect.

To enable CPU isolation using tuned, configure the
ContrailDpdkParameters in
``/tripleo-heat-templates/environments/contrail/contrail-services.yaml``
for RHOSP and SERVICE_CORE_MASK and DPDK_CTRL_THREAD_MASK parameters in
``/vrouter/agent-dpdk/entrypoint.sh`` file for Contrail Ansible
Deployer.
**In contrail-services.yaml**
::

   # Tuned-d profile configuration
   #   TunedProfileName -  Name of tuned profile
   #   IsolCpusList     -  Logical CPUs list to be isolated from the host process (applied via cpu-partitioning tuned).
   #                       It is mandatory to provide isolated cpus for tuned to achive optimal performance.
   #                       Example: "3-8,12-15,18"
   # These paramters are to be set per a role, e.g.:
   #  ComputeParameters:
   #    TunedProfileName: "cpu-partitioning"
   #    IsolCpusList: "3-8,12-15,20"
   #  ContrailDpdkParameters:
   #    TunedProfileName: "cpu-partitioning"
   #    IsolCpusList: "3-20"
   #  ContrailSriovParameters:
   #    TunedProfileName: "cpu-partitioning"
   #    IsolCpusList: "3-20"

**In entrypoint.sh**
::

   # Cpu coremask for DPDK
   # - forwarding threads pinning
   #CPU_CORE_MASK='0x01'
   # - service threads pinning
   #SERVICE_CORE_MASK=''
   # - dpdk ctrl threads pinning
   #DPDK_CTRL_THREAD_MASK=''

To configure isolcpus, modify the following parameters in GRUB:

::

   ContrailDpdkParameters:
       KernelArgs: "default_hugepagesz=1GB hugepagesz=1G hugepages=32 iommu=pt intel_iommu=on isolcpus=3-20"

The isolcpu tuning needs to be done for VNFs (VM) as well. This is to
ensure that the VM can protect and isolate the Poll Mode Driver (PMD)
thread cores from CPU usage by other processes. On Centos and RHEL, CPU
tuning is done by using the utilities isolcpu and tuned.

 
