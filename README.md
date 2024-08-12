# host_prototypes

| [collection](https://galaxy.ansible.com/ui/repo/published/ji_podhead/host_prototypes/) |

creates random mac, password, and ssh keys for cloudinit and stores the facts.
can also output the yaml file for inventory.



## Usage
### create a prototype group and your prototype hosts 
- can be your inventory, or any other yaml
- you specify the target path via parameter later

- our dcworkshop1 host has 2 children 

- in this case those are the vms i used in my anisble playbook als libvirt hosts and created 2 vms on this host
- your prototypes can have additional parameters defined here, they will get copied to the new host that will get created 
```yaml
workshop_machines:
  hosts:
    dcworkshop1:
      vars:
        ansible_ssh_host: omit 
        ansible_user: omit
        ansible_ssh_pass: omit
        ansible_connection: ssh
        ansible_become_password: omit 
        machines: 
            proxmox
            vm

    dcworkshop2:
      vars:
        ansible_ssh_host: omit 
        ansible_user: omit
        ansible_ssh_pass: omit
        ansible_connection: ssh
        ansible_become_password: omit 
        machines: 
            proxmox

prototypes:
  hosts:
    proxmox:
      vars:
        mac: omit
        ansible_ssh_host: omit
        ansible_user:  omit
        ansible_ssh_pass: omit
        ansible_connection: ssh
        ansible_become_password: omit
        password: omit
        proxmox_user: omit
        proxmox_ip: omit
        proxmox_pass: omit
        proxmox_token: omit

    vm:
      vars:
        ansible_ssh_host: omit
        ansible_user:  omit
        ansible_ssh_pass: omit
        ansible_connection: ssh
        ansible_become_password: omit
        password: omit

```

### fire the collection in your ansible playbook
```yaml
---
- hosts: localhost
  gather_facts: no
  become: true
  collections:
    - ji_podhead.host_prototypes 
  tasks:
  - name: create the yamls and update the facts
    delegate_to: "localhost"
    import_role: 
      name: ji_podhead.host_prototypes.create_prototypes
    vars:  
        group: 'workshop_machines'
        target_group: 'vms' #optional
        inventory_path:  /home/ji/Dokumente/podshop-org/Pod-Shop-App-Configs/ansible/inventory.yml
        yaml_path: "/home/ji/Dokumente/podshop-org/Pod-Shop-App-Configs/yamlgen" #optional
        store_yaml: "true" #optional
```
## Test and Debug the Output 
- to test if your host got created and has all the facts, i added a little debug loop for you, this is what it will look like:
```bash
TASK [ji_podhead.host_prototypes.create_prototypes : Debug group facts] ********
task path: /home/ji/.ansible/collections/ansible_collections/ji_podhead/host_prototypes/roles/create_prototypes/tasks/main.yml:36
ok: [localhost] => (item=dcworkshop1-proxmox) => {
    "ansible_loop_var": "item",
    "hostvars[item]": {
        "_raw_params": " mac: \"e3:b0:c4:42:98:fc\"  ansible_ssh_host: \"omit\"  ansible_user: \"omit\"  ansible_ssh_pass: \"$6$RTlEFLiQ/alLy7TP$ZKTisntPdpUhtnAzO7u6nypagjJlLs0atAfO/gPXOGojk4u99gmmexAcx7tVAWeAuzoPE1ImywPUrJMfNoPTX/\"  ansible_connection: \"ssh\"  ansible_become_password: \"$6$RTlEFLiQ/alLy7TP$ZKTisntPdpUhtnAzO7u6nypagjJlLs0atAfO/gPXOGojk4u99gmmexAcx7tVAWeAuzoPE1ImywPUrJMfNoPTX/\"  password: \"$6$RTlEFLiQ/alLy7TP$ZKTisntPdpUhtnAzO7u6nypagjJlLs0atAfO/gPXOGojk4u99gmmexAcx7tVAWeAuzoPE1ImywPUrJMfNoPTX/\"  proxmox_user: \"omit\"  proxmox_ip: \"omit\"  proxmox_pass: \"omit\"  proxmox_token: \"omit\"  private_key: \"ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC1F5nQKnGlBamImDjASQjXM1lGwkUo31Gb23O4zb4W2UC1ZE0N3j/Q7EdRE7Kjo6SeqAvWBDl5rbn6VTAFORIL/IZJZwrSiTE8pSBzWv996XqHjvPHFC2WPXgH7G2BUIysC1hpIX13QAZNvt9/NcI1+yF7upufM+xvTcR5vbOOHqHZIr6Tammz8oOLQXeYU43JOtOkanwmpvHFibRnYrGU+jCiaIWjrFrrZ8dBn1/YXOvk9A/TPn7A/vSD4099oWhkvj7caGWiuxdRKQ6TUX2cvZn/ogPebC/3RQVJjN5/1FLAS6R3wHu/qHFqUjppkJDHq3kXxlv8FKOfHr5IMHLF root@base\"  public_key: \"-----BEGIN OPENSSH PRIVATE KEY-----\nb3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABFwAAAAdzc2gtcn\nNhAAAAAwEAAQAAAQEAtReZ0CpxpQWpiJg4wEkI1zNZRsJFKN9Rm9tzuM2+FtlAtWRNDd4/\n0OxHUROyo6OknqgL1gQ5ea25+lUwBTkSC/yGSWcK0okxPKUgc1r/fel6h47zxxQtlj14B+\nxtgVCMrAtYaSF9d0AGTb7ffzXCNfshe7qbnzPsb03Eeb2zjh6h2SK+k2pps/KDi0F3mFON\nyTrTpGp8JqbxxYm0Z2KxlPowomiFo6xa62fHQZ9f2Fzr5PQP0z5+wP70g+NPfaFoZL4+3G\nhlorsXUSkOk1F9nL2Z/6ID3mwv90UFSYzef9RSwEukd8B7v6hxalI6aZCQx6t5F8Zb/BSj\nnx6+SDByxQAAA8Dk/Sxo5P0saAAAAAdzc2gtcnNhAAABAQC1F5nQKnGlBamImDjASQjXM1\nlGwkUo31Gb23O4zb4W2UC1ZE0N3j/Q7EdRE7Kjo6SeqAvWBDl5rbn6VTAFORIL/IZJZwrS\niTE8pSBzWv996XqHjvPHFC2WPXgH7G2BUIysC1hpIX13QAZNvt9/NcI1+yF7upufM+xvTc\nR5vbOOHqHZIr6Tammz8oOLQXeYU43JOtOkanwmpvHFibRnYrGU+jCiaIWjrFrrZ8dBn1/Y\nXOvk9A/TPn7A/vSD4099oWhkvj7caGWiuxdRKQ6TUX2cvZn/ogPebC/3RQVJjN5/1FLAS6\nR3wHu/qHFqUjppkJDHq3kXxlv8FKOfHr5IMHLFAAAAAwEAAQAAAQABmyQxhcWCAueYFXou\n+BwuHIovqwNdgWFhFfV4SkmfgOKkcbgG488d2CJUpf6fgCIUu4dt4GK/gUIi7n8tJPLG+Y\nlVra7zIzaB7GVxfttrxcN2Tt+QbWc8B4z2HW2U/W2BJqJoRkeCubcmuss9qWyB267rliQi\nR3/9escy2HdU4AkNA3il1JXGgncuY9HrcV0jcDfxYzQoK8zgcBMzxzuTGLYIzro3n5PHHg\nqa2C1W0Ke1OmNOZk+Kqju4sumsSGeYyji4BoDLaQ/HVptgUB1srHwf3zddg8N9JgJ+iU7T\nUH0QcskS7UH4q0GONuJ3WoLxwBNh3Czuho4W+prFuEyxAAAAgCVyqbpslypkL6GKgAEH57\nSB0Wf6meVBDFZF4tJgt3m8dh2y6X9Fm30IAg+kV1i/JzkTwMHrb3DegMyExk52Fw3oMJj1\nqIY6BR1YlH/mYhKjctH3APf3b8hwb0a38gN6EFoaaRLdiuk9kZsMcFCwSAHz8cETb/sMOa\nfSD5i0Y1VdAAAAgQC8EmADXZF/RVbd/oALgsIhzONKR5bHFldPqztFvtUsdjyvoecpSrAL\niAv14lAcu30XeuTXdszNcy7umDcaDnSt9ESIi66EKmGwWRsTSxiABGJquWPxsEp4pr+f8i\nvO/T0zUrHIhg3sX5fU+b84VTezb2c4sJkRfr6RE9C5ZYykdQAAAIEA9n/f02IdAfCmKbS/\nlS4wfkGde1a6Z9OGaYJt5HqRjIWDG6Fcm8XYtqXdxZMG6tHSwpcxetTQJu5Rdti17uPTEV\n95HRqxz8XFbcCDHyI+nKfoUI4dOdvizYP3hWLcAEwXrdcoAZzDhpdSln3uhXFyemBp3ebF\n/j0q7i8tvZCWixEAAAAJcm9vdEBiYXNlAQI=\n-----END OPENSSH PRIVATE KEY-----\" ",
        "ansible_check_mode": false,
        "ansible_config_file": "/etc/ansible/ansible.cfg",
        "ansible_diff_mode": false,
        "ansible_facts": {},
        "ansible_forks": 5,
        "ansible_inventory_sources": [
            "/home/ji/Dokumente/podshop-org/Pod-Shop-App-Configs/ansible/inventory.yml"
        ],
        "ansible_playbook_python": "/usr/bin/python3",
        "ansible_run_tags": [
            "all"
        ],
        "ansible_skip_tags": [],
        "ansible_verbosity": 2,
        "ansible_version": {
            "full": "2.14.14",
            "major": 2,
            "minor": 14,
            "revision": 14,
            "string": "2.14.14"
        },
        "group_names": [
            "vms"
        ],
        ...
```
