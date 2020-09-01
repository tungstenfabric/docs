## **Overview:**
This document focuses on explaining what all configurations need to be done as part of QOS queueing in release R3.2 and how to play around with it.

There are 2 major modules of Qos Queueing in R3.2.

They can be segregated as:

1. Queue mapping : It helps in directing the traffic to a particular physical Queue on the NIC interface
2. Queue scheduling : We can configure the queue scheduling to be strict or weighted round robin.
   The traffic mapped to the queue by consulting the "Queue mapping" will get scheduling behavior as configured in "Queue scheduling"

Logical Queues are what we expose to end user. So, user has to configure logical IDs which will internally map to HW queues.


## **Assumptions:**
Assumption of this wiki page is that you already understand Qos queuing concept.
Please refer to following wiki page to get more information:
https://github.com/Juniper/contrail-controller/wiki/QoS



# **Queue mapping**
Queue mapping is logical to Hardware Queue map.
It is kind of a mapping table where 1 or more Logical Queue IDs maps to a single HW queue.


## **Steps to configure Queue mapping:**
* Before provisioning the setup, we can make the required configurations in the testbed file as follows:

>      env.qos = {host2: [{'hardware_q_id': '3', 'logical_queue':['1', '6-10', '12-15']},
>                     {'hardware_q_id': '11', 'logical_queue':['40-46']},
>                     {'hardware_q_id': '18', 'logical_queue':['70-74, 75, 80-95']},
>                     {'hardware_q_id': '28', 'logical_queue':['115']},
>                     {'hardware_q_id': '36', 'logical_queue':['140-143', '145']},
>                     {'hardware_q_id': '43', 'logical_queue':['175']},
>                     {'hardware_q_id': '53', 'logical_queue':['180-220'], 'default': 'True'},
>                     {'hardware_q_id': '61', 'logical_queue':['245']}],
>              host4: [{'hardware_q_id': '4', 'logical_queue':['1', '6-10', '12-15']},
>                     {'hardware_q_id': '12', 'logical_queue':['40-46']},
>                     {'hardware_q_id': '19', 'logical_queue':['70-74, 75, 80-95']},
>                     {'hardware_q_id': '29', 'logical_queue':['115']},
>                     {'hardware_q_id': '37', 'logical_queue':['140-143', '145']},
>                     {'hardware_q_id': '44', 'logical_queue':['175']},
>                     {'hardware_q_id': '54', 'logical_queue':['180'], 'default': 'True'},
>                     {'hardware_q_id': '62', 'logical_queue':['245']}]}

>       hardware_q_id  : Hardware queue identifier.
>       logical_queue  : Defines the logical queues that map to the hardware queue.
>       default        : When set to True, defines the default hardware queue for Qos. All unspecified logical queues map to this hardware queue.


The provisioning will take care to populate the contrail-vrouter-agent.conf with above mentioned configurations.

* Alternatively, if you have already provisioned the setup without including qos configurations at the time of fresh provisioning, you can directly go and modify the contrail-vrouter-agent.conf on each compute node as follows:


>       [QOS]
>       [QUEUE-4]
>       logical_queue=[1, 6-10, 12-15]

>       [QUEUE-12]
>       logical_queue=[40-46]

>       [QUEUE-19]
>       logical_queue=[70-74, 75, 80-95]

>       [QUEUE-29]
>       logical_queue=[115]

>       [QUEUE-37]
>       logical_queue=[140-143, 145]

>       [QUEUE-44]
>       logical_queue=[175]

>       [QUEUE-62]
>       logical_queue=[245]

>       [QUEUE-54]
>       default_hw_queue= true
>       logical_queue=[180]

Please don't forget to restart contrail-vrouter-agent service after making modifications in contrail-vrouter-agent.conf

* Another way to configure qos mapping in an already running setup is by using fab utility. For that, just update the testbed file and env.qos corresponding to your compute nodes. Run a fab command "fab setup_qos". This fab utility will do the following:

1. Update the contrail-vrouter-agent.conf file with QOS section.
2. Set the bitmap in ps_cpu file of each queue to 0
3. Restart the agent so that changes take effect.




## **How Qos Queueing works:**

1. Using Contrail UI, while configuring a Forwarding class(FC) though UI, you have to mention a Qos Queue ID.
   This will implicitly create a QosQueue object with that ID. This is the Logical Queue ID.
   
   Alternatively, if you don't use UI, then you have to create a QosQueue object using a VNC API mentioning the logical Queue ID.

   Please note that when you provision the setup, Queue mapping gets populated in contrail-vrouter-agent.conf but the logical QosQueue objects do not get created by their own. User have to create them manually if using VncApi. If using UI, it gives us provision that while creating a Forwarding Class and mentioning QosQueue ID, it creates the QosQueue object as well.

2. After FC is created, agent knows that a particular FC maps to some Logical Queue ID.
   It is the task of vrouter to associate the FC to actual HW queue based on the Logical Queue ID used by user.
   For eg:
   User creates a FC using UI and mention QosQueue ID as 141.
   Then, a QosQueue object will get created and it will also get associated with the FC.
   Then contrail-vrouter-agent.conf will be consulted and it will search for corresponding HW queue.
   As per testbed sample above, FC will map to HW queue 36 on host2 and HW queue 37 on host4.
   In case user use QosQueue ID which do not maps to any physical HW queue e.g.:146, then it will map to default HW queue 53 on host2 and 54 on host4.


## How to test Queue mapping:
1. Create QosQueue object using any valid logical id.
2. Create a FC and map the QosQueue ID to the FC. (Step 1 and 2 happens together if using Contrail UI)
3. Create a Qos Config and map some dscp/dot1p/exp to the FC created in step 2.
4. Apply this Qos config on VMI/ VN/ Policy.
5. Send high rate traffic with dscp/dot1p/exp as mentioned in step 3.
6. Verify through "ethtool -S <interfaceName>" that traffic is flowing through the HW queue which maps to the logical queue id used in step 1.




# **Queue scheduling**
In Queue scheduling we set scheduling related configurations for Queues.

Few important but a little confusing things to understand in Qos Scheduling concept are Priority, Traffic Class(TC) and Priority Group(PG). These are standard definitions in which we apply scheduling configurations on Intel NICs.
Explanation about Priority, Traffic Class and Priority Group can be found below in section "How Qos Scheduling works". 

Till then, just assume that we have 8 PGs in a system from PG0 to PG7. 
If we have 64 HW queues, then HW queue 0 - 7 belong to PG0, 8 - 15 belong to PG1 and so on...

Priority group has 2 attributes:

1. Strictness : We configure the PG as strict priority(binary 1) queue or a Round Robin one(binary 0).
2. Bandwidth: This parameter hold significance only for round robin queues. For strict queues, it will be set to 0. For Round robin queues, we set different values of BW. Sum of total BW allotted to all queues should not exceed 100.

The BW and Strictness configurations which we do for PG0 will be applicable to all queues from HW queue 0 to 7. Same is true for other PGs as well.
You can understand the whole concept with this assumption without bothering for Priority and Traffic class. 


Following is the traffic behavior which we expect after configuring scheduling:

1. If traffic congestion happens between 2 PGs with strictness as 1(set), then the PG with higher id (eg. PG7) will preempt the PG with lower ID(e.g. PG0).
2. If traffic congestion happens between 2 PGs with 1 PG having  strictness as 1(set) and other with strictness 0(reset), the PG with strictness set will preempt the traffic of other PG irrespective of PG ID being higher or lower.
3. If traffic congestion happens between 2 PGs with strictness as 0(reset), then the traffic will be scheduled in BW ratio configured for the 2 round robin PGs.

Note:
It is choice of user if he/she wants to use Queue scheduling or not. It is completely optional. The user can have anything of his own to do such configurations. What contrail has done here is just provided a utility named "qosmap" which will help user to configure the NIC queues scheduling parameters. After configurations, behavior of queues of the NIC is dependent on HW. IF HW is having some limitations, few features might not work as expected.
Our commitment is Intel-NIANTEC 10G NIC interface "82599ES". Testing has been done on this NIC.

## **Steps to configure Queue scheduling:**
* Before provisioning the setup, we can make the required configurations in the testbed file as follows:

>       env.qos_niantic = {host2:[
>                           { 'priority_id': '0', 'scheduling': 'strict', 'bandwidth': '10'},
>                           { 'priority_id': '1', 'scheduling': 'rr', 'bandwidth': '0'},
>                           { 'priority_id': '2', 'scheduling': 'strict', 'bandwidth': '25'},
>                           { 'priority_id': '3', 'scheduling': 'rr', 'bandwidth': '0'},
>                           { 'priority_id': '4', 'scheduling': 'strict', 'bandwidth': '30'},
>                           { 'priority_id': '5', 'scheduling': 'rr', 'bandwidth': '0'},
>                           { 'priority_id': '6', 'scheduling': 'strict', 'bandwidth': '35'},
>                           { 'priority_id': '7', 'scheduling': 'rr', 'bandwidth': '0'}],
>                    host4:[
>                           { 'priority_id': '1', 'scheduling': 'strict', 'bandwidth': '0'},
>                           { 'priority_id': '3', 'scheduling': 'rr', 'bandwidth': '25'},
>                           { 'priority_id': '6', 'scheduling': 'rr', 'bandwidth': '50'},
>                           { 'priority_id': '7', 'scheduling': 'strict', 'bandwidth': '0'}]}

>        scheduling     : Defines the scheduling algorithm to be used by the corresponding priority group (strict / rr).
>        bandwidth      : Bandwidth to be used by the corresponding priority group when scheduling is round-robin. 


The provisioning will take care to populate the contrail-vrouter-agent.conf with above mentioned configurations.

* Alternatively, if you have already provisioned the setup without including qos configurations at the time of fresh provisioning, you can directly go and modify the contrail-vrouter-agent.conf on each compute node as follows:

>       [QOS-NIANTIC]
>       [PG-1]
>       scheduling=strict
>       bandwidth=0

>       [PG-3]
>       scheduling=rr
>       bandwidth=25

>       [PG-6]
>       scheduling=rr
>       bandwidth=50

>       [PG-7]
>       scheduling=strict
>       bandwidth=0

Note that restart of agent is not required here. There is no process which is using these configurations until we use some way to read this data and run qosmap utility.

* Another way to configure qos scheduling in an already running setup is by using fab utility. For that, just update the testbed file and env.qos_niantic corresponding to your compute nodes. Run a fab command "fab setup_qos_niantic". This fab utility will do the following:

1. Update the contrail-vrouter-agent.conf file with QOS-NIANTIC section.
2. Run qosmap.py script from "/usr/share/contrail-utils". This python script read the agent.con file and builds a command of qosmap. It hen executes that command which configures the NIC queue scheduling


## **How Qos Scheduling works:**
Please note that when you provision the setup, Queue scheduling gets populated in contrail-vrouter-agent.conf, but the NIC is not programmed with these configurations. 
This is responsibility of user to program the configurations on NIC.

For programming NICs with scheduling related configuration, a utility named "qosmap" can be used. This is the only way provided by us to program NICs. User can use their own ways as well.

There are following ways through which NIC can be programmed:

1. Using qosmap utility directly as a command on compute node.
2. Using a python script named "qosmap.py" kept in "/opt/contrail/utils" which read contrail-vrouter-agent.conf and creates a qosmap command with configured .conf file and run it automatically on that compute node.
3. Using a fab command on cfgm0 which will run "qosmap.py" on all compute nodes of the setup. The advantage of having fab script is:

*      We don’t need to go to each node and run qosmap.py
*      It will take care of keeping the backup of the configurations so that they are restored after compute reboot.

Example of using a qosmap command is as follows:

>       qosmap --set-queue p6p2 --dcbx ieee --bw 0,10,0,20,0,30,0,40 --strict 10101010 --tc 0,1,2,3,4,5,6,7`
>       Priority Operation
>       Interface:                   p6p2
>       DCBX:                        IEEE
>       DCB State:                  Disabled

>                                      P0   P1   P2   P3   P4   P5   P6   P7
>       Traffic Class:                  0    1    2    3    4    5    6    7

>                                     TC0  TC1  TC2  TC3  TC4  TC5  TC6  TC7
>       Priority Group:                 0    1    2    3    4    5    6    7

>                                     PG0  PG1  PG2  PG3  PG4  PG5  PG6  PG7
>       Priority Group Bandwidth:       0   10    0   20    0   30    0   40
>       Strictness:                     1    0    1    0    1    0    1    0

I believe that readers understand the terms "Priority group", "Priority Group Bandwidth" and "Strictness" by now. Please see the above configuration and you can relate why BW is kept 0 where strictness is 1 and why BW sums up to 100. 

Some congestion scenarios and expected output as per the previous example are as follows:

1. If congestion between any queue of PG4 and PG6, queue under PG6 will preempt traffic of queue under PG4 and no drops will be seen in queue under PG6
2. If congestion between any queue of PG4 and PG5, queue under PG4 will preempt all traffic of queue under PG5 and no drops will be seen in queue under PG4.
3. If congestion between any queue of PG3 and PG5, traffic will flow in ratio 20:30 for PG3:PG5. Drops will happen in queues of both PGs.

**Now talking about Priority, TC and Priority Group.**
The hierarchy is that Priority is at the lowest level, then comes traffic class and then Priority group.
See the above output of qosmap command.
Priority P0, P1, P2 etc are user priorities. Ideally, the traffic classification happen based on Priority (say Vlan tag) and it is mapped to corresponding Traffic class.
But, in our case, please note that priority do not hold any significance. We are classifying traffic based on Queue numbers.
So, you can ignore Priority completely.(P0, P1 etc.. , we can ignore)
 
Below in the hierarchy, instead of P0(priority 0) mapping to a traffic class TC0, HW queue 0-7 maps to TC0 in our case. So, the correct statement should be that HW queue 0 to 7 belong to TC0, 8-15 belong to TC1 and so on.
Then, each traffic class or set of traffic classes can map to a single priority group.
 
It means you can have something like this:

>       qosmap --set-queue p6p2 --dcbx cee --pg 1,0,1,2,0,1,2,3 --bw 30,40,20,10 --strict 01010101 --tc 0,1,2,3,4,5,6,7
>       NOTE: Bandwidth specification does not work with strict priority
>       Priority Operation
>       Interface:                   p6p2
>       DCBX:                         CEE
>       DCB State:                  Disabled
>        
>                                      P0   P1   P2   P3   P4   P5   P6   P7
>       Traffic Class:                  0    1    2    3    4    5    6    7
>        
>                                     TC0  TC1  TC2  TC3  TC4  TC5  TC6  TC7
>       Priority Group:                 1    0    1    2    0    1    2    3
>  
>                                     PG0  PG1  PG2  PG3  PG4  PG5  PG6  PG7
>       Priority Group Bandwidth:      30    0   20    0    0    0    0    0
>       Strictness:                     0    1    0    1    0    1    0    1

Note that TC0, TC2 and TC5, all are mapped to PG1.
This means that HW queue 0-7, 16-23 and 40-47, all share same BW and strictness capabilities.
 
Again, we have limitation here also. This configuration(more than 1 TC mapped to single PG) is possible only on CEE mode(which we are not claiming to be supported).
In IEEE mode, as we cannot configure PG(--pg option not supported), we are bound to use 1 to 1 mapping of PG and TC.
Thus, we interchangeably use Traffic class and Priority Group.
Also, with this understanding, using –tc option in “qosmap --set-queue p6p2 --dcbx ieee  --bw 15,5,10,20,5,8,9,10 --strict 00000000 --tc 0,1,2,3,4,5,6,7” does not hold any significance.
Hopefully, it will be removed in future. A bug is there to follow up on this.


## How to test Queue Scheduling:
1. Create at least 2 QosQueue objects using any valid logical id. The 2 logical queues should map to 2 different HW queues.
2. Create 2 FCs and map the QosQueue ID to each FC. (Step 1 and 2 happens together if using Contrail UI)
3. Create a Qos Config and map some dscp/dot1p/exp to the FC1 and FC2 created in step 2.
4. Apply this Qos config on a VMI/ VN/ Policy.
5. Either run qosmap command or fab command or qosmap.py script to configure scheduling on the NIC interface.
6. Send 2 different streams with 10G traffic rate each. Note that stream 1 should classify for entry 1 of Qos config and stream 2 should classify for entry 2 of Qos config. This will create congestion.
7. Use "ethtool -S <interface>" to verify the count of traffic in both queues.
   Alternatively, you can use "tc -s class show dev <interface>" to see the traffic count and drop counts.
   Note the there should not be any drop in strict priority traffic.
   Also, if traffic goes through 2 weighted round robin queues, drop should be observed in both queues and traffic ratio should be same as configured by qosmap utility.


## Limitations of Qos Scheduling:

1. DCB feature supports 2 modes. One is IEEE and other is CEE. We recommend and provide provision to configure Bandwidth and Scheduling values using IEEE mode. User can use CEE mode as well but some limitations are present in that mode which are documented in following bug: https://bugs.launchpad.net/juniperopenstack/+bug/1630865
2. For any NIC interface, if the interface do not support DCB, Qos scheduling configurations do not hold any significance. In that case, user can only take advantage of "Queue mapping" feature.
3. For "Intel based 10G NIC(Niantic)", you will observe 32 queues initially. As soon as you enable dcb on the interface, it shows all 64 queues. Using "qosmap" utility to configure Bandwidth and Scheduling, automatically enables DCB and creates 64 queues.
4. On restart of a compute node, the scheduling configurations are lost if configurations are done directly by using qosmap utility. If we used fab command or qosmap.py to provision the scheduling configurations, it handles these scenarios and scheduling configurations get restored after restart.
5. qosmap utility do not provide with any option to do per queue policing. If the NIC supports per queue scheduling, user can use the NIC API's or any other way to configure the queues. We expect it to work as contrail qosmap is just a configuration tool and do not code any functionality on NIC driver.
6. Queueing and Scheduling will not happen on a Vlan fabric interface. The vlan driver in linux does not support carrying the physical queue mapping to the physical interface from the vlan virtual interface. Please refer to following bug:
https://bugs.launchpad.net/juniperopenstack/+bug/1626406
7. Queueing and Scheduling will not happen on Virtual Functions or SRIOV. Please refer to following bug:
https://bugs.launchpad.net/juniperopenstack/+bug/1633347