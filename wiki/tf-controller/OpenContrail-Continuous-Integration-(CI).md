OpenContrail CI is now live. All commits to contrail-controller git repo will now have to go through CI. This process is very similar to [OpenStack](https://wiki.openstack.org/wiki/Gerrit_Workflow)'s. Pull requests are not longer used for contrail-controller git repo. Necessary .gitreview files are already in place in the repos that are administered through this CI infrastructure.

[Presentation Slides](https://github.com/Juniper/contrail-infra-config/blob/master/setup/OpenContrailCI.pptx)

[CI Project Status](https://github.com/Juniper/contrail-infra-config/blob/master/contrail-ci-todo.txt)

[CI Related Bugs](https://bugs.launchpad.net/juniperopenstack/+bugs?field.searchtext=&orderby=-importance&field.status%3Alist=NEW&field.status%3Alist=CONFIRMED&field.status%3Alist=TRIAGED&field.status%3Alist=INPROGRESS&field.status%3Alist=INCOMPLETE_WITH_RESPONSE&field.status%3Alist=INCOMPLETE_WITHOUT_RESPONSE&assignee_option=any&field.assignee=&field.bug_reporter=&field.bug_commenter=&field.subscriber=&field.structural_subscriber=&field.tag=ci+&field.tags_combinator=ANY&field.has_cve.used=&field.omit_dupes.used=&field.omit_dupes=on&field.affects_me.used=&field.has_patch.used=&field.has_branches.used=&field.has_branches=on&field.has_no_branches.used=&field.has_no_branches=on&field.has_blueprints.used=&field.has_blueprints=on&field.has_no_blueprints.used=&field.has_no_blueprints=on&search=Search)

In order to use the new system, you need to 

1. Login to [review](https://review.opencontrail.org) using your launchpad open id
2. Goto settings and 
    1. Select unique user name (STEP USER)
    2. Select (add if necessary) preferred email address to be same as the one used in your [github] (github.com/Junuper) and launch-pad
3. Add your ssh public keys

### Code review process
1. ```repo init, repo sync ``` etc.
2. ``` cd controller ``` (e.g.)
3. ```git review -s ```(Only required, when you need to do 'git review' for the first time in this git repo)
       It asks for username. You must use the one setup in STEP USER step above (at review.opencontrail.org)
       If keys are correct, it setups a remote named gerrit in your git config
       git-hooks are setup to generate unique change-id with each commit
4. Create a branch e.g. ```git checkout -b bugfix github/master``` (tracking github/master at github.com/juniper/...)
5. Make your changes
6. ``` git commit ``` and provide commit message (This has to be done, after git review -s is successfully complete only)
    Closes-Bug: #1234567 -- use 'Closes-Bug' if the commit is intended to fully fix and close the bug being referenced.

    Partial-Bug: #1234567 -- use 'Partial-Bug' if the commit is only a partial fix and more work is needed.

    Related-Bug: #1234567 -- use 'Related-Bug' if the commit is merely related to the referenced bug.

    Please add a bug id with the right keyword to your commit message on a separate line and gerrit will create a link to the correct bugid(s).

7. If necessary: ``` apt-get -y install git-review ``` (or ```yum -y install git-review```)
     Please see [this](https://bugs.launchpad.net/git-review/+bug/1337701) if you get a pkg_resources.DistributionNotFound error
8. To backup your changes in your private repo (optional)
     Fork off [Juniper/contrail-controller] (github.com/Juniper/contrail-controller) into your private repo at github.com
     ``` git remote-add <ur-private-repo>```
     ``` git push <ur-private-repo> bugfix ```
9. run ```git review``` Check that review is uploaded [here](https://review.opencontrail.org/#/q/status:open,n,z).

First time when you run ```git review```, it asks for the user name. Please use the same that you used in step USER above. But you should do ```git review -s``` first, which does the setup.

If works correctly, a review entry is created in [review server](review.opencontrail.org) Jenkins jobs are run to verify your changes. Jenkins master can be accessed at [jenkins](jenkins.opencontrail.org)

Some one should review and (optionally some one else) must approve the changes. If jenkins job verification also succeeds, the changes get automatically merged and pushed out to [github repo](github.com/Juniper/contrail-controller)

For certain release branches such as R1.10, review entry can only be approved by the release team. Please send email to ci-admin@opencontrail.org in such cases describing your case and requesting for approval.

## Interdependent changes across different projects (git repos)
If you have changes spread across different git repos, then CI cannot handle it, as it does so with only one git repo at a time. However, if you analyze carefully and submit smartly, you can feed changes to CI one at a time, with independent changes going in first, followed by dependent changes after the former gets merged.

To break mutual dependency in packaging rpms with other repos, you can place this in the spec file temporarily "%define _unpackaged_files_terminate_build 0" (And later remove it after the changes get merged with a new review entry)

If that is not feasible, please follow this process.

* **Please make sure that all new, modified and deleted files are add/deleted to/from git before git commit**
* Commit your changes and do 'git review' for all the change sets necessary.
* Get your changes reviewed and approved
* Stand alone changes, which does not break (build and tests) automatically will get merged via the usual CI process
* Run single node sanity tests "fab [run_sanity:ci_sanity](https://github.com/Juniper/contrail-test/blob/master/scripts/ci_sanity_suite.py)" using your image in both centos and in ubuntu (External to Juniper folks can request assistance from ci-admin@opencontrail.org for this part)
* Email the test results URL and all review entry URLs to ci-admin@opencontrail.org with a request to merge the changes
* For controller project, one has to run and send "scons test" and (BUILD_ONLY=TRUE scons flaky-test) command output as well. (exit code must be 0 for both). (preferable to start with 'rm -rf $SANDBOX/build')
* If some dependent commits are in git-repos which are **not in CI**, corresponding **pull request URLs must also be present** (for admin to merge at the right time)
* CI Team can then do the needful to get the changes merged together.

IOW, we follow what CI is doing for all other independent commits, thus keeping the build sane.

## CI Jobs failure debugging

When ever a CI job fails, some of sort of debugging is required. If the failure is due to bugs/failures in CI infrastructure, CI team usually monitors and takes necessary action (such as jobs restart). Otherwise, following steps are recommended.

1. Look at the job console output. Link to this is logged in the review entry and can be found in its audit trial.
[Successful log example] (https://jenkins.opencontrail.org/job/ci-contrail-controller-systest/2248/console)
[Failure log example] (https://jenkins.opencontrail.org/job/ci-contrail-controller-unittest/2223/console)

2. If the trailing end of the console output does not given enough clue, please look at the entire console log (link at the beginning of the console tail output summary url)

3. For failed builds, contents of VM system config and log dirs are collected: /var/log; /etc; /opt/contrail/utils; and /root/contrail-test/logs. These are made available in the *userContent* area of jenkins.opencontrail.org and can be accessed via browser. The general format is:  
    `http://jenkins.opencontrail.org/userContent/$JOB_NAME/$JOB_NUM`  
The actual location will appear very close to the bottom of the console log. Look for the string *VM system log files*. Here is an example from the console log of a failed systest run on ubuntu12 :  
`2015-03-17 13:52:07 VM system log files: http://jenkins.opencontrail.org/userContent/ci-contrail-fabric-utils-systest-ubuntu-precise-pangolin-havana/1055`

3. If it is build issue such as compiler error, the error as reported by the compiler is logged in the console. Using line number, error message, etc. usually the root cause can be found and fixed. In that case, please resubmit the fix as additional patch the same review entry ```(git commit --amend . and git review)```

4. If is is CI infra issue (say due to a flaky job), you can inform ci-admin@opencontrail.org optionally, flip the job (by adding "recheck no bug" comment to the review entry) or simply wait for the admin team to take necessary action

5. contrail-install-* image built is now archived in ubuntu-build02, e.g. /ci-admin/systest-images/2720,1/ci-contrail-packages-systest-ubuntu-precise-pangolin-havana/contrail-install-packages_1.20-4362~havana_all.deb
If a job fails when running the image, one can load this image for testing in private environments.
Note: This is only available for folks inside Juniper Networks. Also, if the job is flipped, this image is fetched and the tests are run (instead of rebuilding the image from scratch). This helps to expedite the jobs completion upon retries. However if for any reason, image needs to be rebuilt, one can do so by uploading a new patch.

6. If the issue cannot be figured out and further need to be debugged
  -- If internal to Juniper networks, 
        log on to the slave VM and debug in the sandbox
```
        touch /root/ci_job_wait # to stop the job from exiting.., 
        service slave_start stop # To stop new jobs from getting scheduled which wipes out the build sandbox).
```
        When _done_ with debugging..
```
            rm /root/ci_job_wait
            service slave_start start # To place the VM goes back into the pool to start serving new jobs.
```

  -- If outside juniper, please email to ci-admin@opencontrail.org

## FAQ

1. **Cannot git commit due to "missing change-id message"..**

    All commits must happen after git-review is issued one time (which sets up git-review git-commit hooks) to generate change-ids for each commit. cheery-pick from older direct commits are not allowed. In such cases, the diff can be patched and committed again (e.g. git show <commit-id> | patch -p1; git commit -m "commit msg" .;)

2. **Review entry is struck, what to do ?**

    Some times, zuul, the queue manager loses track of a review entry. In that case, one should abandon and restore the change again to feed the review entry back into the pipeline. Fresh tests are triggered, upon completion of which, changes would get merged upstream (provided review and approvals are complete)

3. **How to submit a patch to an already submitted entry ?**

    Please see OpenStack documentation. In short, checkout the previous entry changes (```git review --download <review-entry-id>```, make changes, ```git commit --amend```, and ```git review``` again).  If the sandbox and branch where the original changes were made is still available, the first step (i.e. git review --download) can be skipped. Note that git-review fails if the change has been abandoned.

4. **How long does it take for the tests to complete ?**

    At the moment, it takes 4 to 5 hours. Work is in progress to speed this up, while at the same time add additional tests that run in parallel.

5. **How to flip a job so that jobs are restarted**

    Either add a comment "recheck no bug" or "Abandon and Restore" review entry. 

6. **Cannot 'approve' review entries in certain branches such as R.10**

    Commits to release branches are now selectively throttled. Please send email to ci-admin@opencontrail.org describing your case, to get necessary approval

7. **How to backport already merged change (which would be in github.com/...) to a different branch**

    Checkout a new branch of the desired target branch, cherry-pick the commit and do git-review. e.g. for R2.1
    ```
git fetch github # Get latest code off github for all branches
git checkout -b R2.1 github/R2.1 # Checkout a new branch off remote R2.1 branch
git cherry-pick <desired-commit>  # Cherry-pick the desired commit
git review # Submit for git review
    ```

8. **How to submit inter dependent changes spread across different git repos**
  
    Please see [above] (https://github.com/Juniper/contrail-controller/wiki/OpenContrail-Continuous-Integration-(CI)#interdependent-changes-across-different-projects-git-repos)

	e.g. Steps to clone a git repo off your private fork ("rombie" in this e.g.) and submit changes to review for contrail-packaging project to R1.10 branch.

    ```
    git clone git@github.com:rombie/contrail-controller.git contrail-controller            
    cd contrail-controller                                                                    
    git remote add github git@github.com:Juniper/contrail-controller                         
    git fetch github
    git checkout -b R1.10 github/R1.10
    git review -s
       <Use the same user name that is selected in review.opencontrail.org>
    <make your changes>
    git commit -m "msg" .
    git push rombie R1.10
      Optionally (to backup), push your changes to your private repo
    git review      
      Submit changes to review.opencontrail.org                           
    ```
For all other questions, please email to [ci-admin](mailto:ci-admin@opencontrail.org)

Thank you.

OpenContrail-CI-Team

[ci-admin only wiki](https://junipernetworks.sharepoint.com/teams/mvp/Contrail/Contrail%20Wiki/Contrail%20CI.aspx)