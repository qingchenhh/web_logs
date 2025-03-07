web日志分析工具，只能分析nginx、apache默认的日志。

因为很多攻击是POST请求的，没法记录，分析攻击日志没有意义！！！

实际应急中会根据异常行为，来做判断，然后根据时间来查看日志，结合安全设备来溯源。

单纯的分析日志里的攻击日志没有意义。

用法：

```
usage: main.py [-h] -lp LOGPATH

options:
  -h, --help            show this help message and exit
  -lp LOGPATH, --logpath LOGPATH
                        指定日志文件的路径，支持（apache、nginx默认日志）。
```

