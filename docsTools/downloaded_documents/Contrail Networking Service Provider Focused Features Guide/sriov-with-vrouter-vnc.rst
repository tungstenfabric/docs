Configuring Single Root I/O Virtualization (SR-IOV)
===================================================

 

Overview: Configuring SR-IOV
----------------------------

Contrail Networking supports single root I/O virtualization (SR-IOV) on
Ubuntu systems and on Red Hat Enterprise Linux (RHEL) operating systems
as well.

SR-IOV is an interface extension of the PCI Express (PCIe)
specification. SR-IOV allows a device, such as a network adapter to have
separate access to its resources among various hardware functions.

As an example, the Data Plane Development Kit (DPDK) library has drivers
that run in user space for several network interface cards (NICs).
However, if the application runs inside a virtual machine (VM), it does
not see the physical NIC unless SR-IOV is enabled on the NIC.

This topic shows how to configure SR-IOV with your Contrail Networking
system.

Enabling ASPM in BIOS
---------------------

To use SR-IOV, it must have Active State Power Management (ASPM) enabled
for PCI Express (PCIe) devices. Enable ASPM in the system BIOS.

**Note**

The BIOS of your system might need to be upgraded to a version that can
enable ASPM.

Configuring SR-IOV Using the Ansible Deployer
---------------------------------------------

You must perform the following tasks to enable SR-IOV on a system.

1. Enable the Intel Input/Ouput Memory Management Unit (IOMMU) on Linux.

2. Enable the required number of Virtual Functions (VFs) on the selected
   NIC.

3. Configure the names of the physical networks whose VMs can interface
   with the VFs.

4. Reboot Nova compute.

   .. raw:: html

      <div id="jd0e51" class="sample" dir="ltr">

   .. raw:: html

      <div id="jd0e52" dir="ltr">

   ``service nova-compute restart``

   .. raw:: html

      </div>

   .. raw:: html

      </div>

5. Configure a Nova Scheduler filter based on the new PCI configuration,
   as in the following example:

   .. raw:: html

      <div id="jd0e57" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      /etc/nova/nova.conf
           [default]
           scheduler_default_filters = PciPassthroughFilter
           scheduler_available_filters = nova.scheduler.filters.all_filters
           scheduler_available_filters =
      nova.scheduler.filters.pci_passthrough_filter.PciPassthroughFilter

   .. raw:: html

      </div>

   .. raw:: html

      </div>

6. Restart Nova Scheduler.

   .. raw:: html

      <div id="jd0e63" class="sample" dir="ltr">

   .. raw:: html

      <div id="jd0e64" dir="ltr">

   ``service nova-scheduler restart``

   .. raw:: html

      </div>

   .. raw:: html

      </div>

The above tasks are handled by the Ansible Deployer playbook. The
cluster members and its configuration parameters are specified in the
``instances.yaml`` file located in the config directory within the
ansible-deployer repository.

The compute instances that are going to be in SR-IOV mode should have an
SR-IOV configuration. The ``instance.yaml`` snippet below shows a sample
instance definition.

.. raw:: html

   <div id="jd0e76" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   instances:
     bms1:
       provider: bms
       ip: ip-address
       roles:
         openstack:
     bms2:
       provider: bms
       ip:ip-address
       roles:
         config_database:
         config:
         control:
         analytics_database:
         analytics:
         webui:
     bms3:
       provider: bms
       ip: ip-address
       roles:
         openstack_compute:
         vrouter:
           SRIOV: true
           SRIOV_VF: 3
           SRIOV_PHYSICAL_INTERFACE: eno1
           SRIOV_PHYS_NET:  physnet1

.. raw:: html

   </div>

.. raw:: html

   </div>

Configuring SR-IOV Using Helm
-----------------------------

You must perform the following tasks to enable SR-IOV on a system.

1. Enable the Intel Input/Ouput Memory Management Unit (IOMMU) on Linux.

2. Enable the required number of Virtual Functions (VFs) on the selected
   NIC.

3. Configure the names of the physical networks whose VMs can interface
   with the VFs.

4. Reboot Nova compute.

   .. raw:: html

      <div id="jd0e107" class="sample" dir="ltr">

   .. raw:: html

      <div id="jd0e108" dir="ltr">

   ``service nova-compute restart``

   .. raw:: html

      </div>

   .. raw:: html

      </div>

5. Configure a Nova Scheduler filter based on the new PCI configuration,
   as in the following example:

   .. raw:: html

      <div id="jd0e113" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      /etc/nova/nova.conf
            [default]
            scheduler_default_filters = PciPassthroughFilter
            scheduler_available_filters = nova.scheduler.filters.all_filters
            scheduler_available_filters =
            nova.scheduler.filters.pci_passthrough_filter.PciPassthroughFilter

   .. raw:: html

      </div>

   .. raw:: html

      </div>

6. Restart Nova Scheduler.

   .. raw:: html

      <div id="jd0e119" class="sample" dir="ltr">

   .. raw:: html

      <div id="jd0e120" dir="ltr">

   ``service nova-scheduler restart``

   .. raw:: html

      </div>

   .. raw:: html

      </div>

The above tasks are handled by the Helm charts. The cluster members and
its configuration parameters are specified in the
``multinode-inventory`` file located in the config directory within the
openstack-helm-infra repository.

For Helm, the configuration and SR-IOV environment-specific parameters
must be updated in three different places:

-  The compute instance must be set as contrail-vrouter-sriov.

   For example, the following is a snippet from the
   ``tools/gate/devel/multinode-inventory.yaml`` file in the
   openstack-helm-infra repository.

   .. raw:: html

      <div id="jd0e139" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      all:
        children:
          primary:
            hosts:
              node1:
                ansible_port: 22
                ansible_host: host-ip-address
                ansible_user: ubuntu
                ansible_ssh_private_key_file: /home/ubuntu/.ssh/insecure.pem
                ansible_ssh_extra_args: -o StrictHostKeyChecking=no
        nodes:
          children:
            openstack-compute:
              children:
                 contrail-vrouter-sriov: #compute instance set to contrail-vrouter-sriov
                    hosts:
                      node7:
                      ansible_port: 22
                       ansible_host: host-ip-address
                       ansible_user: ubuntu
                       ansible_ssh_private_key_file: /home/ubuntu/.ssh/insecure.pem
                       ansible_ssh_extra_args: -o StrictHostKeyChecking=no

   .. raw:: html

      </div>

   .. raw:: html

      </div>

-  Contrail-vrouter-sriov must be labeled appropriately.

   For example, the following is a snippet from
   the\ ``tools/gate/devel/multinode-vars.yaml`` in the
   openstack-helm-infra repository.

   .. raw:: html

      <div id="jd0e156" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      nodes:
        labels:
          primary:
          - name: openstack-helm-node-class
            value: primary

                  all:
               - name: openstack-helm-node-class
                 value: general
               contrail-controller:
               - name: opencontrail.org/controller
                     value: enabled
               openstack-compute:
               - name: openstack-compute-node
                     value: enabled
                  contrail-vrouter-dpdk:
                  - name: opencontrail.org/vrouter-dpdk
                        value: enabled
                   contrail-vrouter-sriov: # label as contrail-vrouter-sriov
                   - name: vrouter-sriov
                       value: enabled

   .. raw:: html

      </div>

   .. raw:: html

      </div>

-  SR-IOV config parameters must be updated in the
   ``contrail-vrouter/values.yaml`` file.

   For example, the following is a snippet from the
   ``contrail-vrouter/values.yaml`` file in the contrail-helm-deployer
   repository.

   .. raw:: html

      <div id="jd0e170" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      contrail_env_vrouter_kernel:
        AGENT_MODE: kernel

      contrail_env_vrouter_sriov:
        SRIOV: true
        per_compute_info:
          node_name: k8snode1
          SRIOV_VF:  10
          SRIOV_PHYSICAL_INTERFACE: enp129s0f1
          SRIOV_PHYS_NET:  physnet1

   .. raw:: html

      </div>

   .. raw:: html

      </div>

Launching SR-IOV Virtual Machines
---------------------------------

.. raw:: html

   <div class="mini-toc-intro">

After ensuring that SR-IOV features are enabled on your system, use one
of the following procedures to create a virtual network from which to
launch an SR-IOV VM, either by using the Contrail Web UI or the CLI.
Both methods are included.

.. raw:: html

   </div>

-  `Using the Contrail Web UI to Enable and Launch an SR-IOV Virtual
   Machine <sriov-with-vrouter-vnc.html#jd0e181>`__

-  `Using the CLI to Enable and Launch SR-IOV Virtual
   Machines <sriov-with-vrouter-vnc.html#jd0e248>`__

Using the Contrail Web UI to Enable and Launch an SR-IOV Virtual Machine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To use the Contrail Web UI to enable and launch an SR-IOV VM:

1. At **Configure > Networking > Networks**, create a virtual network
   with SR-IOV enabled. Ensure the virtual network is created with a
   subnet attached. In the Advanced section, select the **Provider
   Network** check box, and specify the physical network already enabled
   for SR-IOV (in ``testbed.py`` or ``nova.conf``) and its VLAN ID. See
   `Figure 1 <sriov-with-vrouter-vnc.html#sriov1>`__.

   |Figure 1: Edit Network|

2. On the virtual network, create a Neutron port (**Configure >
   Networking > Ports**), and in the **Port Binding** section, define a
   **Key** value of SR-IOV and a **Value** of direct. See
   `Figure 2 <sriov-with-vrouter-vnc.html#sriov2>`__.

   |Figure 2: Create Port|

3. Using the UUID of the Neutron port you created, use the ``nova boot``
   command to launch the VM from that port.

   ``nova boot --flavor m1.large --image <image name> --nic port-id=<uuid of above port> <vm name>``

Using the CLI to Enable and Launch SR-IOV Virtual Machines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To use CLI to enable and launch an SR-IOV VM:

1. Create a virtual network with SR-IOV enabled. Specify the physical
   network already enabled for SR-IOV (in ``testbed.py`` or
   ``nova.conf``) and its VLAN ID.

   The following example creates ``vn1`` with a VLAN ID of 100 and is
   part of ``physnet1``:

   ``neutron net-create  --provider:physical_network=physnet1  --provider:segmentation_id=100 vn1``

2. Create a subnet in vn1.

   ``neutron subnet-create vn1 a.b.c.0/24``

3. On the virtual network, create a Neutron port on the subnet, with a
   binding type of direct.

   ``neutron port-create --fixed-ip subnet_id=<subnet uuid>,ip_address=<IP address from above subnet> --name <name of port> <vn uuid>  --binding:vnic_type direct``

4. Using the UUID of the Neutron port created, use the ``nova boot``
   command to launch the VM from that port.

   ``nova boot --flavor m1.large --image <image name> --nic port-id=<uuid of above port> <vm name>``

5. Log in to the VM and verify that the Ethernet controller is VF by
   using the ``lspci`` command to list the PCI buses.

   The VF that gets configured with the VLAN can be observed using the
   ``ip link`` command.

 

.. |Figure 1: Edit Network| image:: images/S018550.png
.. |Figure 2: Create Port| image:: images/S018551.png
