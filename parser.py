try:
    import requests, re, argparse, sys, json
    from bs4 import BeautifulSoup
except:
    print('try: pip3 install -r req.txt')
parser = argparse.ArgumentParser(description='Proxy parser from http://foxtools.ru/Proxy, by @EgTer, channel @codepo')
parser.add_argument('-pl', '--page_limit', action='store', dest='pl', help='page load limit')
parser.add_argument('-ap', '--all', action='store', dest='ap', help='save proxy in')
parser.add_argument('-gp', '--good', action='store', dest='gp', help='save good proxy in')
parser.add_argument('-s', '--site', action='store', dest='s', help='site to check')
parser.add_argument('-tl', '--timeout', action='store', dest='tl', help='timeout limit')
parser.add_argument('-c', '--check', action='store', dest='c', help='turn off proxy checking y/n')
parser.add_argument('-n', '--nooutput', action='store_const', const=True, dest='out', help='turn off output')
argv = sys.argv
try:
    argv.remove(__file__)
except:
    pass
prs = parser.parse_args(argv)
if prs.out:
    def print(*a,**k):
        pass
if prs.c not in ['y', 'n', None]:
    print('check - y or n')
    exit(0)
if prs.c == 'n':
    chk = False
else:
    chk = True
print('by @EgTer, channel @codepo')
lst = []
for pg in range(1, int(prs.pl or input('page load limit (4, see http://foxtools.ru/Proxy): ') or 4) + 1):
    curri = pg
    if curri != 1:
        print('\b' * len(str(curri - 1)), end='', flush=True)
        print(curri, end='', flush=True)
    else:
        print('loading page', curri, end='', flush=True)
    r = requests.get("http://foxtools.ru/Proxy?page="+str(pg))
    types = ['http', 'https']
    soup = BeautifulSoup(r.text, 'lxml')
    s = soup.find_all("tr")
    for tr in s:
        soup2 = BeautifulSoup(str(tr), 'lxml')
        s2 = soup2.find_all("td")
        curr = {}
        for td in s2:
            result = re.findall(r'[0-9]\w+.[0-9]\w+.[0-9]\w+.[0-9]\w+', td.text)
            tp = False
            for t in types:
                if td.text.lower().find(t) != -1:
                    tp = True
                    tt = t
            try:
                intt = int(td.text)
            except:
                intt = 0
            if result != []:
                curr['ip'] = result[0]
            elif 60 < intt < 60000:
                curr['port'] = td.text
            elif tp:
                curr['type'] = tt
        if curr != {}:
            lst.append(curr)
else:
    print('\b' * len(str(curri - 1)), end='', flush=True)
    print('completed')

while True:
    p = 0
    for i in range(len(lst)):
        try:
            lst[i]['type']
            lst[i]['ip'].split('.')[3]
            int(lst[i]['port'])
        except:
            del lst[i]
            p += 1
            break
    if p == 0:
        break

f = open(prs.ap or (input('save proxy in (all_proxies.txt): ') or 'all_proxies.txt'), 'w')
f.write(json.dumps(lst))
f.close()
if chk and (prs.c == 'y' or ((input('check proxies? [Y/N] (Y): ').lower() or 'y') == 'y')):
    ln = len(lst)
    site = prs.s or (input('site to check (http://eth0.me): ') or 'http://eth0.me')
    t = float(prs.tl or (input('timeout limit (2): ') or 2))
    print(f'check started ({ln})')
    def proxy_check(proxy, timeout=2, site="http://eth0.me"):
        try:
            rwww = requests.get(site, timeout=timeout, proxies={proxy['type']: proxy['ip']+':'+proxy['port']})
            if rwww.status_code == 200:
                return (True, rwww.elapsed.total_seconds())
            else:
                return (False, rwww.elapsed.total_seconds())
        except requests.ConnectTimeout:
            return (False, -1)
        except Exception as e:
            return (False, -2, str(e))
    good = []
    i = 1
    for pr in lst:
        try:
            ch = proxy_check(pr, timeout=t, site=site.format(ip=str(pr['ip']), port=str(pr['port']), type=str(pr['type'])))
            if ch[0]:
                print('check', pr['type']+'://'+pr['ip']+':'+pr['port'], i, 'in', ln, end='. ')
                pr['uptime'] = ch[1]
                good.append(pr)
                print(f'good proxy (uptime {ch[1]}), added')
            elif ch[1] == -2:
                print('error, not added', ch[2])
            elif ch[1] == -1:
                print('timed out, not added')
        except Exception as e:
            print('error, skip', e)
        i += 1
    f = open(prs.gp or (input('keep good proxies in (good_proxies.txt): ') or 'good_proxies.txt'), 'w')
    # print(good)
    f.write(json.dumps(good))
    f.close()
    print(f'end, total {len(good)} proxies.')
else:
    print('end.')
