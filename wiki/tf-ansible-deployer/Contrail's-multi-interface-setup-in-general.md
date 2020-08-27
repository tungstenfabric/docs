**Terminology:**

* Control/Data network (CTRL/DATA) - network for data traffic of workload and for control traffic between compute nodes and control services.
* API network - network where API services are listening on.
* Management network (MGMT) - network for accessing instances.

If API and MGMT are the same network then **API** will be used for describing.

**Example:**

In order to setup Contrail in multi-interface environment you need to provide IP-s for all networks.
For multi-interface setup it's very important to specify CONTROL_NODES list.
If you have all services (config, control, analytics, webui, rabbitmq, databases, ...) located on the same instance then only CONTROLLER_NODES and CONTROL_NODES must be set. If services are located on different instances then appropriate variable *_NODES must be set.

```
instances:
  server1:
    provider: bms
    # here is MGMT IP
    ip: 10.0.0.1
contrail_configuration:
  # here is API IP
  CONTROLLER_NODES: 172.16.0.1
  # here is CTRL/DATA IP
  CONTROL_NODES: 192.168.0.1
```

PHYSICAL_INTERFACE can be omitted in configuration. It will be derived inside each instance of vrouter-agent by evaluating the network path to IP-s from CONTROL_NODES list.

