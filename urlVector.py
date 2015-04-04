import re
import sys
import urlparse
import uparse
import hashlib
import urllib


class matchChinese:
    def findall(self,s):
        try:
            for charset in ['utf8','gb18030']
            us = s.decode(charset,'replace')
            if re.findall(ur'^[0-9a-zA-Z_\u2019-\u2020\u2e80-\u9fff+\s\uff01-\ufff99]+$',us):
                return True
            else:
                return False
        except:
            return False


class IsBase64:
    def findall(self,s):
        s = s.strip()
        if len(s)<24: return False
        if len(s) % 8!=0: return False
        try:
            if filter(lambda x:ord(x)>128,s.decode('base64')):
                return False
        except:
            return False
        return True


regexps = [
            (re.compile(r'^\d{4}-0\d-0\d$'),'date'),
            (re.compile(r'^\d{4}-1[0-2]-([1-2][0-9]|3[0-1])$'),'date'),
            (re.compile(r'^\d{2}:\d{2}:\d{2}$'),'Time'),
            (re.compile(r'^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}$'),'datetime'),
            (re.compile(r'^http(s)?(://|%3(A|a)%2(F|f))'),'Url'),
            (re.compile(r'^(13|15|18|17)\d{9}$'), 'MobileNumber'),
            (re.compile(r'^[0-9a-zA-Z\._]+(\@|%40)[0-9a-zA-Z\-\.]'), 'Mail'),
            (re.compile(r'[0-9a-zA-Z_\-\s\(\)]+\.([a-zA-Z]{2,4})'),'File'),
            (re.compile(r'^([0-9a-fA-F]{32}|[0-9a-fA-F]{16}|[0-9a-fA-F]{40})$'), 'Hash'),
            (re.compile(r'^([0-9a-fA-F\-]{36}|[0-9a-fA-F\-]{20}|[0-9a-fA-F\-]{44})$'), 'UUID'),
            (re.compile(r'^jQuery\d+_\d+$'),'JQuery'),
            (re.compile(r'^(14)\d{11}$'), 'Timestamp'),
            (re.compile(r'^\d+(\.\d+)?$'), 'Number'),
            (re.compile(r'^(-)\d+(\.\d+)?$'),'unsignedNumber'),
            (re.compile(r'^(\d+[,|_\-])+\d+$'),'NumberWithSplit'),
            (re.compile(r'^[a-zA-Z]+$'), 'Letter'),
            (re.compile(r'^[a-zA-Z_]+$'),'LetterWithUline'),
            (re.compile(r'^[0-9]+[A-Za-z]+$'), 'NumLet'),
            (re.compile(r'^[A-Za-z]+[0-9]+$'), 'LetNum'),
            (re.compile(r'^[A-Za-z0-9]+(_|-)[A-Za-z0-9]+$'), 'WordsWithUline'),
            (re.compile(r'^[A-Za-z0-9]+\s+[A-Za-z0-9]+$'), 'Words'),
            (matchChinese(),'Chinese'),
            (IsBase64(),'Base64')
          ]



def get_exp(s):
    if s=='': return ''
    for reg in regexps:
        if reg[0].findall(s): return reg[1]
    return 'mix'


def directory_exp(dirlist):
    dirExp = ''
    for dir in dirlist:
        if dir.isdigit():
            dirExp+='N/'
        else:
            dirExp+='L'+str(len(dir))+'/'
    return dirExp

        
def filename_exp(s):
    fnExp = []
    if '-' in s:
        for i in s.split('-'): fnExp.append(get_exp(i))
    elif '_' in s:
        for i in s.split('_'): fnExp.append(get_exp(i))
    else:
        fnExp=get_exp(s)
    return fnExp


def get_url_vector(url,pqs=True):
    uriVectorList = []

    parsedURL = urlparse.urlparse(url)
    hostName = parsedURL.hostname
    pathEndsWithFolder = parsedURL.path.endswith('/')

    pathList = [ i for i in parsedURL.path.split('/') if i ]

    pathDepth = parsedURL.path.count('/')
    pathExp = ''
    if pathDepth:
        pathExp = directory_exp(pathList)
    else:
        pathEndsWithFolder  = True

    if pathEndsWithFolder or not pathDepth:
        filenameExp = filename = fileExt = ''
        filenameLen = 0
    else:
        theFile = pathList[-1].rsplit('.',1)
        filename = theFile[0]
        filenameLen = len(filename)
        fileExt = ''
        if len(theFile)>1:
            fileExt = theFile[1]
        filenameExp = filename_exp(filename)

    uriVectorList.extend((hostName, pathDepth, pathEndsWithFolder, filenameLen,filenameExp,fileExt,pathExp))
    urlVector = hashlib.md5(str(uriVectorList)).hexdigest()

    if pqs:
        return urlVector+'?'+urllib.urlencode(map(lambda x:(x[0],get_exp(x[1])),uparse.parse_qsl(parsedURL.query)))
    else:
        return urlVector




if __name__=='__main__':
    print get_url_vector('http://www.kevin1986.com/this/is/a/url/sample/by/kevin/1986?name=kevin&email=kevin@kevin1986.com&website=http://www.kevin1986.com')


