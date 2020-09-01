Contrailctl is configured with per container configuration files kept under /etc/contrailctl. This directory (/etc/contrailctl) is available on the host and is then mounted to the containers to make it available to them. So one can just edit appropriate container spcific config file found under /etc/contrailctl of the host and run contrailctl config sync within the container to get the configurations synced.

One may refer [contrailctl configuration samples](https://github.com/Juniper/contrail-docker/tree/master/tools/python-contrailctl/examples/configs) for all configurations available at this moment.

Also refer [contrailctl spec document](https://github.com/Juniper/contrail-docker/blob/master/specs/contrailctl.md) for more details on contrailctl and its internals