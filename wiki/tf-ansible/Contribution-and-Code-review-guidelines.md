# Contribution and Code review guidelines

* All patches to this repo should be added as pull requests.
* Patches should be submitted as granular chunks which should affect single role. i.e no patch is should have code changes in config role and control role unless it is really required.
* All pull request should have a label[s] attached to it which should talk about what role[s] is affected. The idea here is that all deployment code which affect those roles *MUST BE* reviewed by individual module owners i.e individual role team. For example, a pull request that affect config role must be reviewed and possibly merged by members/experts from contrail-config team.
* Any communication/comments should be added as comments in the pull requests.
* Pull request comment, commit message should have a description that match the change
* Always run ansible-lint against site.yml and try to correct any lint errors. 
  * Install ansible-lint using "pip2 install ansible-lint"
  * Run it using "ansible-lint site.yml"
  * Please check https://github.com/willthames/ansible-lint for more information
* Always test locally before push a change as we still don't have a ci system in place.

Note: This is a draft, the contents in this document supposed to be changed.