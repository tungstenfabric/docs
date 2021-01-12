# Configuring Secure Sandesh and Introspect for Contrail Analytics

 

## Configuring Secure Sandesh Connection

All Contrail services use Sandesh, a southbound interface protocol based
on Apache Thrift, to send analytics data such as system logs, object
logs, UVEs, flow logs, and the like, to the collector service in the
Contrail Analytics node. The Transport Layer Security (TLS) protocol is
used for certificate exchange, mutual authentication, and negotiating
ciphers to secure the Sandesh connection from potential tampering and
eavesdropping.

To configure a secure Sandesh connection, configure the following
parameters in all Contrail services that connect to the collector
(Sandesh clients) and the Sandesh server.

| Parameter                      | Description                                 | Default                                        |
|:-------------------------------|:--------------------------------------------|:-----------------------------------------------|
| `[SANDESH].sandesh_keyfile `   | Path to the node's private key              | `/etc/contrail/ssl/private/server-privkey.pem` |
| `[SANDESH].sandesh_certfile`   | Path to the node's public certificate       | `/etc/contrail/ssl/certs/server.pem`           |
| `[SANDESH].sandesh_ca_cert`    | Path to the CA certificate                  | `/etc/contrail/ssl/certs/ca-cert.pem`          |
| `[SANDESH].sandesh_ssl_enable` | Enable or disable secure Sandesh connection | `false`                                        |

## Configuring Secure Introspect Connection

All Contrail services are embedded with a web server that can be used to
query the internal state of the data structures, view trace messages,
and perform other extensive debugging. The Transport Layer Security
(TLS) protocol is used for certificate exchange, mutual authentication,
and negotiating ciphers to secure the introspect connection from
potential tampering and eavesdropping.

To configure a secure introspect connection, configure the following
parameters in the Contrail service, see
[Table 1](analytics-secure-sandesh-40-vnc.html#sandesh1).

Table 1: Secure Introspect Parameters

| Parameter                         | Description                                     | Default                                        |
|:----------------------------------|:------------------------------------------------|:-----------------------------------------------|
| `[SANDESH].sandesh_keyfile`       | Path to the node's private key.                 | `/etc/contrail/ssl/private/server-privkey.pem` |
| `[SANDESH].sandesh_certfile`      | Path to the node's public certificate.          | `/etc/contrail/ssl/certs/server.pem`           |
| `[SANDESH].sandesh_ca_cert`       | Path to the CA certificate.                     | `/etc/contrail/ssl/certs/ca-cert.pem`          |
| `[SANDESH].introspect_ssl_enable` | Enable or disable secure introspect connection. | `false`                                        |

 
