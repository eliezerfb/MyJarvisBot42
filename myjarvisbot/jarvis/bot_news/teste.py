from cgitb import strong
from urllib.request import Request, urlopen
import urllib
from bs4 import BeautifulSoup
from http.cookiejar import CookieJar
import time

hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}



try:
    sites_monitor = [
                    {'site': "http://www.nfce.se.gov.br/portal/portalNoticias.jsp?jsp=barra-menu/documentos/notasTecnicas.htm", 'doc':'NFC-e SE'}
                    ]
    
    for site in sites_monitor:
        print(site['doc'])
        print('teste')
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

                # if exists_reported(titulo):
                #     continue                

                conteudo = p.text.strip()

                url = site['site']

                data = {"text": f'{titulo}\n{conteudo}\n{url}\n'}
                print(data)

                # add_title(titulo)
                # r.post(url_hornC4, json=data, headers=headers)

                time.sleep(5.0)

except Exception as e:
    print('Erro NFC-e SE - ', e)




# from urllib.request import Request, urlopen
# from bs4 import BeautifulSoup as soup
# url = 'http://www.nfce.se.gov.br/portal/portalNoticias.jsp?jsp=barra-menu/documentos/notasTecnicas.htm'
# req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})

# webpage = urlopen(req).read()
# page_soup = soup(webpage, "html.parser")
# print(page_soup)



# try:
#     sites_monitor = [
#                     {'site': "http://www.nfce.se.gov.br/portal/portalNoticias.jsp?jsp=barra-menu/documentos/notasTecnicas.htm", 'doc':'NFCe - SE'},        
#                     ]
    
#     for site in sites_monitor:
#         print(site['doc'])
#         cj = CookieJar()
#         req = Request(site['site'], headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'})
#         page = urlopen(req)
#         soup = BeautifulSoup(page.read(), features="html.parser")
        
#         noticias_relacao = soup.find_all("div", attrs={"class": "indentacaoNormal"})

#         for noticia in noticias_relacao:
#             # print(noticia.text.strip())
#             all_p = noticia.find_all("p")
#             for p in all_p:
#                 titulo = site['doc']+' '+p.text.strip()
#                 print('--->>', titulo)
#                 print(titulo[0:100])

# except Exception as e:
#     print('Erro NFe - ', e)           