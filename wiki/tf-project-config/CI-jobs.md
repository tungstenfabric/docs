## Job
Every job in Zuul consists of three stages - `pre-run`, `run` and `post-run`. As their names suggest, they are run in a particular order and most importantly - separately from each other. Effectively, in case of failures in one of the stages, others will be unaffected - e.g. allowing us to gather logs in `post-run` after `run` fails.
## Adding a project to Zuul
If a project associated with a job is not listed [zuul/main.yaml](https://github.com/Juniper/contrail-project-config/blob/master/zuul/main.yaml) you need to add it first. 

Applying changes to `main.yaml` requires re-running puppet-agent on Zuul node and reloading `zuul-scheduler` for changes to take effect.
## Adding a job
Now it’s necessary to create the required zuul configuration objects: project and job inside the [zuul.d](https://github.com/Juniper/contrail-project-config/tree/master/zuul.d) directory. Project should list the job name under the correct pipeline name (usually `check`). A minimal job stanza contains only a name and it will inherit all the params from the base job.

Changes in the `zuul.d` directory require a reload of the zuul-scheduler service.

## Job definition
We now have to create the ansible scripts that the job will execute: a playbook and a role. By default, zuul launches an ansible playbook of the same name as the job, so a job named `my-job` will execute playbook located at `playbooks/my-job.yaml`.

The playbook references one or more roles located in the `roles` directory, so the playbook listed below will execute the tasks from `roles/my-role/tasks/main.yaml`.

```
- host: ubuntu-xenial-builder
  roles: my-role
```

The `host` value references the node label from the job definition in `zuul.d`.
Changes in the ansible definitions (playbooks and roles) are automatically picked up by the zuul-executor, so there is no need to perform additional actions. 

## External links
For a detailed guide on Zuul's structure, please refer to https://docs.openstack.org/infra/zuul/feature/zuulv3/user/config.html. If you want to see some examples, take a look [here](https://github.com/openstack-infra/zuul-jobs/tree/master/roles).

