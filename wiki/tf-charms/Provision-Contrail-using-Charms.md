Please follow the following steps to launch Contrail containers using Juju charms

1.Login into the bastion host using the command 'ssh contrail@10.84.33.1' (password is c0ntrail123)

2.From the bastion host ssh into the Juju API Client machine using the command ssh ubuntu@192.168.1.5

3.Deploy the charms using the command './deplay-ha.sh'

4.Issue 'juju status' to know the status of the deployment of charms. Once it says 'Unit is ready' for all the charms we know that it is deployed successfully

5.Once all the charms are provisioned please do the following manual steps for things to work

        a. Go to the 'contrail-agent' charm machine using the command 'juju ssh <machine_id>
        b. Launch the docker container using the command 'docker exec -it contrail-agent bash'
        c. Modify the /etc/contrail/contrail-vrouter-agent.conf' file to replace all the lb server ip's with the controller node ip's
        d. Restart the contrail-vrouter-agent and nodemgr
        e. Exit the docker container and go to the cd /usr/bin directory
        f. Issue the command 'docker cp contrail-agent:/usr/bin/vrouter-port-control .'
        g. Comment out line 18 and 19