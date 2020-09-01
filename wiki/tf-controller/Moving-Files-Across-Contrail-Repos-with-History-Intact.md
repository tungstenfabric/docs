# [How To](https://stosb.com/blog/retaining-history-when-moving-files-across-repositories-in-git/)
The procedure to move files across repos is outlined at [stosb](https://stosb.com/blog/retaining-history-when-moving-files-across-repositories-in-git/). Fundamentally, any file or directory move (across repos) must be viewed as a sequence of two steps: repo split followed by repo merge (of one of the split-parts with the destination repo). A repo is split into two, and one of the split-parts that requires to be moved is merged with destination repo. In instances where entire source repo is merged with a destination repo, skip the split aspect and proceed to the merge step (However, most of the times it may not always be the case, one of the reasons is listed below). 

[A simple “git mv” does not preserve git-history](https://git.wiki.kernel.org/index.php/GitFaq#Why_does_Git_not_.22track.22_renames.3F), and requires in some instances ‘git log’ command be given a –follow option etc., and gives an incorrect impression that "git mv" can preserve history. [A quote from Stackoverflow](https://stackoverflow.com/questions/2314652/is-it-possible-to-move-rename-files-in-git-and-maintain-their-history): It is really annoying that so many people have mindlessly repeated the statement that git automatically tracks moves. Git does no such thing. [By design(!) Git does not track moves at all](https://git.wiki.kernel.org/index.php/GitFaq#Why_does_Git_not_.22track.22_renames.3F).  

Whenever a repo (a source repo) is merged with a destination repo, all the contents of the source repo are spit (or spewed) into the root directory of the destination repo. In most instances, it is not the desired directory structure. One cannot rely on ‘git mv’ to preserve history for the reasons listed above. As a result, one will have to split the source repo into two repos, a desired part and the other, and merge the desired part of the repo with destination repo (while enforcing a desired directory structure). One may end up repeating this process (once per each directory that needs to be moved from the source repo) because of desired directory layout in the destination repo. Once split, the source repo is unusable (the set of git commands invoked to achieve the split make the repo unusable for further splits), hence mandates that a fresh repo be pulled for every repetition (that would merge the next directory, implied in the fresh repo pull is repetition of all the steps).  

Summary: Move of files across repo can be viewed as a two step process, split and merge. One will have to repeat the split and merge per directory under the source repo (All the contents, files and subdirs, under that directory will be moved). To move files across directories within a repo and preserve history [follow this link](https://stackoverflow.com/questions/2314652/is-it-possible-to-move-rename-files-in-git-and-maintain-their-history) 

**Creating a new repo and mapping the directory structure:** 
* Before proceeding to the step of "Merge a repo" listed below - create the a new repo by following the [steps at](https://help.github.com/articles/create-a-repo/), if doesn't already exist. Go to settings tab of your new repo and set the access permissions. 
* Init all your contrail repos by following the contrail guidelines (for e.g. repo init -u git@github.com:Juniper/contrail-vnc-private -m  mainline/ubuntu-14-04/manifest-mitaka.xml)
* Before invoking repo sync edit the manifest file corresponding to the repo sync and add an anchor directory for newly created repo (steps listed below)
* Go to the directory where the manifest file corresponding to your repo init is located. For e.g. in case of mainline/ubuntu-14-04/manifest-mitaka.xml it would be .repo/manifests/mainline/ubuntu-14-04. 
* Edit the manifest file: manifest-mitaka.xml 
* For e.g to host github.com/Juniper/contrail-common repo at src/contrail-common add the following line to manifest-mitaka.xml '<project name="contrail-common" remote="github" path="src/contrail-common"/> '
* If the repo already exists, skip the creation and host it at an appropriate directory 
* Add the new repo to all manifests that require the new repo visibility

**Split a repo**
* Split an existing repo into two
* Part that you requires merge with a destination repo
* And the OTHER part

**Merge a repo**
* Pick the split-part of repo (from above) and merge with a destination repo

The example below walks through how controller/src/base is split into a repo ([a local repo](http://blog.osteele.com/2008/05/my-git-workflow/)) of its own and merged with src/contrail-common. 

**Split a repo: Split contrail-controller into a repo that contains only base:**
Currently, base is part of the contrail-controller repo. Let’s split the controller/src/base from contrail-controller and create a new (local) repo.
* cd controller
* git checkout master
* Run all the commands from the root directory of the source repo (in this case controller)
* create a file called script with following lines:

    ``#!/bin/bash``

    ``/bin/mkdir –p newroot/``

    ``/bin/mv src/base newroot/``

    ``true``

    ``(base is the directory you are moving here. Save the above file as controller/script)``

* In this instance the file:script is located in the directory controller (at the same level as the directory being moved)
* Apply tree filter:
    ``git filter-branch –f –-prune-empty –-tree-filter /build/username/mainline_build/controller/script HEAD``
* Apply sub-directory filter: 
    ``git filter-branch –-prune-empty –f --subdirectory-filter newroot``
* git remote –v
* The above steps create a local repo that contains base (base: the directory you want to move)
* At this point the repo is split and you have the desired part of the repo, a new (local) repo, with ONLY base (the directory you want to move) at the root of the repo

**Merge a repo: Merge the new local repo (pruned contrail-controller with just base) with src/contrail-common:**
* cd src/controller-common (root directory of your destination repo)
* git checkout –b merging_base (create a branch merging_base)
* git remote add moving_base ../../controller (this is the path to the root of your source repo)
* moving_base is the name of your repo
* git remote –v will include (moving_base) after the above command is invoked
* git fetch moving_base
* git merge moving_base/master (build, test, make necessary changes to scons, rules.py etc.)
* (when you edit scons scripts, do not change the variant_dir of compiled and generated files)
* (as you move things around install necessary files in build/include or build/lib)
* git push -u github (whatever is your remote, here it is github) merging_base (merging_base is your branch name in this case)
* create a pull request on github and merge your changes

**Moving a directory to a repo already in production in Jenkins:**
* In this case, create a fork of the repo by following [these steps](https://guides.github.com/activities/forking/)
* At this point, git clone the fork to a directory where you want to do your work
* Move the desired directory to the clone of the fork by following the steps listed in the 'Merge a repo section'
* Verify that the fork shows the files and directory with history
* [Update the fork](https://gist.github.com/CristinaSolana/1885435) if necessary from the parent
* (No need to compile at this point because the objective is to move files to new location with history)
* At this point, contact CI to merge your fork with parent 
* Someone in CI will execute the following steps to merge the fork with parent (locally on review.opencontrail.org, using the userid `gerrit2`):
- 1. Clone the master repo from gerrit to a working copy
- 2. Clone your repo
- 3. In the tree of (1), do ‘git fetch’ from (2), then ‘git merge’ 
- 4. Check it
- 5. stop the gerrit service
- 6. in tree of (1), do ‘git push’ to update master repo
- 7. start the gerrit service
(Steps 1,2,3, and 6 are similar to updating a private fork from upstream)
* After the fork is merged with mainline, enable scons to include new location of sources, and disable scons at the old location of sources (follow the same make before break model and push changes into repos) and push chnages through gerrit