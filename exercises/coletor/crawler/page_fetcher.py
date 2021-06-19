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
        # Nova url para coletar
        url_to_parse = self.obj_scheduler.get_next_url()
        self.obj_scheduler.count_fetched_page()
        # Tenta coletar o html da url
        html = self.request_url(url_to_parse)

        # Caso o não tenha html 
        if html is None:
            return False

        print(url_to_parse.geturl())
        # Desconbre os novos links do html buscado
        new_links = self.discover_links(html)

        # Adiciona os novos links no escalonador
        for link, int_depth in new_links:
            print(link)
            self.obj_scheduler.add_new_page(link, int_depth)

    def run(self):
        while self.obj_scheduler.has_finished_crawl():
            self.crawl_new_url()