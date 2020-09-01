## Step 1. Increase global limits

Ensure `/etc/security/limits.conf` has sufficients limits for number of opened files for a process. An example configuration is

```
root soft nofile 65535
root hard nofile 65535
* hard nofile 65535
* soft nofile 65535
* hard nproc 65535
* soft nofile 65535
```

## Step 2. Increase per-process limits for 
* Supervisord based service
  + in supervisor config file (e.g. `/etc/contrail/supervisord_config.conf`) in the `supervisord` section set minfds and minprocs. for e.g.

      ```
      ...
      [supervisord]
      minfds=10240
      minprocs=200
      ...
      ```
* Upstart based service
  + in upstart config file (e.g. in `/etc/init/zookeeper.conf`) set number of files with `nofile` for e.g.
  
      ```
      limit nofile 8192 8192
      ```

## Step 3. Restart service

  `service <name> restart`