import sys, os, time, re, json, urlparse
import config
import urlVector
import uparse
from itertools import groupby

urldb = {}


httpre = re.compile(config.combined_format_re)


def serialization(log):
    sLog = list(httpre.findall(log)[0])
    if not sLog[4].startswith('http://'):
        sLog[4]='http://localsite'+sLog[4]
    r = dict(zip(config.combined_format_tag,sLog))
    for process in config.urlprocess:
        r['url'] = re.sub(process[0],process[1],r['url'])
    return r


def log_filter(log):
    if log['method'] not in ('POST','GET'): return False
    if log['code'] in config.filter_code: return False

    parsedURL = urlparse.urlparse(log['url'])
    if parsedURL.query == '': return False
    if '=' not in parsedURL.query: return False
    if filter(parsedURL.path.endswith, config.filter_suffix): return False
    if re.findall(r'(%3C|<)+[a-z]+\s+.*(%3E|>)+',parsedURL.path, re.I): return False
    if re.findall(r'&amp;[0-9a-zA-Z_\.]+=',parsedURL.query): return False

    return True


def Analysis(datas):
    global urldb
    for vector in datas:
        urldb.setdefault(vector, {'count':0,'urls':{},'args':{}})
        urldb[vector]['count'] += 1
        for log, paras in datas[vector]:
            for kv in [i for i in uparse.parse_qsl(paras) if i]:
                argString = "%s=%s" % kv
                urldb[vector]['args'].setdefault(argString, 0)
                urldb[vector]['args'][argString] += 1
                bestMatch,currentMatch = db_get_key_value(vector, kv)
                if kv != bestMatch[0][0].split('=', 1) and kv[1] == 'mix' and currentMatch[0][1] < config.Alert_Percent:
                    print '-' * 100
                    print 'Excepted Request:'
                    for item in log.items():
                        print '{0:8}\t{1}'.format(item[0], item[1].strip())
                    print 'Best', bestMatch[0], 'Percent', bestMatch[1],'%'
                    print 'Curr', currentMatch[0][0],'Percent',currentMatch[0][1], '%'
                    print '-' * 100
                    if not isinstance(log['url'], unicode):
                        log['url'] = unicode(log['url'], errors='ignore')
                    open(config.attack_log,"a+").write(json.dumps({'log':log, 'best':bestMatch, 'current':currentMatch[0]})+'\n')

            if len(urldb[vector]['urls'])<10:
                uri = log['url'].split('?',1)[0]
                urldb[vector]['urls'].setdefault(uri, {'count':0,'example':log['url']})
                urldb[vector]['urls'][uri]['count'] += 1


def db_get_key_value(hash,kv):
    args = urldb[hash]['args'].items()
    fetches = [i for i in args if i[0].startswith(kv[0]+'=')]
    allCount = sum(map(lambda x:x[1], fetches))
    percent = map(lambda x:(x, round(x[1]/float(allCount)*100,3)), fetches)
    bestMatch = max(percent,key = lambda x:x[1])
    currentMatch = [i for i in percent if i[0][0] == '%s=%s' % kv]
    return bestMatch, currentMatch



def get_rdd_result(r):
    return dict(
            map(lambda x:(x[0],
                map(lambda n:n[1],list(x[1]))),
                    groupby(
                        sorted(
                            map(lambda x:(x[1][0],(x[0],x[1][1])),
                                map(lambda x:(x, urlVector.get_url_vector(x['url'],True).split('?')),
                                    filter(log_filter,
                                        map(serialization,r)
                                        )
                                    )
                                ),key=lambda x:x[0]
                            ),
                            key=lambda x:x[0]
                        )
                    )
                )


def run():
    Analysis(get_rdd_result(open(config.access_log).read().splitlines()))



if __name__=='__main__':
    run()
