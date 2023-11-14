import re

def mathing(rules,log_list):
    print("[*] 正在匹配规则，请稍后...")
    fall = False
    all_dic = {}
    ip_list = []
    for rule in rules:
        all_dic[rule['family']] = {}
        all_dic[rule['family']]['name'] = rule['name']
        all_dic[rule['family']]['class'] = {}
        for i in rule['poc']:
            all_dic[rule['family']]['class'][i['name']] = []
    # print(all_dic)
    for log in log_list:
        for rule in rules:
            for poc in rule['poc']:
                tmp_rule = ""
                tmp_ua = ""
                all_flag = False
                rule_flag = False
                method_flag = False
                ua_flag = False
                if poc['method'] == "" or poc['method'] == log['request_method']:
                    method_flag = True
                if poc['ua'] != "" and log['request_ua'] != "":
                    if re.search(poc['ua'], log['request_ua'],flags=re.IGNORECASE):
                        tmp_ua = re.search(poc['ua'],log['request_ua'],flags=re.IGNORECASE).group()
                        ua_flag = True
                else:
                    ua_flag = True

                if poc['rule'] != []:
                    if poc['matching'] == "regex":
                        if poc['iscase'] == "true":
                            for r in poc['rule']:
                                if re.search(r,log['request_path']):
                                    tmp_rule = re.search(r,log['request_path']).group()
                                    rule_flag = True
                                    # print(tmp_rule)
                                    break
                                elif re.search(r,log['request_ua']) and poc['ismatchua'] == True:
                                    tmp_ua = re.search(r, log['request_path']).group()
                                    # print(tmp_rule)
                                    rule_flag = True
                                    break
                        else:
                            for r in poc['rule']:
                                # print(r)
                                if re.search(r,log['request_path'],flags=re.IGNORECASE):
                                    tmp_rule = re.search(r,log['request_path'],flags=re.IGNORECASE).group()
                                    rule_flag = True
                                    # print(tmp_rule)
                                    break
                                elif re.search(r,log['request_ua'],flags=re.IGNORECASE) and poc['ismatchua'] == True:
                                    tmp_ua = re.search(r, log['request_ua'],flags=re.IGNORECASE).group()
                                    # print(tmp_rule)
                                    rule_flag = True
                                    break
                    else:
                        if poc['iscase'] == "true":
                            for r in poc['rule']:
                                if (log['request_path'].find(r) != -1) or ((log['request_ua'].find(r) != -1) and poc['ismatchua'] == True):
                                    tmp_rule = r
                                    rule_flag = True
                                    break
                        else:
                            for r in poc['rule']:
                                if (log['request_path'].lower().find(r.lower()) != -1) or ((log['request_ua'].lower().find(r.lower()) != -1) and poc['ismatchua'] == True):
                                    tmp_rule = r
                                    rule_flag = True
                                    break
                else:
                    rule_flag = True


                if rule_flag and method_flag and ua_flag and (poc['rule'] != [] or poc['ua'] != "" or poc['method'] != ""):
                    if (poc['rule']==[] and poc['method'] == "" and log['request_ua'] == ""):
                        continue
                    if log['request_ip'] not in ip_list:
                        ip_list.append(log['request_ip'])
                    tmp_dic = {}
                    tmp_dic['time'] = log['request_time']
                    tmp_dic['ip'] = log['request_ip']
                    if poc['method'] == log['request_method'] and poc['rule'] == [] and poc['ua'] == "":
                        tmp_dic['method'] = '<span style="background:#fd0;color:#ff0000;">'+log['request_method']+'</span>'
                    else:
                        tmp_dic['method'] = log['request_method']
                    tmp_dic['ua'] = log['request_ua']
                    tmp_dic['path'] = log['request_path']
                    if tmp_rule != "":
                        tmp_dic['path'] = log['request_path'].replace(tmp_rule,'<span style="background:#fd0;color:#ff0000;">'+tmp_rule+'</span>')
                    if tmp_ua != "":
                        tmp_dic['ua'] = log['request_ua'].replace(tmp_ua,'<span style="background:#fd0;color:#ff0000;">'+tmp_ua+'</span>')

                    tmp_dic['ua'] = tmp_dic['ua'].replace("<","&lt;")
                    tmp_dic['ua'] = tmp_dic['ua'].replace(">", "&gt;")
                    tmp_dic['path'] = tmp_dic['path'].replace("<", "&lt;")
                    tmp_dic['path'] = tmp_dic['path'].replace(">", "&gt;")
                    tmp_dic['ua'] = tmp_dic['ua'].replace("&lt;span style=", "<span style=")
                    tmp_dic['ua'] = tmp_dic['ua'].replace('#ff0000;"&gt;','#ff0000;">')
                    tmp_dic['ua'] = tmp_dic['ua'].replace("&lt;/span&gt;", "</span>")
                    tmp_dic['path'] = tmp_dic['path'].replace("&lt;span style=", "<span style=")
                    tmp_dic['path'] = tmp_dic['path'].replace('#ff0000;"&gt;', '#ff0000;">')
                    tmp_dic['path'] = tmp_dic['path'].replace("&lt;/span&gt;", "</span>")

                    tmp_dic['original_log'] = log['original_log']
                    tmp_dic['status_code'] = log['status_code']
                    if int(log['status_code']) in poc['status_code']:
                        tmp_dic['success'] = 'success'
                        if fall != True:
                            fall = poc['isfall']
                    else:
                        if log['status_code'] == "404":
                            tmp_dic['success'] = "fail"
                        else:
                            tmp_dic['success'] = "ambiguity"
                    # print(tmp_dic['ua'])
                        # print(tmp_dic)
                    all_dic[rule['family']]['class'][poc['name']].append(tmp_dic)
                    # print(all_dic[rule['family']]['name'])
    return all_dic,fall,ip_list
