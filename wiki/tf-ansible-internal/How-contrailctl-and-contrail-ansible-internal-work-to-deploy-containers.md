![Container startup/contrailctl flow](https://github.com/Juniper/contrail-docker/blob/master/specs/images/contrailctl.jpg "container startup/contrailctl flow")

contrailctl is called during container startup to do initial configuration, service management etc and may be called later when contrailctl configuration found under /etc/contrailctl of the host is updated.

Here are the steps it go through on contrailctl execution
* contrailctl read appropriate contrailctl configuration for that container - e.g /etc/contrailctl/controller.conf for controller container.
* contrailctl map configuration entries to ansible variables and write it to /contrail-ansible-internal/playbooks/vars/contrail_<component>.yml (e.g playbooks/vars/contrail_controller.yml for controller)
* contrailctl to call ansible-playbook with appropriate playbook from /contrail-ansible-internal/playbooks/contrail_<component>.yml - e.g playbooks/contrail_controller.yml for controller.
* Ansible to setup all internal service configurations, and start/restart services as required and then optionally register required components to config api

### How contrailctl map configuration entries to ansible vars.
contrailctl is mapping contrailctl configuration entries to ansible vars which will be used by ansible code to write internal service configurations.

contrailctl configuration file[s] has below kind of sections
* GLOBAL - global section - all configurations that are applicable globally to all components will go here - configurations like contrailler_list, analytics_list etc will go here.
* section name which is same as contrail containerized component (controller, analytics, analyticsdb, agent etc):-  This will act as global configurations for mulitple services within that container - e.g below configuration "vrouter_physical_interface" is global config but only for agent container.
  ```
  [AGENT]
  vrouter_physical_interface = eth0
  ```
* Other sections - there are number of sections mostly named after different internal service names like [RABBITMQ], [CONFIG], [CONTROL], [WEBUI] etc.

#### Mapping global configurations
All global configurations (configs under [GLOBAL] and section named after container name) is directly write to ansible vars. Example

```
[GLOBAL]
controller_list = ["192.168.0.10", "192.168.0.11", "192.168.0.12"]
analytics_list = ["192.168.0.10", "192.168.0.11", "192.168.0.12"]

[AGENT]
vrouter_physical_interface = eth0
compile_vrouter_module = False
```
Above config entries will make below ansible variables

```
controller_list: ["192.168.0.10", "192.168.0.11", "192.168.0.12"]
analytics_list: ["192.168.0.10", "192.168.0.11", "192.168.0.12"]
vrouter_physical_interface: eth0
compile_vrouter_module: false
```
#### Mapping non-global configurations to ansible variables
Non-global configurations are mapped to ansible vars by prepending section name to variable name to make sure their uniqueness - i.e WEBUI.http_listen_port will be mapped to ansible variable webui_http_listen_port, KEYSOTNE.version will be mapped to keystone_version ansible variable.

```
[KEYSTONE]
ip = 192.168.0.20
version = v2.0
admin_port = 35357

[CASSANDRA]
data_dirs = ["/var/lib/cassandra/data"]
java_max_heap_size = 512M

[WEBUI]
http_listen_port = 8085
``` 
Above config entries will make below ansible variables

```
keystone_ip: 192.168.0.20
keystone_version: v2.0
keystone_admin_port: 35357
cassandra_data_dirs: ["/var/lib/cassandra/data"]
cassandra_java_max_heap_size: 512M
webui_http_listen_port: 8085
```
