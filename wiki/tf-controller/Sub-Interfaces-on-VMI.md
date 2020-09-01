This feature supports creation of VLAN sub-interfaces on a VM's interface.

A VMI (virtual machine interface) object is created for each sub-interface, which is similar to any regular VMIs on the virtual machine. This object will have Vlan identifier set in virtual-machine-interface-properties of the VMI in the sub-interface-vlan-tag field. This VMI object is then linked to the regular VMI of the VM, under which it will be a sub-interface. Note that the VMI created for the sub interface can have its own properties, can be part of a different virtual network from the regular VMI etc.

Once the sub-interface VMI is created and linked to the regular VMI, all relevant configuration for the sub-interface is also downloaded to the vrouter-agent. The vrouter adds / strips the vlan tags to the packets sent to / received from the sub-interface.

VLAN sub-interfaces are not supported on ESXi.