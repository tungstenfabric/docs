Getting started as a developer
==============================

This brief note would serve as a reference for a developer looking to
start-up on the Tungsten Fabric development environment.

PLEASE NOTE: Until 2018, Tungsten Fabric was named “OpenContrail”. There
are still several references to the old name in the code and other
utilities.


1. OS installation and configuration
-----------------------------------------

Install Centos 7 for a stable installation of Tungsten Fabric.

You can also use Ubuntu 20.04 (In case of problems, check https://github.com/tungstenfabric/tf-devstack)

1.1 Relevant packages for the Tungsten Fabric installation.
-----------------------------------------------------------

::

        sudo yum update 
        sudo yum install git
        sudo yum install git-core
        sudo yum install openssh-server



1.2 Generate SSH key and add it to local SSH-agent
--------------------------------------------------

Ref:
https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account

::

        ssh-keygen -t rsa -b 4096 -C "<username@someone.com>" //press "Enter" every time you see question
        eval $(ssh-agent -s)
        ssh-add ~/.ssh/id_rsa
        cat ~/.ssh/id_rsa.pub

Copy the entire output line(your public ssh id)


1.3 Add SSH key to GitHub account
---------------------------------

1. Go to profile and select settings

2. Choose SSH and GPG keys -> New SSH key

3. Give a title for the key

4. Paste the key copied in step 1.2

5. Add SSH key

2. Tungsten Fabric + Devstack setup(Ansible Deployer)
-----------------------------------------------------

Ref: https://github.com/tungstenfabric/tf-devstack

If you have any questions, you can see more detailed instructions in this README:

https://github.com/tungstenfabric/tf-devstack/tree/master/ansible

2.1 Create a nonroot user and add it to the wheel group
------------------------------------------------------

::
         sudo useradd <username>
         sudo passwd <username> 
         sudo usermod -aG wheel <username>


Modify user rigths configuration. Open the sudoers file

::
         sudo visudo

In the opened file, locate the line
::
         %wheel  ALL=(ALL)       ALL
Change it to 
::
         %wheel ALL=(ALL)        NOPASSWD: ALL

Switch to the new user and navigate to the home directory
         su <username>
         cd


2.1 Clone Contrail-installer and devstack Repositories
------------------------------------------------------

::

        git clone http://github.com/tungstenfabric/tf-devstack
   

2.2 Set up Tungsten Fabric
--------------------------

Execute script and wait for installation:
::

        ./tf-devstack/ansible/run.sh  // 

2.3 Accessing Openstack and Tungsten Fabric GUIs
-------------------------------------------------
Openstack and contrail GUIs can be accessed as follows:-

1. Tungsten Fabric GUI: :code:`http://localhost:8143/`

2. Openstack GUI: :code:`http://localhost/dashboard/` (only if you have installed with the openstack orchestrator)


3. Setting up Gerrit for committing code-changes for review
-----------------------------------------------------------

https://gerrit-review.googlesource.com/Documentation/user-notify.html

3.1 Setup SSH access
--------------------

1. Log into your account at https://tf-gerrit.gz1.progmaticlab.com (also via GitHub)

2. Go to top-right corner -> settings

3. Left panel: SSH Keys -> New SSH key

4. Copy ssh key from step 1.2

5. Test the SSH access

   ::

      $ ssh -p 29418 sshusername@tf-gerrit.gz1.progmaticlab.com

      **** Welcome to Gerrit Code Review ****

      Hi <sshusername>, you have successfully connected over SSH.

   Unfortunately, interactive shells are disabled. 
   To clone a hosted Git repository, use:

   ::

      git clone ssh://sshusername@tf-gerrit.gz1.progmaticlab.com:29418/REPOSITORY_NAME.git   

      Connection to hostname closed.

3.2 Pushing code-changes for review
-----------------------------------


1. Install git-review

   ::

      sudo yum install git-review

2. Configure Gerrit

   ::

      git config –global user.email username@someone.com gitdir=$(git
      rev-parse –git-dir); scp -p -P 29418
      username@tf-gerrit.gz1.progmaticlab.com:hooks/commit-msg ${gitdir}/hooks/

3. Clone the repo where changes need to be committed

   ::

      git clone
      ssh://sshusername@tf-gerrit.gz1.progmaticlab.com:29418/REPOSITORY_NAME.git

4. Commit the changes

   ::

      git commit -m "<commit-note>"

   Note: please ensure that any change being committed should have a corresponding
   launch-pad bug-id mentioned in the commit message, i.e. "Bug #1679466"

5. Push the locally committed changes up for review

   ::

      git push ssh://username@tf-gerrit.gz1.progmaticlab.com:29418/REPOSITORY_NAME \
      HEAD:refs/for/<branch>%topic=<few-words-describing-the-change>, \
      r=reviewername@someone.com, cc=otherreviewer@someone.com

NOTE. If any of the steps above have raised questions, you can read the documentation at the link above
