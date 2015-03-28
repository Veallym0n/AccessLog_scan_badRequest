## scan bad request from Access_log ##

```
vim config.py
```
for simply configures, and then run
 
```
python scan.py
```

this script will find the bad Request(almost like attacks log) in the access log.

like this

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