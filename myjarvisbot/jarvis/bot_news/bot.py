
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myjarvisbot.settings")


from io import BytesIO
import urllib
from urllib.request import Request, urlopen
import time
from dateutil.parser import parse

from bs4 import BeautifulSoup
from decouple import config
import json
import requests as r
from http.cookiejar import CookieJar



def exists_reported(title):
    from myjarvisbot.jarvis.models import NewsReported
    news = NewsReported.objects.filter(title=title[:100])
    return news.count() > 0


def add_title(title):
    from myjarvisbot.jarvis.models import NewsReported
    news = NewsReported(title=title[:100])
    news.save()


def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False



hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
url_horn = "https://integram.org/webhook/"+config('WEBHOOK')
url_hornC4 = "https://integram.org/webhook/"+config('WEBHOOK_C4')

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}



try:
    print('NFC-e PE')
    site = "https://www.sefaz.pe.gov.br/Servicos/Nota-Fiscal-de-Consumidor-Eletronica/Paginas/Avisos-NFC-e.aspx"
    req = Request(site,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, features="html.parser")

    noticias_relacao = soup.find_all("div", attrs={"class":"article article-body"})

    for noticia in noticias_relacao:
        all_strong = noticia.find_all("strong")
        for s in all_strong:
            if len(s.text.strip()) <= 12:
                continue
            titulo = 'NFC-e PE '+s.text.strip()
            
            if exists_reported(titulo):
                continue

            add_title(titulo)

            url = site
                        
            data = {"text": f'{titulo}\n{url}\n'}

            print(data)

            # r.post(url_hornC4, json=data, headers=headers)
            time.sleep(5.0)


except Exception as e:
    print('Erro NFC-e PE - ', e)
    pass



try:
    ##### Monitor data tabela IBPT - github ######
    sites_monitor = [{'site': "https://github.com/frones/ACBr/tree/master/Exemplos/ACBrTCP/ACBrIBPTax/tabela", 'doc':'Tabela IBPT'}]
    print('Tabela IBPT')

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

            # r.post(url_hornC4, json=data, headers=headers)
            time.sleep(5.0)

except Exception as e:
    print('Erro Tabela IBPT - ', e)
    pass           


##### Monitor NFC-e SC ######
try:
    sites_monitor = [{'site': "http://www.sef.sc.gov.br/servicos/servico/136", 'doc':'NFC-e'}]
    print('NFC-e SC')

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

                print(data)

                # r.post(url_hornC4, json=data, headers=headers)
                time.sleep(5.0)

except Exception as e:
    print('Erro NFCe SC - ', e)
    pass


##### Monitor SEFAZ ######
try:
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    sites_monitor = [
                    {'site': "https://www.cte.fazenda.gov.br/portal/listaConteudo.aspx?tipoConteudo=Y0nErnoZpsg=", 'doc':'CT-e'}
                    ]
    print('CT-e')
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

                # r.post(url_hornC4, json=data, headers=headers)
                time.sleep(5.0)

except Exception as e:
    print('Erro CTe - ', e)
    pass


try:
    sites_monitor = [
                    {'site': "https://www.nfe.fazenda.gov.br/portal/informe.aspx?ehCTG=false", 'doc':'NF-e'}
                    ]
    
    for site in sites_monitor:
        print(site['doc'])
        cj = CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        req = Request(site['site'], None, {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'gzip, deflate, sdch','Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'})
        page = opener.open(req)
        soup = BeautifulSoup(page.read(), features="html.parser")

        noticias_relacao = soup.find_all("div", attrs={"class": "divInforme"})
        for noticia in noticias_relacao:
            all_p = noticia.find_all("p")
            for p in all_p:
                titulo = p.text.strip()
                url = site['site']
        
                if exists_reported(titulo):
                    continue

                titulo = site['doc'] + ' ' + titulo

                data = {"text": f'{titulo}\n{url}\n'}

                add_title(titulo)

                # r.post(url_hornC4, json=data, headers=headers)
                time.sleep(5.0)

except Exception as e:
    print('Erro NFe - ', e)
    pass


try:
    sites_monitor = [
                    {'site': "http://www.nfe.fazenda.gov.br/portal/listaConteudo.aspx?tipoConteudo=04BIflQt1aY=", 'doc':'NT NF-e'},
                    ]
    
    for site in sites_monitor:
        print(site['doc'])
        cj = CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        req = Request(site['site'], None, {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'gzip, deflate, sdch','Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'})
        page = opener.open(req)
        soup = BeautifulSoup(page.read(), features="html.parser")

        noticias_relacao = soup.find_all("span", attrs={"class": "tituloConteudo"})
        for noticia in noticias_relacao:
            titulo = noticia.text.strip()
            titulo = site['doc'] + ' ' + titulo
            url = site['site']

            if exists_reported(titulo):
                continue

            data = {"text": f'{titulo}\n{url}\n'}

            add_title(titulo)
            print(data)

            # r.post(url_hornC4, json=data, headers=headers)
            time.sleep(5.0)


except Exception as e:
    print('Erro NFe - ', e)
    pass



try:
    sites_monitor = [
                    {'site': "http://www.nfce.se.gov.br/portal/portalNoticias.jsp?jsp=barra-menu/documentos/notasTecnicas.htm", 'doc':'NFC-e SE'}
                    ]
    
    for site in sites_monitor:
        print(site['doc'])
        req = Request(site['site'], headers=hdr)
        page = urlopen(req, timeout = 15)
        soup = BeautifulSoup(page, features="html.parser")

        noticias_relacao = soup.find_all("div", attrs={"class": "indentacaoConteudo"})
        for noticia in noticias_relacao:
            all_p = noticia.find_all("p")
            for p in all_p:
                span = p.find("span", attrs={"class": "tituloConteudo"})
                if span == None:
                    continue
                titulo = site['doc'] + ' ' + span.text.strip()

                if exists_reported(titulo):
                    continue                

                conteudo = p.text.strip()

                url = site['site']

                data = {"text": f'{titulo}\n{conteudo}\n{url}\n'}
                print(data)

                add_title(titulo)
                # r.post(url_hornC4, json=data, headers=headers)

                time.sleep(5.0)

except Exception as e:
    print('Erro NFC-e SE - ', e)
    pass



try:
    sites_monitor = [
                    {'site': "https://receita.fazenda.rs.gov.br/lista/762/avisos", 'doc':'NFC-e RS'}
                    ]
    
    for site in sites_monitor:
        print(site['doc'])
        cj = CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        req = Request(site['site'], None, hdr)
        page = opener.open(req)
        soup = BeautifulSoup(page.read(), features="html.parser", from_encoding="iso-8859-1")
        
        noticias_relacao = soup.find_all("ul", attrs={"class": "cConteudoListaSimples"})
        print(noticias_relacao)
     

        for noticia in noticias_relacao:
            all_li = noticia.find_all("li")
            for li in all_li:
                titulo = site['doc']+' '+li.text.strip()
                url = site['site']
        
                if exists_reported(titulo):
                    continue

                data = {"text": f'{titulo}\n{url}\n'}

                add_title(titulo)

                # r.post(url_hornC4, json=data, headers=headers)
                print(data)
                time.sleep(5.0)

except Exception as e:
    print('Erro NFe - ', e)
    pass


try:
    sites_monitor = [
                    {'site': "https://www.economia.go.gov.br/receita-estadual/documentos-fiscais.html", 'doc':'NF-e GO'}
                    ]
    
    for site in sites_monitor:
        print(site['doc'])
        req = Request(site['site'], headers=hdr)
        page = urlopen(req, timeout = 15)
        soup = BeautifulSoup(page, features="html.parser")

        noticias_relacao = soup.find_all("ul", attrs={"class": "inner"})
        for noticia in noticias_relacao:
            all_li = noticia.find_all("li")
            for li in all_li:
                titulo = site['doc'] + ' ' + li.text.strip()

                if exists_reported(titulo):
                    continue                

                url = site['site']

                data = {"text": f'{titulo}\n{url}\n'}
                print(data)

                add_title(titulo)
                # r.post(url_hornC4, json=data, headers=headers)

                time.sleep(5.0)

except Exception as e:
    print('Erro NF-e GO - ', e)
    pass


try:
    sites_monitor = [
                    {'site': "https://www.sefaz.pe.gov.br/Servicos/nota-fiscal-eletronica/Paginas/Avisos0808-6156.aspx", 'doc':'NF-e PE'}
                    ]
    
    for site in sites_monitor:
        print(site['doc'])
        req = Request(site['site'], headers=hdr)
        page = urlopen(req, timeout = 15)
        soup = BeautifulSoup(page, features="html.parser")

        next_is_title = False
        news_date = ''

        noticias_relacao = soup.find_all("div", attrs={"class": "article article-body"})
        for noticia in noticias_relacao:
            all_strong = noticia.find_all("strong")
            for s in all_strong:
                titulo = s.text.strip().replace(u'\u200b', '')

                if (len(titulo) >= 10) and is_date(titulo):
                    next_is_title = True
                    news_date = titulo
                    continue

                if not next_is_title:
                    continue

                next_is_title = False
                titulo = site['doc'] + ' ' + news_date + ' '+ titulo

                if exists_reported(titulo):
                    continue
              
                url = site['site']
                data = {"text": f'{titulo}\n{url}\n'}
                print(data)

                add_title(titulo)
                # r.post(url_hornC4, json=data, headers=headers)

                time.sleep(5.0)


except Exception as e:
    print('Erro NF-e PE - ', e)



try:
    sites_monitor = [
                    {'site': "https://www.nfce.ms.gov.br/noticias/", 'doc':'NFC-e MS'}
                    ]
    
    for site in sites_monitor:
        print(site['doc'])
        req = Request(site['site'], headers=hdr)
        page = urlopen(req)
        soup = BeautifulSoup(page, features="html.parser")

        noticias_relacao = soup.find_all("div", attrs={"class": "container"})
        for noticia in noticias_relacao:
            all_box = noticia.find_all("div", attrs={"class": "noticiaBox"})
            for b in all_box:
                titulo = b.find("a").text.strip()
                titulo = site['doc'] + ' ' + titulo

                conteudo = b.find("p").text.strip()
                url = site['site']
        
                if exists_reported(titulo):
                    continue

                data = {"text": f'{titulo}\n{conteudo}\n{url}\n'}

                add_title(titulo)

                print(data)

                # r.post(url_hornC4, json=data, headers=headers)
                time.sleep(5.0)

except Exception as e:
    print('Erro NFCe MS - ', e)
    pass




try:
    sites_monitor = [{'site':'https://dfe-portal.svrs.rs.gov.br/Mdfe/Documentos', 'doc':'MDF-e'},
                    {'site':'https://dfe-portal.svrs.rs.gov.br/Mdfe/Avisos', 'doc':'MDF-e'}]

    print('MDF-e')

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

            # r.post(url_hornC4, json=data, headers=headers)
            time.sleep(5.0)

except Exception as e:
    print('Erro MDF-e - ', e)
    pass



######  RADIO RURAL   #######
try:
    print('Rádio Rural')
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
        # r.post(url_horn, json=data, headers=headers)
        time.sleep(5.0)
except Exception as e:
    print('Erro Rural - ', e)
    pass


######  ATUAL FM   #######
try:
    print('Rádio Atual')
    site= "https://atualfm.com.br/tdb_templates/category-template-week-pro/"
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    req = Request(site,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, features="html.parser")


    noticias_relacao = soup.find_all("div", attrs={"class":"td-module-container td-category-pos-above"})


    for noticia in noticias_relacao:
        all_h = noticia.find_all("h3", attrs={"class":"entry-title td-module-title"})
        for h in all_h:
            titulo = h.text.strip()
            continue
        conteudo = ''

        url = noticia.find('a', href=True)['href']
        if exists_reported(titulo):
          continue

        add_title(titulo)

        data = {"text": f'{titulo}\n{url}\n'}
        print(data)

        # if not(titulo.startswith('Nota de falecimento')):
            # r.post(url_horn, json=data, headers=headers)

        time.sleep(5.0)
        

except Exception as e:
    print('Erro Atual - ', e)
    pass
