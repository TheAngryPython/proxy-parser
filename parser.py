try:
    import requests, re, argparse
    from bs4 import BeautifulSoup
    import sys
except:
    print('try: pip3 install -r req.txt')
parser = argparse.ArgumentParser(description='Proxy parser from http://foxtools.ru/Proxy, by @EgTer, channel @codepo')
parser.add_argument('-pl', action='store', dest='pl', help='PAGE LIMIT')
parser.add_argument('-ap', action='store', dest='ap', help='SAVE ALL PROXIES')
parser.add_argument('-gp', action='store', dest='gp', help='SAVE GOOD PROXIES')
parser.add_argument('-s', action='store', dest='s', help='SITE TO CHECK')
parser.add_argument('-tl', action='store', dest='tl', help='TIMEOUT LIMIT')
parser.add_argument('--nooutput', action='store_const', const=True, dest='out', help='TOGGLE OUTPUT')
argv = sys.argv
try:
    argv.remove(__file__)
except:
    pass
prs = parser.parse_args(argv)
if prs.out:
    def print(*a,**k):
        pass
print('by @EgTer, channel @codepo')
lst = []
for pg in range(1, int(prs.pl or input('PAGE LIMIT (4, see http://foxtools.ru/Proxy): ') or 4) + 1):
    curri = pg
    if curri != 1:
        print('\b' * len(str(curri - 1)), end='', flush=True)
        print(curri, end='', flush=True)
    else:
        print('GETTING PAGE', curri, end='', flush=True)
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
    print('SUCCESS')
# print(lst)
f = open(prs.ap or (input('SAVE ALL PROXIES TO (all_proxies.txt): ') or 'all_proxies.txt'), 'w')
f.write(str(lst))
f.close()
ln = len(lst)
site = prs.s or (input('SITE TO CHECK (http://eth0.me): ') or 'http://eth0.me')
t = int(prs.tl or (input('timeout limit (2): '.upper()) or 2))
print(f'CHECKING START ({ln})')
def proxy_check(proxy, timeout=2, site="http://eth0.me"):
    try:
        rwww = requests.get(site, timeout=timeout, proxies={proxy['type']: proxy['ip']+':'+proxy['port']})
        if rwww.status_code == 200:
            return (True, rwww.elapsed.total_seconds())
        else:
            pass
    except:
        return (False)
good = []
i = 1
for pr in lst:
    try:
        print('CHECKING', pr['type']+'://'+pr['ip']+':'+pr['port'], i, 'OF', ln, end='. ')
        ch = proxy_check(pr, timeout=t, site=site)
        if ch[0]:
            pr['uptime'] = ch[1]
            good.append(pr)
            print(f'GOOD PROXY (UPTIME {ch[1]}), ADDED')
        else:
            print('TIMED OUT, NOT ADDED')
    except Exception as e:
        print('ERROR, SKIP', e)
    i += 1
f = open(prs.gp or (input('SAVE GOOG PROXIES TO (good_proxies.txt): ') or 'good_proxies.txt'), 'w')
# print(good)
f.write(str(good))
f.close()
print(f'END, TOTAL {len(good)} PROXIES.')