## Launchpad bug management
Contrail project related issues and releases are managed through Launchpad on [JuniperOpenstack](https://launchpad.net/juniperopenstack) project. Launchpad, while being pretty powerful lacks few desired features around searching and assigning bugs, so few rules need to be followed to make it easier to manage lifecycle of bugs in launchpad to make it easier to track bugs and releases.


##### Series & milestones:
Contrail release schedules and branch information is maintained on [Launchpad](https://launchpad.net/juniperopenstack/+series). All major Contrail release is done on its own throttle branch which is called '_series_' on Launchpad. The code consists of multiple git repostiory maintainted on [github](https://github.com/orgs/Juniper/dashboard). Corresponding to each series on Launchpad, there exists a branch with the same name on github repos.

On each throttle branch (aka 'series' in launchpad), in general we do multiple maintenance releases for contrail software. Each maintenance release is represented on Launhcpad as '_milestone_'. When we do official releases, we mark the 'milestone' as 'released' on Launchpad. E,g., [r2.0](https://launchpad.net/juniperopenstack/r2.0/r2.0-fcs). Snapshot from release timeline page is below:

!['series' & 'milestone](https://github.com/aranjan7/contrail-misc/blob/master/images/series.png).

##### Bugs scopes and milestones:
It is a requirement to create bugs in Contrail project with correct 'scope'. 'Scope' is the 'series' (aka branch) on which the bug was found. The 'branch' could be actual git branch or 'trunk' its found on builds off master git repo.

If the bug was found on mainline trunk, the scope needs to be set to 'trunk'. Bugs 'must' be created with correct scope. Scopes are not created by default, so one must create it explicitly even if the bug was found on mainline trunk.

For each scope the '_milestone_' must be set as next release on that '_series_'. In general this is the upcomping '_milestone_' for the release. e.g., in above snapshot its 'r2.30' for 'trunk' series. If you are not clear on current milestone, please send an email to [dev alias](mailto:dev@lists.opencontrail.org?subject=current%20milestone&body=Let%20me%20know%20the%20current%20milestone%20for%20mainline%20bugs.). In case 'scope' is for throttle branch, the 'milestone' must be set to next upcoming maintenance release on the 'series'. e.g., per above snapshot current active milestone for r2.1 series is r2.11 or r2.12 as you may be targeting the fix towards. It must not be set to r2.10 or anything else on other series. The current milestone for a given series can be determined from this [timeline](https://launchpad.net/juniperopenstack/+series "Click to go to release timeline chart").

Example of bugs with **correct** scopes:
![Correct bug](https://github.com/aranjan7/contrail-misc/blob/master/images/bug-scope1.png)

Example of bugs with **incorrect** scopes: 
Here the 'series' for 'trunk' is not created and 'milestone' is also missing. Without 'milestone' its not clear which release onwards the fix exists or if we forgot to commit code on master.
![Incorrect bug](https://github.com/aranjan7/contrail-misc/blob/master/images/bug-scope-incorrect.png)

As part of bug scrub and release cycle, unresolved bugs will be prioritized to future releases and 'milestone' field will be updated accordingly.

##### Tags:
Each bug should at least contain one 'official tag' depending on the component of software the bug belongs to. E.g., bugs in vrouter needs to have 'vrouter' tag. List of 'official tags' is on right side [on this page](https://bugs.launchpad.net/juniperopenstack).

One can put extra tags on the bug for better bug management. Such tags may or may not be from the official list. A bug can have any number of tags.

##### Public vs Private bugs:
As a policy all Contrail bugs should be in public. Only exceptions are bugs which has reference to Juniper customers. They MUST be private. When you create a bug, pl make this judgement yourself, without defering this to bug admin. By default the bugs are created as private, so please mark it public once you create the bug (and create appropriate scope(s)). You can mark the bug public by clicking URL on top right as shown below.

![Set public bugs](https://github.com/aranjan7/contrail-misc/blob/master/images/public-bug.png)

Private bugs can be shared with select Launchpad members, or bug creator could opt to be notified. To do this 'subscribe' to the bug as below. If there is 'group' which needs to be notified, the organization/team should create a 'launchpad team' and that team can be added in bug notification list. This 'team' can be independently managed by their 'team owners'. 
![sharing bugs](https://github.com/aranjan7/contrail-misc/blob/master/images/subs.png)

##### Bug query:
Bugs on this project can be queried based on tag and status [in advanced search](https://bugs.launchpad.net/juniperopenstack/+bugs?advanced=1) page. If a fix for the bug is merged by CI, appropriate milestone will be set automatically. One can manually set the milestone as well, if you want to specifically target a bug to a given release.

On a given release all the pending/fixed bugs can be found by clicking on the '_milestone_'. E,g., for r2.11 milestone on r2.1 series all the bugs are: [https://launchpad.net/juniperopenstack/+milestone/r2.11](https://launchpad.net/juniperopenstack/+milestone/r2.11)



