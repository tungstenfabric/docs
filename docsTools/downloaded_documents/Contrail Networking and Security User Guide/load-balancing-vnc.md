# ECMP Load Balancing in the Service Chain

 

Traffic flowing through a service chain can be load-balanced by
distributing traffic streams to multiple service virtual machines (VMs)
that are running identical applications. This is illustrated in
[Figure 1](load-balancing-vnc.html#load-balance), where the traffic
streams between VM-A and VM-B are distributed between Service VM-1 and
Service VM-2. If Service VM-1 goes down, then all streams that are
dependent on Service VM-1 will be moved to Service VM-2.

![Figure 1: Load Balancing a Service Chain](images/s041830.gif)

The following are the major features of load balancing in the service
chain:

-   Load balancing can be configured at every level of the service
    chain.

-   Load balancing is supported in routed and bridged service chain
    modes.

-   Load balancing can be used to achieve high availability—if a service
    VM goes down, the traffic passing through that service VM can be
    distributed through another service VM.

-   A load balanced traffic stream always follows the same path through
    the chain of service VM.

 
