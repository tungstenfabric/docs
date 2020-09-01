Run below commands against your zookeeper cluster nodes
  ```
  $ echo stat | nc 192.168.0.102 2181 | grep Mode
  Mode: leader

  $ echo stat | nc 192.168.0.100 2181 | grep Mode
  Mode: follower
  ```