## GDB Macros

The following GDB macros are useful in analyzing contrail-vrouter-agent core file. <br>

* STL GDB macros (https://sourceware.org/gdb/wiki/STLSupport) <br>
* Boost pretty printers (https://github.com/ruediger/Boost-Pretty-Printer) <br>
* Contrail Vrouter Agent GDB macros (https://github.com/Juniper/contrail-controller/tree/master/src/vnsw/agent/gdb) <br>
* Contrail DB GDB macros (https://github.com/Juniper/contrail-controller/blob/master/src/db/db.gdb) <br>
* Contrail Task GDB macros (https://github.com/Juniper/contrail-controller/blob/master/src/base/task.gdb) <br>

Source these macros in gdb and use them to analyze the core file. If the downloaded macro files are in /root/gdbmacro, the following snippet shows the sourcing of these macros.

> root@node:~/$ gdb contrail-vrouter-agent core.contrail-vroute*
> (gdb) python                                                                          
 \>import sys                                                                      
 \>                                                                                
 \>sys.path.insert(0, '/root/gdbmacro/stl')                                        
 \>sys.path.insert(0, '/root/gdbmacro/stl/libstdcxx/v6')                           
 \>                                                                                
 \>from libstdcxx.v6.printers import register_libstdcxx_printers                   
 \>register_libstdcxx_printers(None)                                               
 \>                                                                                
 \>sys.path.insert(0, '/root/gdbmacro/boost_pretty_printer')                       
 \>from boost.printers import register_printer_gen                                 
 \>register_printer_gen(None)                                                      
 \>                                                                                
 \>sys.path.insert(0, '/root/gdbmacro/agent_printer')   
 \>
 \>end

>(gdb) source /root/gdbmacro/stl.gdb <br> 
>(gdb) source /root/gdbmacro/db.gdb <br>
>(gbd) source /root/gdbmacro/task.gdb <br> 
>(gdb) source /root/gdbmacro/agent_db.py <br>
>(gdb) source /root/gdbmacro/agent_ksync.py <br>

The operational data in the vrouter-agent can be printed as follows.

>(gdb) python dump_vrf_entries()  # dump all the VRF entries in the operational data <br>
>(gdb) python dump_vn_entries()   # dump all the VN entries in the operational data <br>
>(gdb) python dump_vm_entries()   # dump all the VM entries in the operational data <br>
>(gdb) python dump_intf_entries() # dump all the interface entries in the operational data <br>
>(gdb) python dump_nh_entries()   # dump all the nexthop entries in the operational data <br>
>(gdb) python dump_mpls_entries()       # dump all the MPLS entries in the operational data <br>
>(gdb) python dump_vxlan_entries()      # dump all the VxLAN entries <br>
>(gdb) python dump_vrf_assign_entries() # dump the VRF assign rules <br>
>(gdb) python dump_acl_entries()        # dump the ACL rules <br>
>(gdb) python dump_sg_entries()         # dump the SG entries <br>
>(gdb) python dump_uc_v4_route_entries(<route-table-address>) # dump the unicast route entries <br>
>(gdb) python dump_mc_v4_route_entries(<mcast-table-address>) # dump the multicast route entries <br>
>(gdb) python dump_l2_route_entries(<l2-table-address>) # dump the L2 table entries <br>

The paths in a route entry can be printed using:
>(gdb) python dump_route_paths(<route-entry-address>) <br>

Any operational database entry can be expanded using:
>(gdb) p *(DBEntry *)<database-entry-address>

All the DB tables in the vrouter-agent can be printed using: 
>(gdb) pdb_tables Agent::singleton_->db_ <br>
* The entries starting with __ifmap__ in the name are the config database tables
* The entries starting with __db__ in the name are operational database tables
* Entries ending with __uc.route.0__ are unicast IPv4 route tables
* Entries ending with __uc.route6.0__ are unicast IPv6 route tables
* Entries ending with __evpn.route.0__ are EVPN tables
* Entries ending with __l2.route.0__ are L2 tables

All the ifmap entries in the config database can be printed using:
>(gdb) python dump_ifmap_entries(<ifmap-table-address>) <br>
>(gdb) python dump_ifmap_link_entries(<ifmap-table-address>) <br>

All the configured mirror entries can be printed using:
>(gdb) python dump_mirror_entries() <br>

## Trace Messages
Printing trace messages from the core file is explained [here](https://github.com/Juniper/contrail-controller/wiki/Dump-sandesh-trace-buffer).