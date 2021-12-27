from http.cookiejar import CookieJar
from urllib.request import Request, urlopen
import urllib
from bs4 import BeautifulSoup


site = 'https://www.nfe.fazenda.gov.br/portal/informe.aspx?ehCTG=false'
# site = 'https://www.cte.fazenda.gov.br/portal/listaConteudo.aspx?tipoConteudo=Y0nErnoZpsg='

# hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
hdr = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'gzip, deflate, sdch','Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'}

cj = CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
req = Request(site, None, {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'gzip, deflate, sdch','Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'})

page = opener.open(req)
soup = BeautifulSoup(page.read(), features="html.parser")

noticias_relacao = soup.find_all("div", attrs={"class": "divInforme"})
for noticia in noticias_relacao:
    all_p = noticia.find_all("p")
    for p in all_p:
        print(p.text.strip())
