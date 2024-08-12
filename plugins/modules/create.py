# ji_podhead/host_prototypes/utils/generate_mac_adress.py

DOCUMENTATION = '''
---
module: generate_mac_adress
short_description: Generiert eine MAC-Adresse
description:
    - Generiert eine zufällige MAC-Adresse
options:
    - name:
        description:
            - Der Name der MAC-Adresse
        required: true
        type: str
author:
    - Ihr Name
'''
#!/usr/bin/env python3
import os

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native
from ..module_utils.prototype_facts import  create_facts as pf
class AnsiblePrint:
    def __init__(self, module):
        self.status = {"log":[], "return":None}
        self.module = module

    def log(self, string):
        string = str(string)
        self.status["log"].append(string)
        self.module.log(string)
        # self.module.info(string)

    def fail(self, msg, err):
        self.status["return"] = {"type": "Error", "value": err}
        to_native(self.status)
        self.module.fail_json(msg=msg)

def main():
    module = AnsibleModule(
        argument_spec=dict(
            yaml_path=dict(required=False),  
            group=dict(required=True),
            inventory_path=dict(required=True),
            store_yaml=dict(required=False),
        ),
        required_together=[
            ('group')
        ],
    )
    try:
        ansiblePrint = AnsiblePrint(module=module)
        module_path = os.path.dirname(__file__)
        ansiblePrint.log(module_path)
        params=module.params
        store_yaml = params['store_yaml'] if params['store_yaml'] else False #eigentlich unnötig wegen defaults
        yaml_path = params['yaml_path'] if params['yaml_path'] else "./yamlgen/"
        group = params['group']
        inventory_path = params['inventory_path']
        ansiblePrint.status["return"]=pf(group=group,inventory_path=inventory_path,yamlpath=yaml_path,ansiblePrint=ansiblePrint,store_yaml=store_yaml)
    except Exception as e:
        ansiblePrint.fail("error",e) 
    module.exit_json(result=ansiblePrint.status)
    module._log_to_syslog


if __name__ == "__main__":
    main()