from bs4 import BeautifulSoup
from threading import Thread
import requests
from urllib.parse import urlparse, urljoin


class PageFetcher(Thread):
    def __init__(self, obj_scheduler):
        self.obj_scheduler = obj_scheduler

    def request_url(self, obj_url):
        """
            Faz a requisição e retorna o conteúdo em binário da URL passada como parametro

            obj_url: Instancia da classe ParseResult com a URL a ser requisitada.
        """
        response = None


        return response.content

    def discover_links(self, obj_url, int_depth, bin_str_content):
        """
        Retorna os links do conteúdo bin_str_content da página já requisitada obj_url
        """

        """
            Percorre o codigo retornado, selecioando as tags HTML <a>
            Caso essa tag possua http no componente 'href' é criado um novo objeto de urlparse
            Caso contrario é utilizado o obj_url recebido como paramentro para ser a url base
            Se o dominio é igual ao recebido no parametro pelo obj_url a profundidade é oincrementada
            Caso contrario a profundidade é 0
        """
        soup = BeautifulSoup(bin_str_content, features="lxml")
        for link in soup.select('a'):
            if 'http' in link['href']:
                obj_new_url = urlparse(link['href'])
            else:
                obj_new_url = urlparse(obj_url.geturl() + '/' + link['href'])

            if obj_new_url.netloc == obj_url.netloc:
                int_new_depth = int_depth + 1
            else:
                int_new_depth = 0

            yield obj_new_url, int_new_depth

    def crawl_new_url(self):
        """
            Coleta uma nova URL, obtendo-a do escalonador
        """
        pass

    def run(self):
        """
            Executa coleta enquanto houver páginas a serem coletadas
        """
        pass
