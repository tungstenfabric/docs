# Ansible
* tags:- ansible tags are used to run specific tasks without running whole playbook. Any tasks can be tagged with any arbitrary string which can be used with "-t <comma separated tag list>" with ansible-playbook to run specific part of the playbook. Special tag is "always" which run always. Reference: http://docs.ansible.com/ansible/playbooks_tags.html
* role:- ansible role is group of reusable ansible code which usually setup one system. Example, ansible-role-nginx setup nginx, ansible-role-cassandra setup cassandra.

