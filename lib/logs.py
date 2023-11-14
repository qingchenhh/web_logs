import re,os
from html import escape

def logs(logpath):
    if not os.path.exists(logpath):
        print("[-] 找不到日志文件！")
        exit()
    re_req_path = re.compile('"[A-Z]+ (?P<request_path>.*) HTTP/')
    re_req_method = re.compile('"(?P<request_method>[A-Z]+) ')
    re_req_ua = re.compile('" "(?P<request_ua>.*)"$')
    re_req_time = re.compile('(?P<request_time>\[.+?\])')
    re_req_referer = re.compile('[0-9]+ "(?P<request_referer>.*)" "')
    re_status_code = re.compile('HTTP/[1-2]\.[0-9]" (?P<status_code>[0-9]+) ')
    # re_rep_length = re.compile('[0-9]+ (?P<rep_length>[0-9-]+) "')
    re_req_ip = re.compile('(?P<req_ip>^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}) ')

    log_list = []
    error_list = []
    print("[*] 正在处理nginx日志，请稍后...")
    with open(logpath,mode='r',encoding='utf-8') as f:
        for i in f:
            try:
                dic = {}
                temp = i.replace('\n','')
                dic['original_log'] = temp
                dic['request_method'] = re_req_method.search(temp).group('request_method')
                dic['request_path'] = re_req_path.search(temp).group('request_path')
                dic['status_code'] = re_status_code.search(temp).group('status_code')
                # dic['rep_length'] = re_rep_length.search(temp).group('rep_length')
                dic['request_ip'] = re_req_ip.search(temp).group('req_ip')
                try:
                    dic['request_ua'] = re_req_ua.search(temp).group('request_ua')
                except Exception as e:
                    dic['request_ua'] = ""
                dic['request_time'] = re_req_time.search(temp).group('request_time')
                try:
                    dic['referer'] = re_req_referer.search(temp).group('request_referer')
                except Exception as e:
                    dic['referer'] = ""

                log_list.append(dic)
            except Exception as e:
                error_list.append(escape(temp))
                # print("日志处理出错！报错日志：",temp,"，报错信息：",e)
    return log_list,error_list

if __name__ == '__main__':
    pass
    # log_list,error_list = logs(r"E:\Python3\qc\web_logs\test\access.log")
    # for i in log_list:
    #     print(i['request_ua'])