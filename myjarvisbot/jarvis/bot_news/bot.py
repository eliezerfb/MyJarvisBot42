
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myjarvisbot.settings")


from io import BytesIO
from urllib.request import Request, urlopen
import time

from bs4 import BeautifulSoup
from decouple import config
import requests as r
import rows



def exists_reported(title):
    from myjarvisbot.jarvis.models import NewsReported
    # news = NewsReported.objects.all()
    news = NewsReported.objects.filter(title=title[:100])
    return news.count() > 0


def add_title(title):
    from myjarvisbot.jarvis.models import NewsReported
    news = NewsReported(title=title[:100])
    news.save()


url_horn = "https://integram.org/webhook/"+config('TELEGRAM_BOT_TOKEN')
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

######  RADIO RURAL   #######

# site= "http://www.radiorural.com.br/noticias/categoria/33-coronavirus"
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
    r.post(url_horn, data=json.dumps(data), headers=headers)
    time.sleep(5.0)


######  ATUAL FM   #######

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
    r.post(url_horn, data=json.dumps(data), headers=headers)
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
#         # r.post(url_horn, data=json.dumps(data), headers=headers)
#         # api_twitter.PostUpdate(f'{titulo}\n{url}\n{hashtag}'[:280])
#         time.sleep(5.0)


#### CASOS worldometers ####
url = "https://www.worldometers.info/coronavirus/"
response = r.get(url)
html = response.content

table = rows.import_from_html(BytesIO(html), index=0)


for row in table:
    if row.country_other == 'Brazil':
        conteudo = f'Total de casos no Brasil: {row.total_cases}\nMortos: {row.total_deaths}\nRecuperados: {row.total_recovered}\nCasos Críticos: {row.serious_critical}'
        titulo = f'br: {row.total_cases} M: {row.total_deaths} R: {row.total_recovered} C: {row.serious_critical}'

if not exists_reported(titulo):
    add_title(titulo)

    data = {"text": f'\n{conteudo}\nFonte: https://www.worldometers.info/coronavirus/\n'}
    r.post(url_horn, data=json.dumps(data), headers=headers)
    print(data)


##### Brasil.IO #####
req = r.get('https://brasil.io/api/dataset/covid19/caso/data?search=&date=&state=SC&city=&place_type=state')

data = req.json()

conteudo = f"COVID-19 em SC. Casos confirmados: {data['results'][0]['confirmed']}.\nMortes: {data['results'][0]['deaths']}."
titulo = f"SC: {data['results'][0]['confirmed']}.M: {data['results'][0]['deaths']}."

if not exists_reported(titulo):
    add_title(titulo)

    data = {"text": f'\n{conteudo}\nFonte: https://brasil.io/\n'}
    r.post(url_horn, data=json.dumps(data), headers=headers)
    print(data)


cities_monitor = ['Alto Bela Vista', 'Arabutã', 'Arvoredo', 
                  'Concórdia', 'Ipira', 'Ipumirim', 'Irani', 
                  'Ita', 'Jaborá', 'Lindóia do Sul', 'Paial', 
                  'Peritiba', 'Piratuba', 'Presidente Castello Branco', 
                  'Seara', 'Xavantina', 'Chapecó', 'Xaxim', 
                  'Xanxerê', 'São Miguel do Oeste', 
                  'Catanduvas', 'Joaçaba', "Herval D'Oeste",
                  'Florianópolis', 'Caçador', 'Videira']

req = r.get('https://brasil.io/api/dataset/covid19/caso/data?search=&date=&state=SC&city=&place_type=')

data = req.json()


for result in data['results']:
    if not(result['is_last']):
        continue

    if result['city'] in cities_monitor:
        conteudo = f"COVID-19 em {result['city']}-SC.\nCasos confirmados: {result['confirmed']}.\nMortes: {result['deaths']}."
        titulo = f"{result['city']}.: {result['confirmed']}.M: {result['deaths']}."

        if not exists_reported(titulo):
            add_title(titulo)

            data = {"text": f'\n{conteudo}\nFonte: https://brasil.io/\n'}
            r.post(url_horn, data=json.dumps(data), headers=headers)
            print(data)

