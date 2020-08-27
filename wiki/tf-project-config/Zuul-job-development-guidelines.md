1. Avoid placing tasks in playbooks, include roles instead
1. Role naming:
   * roles that are used to transfer data to the zuul-executor (logs, artifacts, etc.) should be named `fetch-*` 
1. when the job requires source tree prepared by android repo, you should use the `contrail-vnc-base` base job
  * in this case, the repo root will be located in `{{ ansible_env.HOME }}/contrail-5.0`
1. when the job requires a regular (flat) source tree checkout, use `contrail-src-base` base job.
  * in this case, the location of zuul-merger prepared code should be specified as `{{ ansible_env.HOME }}/src/{{ zuul.project.canonical_hostname }}`, for example `/home/zuul/src/review.opencontrail.org/Juniper/contrail-controller`