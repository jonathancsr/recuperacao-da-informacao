from urllib import robotparser
import time
from urllib.parse import urlparse
from util.threads import synchronized
from collections import OrderedDict
from .domain import Domain


class Scheduler():
    # tempo (em segundos) entre as requisições
    TIME_LIMIT_BETWEEN_REQUESTS = 20

    def __init__(self, str_usr_agent, int_page_limit, int_depth_limit, arr_urls_seeds):
        """
            Inicializa o escalonador. Atributos:
                - `str_usr_agent`: Nome do `User agent`. Usualmente, é o nome do navegador, em nosso caso,  será o nome do coletor (usualmente, terminado em `bot`)
                - `int_page_limit`: Número de páginas a serem coletadas
                - `int_depth_limit`: Profundidade máxima a ser coletada
                - `int_page_count`: Quantidade de página já coletada
                - `dic_url_per_domain`: Fila de URLs por domínio (explicado anteriormente)
                - `set_discovered_urls`: Conjunto de URLs descobertas, ou seja, que foi extraída em algum HTML e já adicionadas na fila - mesmo se já ela foi retirada da fila. A URL armazenada deve ser uma string.
                - `dic_robots_per_domain`: Dicionário armazenando, para cada domínio, o objeto representando as regras obtidas no `robots.txt`
        """
        self.str_usr_agent = str_usr_agent
        self.int_page_limit = int_page_limit
        self.int_depth_limit = int_depth_limit
        self.int_page_count = 0

        self.dic_url_per_domain = OrderedDict()
        self.set_discovered_urls = set()
        self.dic_robots_per_domain = {}

        for str_url in arr_urls_seeds:
            self.add_new_page(str_url, 0)

    @synchronized
    def count_fetched_page(self):
        """
            Contabiliza o número de paginas já coletadas
        """
        self.int_page_count += 1

    def has_finished_crawl(self):
        """
            Verifica se finalizou a coleta
        """
        if (self.int_page_count > self.int_page_limit):
            return True
        return False

    @synchronized
    def can_add_page(self, obj_url, int_depth):
        """
            Retorna verdadeiro caso  profundade for menor que a maxima
            e a url não foi descoberta ainda
        """
        return (obj_url not in self.set_discovered_urls) and (int_depth < self.int_depth_limit)

    @synchronized
    def add_new_page(self, obj_url, int_depth):
        """
            Adiciona uma nova página
            obj_url: Objeto da classe ParseResult com a URL a ser adicionada
            int_depth: Profundidade na qual foi coletada essa URL
        """
        # https://docs.python.org/3/library/urllib.parse.html
        """
            Verifica se é possivel adionar a nova pagina
        """
        if self.can_add_page(obj_url=obj_url, int_depth=int_depth):
            """
                Caso o dominio não exista, é criado uma nova instancia se o dominio existe é 
                adicionado a lista de tuplas
                domain_new: Objeto da classe Domain com novo dominio
            """
            domain_new = Domain(nam_domain=obj_url.netloc,
                                int_time_limit_between_requests=self.TIME_LIMIT_BETWEEN_REQUESTS)
            if domain_new in self.dic_url_per_domain:
                self.dic_url_per_domain[domain_new] += (obj_url, int_depth)
            else:
                self.dic_url_per_domain[domain_new] = [(obj_url, int_depth)]

            self.set_discovered_urls.add(obj_url)

            return True
        return False

    @synchronized
    def get_next_url(self):
        """
        Obtem uma nova URL por meio da fila. Essa URL é removida da fila.
        Logo após, caso o servidor não tenha mais URLs, o mesmo também é removido.
        """

        """
        É percorrido o dicionário de URL's e verificado se o domínio é acessível
        Se não acessível:  passa para o próximo elemento do dicionário
        Se acessível: marca como acessada (accessed_now()), remove a URL da lista, retorna a url e sua profundidade
        Caso o array de urls estiver vazio remove o domínio do dicionário     
        """
        for domain, urls in self.dic_url_per_domain.items():
            if domain.is_accessible():
                domain.accessed_now()
                if len(urls) > 0:
                    obj_url, int_depth = urls.pop(0)
                    if len(urls) == 0:
                        self.dic_url_per_domain.pop(domain)
                else:
                    self.dic_url_per_domain.pop(domain)
                    return None, None

                return obj_url, int_depth

        """
        Caso não encontre uma url para coletar, a thread espera pelo tempo definido na variavel TIME_LIMIT_BETWEEN_REQUESTS
        e tenta novamente
        """
        time.sleep(self.TIME_LIMIT_BETWEEN_REQUESTS)

        return None, None

    def can_fetch_page(self, obj_url):
        """
        Verifica, por meio do robots.txt se uma determinada URL pode ser coletada
        """
        """
        É verificado se o robots.txt ja foi requisitado verificando o dicionário dic_robots_per_domain
        Se não foi requisitado utiliza-se o RobotFileParser passando a URL do dominio, fazendo a leitura do robots.txt
        E adiciona o robot no dicionário dic_robots_per_domain
        Por fim verifica-se através do metodo can_fetch(), passando o usr_agent e url, se possui permissão 
        """
        if obj_url.netloc in self.dic_robots_per_domain:
            robot = self.dic_robots_per_domain[obj_url.netloc]
        else:
            try:
                robot = robotparser.RobotFileParser(url=obj_url.geturl() + '/robots.txt')
                robot.read()
                self.dic_robots_per_domain[obj_url.netloc] = robot
            except:
                return False
        return robot.can_fetch(self.str_usr_agent, obj_url.geturl())
