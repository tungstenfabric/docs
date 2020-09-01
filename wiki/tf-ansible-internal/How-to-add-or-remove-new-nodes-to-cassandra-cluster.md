# Add node to existing cassandra cluster
## Step 1: Configure new cassandra node with seed list
* Edit /etc/cassandra/cassandra.yml and add configuration "seeds" with comma separated list of existing nodes in the cluster
* start cassandra service on new node

## Step 2: Run nodetool cleanup
After all new nodes are running, run nodetool cleanup on each of the previously existing nodes to remove the keys that no longer belong to those nodes. Wait for cleanup to complete on one node before running nodetool cleanup on the next node.

(Need a confirmation to confirm if step #2 is required)

# Remove node from existing cassandra cluster
TBC

# Reference
* http://docs.datastax.com/en/archived/cassandra/2.2/cassandra/operations/opsAddNodeToCluster.html?hl=add%2Cnew%2Cnode
* https://docs.datastax.com/en/cassandra/2.1/cassandra/operations/opsRemoveNode.html
