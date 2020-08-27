### Adding a new compute node
* To add a new compute node in contrail API server (commission it from contrail point-of-view), do the following on any contrail controller:

    ``
    python /opt/contrail/utils/provision_vrouter.py --host_name <compute-host-name> --host_ip <compute-host-ip> --api_server_ip <api-server ip or name>
    ``

### Removing a new compute node
* To remove an old compute node in contrail API server (de-commission it from contrail point-of-view), do the following on any contrail controller:

    ``
    python /opt/contrail/utils/provision_vrouter.py --oper del --host_name <compute-host-name> --host_ip <compute-host-ip> --api_server_ip <api-server ip or name>
    ``