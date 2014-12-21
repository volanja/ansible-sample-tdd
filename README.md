ansible-sample-tdd
==================

Test Driven Development for Ansible  by ServerSpec. It's Sample

ServerSpec is test framework based on Ruby.

*NOTICE*
If you want to use these specfiles on other project, please use ansible_spec that ruby-gem for create Rakefile and spec/spec_helper.rb  
[ansible_spec](http://rubygems.org/gems/ansible_spec)

# Environment

```
$ ruby -v
ruby 1.9.3p194 (2012-04-20 revision 35410) [x86_64-darwin11.4.2]

$ gem list |grep serverspec
serverspec (0.13.5)

```

# Directory

```
.
├── .ansiblespec                 #Create file (use Serverspec)
├── README.md
├── hosts                        #use Ansible and Serverspec if .ansiblespec is not exist.
├── site.yml                     #use Ansible and Serverspec if .ansiblespec is not exist.
├── nginx.yml                    #(comment-out) incluted by site.yml
├── roles
│   ├── mariadb
│   │   ├── spec
│   │   │   └── mariadb_spec.rb
│   │   ├── tasks
│   │   │   └── main.yml
│   │   └── templates
│   │       └── mariadb.repo
│   └── nginx
│       ├── handlers
│       │   └── main.yml
│       ├── spec                 #use Serverspec
│       │   └── nginx_spec.rb
│       ├── tasks
│       │   └── main.yml
│       ├── templates
│       │   └── nginx.repo
│       └── vars
│           └── main.yml
├── Rakefile                     #use Serverspec
└── spec                         #use Serverspec 
    └── spec_helper.rb
```

## Change .ansiblespec(v0.0.1.3)
read [this seciton](https://github.com/volanja/ansible_spec#change-ansiblespecv0013)
If `.ansiblespec` is exist, use variables(playbook and inventory).  
So, If you don't use `site.yml` and `hosts`, you change this file.  
If `.ansiblespec` not found, use `site.yml` as playbook and `hosts` as inventory.  

```.ansiblespec
--- 
- 
  playbook: site.yml
  inventory: hosts
```

# Run Playbook

**Please re-write Your target IP-Adress of Server -> hosts (default is 192.168.0.103 and 104)**

```
$ ansible-playbook site.yml -i hosts
```

#Test
## Serverspec with Ansible
Serverspec use this file.  (Rakefile understand Notation of Ansible.)  

* hosts  
hosts can use [group_name]  

```hosts
[server]
192.168.0.103
192.168.0.104
```

* site.yml  
site.yml can use ```include```  

```site.yml
- name: Ansible-Sample-TDD
  hosts: server
  user: root
  roles:
    - nginx
    - mariadb
```

## Run Test

```
$ rake -T
rake serverspec:Ansible-Sample-TDD  # Run serverspec for Ansible-Sample-TDD / Run serverspec for Ansible-Sample-TDD 

$ rake serverspec:Ansible-Sample-TDD
Run serverspec for Ansible-Sample-TDD to 192.168.0.103
/Users/Adr/.rvm/rubies/ruby-1.9.2-p320/bin/ruby -S rspec roles/mariadb/spec/mariadb_spec.rb roles/nginx/spec/nginx_spec.rb
...........

Finished in 0.40289 seconds
11 examples, 0 failures
Run serverspec for Ansible-Sample-TDD to 192.168.0.104
/Users/Adr/.rvm/rubies/ruby-1.9.2-p320/bin/ruby -S rspec roles/mariadb/spec/mariadb_spec.rb roles/nginx/spec/nginx_spec.rb
...........

Finished in 0.4004 seconds
11 examples, 0 failures
```

## Run Test only Ansible
Switch branch to add-test.  
And Run Task.  

```
ansible-playbook site.yml -i hosts -t test
```

test is exist in `roles/nginx/tasks/test.yml`  

# TODO

* hard-coding some things in Rakefile (inventory-file, private-key) to Configfile??
