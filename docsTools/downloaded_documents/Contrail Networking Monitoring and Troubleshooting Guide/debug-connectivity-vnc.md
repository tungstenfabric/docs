# Example: Debugging Connectivity Using Monitoring for Troubleshooting

 

## Using Monitoring to Debug Connectivity

This example shows how you can use monitoring to debug connectivity in
your Contrail system. You can use the demo setup in Contrail to use
these steps on your own.

1.  <span id="jd0e22">Navigate to **Monitor -&gt; Networking -&gt;
    Networks -&gt;** `default-domain:demo:vn0`, **Instance**
    `ed6abd16-250e-4ec5-a382-5cbc458fb0ca `with **IP address**
    `192.168.0.252` in the virtual network `vn0`. See
    [Figure 1](debug-connectivity-vnc.html#ex-mon-netw-1).</span>

    ![Figure 1: Navigate to Instance](images/s041879.gif)

2.  <span id="jd0e52">Click the instance to view **Traffic Statistics
    for Instance**. See
    [Figure 2](debug-connectivity-vnc.html#ex-mon-netw-2).</span>

    ![Figure 2: Traffic Statistics for Instance](images/s041880.gif)

3.  <span id="jd0e64">**Instance**
    `d26c0b31-c795-400e-b8be-4d3e6de77dcf  `with **IP address**
    `192.168.0.253` in the virtual network `vn16`. See
    [Figure 3](debug-connectivity-vnc.html#ex-mon-netw-3) and
    [Figure 4](debug-connectivity-vnc.html#ex-mon-netw-4).</span>

    ![Figure 3: Navigate to Instance](images/s041881.gif)

    ![Figure 4: Traffic Statistics for Instance](images/s041882.gif)

4.  <span id="jd0e93">From **Monitor-&gt;Infrastructure-&gt;Virtual
    Routers-&gt;a3s18-&gt;Interfaces**, we can see that
    **Instance**` ed6abd16-250e-4ec5-a382-5cbc458fb0ca` is hosted on
    **Virtual Router** `a3s18`. See
    [Figure 5](debug-connectivity-vnc.html#ex-mon-netw-5).</span>

    ![Figure 5: Navigate to a3s18 Interfaces](images/s041883.gif)

5.  <span id="jd0e117">From **Monitor-&gt;Infrastructure-&gt;Virtual
    Routers-&gt;a3s19-&gt;Interfaces**, we can see that **Instance**
    `d26c0b31-c795-400e-b8be-4d3e6de77dcf  ` is hosted on **Virtual
    Router** `a3s19`. See
    [Figure 6](debug-connectivity-vnc.html#ex-mon-netw-6).</span>

    ![Figure 6: Navigate to a3s19 Interfaces](images/s041884.gif)

6.  <span id="jd0e141">**Virtual Routers** `a3s18` and `a3s19` have the
    **ACL** entries to allow connectivity between
    `default-domain:demo:vn0 `and `default-domain:demo:vn16` networks.
    See [Figure 7](debug-connectivity-vnc.html#ex-mon-netw-7) and
    [Figure 8](debug-connectivity-vnc.html#ex-mon-netw-8).</span>

    ![Figure 7: ACL Connectivity a3s18](images/s041885.gif)

    ![Figure 8: ACL Connectivity a3s19](images/s041886.gif)

7.  <span id="jd0e173">Next, verify the routes on the control node for
    routing instances `default-domain:demo:vn0:vn0` and
    `default-domain:demo:vn16:vn16`. See
    [Figure 9](debug-connectivity-vnc.html#ex-mon-netw-9) and
    [Figure 10](debug-connectivity-vnc.html#ex-mon-netw-10).</span>

    ![Figure 9: Routes default-domain:demo:vn0:vn0](images/s041887.gif)

    ![Figure 10: Routes
    default-domain:demo:vn16:vn16](images/s041888.gif)

8.  <span id="jd0e194">We can see that VRF `default-domain:demo:vn0:vn0`
    on Virtual Router `a3s18` has the appropriate route and next hop to
    reach VRF `default-domain:demo:front-end` on Virtual Router `a3s19`.
    See [Figure 11](debug-connectivity-vnc.html#ex-mon-netw-11).</span>

    ![Figure 11: Verify Route and Next Hop a3s18](images/s041889.gif)

9.  <span id="jd0e215">We can see that VRF
    `default-domain:demo:vn16:vn16 ` on Virtual Router `a3s19` has the
    appropriate route and next hop to reach VRF
    `default-domain:demo:vn0:vn0 ` on Virtual Router `a3s18`. See
    [Figure 12](debug-connectivity-vnc.html#ex-mon-netw-12).</span>

    ![Figure 12: Verify Route and Next Hop a3s19](images/s041890.gif)

10. <span id="jd0e236">Finally, flows between instances (IPs
    `192.168.0.252` and `192.168.16.253`) can be verified on Virtual
    Routers `a3s18` and `a3s19`. See
    [Figure 13](debug-connectivity-vnc.html#ex-mon-netw-13) and
    [Figure 14](debug-connectivity-vnc.html#ex-mon-netw-14).</span>

    ![Figure 13: Flows for a3s18](images/s041891.gif)

    ![Figure 14: Flows for a3s19](images/s041892.gif)

 
