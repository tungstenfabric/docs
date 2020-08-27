### Problem Summary:
 
1. Zookeeper was down because it did not have quorum.
2. RabbitMQ DB was corrupted.
3. Docker service was corrupt on 2nd controller due to which containers were not coming up.
 
### Problem resolution:
 
1.  	Zookeeper issue
We looked at the zookeeper logs and saw that there was no quorum as other two controllers were down. We recovered from this issue by bringing up the other controllers.
 
2.  	RabbitMQ issue
We noticed that RabbitMQ DB was corrupted. We recovered it using the following steps on all three nodes.
 
Logged on to controller docker container using following command:
docker exec -it controller bash
 
Cleared the rabbitMQ DB by delete the following directory.
rm -rf /var/lib/rabbitmq/mnesia/
 
Restarted RabbitMQ using the following two commands:
service rabbitmq-server stop
epmd –kill
service rabbitmq-server start
 
Checked RabbitMQ cluster status using:
rabbitmqctl cluster_status
rabbitmqctl status
    	
Checked contrail status using:
contrail-status
 
3.  	Docker Service corrupted
On Node 2, we also noticed that docker service was corrupted. To recover from this using the following steps on Node2.
 
We first stopped both the other docker containers running on Node2, namely: analytics and analyticsdb. Using the following command:
docker stop analytics
docker stop analyticsdb
 
Following the confirmation that all three dockers were stopped, we tried to restart the docker service using:
service docker restart
 
But this command failed again, hence we rebooted the entire Node 2 to recover from this.
 
 
### Root cause of the issue:
 
Because of the RabbitMQ being down, API server was not coming up which lead to restarts of the controller container. Since controller container was down, there were not enough nodes for the Zookeeper to reach a quorum.  This was resolved after clearing the RabbitMQ DB and restarting it.
 
Although we couldn’t accurately determine the cause of the RabbitMQ going down, it could be due to Network Partitioning in RabbitMQ cluster.  
