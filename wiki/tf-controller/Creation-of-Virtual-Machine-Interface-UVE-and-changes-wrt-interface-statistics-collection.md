# Addition of Virtual Machine Interface UVE, Logical Interface UVE and Physical Interface UVE
Starting from Release R2.20 the following new UVEs are added, which will be
sent from contrail-vrouter-agent. These new UVEs correspond to VM interfaces,
logical interfaces and physical interfaces. Prior to R2.20, these were sent
in the parent objects _viz_. VM uve and Prouter uve.

The issue with the interface UVEs being part of parent object are 2 fold.  
1. there needs to exist a parent object before UVEs for these are created  
2. as the UVE mechanism requires the whole field [in this case the list of interface structures] to be send even when only one field in one interface has changed.

Both these led us to create interface UVEs at the top level and only
carry the keys in the parent object.

## UveVMInterfaceAgentTrace
UVE to represent Virtual-machine-interface.  This UVE carries all the
information about virtual-machine interface including statistics. Before
release R2.20, this information was being sent in UveVirtualMachineAgentTrace
and VirtualMachineStatsTrace Uves

## UveLogicalInterfaceAgentTrace
UVE to represent Logical Interface information. Before release R2.20, this
information was being sent in UveProuterAgent.

## UvePhysicalInterfaceAgentTrace
UVE to represent Physical Interface information. Before release R2.20, this
information was being sent in UveProuterAgent

## Effect of this change on network statistics
Earlier we were using the following structures for sending interface and
floating ip statistics.

`struct UveVirtualMachineAgent {`  
    `1: string         name (key="ObjectVMTable")`  
`...`  
    `13: optional list<VmFloatingIPStats> fip_stats_list;`  
`...`  
`}`  

`struct VirtualMachineStats {`  
    `1: string         name (key="ObjectVMTable")`  
`...`  
    `3: optional list<VmFloatingIPStatSamples> fip_stats (tags=".vn,.iface_name,.ip_address")`  
    `4: optional list<VmInterfaceStats> if_stats (tags=".name")`  
`...`  
`}`  

With the proposed changes, these statistics are moved to under VMInterface UVE as below, hence
the APIs to retrieve these statistics is changed too.

`struct UveVMInterfaceAgent {`  
    `1: string                name (key="ObjectVMITable")`  
`...`  
   `16: optional list<VmFloatingIPStats> fip_agg_stats;`  
   `17: optional list<VmFloatingIPStats> fip_diff_stats (tags=".virtual_network,.ip_address")`  
   `18: optional VmInterfaceStats if_stats (tags="vm_name,virtual_network,vm_uuid")`  
`...`  
`}`  

### Current API
Current API is into VirtualMachineStats.if_stats table as below. Example 1 shows extracting in_bytes, out_bytes **raw** samples. Example 2 shows extracting time series values for in_bytes, out_bytes.

**Example 1:**  
`root@a6s45:~# contrail-stats --dtable VirtualMachineStats.if_stats --where "Source=*" --select T name if_stats.name if_stats.in_bytes if_stats.out_bytes --last 1m`  

`{"start_time": "now-1m", "sort_fields": [], "end_time": "now", "select_fields": ["T", "name", "if_stats.name", "if_stats.in_bytes", "if_stats.out_bytes"], "table": "StatTable.VirtualMachineStats.if_stats", "where": [[{"suffix": null, "value2": null, "name": "Source", "value": "", "op": 7}]]}`  

`{u'if_stats.in_bytes': 0, u'if_stats.out_bytes': 0, u'T': 1430333913672357, u'name': u'4d1595a2-3d85-44ca-8207-d4a53de242c7', u'if_stats.name': u'default-domain:admin:48b9de3f-e70c-4390-8feb-bde32f027e1a'}`  
`{u'if_stats.in_bytes': 0, u'if_stats.out_bytes': 0, u'T': 1430333913672381, u'name': u'65169549-5c2a-4638-824f-faa39d369fae', u'if_stats.name': u'default-domain:admin:4822e9d0-aeb5-4ca3-bdf9-64b2714bf9b7'}`  
`{u'if_stats.in_bytes': 0, u'if_stats.out_bytes': 0, u'T': 1430333913672399, u'name': u'6b36b3ac-ccf7-4959-a9c6-d0ca5f4bce15', u'if_stats.name': u'default-domain:admin:1af07e49-e007-4708-940e-491b73cb1ea2'}`  
`{u'if_stats.in_bytes': 0, u'if_stats.out_bytes': 0, u'T': 1430333913672425, u'name': u'88dd3252-5b2e-4c7d-a7c2-46a5640af07b', u'if_stats.name': u'default-domain:admin:bba50c17-d9d2-423d-bda7-f69c2382a7d9'}`  
`{u'if_stats.in_bytes': 0, u'if_stats.out_bytes': 0, u'T': 1430333913672442, u'name': u'bf26ebe3-53e5-4eb1-a7c7-de8949d26e26', u'if_stats.name': u'default-domain:admin:91a511bc-3d8b-4736-abea-955b6f5ed944'}`  

**Example 2:**  
`root@a6s45:~# contrail-stats --dtable VirtualMachineStats.if_stats --where "Source=*" --select "T=120" name if_stats.name "SUM(if_stats.in_bytes)" "SUM(if_stats.out_bytes)" --last 10m`  

`{"start_time": "now-10m", "sort_fields": [], "end_time": "now", "select_fields": ["T=120", "name", "if_stats.name", "SUM(if_stats.in_bytes)", "SUM(if_stats.out_bytes)"], "table": "StatTable.VirtualMachineStats.if_stats", "where": [[{"suffix": null, "value2": null, "name": "Source", "value": "", "op": 7}]]}`  

`{u'SUM(if_stats.in_bytes)': 0, u'if_stats.name': u'default-domain:admin:91a511bc-3d8b-4736-abea-955b6f5ed944', u'SUM(if_stats.out_bytes)': 0, u'T=': 1430333400000000, u'name': u'bf26ebe3-53e5-4eb1-a7c7-de8949d26e26'}`  
`{u'SUM(if_stats.in_bytes)': 0, u'if_stats.name': u'default-domain:admin:bba50c17-d9d2-423d-bda7-f69c2382a7d9', u'SUM(if_stats.out_bytes)': 0, u'T=': 1430333400000000, u'name': u'88dd3252-5b2e-4c7d-a7c2-46a5640af07b'}`  
`{u'SUM(if_stats.in_bytes)': 0, u'if_stats.name': u'default-domain:admin:1af07e49-e007-4708-940e-491b73cb1ea2', u'SUM(if_stats.out_bytes)': 0, u'T=': 1430333400000000, u'name': u'6b36b3ac-ccf7-4959-a9c6-d0ca5f4bce15'}`  
`{u'SUM(if_stats.in_bytes)': 0, u'if_stats.name': u'default-domain:admin:4822e9d0-aeb5-4ca3-bdf9-64b2714bf9b7', u'SUM(if_stats.out_bytes)': 0, u'T=': 1430333400000000, u'name': u'65169549-5c2a-4638-824f-faa39d369fae'}`  
`{u'SUM(if_stats.in_bytes)': 0, u'if_stats.name': u'default-domain:admin:48b9de3f-e70c-4390-8feb-bde32f027e1a', u'SUM(if_stats.out_bytes)': 0, u'T=': 1430333400000000, u'name': u'4d1595a2-3d85-44ca-8207-d4a53de242c7'}`  
`{u'SUM(if_stats.in_bytes)': 0, u'if_stats.name': u'default-domain:admin:bba50c17-d9d2-423d-bda7-f69c2382a7d9', u'SUM(if_stats.out_bytes)': 0, u'T=': 1430333520000000, u'name': u'88dd3252-5b2e-4c7d-a7c2-46a5640af07b'}`  
`{u'SUM(if_stats.in_bytes)': 0, u'if_stats.name': u'default-domain:admin:91a511bc-3d8b-4736-abea-955b6f5ed944', u'SUM(if_stats.out_bytes)': 0, u'T=': 1430333520000000, u'name': u'bf26ebe3-53e5-4eb1-a7c7-de8949d26e26'}`  
`{u'SUM(if_stats.in_bytes)': 0, u'if_stats.name': u'default-domain:admin:48b9de3f-e70c-4390-8feb-bde32f027e1a', u'SUM(if_stats.out_bytes)': 0, u'T=': 1430333520000000, u'name': u'4d1595a2-3d85-44ca-8207-d4a53de242c7'}`  

### New API
New API is into VirtualMachineStats.if_stats table as below. As before, Example 1 shows extracting in_bytes, out_bytes **raw** samples. Example 2 shows extracting time series values for in_bytes, out_bytes.


**Example 1**  
`root@b5s29:~# contrail-stats --table UveVMInterfaceAgent.if_stats --where "Source=*" --select T name if_stats.in_bytes if_stats.out_bytes --last 1m`  

`{"start_time": "now-1m", "sort_fields": [], "end_time": "now", "select_fields": ["T", "name", "if_stats.in_bytes", "if_stats.out_bytes"], "table": "StatTable.UveVMInterfaceAgent.if_stats", "where": [[{"suffix": null, "value2": null, "name": "Source", "value": "", "op":`
     `7}]]}`  

`{u'if_stats.in_bytes': 0, u'T': 1433540321416693, u'name': u'default-domain:development:cd4c9bb0-39fc-497c-8a9b-95faecbcea98', u'if_stats.out_bytes': 0}`  
`{u'if_stats.in_bytes': 0, u'T': 1433540321416731, u'name': u'default-domain:webui:st6_port134', u'if_stats.out_bytes': 0}`  
`{u'if_stats.in_bytes': 0, u'T': 1433540321416755, u'name': u'default-domain:webui:st6_port143', u'if_stats.out_bytes': 0}`  
`{u'if_stats.in_bytes': 5494, u'T': 1433540321924851, u'name': u'default-domain:admin:0851101a-790e-41fd-becb-f56b7def28f9', u'if_stats.out_bytes': 4254}`  
`{u'if_stats.in_bytes': 7682, u'T': 1433540321924884, u'name': u'default-domain:admin:459d6a27-4d45-44bd-b44d-4106e1381316', u'if_stats.out_bytes': 5646}`  
`{u'if_stats.in_bytes': 0, u'T': 1433540321924997, u'name': u'default-domain:webui:st5_port22', u'if_stats.out_bytes': 0}`  
`...`  

**Example 2**  
`root@b5s29:~# contrail-stats --table UveVMInterfaceAgent.if_stats --where "name=default-domain:admin:da96b304-0452-4754-a19e-cd341ebadcbf" --select "T=120" name "SUM(if_stats.in_bytes)" "SUM(if_stats.out_bytes)" --last 5m`  
`{"start_time": "now-5m", "sort_fields": [], "end_time": "now", "select_fields": ["T=120", "name", "SUM(if_stats.in_bytes)", "SUM(if_stats.out_bytes)"], "table": "StatTable.UveVMInterfaceAgent.if_stats", "where": [[{"suffix": null, "value2": null, "name": "name", "value": "default-domain:admin:da96b304-0452-4754-a19e-cd341ebadcbf", "op": 1}]]}`  

`{u'SUM(if_stats.in_bytes)': 5288, u'SUM(if_stats.out_bytes)': 5256, u'T=': 1433540160000000, u'name': u'default-domain:admin:da96b304-0452-4754-a19e-cd341ebadcbf'}`  
`{u'SUM(if_stats.in_bytes)': 7028, u'SUM(if_stats.out_bytes)': 8010, u'T=': 1433540280000000, u'name': u'default-domain:admin:da96b304-0452-4754-a19e-cd341ebadcbf'}`  
`{u'SUM(if_stats.in_bytes)': 5346, u'SUM(if_stats.out_bytes)': 5910, u'T=': 1433540400000000, u'name': u'default-domain:admin:da96b304-0452-4754-a19e-cd341ebadcbf'}`  
`...`  

## Removal of VN stats from VN Uve
The fields in_tpkts, in_bytes, out_tpkts, out_bytes from UveVirtualNetworkAgent
which is member of UveVirtualNetworkAgentTrace have been removed. This
information can be obtained VMInterface UVE and aggregation and slicing/dicing
mechanism will allow to get the same statistics, but using a different API.

`diff --git a/src/vnsw/agent/uve/virtual_network.sandesh b/src/vnsw/agent/uve/virtual_network.sandesh`  
`index 04a8777..4cd52eb 100644`  
`--- a/src/vnsw/agent/uve/virtual_network.sandesh`  
`+++ b/src/vnsw/agent/uve/virtual_network.sandesh`  
`@@ -43,10 +43,6 @@ struct UveVirtualNetworkAgent {`  
     `2: optional bool                       deleted`  
     `3: optional i32                        total_acl_rules;`  
     `4: optional list<string>               interface_list (aggtype="union")`  
`-    5: optional u64                        in_tpkts  (aggtype="counter")`  
`-    6: optional u64                        in_bytes  (aggtype="counter")`  
`-    7: optional u64                        out_tpkts (aggtype="counter")`  
`-    8: optional u64                        out_bytes (aggtype="counter")`  
     `9: optional list<UveInterVnStats>      in_stats  (aggtype="append")`  
     `10: optional list<UveInterVnStats>     out_stats (aggtype="append")`  
     `11: optional list<string>              virtualmachine_list (aggtype="union")`  
