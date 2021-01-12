# Node Memory and CPU Information

 

To help in monitoring and debugging, the following statistics have been
added for all node types. The statistics are updated every 60 seconds.

-   System CPU info

-   System memory and CPU usage

-   Memory and CPU usage of all processes

You can see a current sample from the UVE in your system at:

`http://<analytics-ip>:8081/analytics/uves/<node-type>/<hostname>?flat `

You can also use the statistics tables to get historical data with all
supported aggregations, such as SUM, AVG, and so on:

-   `NodeStatus.process_mem_cpu_usage`

-   `NodeStatus.system_mem_cpu_usage`

The schema for the tables are at the following locations on your system:

` http://<analytics-ip>:8081/analytics/table/StatTable.NodeStatus.process_mem_cpu_usage/schema`

`http://<analytics-ip>:8081/analytics/table/StatTable.NodeStatus.system_mem_cpu_usage/schema`

 
