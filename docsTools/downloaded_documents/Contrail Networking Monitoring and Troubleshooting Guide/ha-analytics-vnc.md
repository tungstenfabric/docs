# High Availability for Analytics

 

Contrail supports multiple instances of analytics for high availability
and load balancing.

Contrail analytics provides two broad areas of functionality:

-   **contrail-collector** —Receives status, logs, and flow information
    from all Contrail processing elements (for example, generators) and
    records them.

    Every generator is connected to one of the **contrail-collector**
    instances at any given time. If an instance fails (or is shut down),
    all the generators that are connected to it are automatically moved
    to another functioning instance, typically in a few seconds or less.
    Some messages may be lost during this movement. UVEs are resilient
    to message loss, so the state shown in a UVE is kept consistent to
    the state in the generator.

-   **contrail-opserver** —Provides an external API to report UVEs and
    to query logs and flows.

    Each analytics component exposes a northbound REST API represented
    by the **contrail-opserver** service (port 8081) so that the failure
    of one analytics component or one **contrail-opserver** service
    should not impact the operation of other instances.

    These are the ways to manage connectivity to the
    **contrail-opserver** endpoints:

    -   Periodically poll the **contrail-opserver** service on a set of
        analytics nodes to determine the list of functioning endpoints,
        then make API requests from one or more of the functioning
        endpoints.

    -   The Contrail user interface makes use of the same northbound
        REST API to present dashboards, and reacts to any
        **contrail-opserver** high availability event automatically.

 
