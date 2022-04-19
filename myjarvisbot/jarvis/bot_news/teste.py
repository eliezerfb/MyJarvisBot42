from cgitb import strong
from urllib.request import Request, urlopen
import urllib
from bs4 import BeautifulSoup


try:
    print('SEFAZ PE')
    site= "https://www.sefaz.pe.gov.br/Servicos/Nota-Fiscal-de-Consumidor-Eletronica/Paginas/Avisos-NFC-e.aspx"
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    req = Request(site,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, features="html.parser")


    noticias_relacao = soup.find_all("div", attrs={"class":"article article-body"})

    for noticia in noticias_relacao:
        all_strong = noticia.find_all("strong")
        for s in all_strong:
            if len(s.text.strip()) <= 12:
                continue
            print(s.text.strip())

    #     all_h = noticia.find_all("h3", attrs={"class":"entry-title td-module-title"})
    #     for h in all_h:
    #         print(h.text.strip())
    #         continue
    #     conteudo = ''

        # url = noticia.find('a', href=True)['href']
        # print(url)
        
        # all_a = noticia.find_all("a", attrs={"class":"td-image-wrap"}, href=True)
        # for a in all_a:
            # print(a.text.strip())        
        # url = noticia.find('a', attrs={"class":"td-image-wrap"} href=True)['href']
        
        # titulo = noticia.find_all("div", {"class": "entry-title td-module-title"})
        # titulo = noticia.find_all("div", {"class": "entry-title td-module-title"})
        # print(titulo)

        # conteudo = noticia.find("div", {"class": "blog-content"}).text.strip()
        # url = noticia.find('a', href=True)['href']

        # data = {"text": f'{titulo}\n{conteudo}\n{url}\n'}
        # print(data)

except Exception as e:
    print('Erro Atual - ', e)



# site = 'https://www.nfe.fazenda.gov.br/portal/informe.aspx?ehCTG=false'
# # site = 'https://www.cte.fazenda.gov.br/portal/listaConteudo.aspx?tipoConteudo=Y0nErnoZpsg='

# # hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
# hdr = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'gzip, deflate, sdch','Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'}

# cj = CookieJar()
# opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
# req = Request(site, None, {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'gzip, deflate, sdch','Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'})

# page = opener.open(req)
# soup = BeautifulSoup(page.read(), features="html.parser")

# noticias_relacao = soup.find_all("div", attrs={"class": "divInforme"})
# for noticia in noticias_relacao:
#     all_p = noticia.find_all("p")
#     for p in all_p:
#         print(p.text.strip())
