### VM doesn't have link-local (169.254.x.x) address upon boot

       1. check on hypervisor 8085/Snh_ItfReq to see if config is missing (i.e. state in ERROR, vn-null etc.)[ eg: http://10.92.249.119:8085/Snh_ItfReq?name= 10.92.249.119 is one of my hypervisor's ip]

       if missing, config has not come from controller

       a. check api-server 8082/virtual-machine-interface/<uuid> if routing_instance_refs are present
          eg: curl -u admin:secret123 http://localhost:8095/virtual-machine-interface/39f49c43-e6fc-471b-ac1d-5cf3c6317221 | python -m json.tool > /tmp/vmis ( Here '39f49c43-e6fc-471b-ac1d-5cf3c6317221' is the interface which we got from step 1. for whom ERROR state was seen)

          if missing,
            a. check if contrail-schema is running on atleast one controller( cmd: contrail-status )
                 if running
                   a. check if VMI present in ifmap on all controllers via 

                          ifmap-view localhost 8443 visual visual | grep <vmi-name>

                        if missing in ifmap,
                          a. check if rabbitmq is clustered fine and all api servers are connected to it.( cmd: rabbitmqctl cluster_status)
                          b. check contrail-api introspect port (8084) for rest/db/messagebus/ifmap traces
                        else
                          a. need to check why contrail-schema didnt establish link between VMI to RI maybe check /var/log/contrail/schema.err
                          b. check 
                              contrail-logs --object-type config --object-values 

                             followed by 

                              contrail-logs --object-type config --object-id <id from above>
                 else
                   a. check last log from contrail to stdout + log file
                   b. check connection status http://<config-node-where-schema-active>:8084/Snh_SandeshUVECacheReq?x=NodeStatus
                                                                                                                                                                                                                                                
### VM doesn't ping the default gateway (subnet gateway)
1. Initiate continuous ping from VM to subnet gateway
2. Find tap interface of VM (TODO a. from contrail UI b. agent introspect)
3. tcpdump -ni `<tap-intf>` - see ICMP requests but no replies received
4. tcpdump -ni pkt0 -X - don't see the packet going to Vrouter-Agent with metadata
5. watch -n1 "dropstats | egrep '[1-9]+'" - observed flow unsable count increases
6. find VRF id for net from introspect (TODO)
7. rt --dump 34 | less observed NH for VJX0 ip is 0 which is discard.
8. Source code check to determine bug in state machine sending from Agent to kernel module.