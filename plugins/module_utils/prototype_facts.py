import yaml
import sys
import copy
import subprocess
import os
import tempfile
bashFolder="./"

yamlpath1="./yamlgen/"
temppath="./temp/"
def generate_keys(dir):
    key_name = f"{dir}/temp_key"
    subprocess.run(["ssh-keygen", "-t", "rsa", "-b", "2048", "-N", "", "-f", key_name])
    with open(key_name, "r") as private_file:
        private_key = private_file.read().strip()
        print(private_key)
    with open(key_name+".pub", "r") as private_file:
        public_key = private_file.read().strip()
        # Delete the files

    return public_key, private_key
def create_facts(group,inventory_path,yamlpath,ansiblePrint,store_yaml):
    # Checks if a file path has been passed as an argument
    if group and inventory_path:
        file_path = inventory_path
        group = group
        yamlpath=yamlpath if (yamlpath)  else yamlpath1

        try:
            

         
            # ---------- childpr. scripts -------------
            #ssh_keygen =  generate_keys()
            password_script = r"""
#!/bin/bash
# generates a pwassword and hashes it
password=$(openssl rand -base64 32 | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
# Hashes des Passwords
hashed_password=$(echo -n "$password" | openssl passwd -6 -stdin)
#echo "$password"
echo "$hashed_password"
"""
            mac_script = r"""
#!/bin/bash
vm_name=$1
hash_value=$(echo -n "$vm_name" | sha256sum | cut -d' ' -f1)
hex_part=${hash_value:0:12}
mac_address="${hex_part:0:2}:${hex_part:2:2}:${hex_part:4:2}:${hex_part:6:2}:${hex_part:8:2}:${hex_part:10:2}"
echo "$mac_address"
"""
            # -------------PROTOTYPES-------------------
            prototypes={}
            with open(file_path, 'r') as stream:
                try:
                    prototypes = yaml.safe_load(stream)["prototypes"]["hosts"]
                except yaml.YAMLError as exc:
                    ansiblePrint.fail("error",exc)            
            # -----------------Hosts---------------------
            with open(file_path, 'r') as stream:
                try:
                    obj = yaml.safe_load(stream)[group]["hosts"]
                    ansiblePrint.log("-----------------------")
                    ansiblePrint.log(group)
                    ansiblePrint.log("-----------------------")
                    hosts=[]
                    for host,host_obj in obj.items():
                        ansiblePrint.log(host)
                        #ansiblePrint.log(obj)
                        ansiblePrint.log("  machines:")
                        #---------------Machines-----------------
                        for machine in host_obj["vars"]["machines"].split(" "):
                            with tempfile.TemporaryDirectory() as tmp_dir:
                                cname= str(host+"-"+machine)
                                ansiblePrint.log("     - "+ cname)

                                priv,pub=generate_keys(tmp_dir)
                                machineObj=copy.copy(prototypes[machine])
                                machineObj["vars"]["mac"] = subprocess.check_output(mac_script, shell=True).decode("utf-8").strip()
                                machineObj["vars"]["password"]= machineObj["vars"]["ansible_ssh_pass"]=machineObj["vars"]["ansible_become_password"]= subprocess.check_output(password_script, shell=True).decode("utf-8").strip()
                                machineObj["vars"]["private_key"]=str(priv)
                                machineObj["vars"]["public_key"]=str(pub)
                                #ansiblePrint.log(machineObj)
                                hosts.append(machineObj)
                                if(store_yaml=="True"):
                                    os.mkdir(yamlpath) if not os.path.exists(yamlpath) else None
                                    with open(f'{yamlpath}/{cname}.yaml', 'w') as f:   
                                        
                                        yamlObj= {cname:machineObj}
                                        yaml.dump(yamlObj, f, default_flow_style=False)
                                machineObj["name"]=str(cname)
                                
                except yaml.YAMLError as exc:
                    ansiblePrint.fail("error",exc)
                return hosts
        except Exception as e:
                    ansiblePrint.fail("error",e)

    else:
                    ansiblePrint.fail("No file path provided. Specify the path as an argument.","exc")

    
#yaml_data = yaml.dump(data); 
    # 'host': '$host', 
    # 'hypervisor': '$hypervisor', 
    # 'password': '$pass', 
    # 'ip': '0.0.0.0', 
    # 'mac': '$mac', 
    # 'proxmox_pass': 
    # '$proxmox_pass', 
    # 'proxmox_user': 
    # 'root', 
    # 'proxmox_ip': '0.0.0.0'
