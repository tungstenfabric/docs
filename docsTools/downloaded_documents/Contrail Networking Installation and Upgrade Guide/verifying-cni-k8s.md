# Verifying Configuration for CNI for Kubernetes

 

<div id="intro">

<div class="mini-toc-intro">

Use the verification steps in this topic to view and verify your
configuration of Contrail Container Network Interface (CNI) for
Kubernetes.

</div>

</div>

## View Pod Name and IP Address

Use the following command to view the IP address allocated to a pod.

<div id="jd0e22" class="example" dir="ltr">

    [root@device ~]# kubectl get pods --all-namespaces -o wide 
    NAMESPACE       NAME               READY     STATUS    RESTARTS   AGE       IP                         NODE
    default             client-1            1/1         Running     0               19d       10.47.25.247   k8s-minion-1-3
    default             client-2            1/1         Running     0               19d       10.47.25.246   k8s-minion-1-1
    default             client-x             1/1        Running     0               19d       10.84.21.272   k8s-minion-1-1

</div>

## Verify Reachability of Pods

Perform the following steps to verify if the pods are reachable to each
other.

1.  <span id="jd0e38">Determine the IP address and name of the
    pod.</span>
    <div id="jd0e41" class="example" dir="ltr">

        [root@device ~]# kubectl get pods --all-namespaces -o wide
        NAME                        READY     STATUS    RESTARTS   AGE       IP              NODE
        example1-36xpr   1/1       Running   0          43s       10.47.25.251   b3s37
        example2-pldp1   1/1       Running   0          39s       10.47.25.250   b3s37

    </div>
2.  <span id="jd0e47">Ping the destination pod from the source pod to
    verify if the pod is reachable.</span>
    <div id="jd0e50" class="example" dir="ltr">

        root@device ~]# kubectl exec -it example1-36xpr  ping 10.47.25.250
        PING 10.47.25.250 (10.47.25.250): 56 data bytes
        64 bytes from 10.47.25.250: icmp_seq=0 ttl=63 time=1.510 ms
        64 bytes from 10.47.25.250: icmp_seq=1 ttl=63 time=0.094 ms

    </div>

## Verify If Isolated Namespace-Pods Are Not Reachable

Perform the following steps to verify if pods in isolated namespaces
cannot be reached by pods in non-isolated namespaces.

1.  <span id="jd0e70">Determine the IP address and name of a pod in an
    isolated namespace.</span>
    <div id="jd0e73" class="example" dir="ltr">

        [root@device ~]# kubectl get pod -n test-isolated-ns -o wide
        NAME                        READY     STATUS    RESTARTS   AGE       IP              NODE
        example3-bvqx5   1/1       Running   0          1h        10.47.25.249   b3s37

    </div>
2.  <span id="jd0e82">Determine the IP address of a pod in a non-solated
    namespace.</span>
    <div id="jd0e85" class="example" dir="ltr">

        [root@device ~]# kubectl get pods
        NAME                        READY     STATUS    RESTARTS   AGE
        example1-36xpr   1/1       Running   0          15h
        example2-pldp1   1/1       Running   0          15h

    </div>
3.  <span id="jd0e91">Ping the IP address of the pod in the isolated
    namespace from the pod in the non-isolated namespace.</span>
    <div id="jd0e94" class="example" dir="ltr">

        [root@device ~]# kubectl exec -it example1-36xpr ping 10.47.25.249
                --- 10.47.255.249 ping statistics ---
         2 packets transmitted, 0 packets received, 100% packet loss

    </div>

## Verify If Non-Isolated Namespace-Pods Are Reachable

Perform the following steps to verify if pods in non-isolated namespaces
can be reached by pods in isolated namespaces.

1.  <span id="jd0e114">Determine the IP address of a pod in a
    non-isolated namespace.</span>
    <div id="jd0e117" class="example" dir="ltr">

        [root@device ~]# kubectl get pods -o wide
        NAME                        READY     STATUS    RESTARTS   AGE       IP              NODE
        example1-36xpr   1/1       Running   0          15h       10.47.25.251   b3s37
        example2-pldp1   1/1       Running   0          15h       10.47.25.250   b3s37

    </div>
2.  <span id="jd0e123">Determine the IP address and name of a pod in an
    isolated namespace.</span>
    <div id="jd0e126" class="example" dir="ltr">

        [root@device ~]# kubectl get pod -n test-isolated-ns -o wide
        NAME                        READY     STATUS    RESTARTS   AGE       IP              NODE
        example3-bvqx5   1/1       Running   0          1h        10.47.25.249   b3s37

    </div>
3.  <span id="jd0e135">Ping the IP address of the pod in the
    non-isolated namespace from a pod in the isolated namespace.</span>
    <div id="jd0e138" class="example" dir="ltr">

        [root@device ~]# kubectl exec -it example3-bvqx5 -n test-isolated-ns ping 10.47.25.251
        PING 10.47.25.251 (10.47.25.251): 56 data bytes
        64 bytes from 10.47.25.251: icmp_seq=0 ttl=63 time=1.467 ms
        64 bytes from 10.47.25.251: icmp_seq=1 ttl=63 time=0.137 ms
        ^C--- 10.47.25.251 ping statistics ---
        2 packets transmitted, 2 packets received, 0% packet loss
        round-trip min/avg/max/stddev = 0.137/0.802/1.467/0.665 ms

    </div>

## Verify If a Namespace is Isolated

Namespace annotations are used to turn on isolation in a Kubernetes
namespace. In isolated Kubernetes namespaces, the namespace metadata is
annotated with the `opencontrail.org/isolation : true` annotation.

Use the following command to view annotations on a namespace.

<div id="jd0e164" class="example" dir="ltr">

    [root@a7s16 ~]#
    kubectl describe namespace test-isolated-ns   
    Name:       test-isolated-ns
    Labels:     <none>
    Annotations:    opencontrail.org/isolation : true     Namespace is isolated
    Status:     Active

</div>

 
