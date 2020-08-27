This is to make sure same resources are allocated after restart. These are the resources allocated locally by agent. One of the resource which is visible across system is MPLS label.  On restart if agent sends new label for local routes then it will cause change in whole system. Presence of resource manager makes sure that same label is given and hence system does not see any change.
 
**Resource Manager is divided in two parts - allocator and backup.**

**Allocator**

It is responsible for identifying what kind of resource is needed and manages the users claims on them. Each user specifies a key and allocator allocates one resource to same. This key to resource mapping is stored in manager as a map. Keys can be heterogenous depending on users. For example MPLS label can have users like VRF, VMI, Multicast. Each of them can have different key.
Currently index vector has been made as a resource, but more can be added as and when needed.
 
**Backup**

Each resource allocated above has an option to be backed up. For backup the resource key and data is converted to sandesh format. In case of MPLS above each type of user key will have its sandesh representation and mpls label will be represented as one more sandesh. The key data pair is then pushed into a sandesh map which is then written to a file. Each resource update keeps on modifying this map. Point to note update does not result in file operation. There is a separate timer which is responsible for dumping all backed up resource to file.
On restarting these files will be read and resource manager populated before any config is processed. This makes sure that same data is allocated for a key requested by config and hence persistence is achieved.
 
Though backup module is flexible to not only take data to be backed up from resource manager but from any other source as well. All it needs is a sandesh representation of same and consumer once restore is done.
 
This will be further extended to back up config later. Other extensions which have to be done are agent resources like nexthop-id, vrf-id, i/f-id etc.
 