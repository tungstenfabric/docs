#Overview  
OpenContrail supports Health Check Service in **R3.0** and onwards. It runs and monitors liveliness of a service provided by a Virtual Machine by configured method (HTTP/PING). Once it finds out that the service provided by the Virtual Machine is not available anymore it ends up removing the routes for the Virtual Machine, thus disable forwarding packets to it.  
Currently Health Check can only use two methods/protocols HTTP and PING.  
#Configuration Model  
following figure depicts the configuration model used in the system  
HealthCheck Object has the following properties associated to it  
>  
      - enabled            
      - monitor-type     # Health Check protocol type to be used (HTTP/PING)  
      - delay            # delay between two health check attempts  
      - timeout          # timeout for single health check attempt  
      - max-retries      # number of retries to attempt before declaring a failure  
      - http-method      # HTTP method valid only for monitor-type(HTTP) (currently not supported)  
      - url-path         # url string for HTTP, destination IP for all other cases    
      - expected-codes   # expected exit codes (currently not supported)  
>  
  
HeathCheck Object can be linked to multiple Virtual Machine Interfaces and a Virtual Machine Interface at the same time can also have association to Multiple Health Check Objects  
>  
    HealthCheckObject 1 ---------------- VirtualMachineInterface 1 ---------------- HealthCheckObject 2   
          |  
          |  
    VirtualMachineInterface 2 
>  
  
#Configuration  
Create Virtual Machine from horizon UI, then using REST API or Contrail UI(currently not available) Create Health Check Object defining above mentioned properties and add link to the Virtual Machine Interface of the already created Virtual Machine  
  
#Contrail Vrouter Agent
Contrail Vrouter Agent is responsible for providing health check service. It spawns a python script to monitor status of a service hosted on a **Virtual Machine on the same compute node**, which updates status back to vrouter agent. Vrouter agent acts on the status provided by the script to withdraw/restore the exported interface routes. It is also responsible for providing a LinkLocal Metadata IP for allowing script to communicate with the destination IP from the underlay network using appropriate NAT translations.  
In a running system this information is displayed in vrouter agent introspect under  
http://\<compute-node-ip\>:8085/Snh_HealthCheckSandeshReq?uuid=  
  
#Caveats  
Running Health Check Entries need to create flow entries to do translation from underlay to overlay, so in a heavily loaded scenario where flow table is full it may observe false failures.  
  