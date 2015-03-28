# access log path
access_log = 'access_log'

# log format. 
combined_format_re = r'''(\d+\.\d+\.\d+\.\d+)\s-\s(.*)\s\[(\d+/\w+/\d{4}:\d{2}:\d{2}:\d{2}\s[+-]\d{4})\]\s"(\w+)\s(.*)\s(HTTP/\d+\.\d+)"\s(\d{3})\s(\d+)\s"(.*)"\s"(.*)"'''
combined_format_tag = ('ip','user','time','method','url','protocol','code','size','ref','ua')


# filted http status code
filter_code = ('404','502','503','204','206','501','302','301') 

# filted filename suffix
filter_suffix = ('css', 'js', 'jpg', 'tif', 'gif', 'jpeg', 'png', 'ico', 'webp', 'htm', 'html', '7z', 'tar', 'tgz', 'gz', 'rar', 'zip', 'csv', 'xls', 'xlsx', 'doc', 'docx', 'wav', 'swf', 'asf', 'mp3', 'wma', 'fla', 'flv', 'rmvb', 'avi', 'mpeg', 'mpg')

# alert_percent should between 0 to 100
Alert_Percent = 10

# attack_log filename
attack_log = 'attack.log'

# somekind of wilddomain can be parsed here
# etc, (r'''.*\.example\.com''','*.example.com')
urlprocess = [
        (r'''(qq-pf-to=[^&]+)''','')
        ]
