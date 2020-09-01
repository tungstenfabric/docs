# Code flow

## Start with container specific high level playbook
contrail-ansible-internal code flow start with container specific high level playbooks found right under https://github.com/Juniper/contrail-ansible-internal/tree/master/playbooks. 

For example, code flow for "controller" container start with https://github.com/Juniper/contrail-ansible-internal/blob/master/playbooks/contrail_controller.yml.

```
0 ---
1 - name: "Setup Controller"
2  hosts: contrail-controllers
3
4  pre_tasks:
5    - include_vars: contrail_controller.yml
6      tags: always
7
8  roles:
9    - role: common
10
11    - role: contrail/config
12      tags: [contrail.controller, contrail.config]
13
14    - role: contrail/control
15      tags: [contrail.controller, contrail.controlnode]
16
17    - role: contrail/webui
18      tags: [contrail.controller, contrail.webui]
```

Line #1 Start with a name to the play
Line #2 specify what host/host groups the play (tasks below that line) to be running. "contrail-controllers" are the host group read from the inventory and this play will be executed on all nodes that is found under contrail-controllers.
Line #4 talks about the "pre_tasks" which are list of tasks that run before any other tasks
Line #5 read the variables from contrail_controller.yml found under playbooks/vars/ - this is the file which is updated by contrailctl with the mapped variables from contrailctl configuration files.
Line #6 specify the tag to run this task all the time
Line #8 start list of roles to be included
Line #9 include common role - this role is supposed to have any common tasks which applicable for any other roles - contrail specific or non-contrail specific roles
Line #11 Include contrail/config role which setup contrail config services
Line #14 include contrail/control role which setup contrail control services
Line #17 include contrail/webui role which setup contrail webui services

## Ansible Role
Ansible role is group of reusable ansible code which usually setup one system. Example, ansible-role-nginx setup nginx, ansible-role-cassandra setup cassandra.

Usually a role have below directory structure.

Each below directory contain at least one file named main.yml which ansible can read. Any other files in any of the directories need specifically include from main.yml directly or indirectly.

* defaults/ - This directory contain all the default variables used within the role. These are "defaults" which may be overridden by any other mean - variables from inventory, variables defined using set_fact tasks, any ansible tasks, variables defined in any other var files.
* files/ - this directory contain static files that would be used by copy or any other modules
* handlers/ - this directory contain any handlers. handlers are used to run specific event handlers- usually they are used to restart service after the configuration. Handlers only run once after running all tasks or by explicitly using "meta: flush_handlers" task.
* meta/ - this directory contain metadata about the role such as dependencies of the role. role dependencies will be executed before the role itself. 
* tasks/ - This directory contain actual tasks that perform various operations.
* templates/ - This directory contain jinja2 templates that is processed using "template" module coded within the tasks.
* vars/ - this directory contain the variables that will never be overridden. Usually this directory contain derived variables which never needed to be overridden by any mean. Note that these variables can only be overridden by using "set_fact" task.

### Inputs to the contrail-ansible-internal
All inputs to the container should be handled using contrailctl, so any new variables created within contrail-ansible-internal which would need to be get any user inputs, one would have to create new contrailctl configuration. Along with contrail-ansible-internal change, one will have to add/update sample configuration entries under https://github.com/Juniper/contrail-docker/tree/master/tools/python-contrailctl/examples/configs. Also appropriate schema will have to be added for the configurations https://github.com/Juniper/contrail-docker/tree/master/tools/python-contrailctl/schema.


# Reference
* https://github.com/Juniper/contrail-ansible-internal/wiki/Glossary
* https://github.com/Juniper/contrail-docker/blob/master/specs/contrailctl.md
* https://github.com/Juniper/contrail-ansible-internal/wiki/How-contrailctl-and-contrail-ansible-internal-work-to-deploy-containers%3F
