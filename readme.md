## scan bad request from Access_log ##

**About**
 
```
vim config.py
```

for simply configures, 

首先先配置些个参数，比如

	+ 需要扫描的日志文件
	+ 日志格式
	+ 输出记录文件
	+ 报警百分比
	+ url预处理条件

 
 and then run
 
 然后走着
 
```
python scan.py
```

this script will find the bad Request(almost like attacks log) in the access log.

就能把那些参数中存在问题的URL给跑出来。基本就是个统计比值，找出阈值以下的那些东西。

代码很挫，属于边看动画边写的那种，就将就好了。


like this

结果是这样的

```
----------------------------------------------------------------------------------------------------
Excepted Request:
code    	200
protocol	HTTP/1.1
url     	http://localsite/photo/show.php?userid=9%27%20and%20-1%20union%20select%20version%28%29,1,1,1,1,1,%25%23&photoname=hello
ip      	192.168.1.2
ua      	Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;AS.Heimdall.111111)
user    	-
time    	29/Jan/2015:19:14:04 +0800
ref     	http://www.kevin1986.com:80/photo/
method  	GET
size    	160
Best (u'userid=Number', 49) Percent 98.0 %
Curr (u'userid=mix', 1) Percent 2.0 %
----------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------
Excepted Request:
code    	200
protocol	HTTP/1.1
url     	http://localsite/photo/show.php?userid=9%27%20and%20-1%20union%20select%20version%28%29,1,1,1,1,1,%25%23&photoname=hello
ip      	192.168.1.2
ua      	Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;AS.Heimdall.111111)
user    	-
time    	29/Jan/2015:19:14:04 +0800
ref     	http://www.kevin1986.com:80/photo/
method  	GET
size    	160
Best (u'userid=Number', 109) Percent 98.198 %
Curr (u'userid=mix', 2) Percent 1.802 %
----------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------
Excepted Request:
code    	200
protocol	HTTP/1.1
url     	http://localsite/photo/show.php?userid=9%27%20and%20-1%20union%20select%20version%28%29,1,1,1,1,1,%25%23&photoname=hello
ip      	192.168.1.2
ua      	Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;AS.Heimdall.111111)
user    	-
time    	29/Jan/2015:19:14:04 +0800
ref     	http://www.kevin1986.com:80/photo/
method  	GET
size    	160
Best (u'userid=Number', 169) Percent 98.256 %
Curr (u'userid=mix', 3) Percent 1.744 %
----------------------------------------------------------------------------------------------------
```