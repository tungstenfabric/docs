# Cassandra Maintenance Scripts

## Problem Statement
In a cassandra cluster where deletes are performed, anti-entropy repair needs to be run periodically for maintenance and specially in cases where nodes go down and come back up to prevent deleted data from showing up again. Deleted data can show up again in the following cases:
1. Network partition lasting more than `gc_grace_seconds`, followed by node re-joining the cluster
2. Node being down more than `gc_grace_seconds`, followed by node re-joining the cluster
Anti-entropy repair is performed by running the `nodetool repair` command

## Implementation
### Assumptions
* `gc_grace_seconds` is set to default of 10 days
* `hinted_handoff` time is set to default of 3 hours
* `nodetool repair` needs to be run with the `-pr` option when running it periodically so that no coordination to not run `nodetool repair` in parallel across nodes is needed.

### Details
Two scripts are developed:
* `contrail-cassandra-status`
* `contrail-cassandra-repair`

To handle case 1, we will run `nodetool status` every minute and if the local node is not determined to be up for greater than 90% of `gc_grace_seconds`, then cassandra will be be stopped. To achieve this, we have written a python script - `contrail-cassandra-status.py` and it will be run periodically every minute via the nodemgr. The script will do the following:
1. Run `nodetool status` and if the self node status is up in the output and the cluster is not partitioned, then it will touch a file `/var/log/cassandra/status-up`
2. Cluster being partitioned is determined by checking that at least half plus one of the cluster nodes are up. Assumption here is that the replication factor used by the config keyspaces is equal to the number of cluster nodes 
3. If the self node is determined to be down (either because the `nodetool status` shows the node to be down or the cluster is partitioned) then it will determine the difference between the current time and the time the file `/var/log/cassandra/status-up` file was last modified and issue `service contrail-database stop` if the time is greater than `gc_grace_seconds`

To handle case 2, we need to determine the difference between current time and the last reboot/shutdown time and if it is greater than 90% of `gc_grace_seconds`, then cassandra should not be started. To achieve this, we have created a wrapper init.d service file called contrail-database. 
1. When user issues `service contrail-database start`, it will first determine the difference between the current time and the time the file `/var/log/cassandra/status-up` file was last modified and if the time is greater than 90% `gc_grace_seconds`, then it will return with error. 
2. If the difference is greater than 90% of `hinted_handoff` time but less than 90% `gc_grace_seconds` it will forward the start request to the cassandra init.d service and then invoke the `contrail-cassandra-repair` to run a `nodetool repair` on the config keyspaces
3. If difference is less than 90% of `hinted_handoff` time, it will forward the start request to the cassandra init.d service.

`contrail-cassandra-repair.py` script will be invoked to perform periodic `nodetool repair -pr` from nodemgr every 24 hours by default. Currently there does not seem to be a way to find out if a repair is already running on the cassandra node for a keyspace. Hence we will create a file `/var/log/cassandra/repair-<keyspace>-running` file before running `nodetool repair -pr` on all the config keyspaces. We will log the start time and the end time of repair in /`var/log/cassandra/repair-<keyspace-name>.log` and remove the `/var/log/cassandra/repair-<keyspace>-running` file once the repair is done.


### Testing
The above two scenarios mentioned in the problem statement need to be tested.
1. Test 1 - Network partition, on 3 database node, bring down the cassandra gossip port using `nodetool/iptables`. Verify that cassandra is stopped after 90% of `gc_grace_seconds`
2. Test 2 - Node down, bring node down for greater than 90% of `gc_grace_seconds`, verify that when node comes up, cassandra is not started
3. Test 3 - Node down, bring node down for greater than 90 % of hinted handoff but less than 90% of `gc_grace_seconds`, verify that when node comes up, cassandra is started and nodetool repair is run
4. Test 4 - Node down, bring node down for less than 90% of hinted handoff and verify that when node comes up, cassandra is started
5. Test 5 - Cluster reboot, verify that on cluster reboot, cassandra is started on all nodes and cluster is formed