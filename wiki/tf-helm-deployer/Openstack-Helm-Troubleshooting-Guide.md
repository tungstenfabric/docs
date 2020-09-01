## Wiki where we maintain issues/solutions related to openstack-helm aio/multinode installation 


### In Openstack-helm deployment, ceph pods are all functional but mariadb is not coming up? 

     Solution: "helm delete --purge mariadb" does not cleanup all the objects it creates. 
  
     Please do the following: 
```

     a) helm delete --purge mariadb 

     b) kubectl get pvc -n openstack 

     c) kubectl delete pvc <pvc-name> -n openstack. e.g. kubectl delete pvc mysql-data-mariadb-0 -n openstack 
```

### How to troubleshoot when contrail vrouter agent pod stuck at “PodInitializing”?

Check contrail vrouter-agent pod status and container logs with following command: 
* Describe pod with the following command to check events:
```
# kubectl describe pods contrail-vrouter-agent-8g4gk -n kube-system
vents:
  Type     Reason      Age                From                         Message
  ----     ------      ----               ----                         -------
  Normal   Pulled      47m (x39 over 3h)  kubelet, ubuntu-contrail-12  Container image "10.13.82.36:5000/contrail-agent-vrouter-init-kernel:5.0.0-170-ubuntu16-newton" already present on machine
  Warning  BackOff     7m (x960 over 3h)  kubelet, ubuntu-contrail-12  Back-off restarting failed container
  Warning  FailedSync  2m (x983 over 3h)  kubelet, ubuntu-contrail-12  Error syncing pod
```
From "kubectl describe" command check which container in the POD is failing and in error state, in the above scenarios the container “contrail-agent-init-kernel” failed, which runs initially to compile vRouter for OS kernel module.
```
# kubectl logs -f contrail-vrouter-agent-s9fqc -c contrail-agent-init-kernel -n kube-system
INFO: detected linux id: ubuntu
INFO: Compiling vrouter kernel module for ubuntu...
INFO: Load kernel module for kver=4.4.0-87-generic
ERROR: There is no kernel headers in /usr/src for current kernel. Exiting…
```
The above error pointing to missing kernel headers from the host OS. Please install Linux header using the following command.
```
# apt-get install linux-headers-$(uname -r)
```

### Compute nodes with single interface face issues during docker image download

When your compute nodes have the single interface you might face an issue in downloading contrail images during vrouter-agent POD creation. The issue is caused by network connection lost during vhost0 creation and init-kernel during agent POD creation. To above this issue it is recommended downloading contrail images on all compute nodes manually using following commands:
```
Download contrail-nodemgr
# docker pull docker.io/opencontrail/contrail-nodemgr:5.0.0-175-centos7-newton

Download contrail-agent
# docker pull docker.io/opencontrail/contrail-agent-vrouter:5.0.0-175-centos7-newton

Download contrail-agent-vrouter-init-kernel (vRouter Kernel Module compilation and kernel load)
# # docker pull docker.io/opencontrail/contrail-agent-vrouter-init-kernel:5.0.0-175-ubuntu16-newton
```
You will not face this issue with compute node with multiple interfaces where a separate interface is used for a control-data plane.  


## Troubleshooting VM creation in OpenContrail & OpenStack Helm Cluster (vRouter Agent & Calico Felix port 9091 conflict Issue):

### Issue Description:

VM creation is successful via OpenStack CLI or Horizon but there is no VIF attach to the VM and nova-compute logs were reporting following errors:

```
2018-02-27 05:17:06.864 1996 ERROR nova.virt.libvirt.vif [instance: 5dd76e8a-b80b-4ddb-a462-ff13554c1088] Command: sudo nova-rootwrap /etc/nova/rootwrap.conf vrouter-port-control --oper=add --uuid=5b0417d8-a4e7-4ab8-a990-f4415372cfe4 --instance_uuid=5dd76e8a-b80b-4ddb-a462-ff13554c1088 --vn_uuid=16695d77-2575-4d9b-bdde-b2317557351d --vm_project_uuid=bd4439035e7342e986356307c67c255b --ip_address=172.16.1.6 --ipv6_address=None --vm_name=Test-05 --mac=02:5b:04:17:d8:a4 --tap_name=tap5b0417d8-a4 --port_type=NovaVMPort --tx_vlan_id=-1 --rx_vlan_id=-1
2018-02-27 05:17:06.864 1996 ERROR nova.virt.libvirt.vif [instance: 5dd76e8a-b80b-4ddb-a462-ff13554c1088] Exit code: 4
2018-02-27 05:17:06.864 1996 ERROR nova.virt.libvirt.vif [instance: 5dd76e8a-b80b-4ddb-a462-ff13554c1088] Stdout: u'Request failed: 404 page not found\n\n’
```

### Troubleshooting steps:

Create VM via CLI targeting one of the compute node, in below example host “ubuntu-contrail-10” is used for VM creation 
```
$ openstack server create --flavor m1.tiny --image "Cirros 0.3.5 64-bit" --nic net-id=16695d77-2575-4d9b-bdde-b2317557351d Test-04 --availability-zone nova:ubuntu-contrail-10
```

While creating VM start monitoring "nova-compute” logs using following commands:
```
$ kubectl get pods -n openstack -o wide | grep nova-compute
nova-compute-default-4gpg8            1/1       Running                 0          16h       10.13.82.45       ubuntu-contrail-11
nova-compute-default-chhnc            1/1       Running                 0          16h       10.13.82.44       ubuntu-contrail-10

$ kubectl logs -f nova-compute-default-chhnc -n openstack
```
Above Errors is reported with "Exit Code 4” which indicates that “router-port-control” utility tried adding the port as per config data received from Nova but did not get “200 OK” and failed with “404 Page not found”, in this whole process port 9091 is used by vRouter-Agent for port addition/deletion/status update. In this cluster the port 9091 was used by “calico-felix” process and causing the issue. 

```
Port Conflict with calico-felix Cluster:
$ sudo netstat -anlp | grep 9091
tcp6       0      0 :::9091                :::*                    LISTEN      31171/calico-felix

Normal Cluster:
$ netstat -anlp | grep 9091
tcp        0      0 0.0.0.0:9091            0.0.0.0:*               LISTEN      3198/contrail-vrout
```

* Other symptoms: When you restart contrail-vrouter-agent POD and check “/var/log/contrail/contrail-vrouter-agent.log” following SYS_ERR will be reported for 9091 port conflict as well.

```
2018-02-26 Mon 20:00:51:063.474 UTC  osh-contrail-multinode-4 [Thread 140487261325056, Pid 1]: TCP [SYS_ERR]: TcpServerMessageLog: Server   TCP bind(0.0.0.0:9091): Address already in use src/contrail-common/io/tcp_server.cc 95
```

### Solution/Fix:

Please make sure no other process uses port 9091 on compute host as port 9091 is used by Contrail-vRouter for port add/delete/status.