
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myjarvisbot.settings")


from io import BytesIO
from urllib.request import Request, urlopen
import time

from bs4 import BeautifulSoup
from decouple import config
import json
import requests as r
import rows



def exists_reported(title):
    from myjarvisbot.jarvis.models import NewsReported
    news = NewsReported.objects.filter(title=title[:100])
    return news.count() > 0


def add_title(title):
    from myjarvisbot.jarvis.models import NewsReported
    news = NewsReported(title=title[:100])
    news.save()

hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
url_horn = "https://integram.org/webhook/"+config('WEBHOOK')
url_hornC4 = "https://integram.org/webhook/"+config('WEBHOOK_C4')

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

##### Monitor data tabela IBPT - github ######
sites_monitor = [{'site': "https://github.com/frones/ACBr/tree/master/Exemplos/ACBrTCP/ACBrIBPTax/tabela", 'doc':'Tabela IBPT'}]

for site in sites_monitor:
    req = Request(site['site'], headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, features="html.parser")
    noticias_relacao = soup.find_all("div", attrs={"class": "Box-header"})
    titulo = 'ACBrIBPTax'
    for noticia in noticias_relacao:
        all_a = noticia.find_all("a", attrs={"class": "Link--primary"})
        for a in all_a:
            titulo = titulo+' '+a.text.strip()
            break

        all_a = noticia.find_all("a", attrs={"class": "Link--secondary"})
        for a in all_a:
            titulo = titulo + ' ' + a.text.strip()

        if exists_reported(titulo):
            continue

        conteudo = titulo
        url = site['site']
        data = {"text": f'{titulo}\n{conteudo}\n{url}\n'}
        print(data)

        add_title(titulo)

        r.post(url_hornC4, json=data, headers=headers)
        time.sleep(5.0)

##### Monitor NFC-e SC ######

sites_monitor = [{'site': "http://www.sef.sc.gov.br/servicos/servico/136", 'doc':'NFC-e'}]

for site in sites_monitor:
    req = Request(site['site'], headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, features="html.parser")

    noticias_relacao = soup.find_all("div", attrs={"class": "panel-body"})
    for noticia in noticias_relacao:
        all_p = noticia.find_all("p")
        for p in all_p:
            a = p.find("a")
            if a:
                titulo = site['doc']+' '+a.text.strip()
            else:
                continue

            conteudo = p.text.strip().replace(titulo, '')
            url = site['site']
            data = {"text": f'{titulo}\n{conteudo}\n{url}\n'}

            if exists_reported(titulo):
                continue

            add_title(titulo)

            r.post(url_hornC4, json=data, headers=headers)
            time.sleep(5.0)


##### Monitor SEFAZ ######
hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}

sites_monitor = [{'site': "https://www.nfe.fazenda.gov.br/portal/listaConteudo.aspx?tipoConteudo=tW+YMyk/50s=", 'doc':'NF-e'},
                 {'site': "https://www.cte.fazenda.gov.br/portal/listaConteudo.aspx?tipoConteudo=Y0nErnoZpsg=", 'doc':'CT-e'}]

for site in sites_monitor:
    req = Request(site['site'], headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, features="html.parser")

    noticias_relacao = soup.find_all("div", attrs={"class": "indentacaoNormal"})
    for noticia in noticias_relacao:
        all_p = noticia.find_all("p")
        for p in all_p:
            span = p.find("span", attrs={"class": "tituloConteudo"})
            if span:
                titulo = site['doc']+' '+span.text.strip()
            conteudo = p.text.strip().replace(titulo, '')      
            url = site['site']
            data = {"text": f'{titulo}\n{conteudo}\n{url}\n'}
    
            if exists_reported(titulo):
                continue

            add_title(titulo)

            r.post(url_hornC4, json=data, headers=headers)
            time.sleep(5.0)

            


sites_monitor = [{'site':'https://dfe-portal.svrs.rs.gov.br/Mdfe/Documentos', 'doc':'MDF-e'},
                 {'site':'https://dfe-portal.svrs.rs.gov.br/Mdfe/Avisos', 'doc':'MDF-e'}]

for site in sites_monitor:
    req = Request(site['site'], headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, features="html.parser")

    noticias_relacao = soup.find_all("article", attrs={"class": "conteudo-lista__item clearfix"})
    for noticia in noticias_relacao:
        h2 = noticia.find("h2", attrs={"class": "conteudo-lista__item__titulo"})
        titulo = site['doc']+' '+h2.text.strip()
        conteudo = noticia.find("p").text.strip()
        url = site['site']
        data = {"text": f'{titulo}\n{conteudo}\n{url}\n'}

        if exists_reported(titulo):
            continue

        add_title(titulo)

        r.post(url_hornC4, json=data, headers=headers)
        time.sleep(5.0)


# issue_data = {
#     "name": titulo,
#     "body": conteudo,
# }

# github_hdr = {
#     'Authorization': 'token '+GITHUB_TOKEN,
#     'User-Agent': 'Awesome-Octocat-App',
#     'Accept': 'application/vnd.github.inertia-preview+json'
# }
# card = r.post(url_github, json=issue_data, headers=github_hdr)
# print(card)


######  RADIO RURAL   #######

site = "http://www.radiorural.com.br/noticias/"
hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
req = Request(site, headers=hdr)
page = urlopen(req)
soup = BeautifulSoup(page, features="html.parser")


noticias_relacao = soup.find_all("div", attrs={"class":"box_noticias_relacao"})

for noticia in noticias_relacao:
    titulo = noticia.find("div", {"class": "linha_titulo"}).text.strip()
    if exists_reported(titulo):
        continue
    
    add_title(titulo)

    conteudo = noticia.find("div", {"class": "conteudo"}).text.strip()
    url = noticia.find('a', href=True)['href']
    url = f'http://www.radiorural.com.br/{url}'

    data = {"text": f'{titulo}\n{conteudo}\n{url}\n'}
    print(data)
    r.post(url_horn, json=data, headers=headers)
    time.sleep(5.0)


# ######  ATUAL FM   #######

site= "https://www.atualfm.com.br/site/category/ultimas-noticias/"
hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
req = Request(site,headers=hdr)
page = urlopen(req)
soup = BeautifulSoup(page, features="html.parser")


noticias_relacao = soup.find_all("div", attrs={"class":"post-area"})


for noticia in noticias_relacao:
    titulo = noticia.find("div", {"class": "blog-title"}).text.strip()
    if exists_reported(titulo):
        continue
    
    add_title(titulo)

    conteudo = noticia.find("div", {"class": "blog-content"}).text.strip()
    url = noticia.find('a', href=True)['href']

    data = {"text": f'{titulo}\n{conteudo}\n{url}\n'}
    print(data)
    r.post(url_horn, json=data, headers=headers)
    time.sleep(5.0)


