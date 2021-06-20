from bs4 import BeautifulSoup
from threading import Thread
import requests
from urllib.parse import urlparse, urljoin


class PageFetcher(Thread):

    def __init__(self, obj_scheduler):
        super().__init__()
        self.obj_scheduler = obj_scheduler

    def request_url(self, obj_url):
        """
            Faz a requisição e retorna o conteúdo em binário da URL passada como parametro

            obj_url: Instancia da classe ParseResult com a URL a ser requisitada.
        """
        try:
            response = requests.get(obj_url.geturl(),
                                    headers={"User-Agent": self.obj_scheduler.str_usr_agent},
                                    timeout=6)
            if response:
                if "text/html" in response.headers['content-type']:
                    return response.content
            return None
        except:
            return None

    def discover_links(self, obj_url, int_depth, bin_str_content):
        """
        Retorna os links do conteúdo bin_str_content da página já requisitada obj_url
        """
        """
            Percorre o codigo retornado, selecioando as tags HTML <a>
            Caso essa tag possua http no componente 'href' é criado um novo objeto de urlparse
            Caso contrario é utilizado o obj_url recebido como paramentro para ser a url base
            Se o dominio é igual ao recebido no parametro pelo obj_url a profundidade é incrementada
            Caso contrario a profundidade é 0
        """
        soup = BeautifulSoup(bin_str_content, features="lxml")
        for link in soup.select('a'):
            href = link.get("href")

            if href:
                if 'http' in href:
                    obj_new_url = urlparse(href)
                else:
                    int_ulr_len = len(obj_url.geturl())
                    if href[0] == '/' or obj_url.geturl()[int_ulr_len - 1] == '/':
                        obj_new_url = urlparse(obj_url.geturl() + href)
                    else:
                        obj_new_url = urlparse(obj_url.geturl() + '/' + href)

                int_new_depth = 0
                if obj_new_url.netloc == obj_url.netloc:
                    int_new_depth = int_depth + 1

                yield obj_new_url, int_new_depth

    def crawl_new_url(self):
        """
            Coleta uma nova URL, obtendo-a do escalonador
        """
        # Nova url para coletar
        url_to_parse = self.obj_scheduler.get_next_url()
        if url_to_parse[0] is not None:

            self.obj_scheduler.count_fetched_page()
            # Tenta coletar o html da url
            html = self.request_url(url_to_parse[0])

            # Caso o não tenha html
            if html is None:
                return False

            print(
                f"Buscando {url_to_parse[0].geturl()} na profundidade {url_to_parse[1]}, número de paginas coletadas : "
                f"{self.obj_scheduler.int_page_count}")
            # Desconbre os novos links do html buscado
            new_links = self.discover_links(obj_url=url_to_parse[0], int_depth=url_to_parse[1], bin_str_content=html)

            # Adiciona os novos links no escalonador
            for link, int_depth in new_links:
                self.obj_scheduler.add_new_page(link, int_depth)

    def run(self):
        while self.obj_scheduler.has_finished_crawl() is False:
            self.crawl_new_url()
