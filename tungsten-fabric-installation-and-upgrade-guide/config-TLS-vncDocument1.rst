Configuring Transport Layer Security-Based XMPP in Tungsten Fabric
==================================================================

 

Overview: TLS-Based XMPP
------------------------

Transport Layer Security (TLS)-based XMPP can be used to secure all
Extensible Messaging and Presence Protocol (XMPP)-based communication
that occurs in the TF environment.

Secure XMPP is based on RFC 6120, Extensible Messaging and Presence
Protocol (XMPP): Core.

TLS XMPP in Tungsten Fabric
~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the TF environment, the Transport Layer Security (TLS) protocol
is used for certificate exchange, mutual authentication, and negotiating
ciphers to secure the stream from potential tampering and eavesdropping.

The RFC 6120 highlights a basic stream message exchange format for TLS
negotiation between an XMPP server and an XMPP client.

.. note::

   Simple Authentication and Security Layer (SASL) authentication is not
   supported in the TF environment.

Configuring XMPP client and server in Tungsten Fabric
-----------------------------------------------------

In the TF environment, XMPP based communications are used in
client and server exchanges, between the compute node (as the XMPP
client), and:

-  the control node (as the XMPP server)

-  the DNS server (as the XMPP server)

Configuring Control Node for XMPP Server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To enable secure XMPP, the following parameters are configured at the
XMPP server.

| On the control node, enable the parameters in the configuration file:
| ``/etc/contrail/contrail-control.conf``.

.. list-table:: 
      :header-rows: 1

      * - Parameter
        - Description
        - Default
      * - ``xmpp_server_cert``
        - Path to the node's public certificate
        - ``/etc/contrail/ssl/certs/server.pem``
      * - ``xmpp_server_key``
        - Path to server's or node's private key
        - ``/etc/contrail/ssl/certs/server-privkey.pem``
      * - ``xmpp_ca_cert``
        - Path to CA certificate
        - ``/etc/contrail/ssl/certs/ca-cert.pem``
      * - ``xmpp_auth_enable=true``
        - Enables SSL based XMPP
        - Default is set to false, XMPP is disabled.
          *Note*: The keyword ``true`` is case sensitive.


Configuring DNS Server for XMPP Server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To enable secure XMPP, the following parameters are configured at the
XMPP DNS server.

| On the DNS server control node, enable the parameters in the
  configuration file:
| ``/etc/contrail/contrail-control.conf``


.. list-table:: 
      :header-rows: 1

      * - Parameter
        - Description
        - Default
      * - ``xmpp_server_cert``
        - Path to the node's public certificate
        - ``/etc/contrail/ssl/certs/server.pem``
      * - ``xmpp_server_key``
        - Path to server's or node's private key
        - ``/etc/contrail/ssl/certs/server-privkey.pem``
      * - ``xmpp_ca_cert``
        - Path to CA certificate
        - ``/etc/contrail/ssl/certs/ca-cert.pem``
      * - ``xmpp_dns_auth_enable=true``
        - Enables SSL based XMPP
        - Default is set to false, XMPP is disabled.
          *Note*: The keyword ``true`` is case sensitive.


Configuring Control Node for XMPP Client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To enable secure XMPP, the following parameters are configured at the
XMPP client.

| On the compute node, enable the parameters in the configuration file:
| ``/etc/contrail/contrail-vrouter-agent.conf``

.. list-table:: 
      :header-rows: 1

      * - Parameter
        - Description
        - Default
      * - ``xmpp_server_cert``
        - Path to the node's public certificate
        - ``/etc/contrail/ssl/certs/server.pem``
      * - ``xmpp_server_key``
        - Path to server's/node's private key
        - ``/etc/contrail/ssl/private/server-privkey.pem``
      * - ``xmpp_ca_cert``
        - Path to CA certificate
        - ``/etc/contrail/ssl/certs/ca-cert.pem``
      * - ``xmpp_auth_enable=true``
          ``xmpp_dns_auth_enable=true``
        - Enables SSL based XMPP
        - Default is set to false, XMPP is disabled.
          *Note*: The keyword ``true`` is case sensitive.

