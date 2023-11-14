import argparse
from lib.yml import yml
from lib.logs import logs
from lib.matching import mathing
from lib.output import outhtml
import os,time

start_time = int(time.time())
def myargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-lp','--logpath',dest="logpath",required=True, type=str,help="指定日志文件的路径，支持（apache、nginx默认日志）。")

    return parser.parse_args()

def run():
    args = myargs()
    logpath = args.logpath
    rules = yml()
    log_list, error_list = logs(logpath)
    all_dic,fall,ip_list = mathing(rules,log_list)
    outhtml(all_dic,error_list,fall,ip_list)


if __name__ == '__main__':
    run()
    end_time = int(time.time())
    print("[+] 程序执行完毕！程序执行了"+str((end_time - start_time))+"秒。")
