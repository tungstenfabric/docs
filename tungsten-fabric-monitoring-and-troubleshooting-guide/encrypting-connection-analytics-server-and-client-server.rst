Encryption Between Analytics API Servers and Client Servers
===========================================================

:data: 2019-10-15 

Tungsten Fabric Release 2011 supports SSL encryption for the
connection between Analytics API servers and Client servers. 
In releases prior to release 2011, the connection between Analytics API servers and the
Client servers was not encrypted, which could pose a security threat.

SSL encryption is supported in Tungsten Fabric Release 2011 only
when Tungsten Fabric is deployed with Red Hat OpenStack Platform
(RHOSP). In the RHOSP deployment, a global flag is added, which
determines the status of the SSL encryption.

If the global flag is enabled:

-  You do not have to modify the configuration files as SSL encryption
   is automatically enabled.

-  You must modify the configuration files if you want to disable SSL
   encryption.

If the global flag is disabled:

-  You do not have to modify the configuration files as SSL encryption
   is automatically disabled.

-  You cannot enable SSL encryption, even if you modify the
   configuration files. The certificates are not generated during
   deployment as the global flag is disabled.

The configuration files are contrail-analytics-api.conf,
contrail-svc-monitor.conf, and command_servers.yml. In the configuration
files, modify the following parameters in the
Table 1 below to enable or disable SSL based encryption:

Table 1: SSL Encryption Parameters

.. list-table:: 
      :header-rows: 1

      * - Parameters
        - Description
        - Default
      * - analytics_api_ssl_enable
        - Enables or disables support for SSL encryption between Analytics API server and Client server.
        - If the value is assigned TRUE: Support for SSL encryption is enabled.
          
          If the value is assigned FALSE: Support for SSL encryption is not enabled and the Analytics API server does not accept HTTPS requests.

      * - analytics_api_insecure_enable
        - Enables or disables support for required certificates in HTTPS requests.
        - If the value is assigned TRUE: HTTPS connection is supported without the certificates.
          
          If the value is assigned FALSE: HTTPS connection is not supported without the certificates.

      * - analytics_api_ssl_keyfile
        - Path to the node’s private key.
        - /etc/contrail/ssl/private/server-privkey.pem
      * - analytics_api_ssl_certfile
        - Path to the node's public certificate.
        - /etc/contrail/ssl/certs/server.pem
      * - analytics_api_ssl_ca_cert
        - Path to the CA certificate
        - /etc/ipa/ca.crt

Once these parameters are configured, the Analytics API server starts
using SSL certificates, which enables SSL encryption support for
connection between Analytics API servers and Client servers.

.. list-table:: Release History Table
      :header-rows: 1

      * - Release
        - Description
      * - 2011
        - Tungsten Fabric 2011 supports SSL encryption for the
          connection between Analytics API servers and Client servers.
