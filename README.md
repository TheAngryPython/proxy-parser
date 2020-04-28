# proxy-parser
Proxy parser from http://foxtools.ru/Proxy, by @EgTer, channel @codepo

optional arguments:

  -h, --help  show this help message and exit

  -pl PL      PAGE LIMIT

  -ap AP      SAVE ALL PROXIES

  -gp GP      SAVE GOOD PROXIES

  -s S        SITE TO CHECK

  -tl TL      TIMEOUT LIMIT

  --nooutput  TOGGLE OUTPUT

  --check TOGGLE CHECK

# Example

python parser.py -pl 4 -ap all.txt -gp good.txt -s http://eth0.me -tl 2
