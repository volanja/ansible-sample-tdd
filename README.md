# ansible-sample-tdd

Test Driven Development for Ansible  by ServerSpec. It's Sample

ServerSpec is a test framework based on Ruby.

**NOTICE**  
If you want to use these specfiles on other project,  
Please install `ansible_spec` ruby-gem to parse Ansible playbook & inventory files.
- [Rubygems - ansible_spec](http://rubygems.org/gems/ansible_spec)
- [Github - ansible_spec](https://github.com/volanja/ansible_spec)

# Environment

```
$ ruby -v
ruby 2.0.0p353 (2013-11-22 revision 43784) [x86_64-darwin11.4.2]

$ gem list (needs)
ansible_spec (0.2.6)
serverspec (2.23.1)
specinfra (2.43.4)
hostlist_expression (0.2.1)
```

# Important( from v0.1)
this sample use `(Rubygem) ansible_spec`

```
gem install ansible_spec
```

# Directory

```
.
├── .ansiblespec                 #Create file (use Serverspec)
├── README.md
├── hosts                        #use Ansible and Serverspec if `.ansiblespec` do not exist.
├── exec_hosts.sh                #Dynamic Inventory sample. if you use DynamicInventory, change `.ansiblespec`
├── site.yml                     #use Ansible and Serverspec if `.ansiblespec` do not exist.
├── nginx.yml                    #(comment-out) included by site.yml
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
read [this section](https://github.com/volanja/ansible_spec#change-ansiblespecv0013)
If `.ansiblespec` exist, use variables(playbook and inventory).  
So, If you don't use `site.yml` and `hosts`, you need to change this file.  
If `.ansiblespec` is not found, use `site.yml` as playbook and `hosts` as inventory.  

```.ansiblespec
--- 
- 
  playbook: site.yml
  inventory: hosts
```

# Run Playbook

Please change the target IP address of server -> hosts (default is 192.168.0.103 and 104)

```
$ ansible-playbook site.yml -i hosts
```

#Test
## Serverspec with Ansible
Serverspec use this file.  (Rakefile understand the syntax of Ansible.)  

* hosts  
hosts can use [group_name]  

```hosts
[server]
192.168.0.103

# under sample

#192.168.0.103:22
#192.168.0.103 ansible_ssh_port=22
#192.168.0.103 ansible_ssh_private_key_file=~/.ssh/id_rsa
#test ansible_ssh_host=192.168.0.103
#192.168.0.103 ansible_ssh_user=root
#jumper ansible_ssh_port=22 ansible_ssh_host=192.168.0.103

#[sample]
#(comment) www1.example.com to www99.example.com
#www[1:99].example.com

#(comment)  www01.example.com to www99.example.com
#www[01:99].example.com

#(comment)  db-a.example.com to db-z.example.com
#db-[a:z].example.com

#(comment)  db-A.example.com to db-Z.example.com
#db-[A:Z].example.com

#[databases]
#192.168.0.103

#(comment)  Multi Group. use server & databases
#[group:children]
#sample
#databases
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

