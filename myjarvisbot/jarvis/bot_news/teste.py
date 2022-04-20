from cgitb import strong
from urllib.request import Request, urlopen
import urllib
from bs4 import BeautifulSoup
from http.cookiejar import CookieJar
import time

hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}



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
                conteudo = b.find("p").text.strip()
                # titulo = p.text.strip()
                url = site['site']
        
                # if exists_reported(titulo):
                    # continue

                titulo = site['doc'] + ' ' + titulo

                data = {"text": f'{titulo}\n{conteudo}\n{url}\n'}

                # add_title(titulo)

                print(data)

                # r.post(url_hornC4, json=data, headers=headers)
                # time.sleep(5.0)

except Exception as e:
    print('Erro NFe - ', e)




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