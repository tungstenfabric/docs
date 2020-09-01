## Below are the steps to provision RBAC in an existing setup

#### In /etc/contrail/contrail-api.conf

          “aaa_mode = rbac”

#### In /etc/neutron/api-paste.ini

          REPLACE

          “keystone = cors request_id catch_errors authtoken keystonecontext extensions neutronapiapp_v2_0”  
          
          WITH  

          “keystone = user_token cors request_id catch_errors authtoken keystonecontext extensions neutronapiapp_v2_0”

           AND ADD BELOW LINES,

           [filter:user_token]
           paste.filter_factory = neutron_plugin_contrail.plugins.opencontrail.neutron_middleware:token_factory

#### In /etc/contrail/contrail-analytics-api.conf

           "aaa_mode = no-auth"

#### Restart services

           service contrail-api restart
           service neutron-server restart
           service supervisor-analytics restart
           service supervisor-webui restart