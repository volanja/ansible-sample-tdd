ansible-sample-tdd
==================

Test Driven Development for Ansible  by ServerSpec. It's Sample

ServerSpec is test framework based on Ruby.

# Environment

```
$ ruby -v
ruby 1.9.3p194 (2012-04-20 revision 35410) [x86_64-darwin11.4.2]

$ gem list |grep serverspec
serverspec (0.13.5)

```

# Run Playbook

**Please re-write Your target IP-Adress of Server -> hosts, spec/192.168.0.103. default is 192.168.0.103**

```
$ ansible-playbook site.yml -i hosts

PLAY [Ansible-Sample-TDD] ***************************************************** 

GATHERING FACTS *************************************************************** 
ok: [192.168.0.103]

TASK: [nginx | Template nginx.repo] ******************************************* 
changed: [192.168.0.103]

TASK: [nginx | install Nginx] ************************************************* 
changed: [192.168.0.103] => (item=nginx)

TASK: [nginx | ensure nginx is running automatically at boot time] ************ 
changed: [192.168.0.103]

TASK: [nginx | insert iptables rule] ****************************************** 
changed: [192.168.0.103]

TASK: [nginx | Restart iptables] ********************************************** 
changed: [192.168.0.103]

NOTIFIED: [nginx | restart iptables] ****************************************** 
changed: [192.168.0.103]

PLAY RECAP ******************************************************************** 
192.168.0.103              : ok=7    changed=6    unreachable=0    failed=0   

```

#Run Test

```
$rake spec
/Users/Adr/.rvm/rubies/ruby-1.9.3-p194/bin/ruby -S rspec spec/192.168.0.103/nginx_spec.rb
......

Finished in 0.24233 seconds
6 examples, 0 failures
```


