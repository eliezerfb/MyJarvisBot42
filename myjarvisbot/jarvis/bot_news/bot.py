
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


######  SAÚDE SC   #######

# site= "http://www.saude.sc.gov.br/coronavirus/noticias.html"
# site =  http://www.coronavirus.sc.gov.br/noticias/
# hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
# req = Request(site,headers=hdr)
# page = urlopen(req)
# soup = BeautifulSoup(page, features="html.parser")


# for ultag in soup.find_all('ul', {'class': 'wp_rss_retriever_item_wrapper'}):
#     for litag in ultag.find_all('wp_rss_retriever_title'):
#         titulo = litag.text
#         for link in litag.find_all('a', href=True):
#             url = f'http://www.saude.sc.gov.br/coronavirus/{link["href"]}'
#             url = url.replace('', '\')

#         if titulo in titles_lst:
#             break

#         data_json.append({'title': titulo})

#         data = {"text": f'{titulo}\n{url}\n'}
#         print(data)
#         # r.post(url_horn, json=data, headers=headers)
#         # api_twitter.PostUpdate(f'{titulo}\n{url}\n{hashtag}'[:280])
#         time.sleep(5.0)


#### CASOS worldometers ####
#url = "https://www.worldometers.info/coronavirus/"
#response = r.get(url)
#html = response.content

#table = rows.import_from_html(BytesIO(html), index=0)


#for row in table:
#    if row.country_other == 'Brazil':
#        conteudo = f'Total de casos no Brasil: {row.total_cases}\nMortos: {row.total_deaths}\nRecuperados: {row.total_recovered}\nCasos Críticos: {row.serious_critical}'
#        titulo = f'br: {row.total_cases} M: {row.total_deaths} R: {row.total_recovered} C: {row.serious_critical}'

#if not exists_reported(titulo):
#    add_title(titulo)

#    data = {"text": f'\n{conteudo}\nFonte: https://www.worldometers.info/coronavirus/\n'}
#    r.post(url_horn, json=data, headers=headers)
#    print(data)


##### Brasil.IO #####
#req = r.get('https://brasil.io/api/dataset/covid19/caso/data?search=&date=&state=SC&city=&place_type=state')

#data = req.json()

#conteudo = f"COVID-19 em SC. Casos confirmados: {data['results'][0]['confirmed']}.\nMortes: {data['results'][0]['deaths']}."
#titulo = f"SC: {data['results'][0]['confirmed']}.M: {data['results'][0]['deaths']}."

#if not exists_reported(titulo):
#    add_title(titulo)

#    data = {"text": f'\n{conteudo}\nFonte: https://brasil.io/\n'}
#    r.post(url_horn, json=data, headers=headers)
#    print(data)


# cities_monitor = ['Alto Bela Vista', 'Arabutã', 'Arvoredo', 
#                   'Concórdia', 'Ipira', 'Ipumirim', 'Irani', 
#                   'Ita', 'Jaborá', 'Lindóia do Sul', 'Paial', 
#                   'Peritiba', 'Piratuba', 'Presidente Castello Branco', 
#                   'Seara', 'Xavantina', 'Chapecó', 'Xaxim', 
#                   'Xanxerê', 'São Miguel do Oeste', 
#                   'Catanduvas', 'Joaçaba', "Herval D'Oeste",
#                   'Florianópolis', 'Caçador', 'Videira']

#cities_monitor = ['Concórdia']

#req = r.get('https://brasil.io/api/dataset/covid19/caso/data?search=&date=&state=SC&city=&place_type=')

#data = req.json()


#for result in data['results']:
#    if not(result['is_last']):
#        continue

#    if result['city'] in cities_monitor:
#        conteudo = f"COVID-19 em {result['city']}-SC.\nCasos confirmados: {result['confirmed']}.\nMortes: {result['deaths']}."
#        titulo = f"{result['city']}.: {result['confirmed']}.M: {result['deaths']}."

#        if not exists_reported(titulo):
#            add_title(titulo)

 #           data = {"text": f'\n{conteudo}\nFonte: https://brasil.io/\n'}
 #           r.post(url_horn, json=data, headers=headers)
 #           print(data)

