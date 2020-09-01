![Container startup/contrailctl flow](https://github.com/Juniper/contrail-docker/blob/master/specs/images/contrailctl.jpg "container startup/contrailctl flow")

#### supervisord based containers e.g ubuntu 14.04 based containers
* During container startup, docker will run ENTRYPOINT - which is [/entrypoint.sh](https://github.com/Juniper/contrail-docker/blob/master/docker/analytics/ubuntu14.04/entrypoint.sh)
* /entrypoint.sh first run contrailctl with [configure tag](https://github.com/Juniper/contrail-docker/blob/master/docker/analytics/ubuntu14.04/entrypoint.sh#L35). contrailctl will run ansible-playbook with contrail-ansible-internal which will configure all internal/contrail services but will not start them - especially those services which are under supervisord
* /entrypoint.sh then [run supervisord](https://github.com/Juniper/contrail-docker/blob/master/docker/analytics/ubuntu14.04/entrypoint.sh#L36). This will start supervisord and services managed by supervisord.
* /entrypoint.sh finally [run contrailctl with tags install,provision](https://github.com/Juniper/contrail-docker/blob/master/docker/analytics/ubuntu14.04/entrypoint.sh#L40). This part will make sure internal/contrail services are started and will optionally register them in contrail api

#### systemd based containers e.g ubuntu 16.04
Note: In systemd based system, systemd must be the first process.
 
* During container startup, docker will run ENTRYPOINT which is systemd
* During container image creation, one systemd service is created for contrailctl execution, and thus systemd start [contrailctl with tags configure, service, provision](https://github.com/Juniper/contrail-ansible-internal/blob/master/playbooks/roles/contrail/analytics/files/systemd/contrail-ansible.service). Then contrailctl will run ansible-playbook with contrail-ansible-internal which will configure internal/contrail services, start them, and register them to contrail-api.
