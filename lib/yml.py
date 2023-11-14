import yaml
import os

def yml():
    print("[*] 正在提取规则列表，请稍后...")
    if os.path.exists('rules/rules.yml'):
        with open(r'rules/rules.yml','r',encoding='utf-8') as rf:
            yaml_rules = yaml.load(rf,Loader=yaml.SafeLoader)
    else:
        print("[-] 找不到规则文件！！！")
        exit()
    return yaml_rules['rules']
