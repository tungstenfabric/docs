ECMP Support in Service Chain
=============================

 

Equal-cost multipath (ECMP) can be used to distribute traffic across
VMs.

Service Chain with Equal-Cost Multipath in Active-Active Mode
-------------------------------------------------------------

To support ECMP in the service chain, create multiple port tuples within
the same service instance. The labels should be the same for the VM
ports in each port tuple. For example, if port tuple 1 uses the labels
``left`` and ``right``, then port tuple 2 in the same service instance
should also use the labels ``left`` and ``right`` for its ports.

When there are multiple port tuples, the default mode of operation is
``active-active``.

Service Chain with Health Check
-------------------------------

Service chain Version 2 also allows service instance health check
configuration on a per interface label. This is used to monitor the
health of the service.

For more information about the service instance health check, see
`Service Instance Health
Checks <../topic-map/service-instance-health-check.html>`__.

 
