---
title: Landerito Bot
---
## Seja Bem-Vindo ao Landerito Bot

Este projeto foi desenvolvido por [Jonathan Candido](https://github.com/jonathancsr) e [Raylander Frois](https://github.com/Raylander96) como parte da discplina de Tópicos Especiais em Computação e Algoritmos: Algorimos de Organização e Recuperação de Informação do Centro Federal de Educação Tecnológica de Minas Gerais (CEFET-MG). Seu objetivo é promover o estudo e aprendizado de um coletor de próposito geral para Web.

### Identificando o Landerito Bot
O tráfego proveniente é identificado por seu agente de usuário: landeritoBot.

### Customizando as regras de _robots.txt_
O Landerito Bot respeita as diretivas padrão de robots.txt. O Landerito Bot não coleta documentos em `private` ou `not-allowed` por meio do uso da biblioteca _RobotFileParser_: 
```
User-agent: landeritoBot
Allow: /                     # Allow everything
Disallow: /private/          # Disallow this directory
```
```
User-agent: *                # Any robot
Disallow: /not-allowed/      # Disallow this directory
```

#### Regras de Renderização e Robô
O Landerito Bot pode processar o conteúdo de sites. Se as urls forem bloqueados por meio de _robots.txt_, o Landerito Bot não é capaz de processar o conteúdo corretamente quando está incluso XHR, JS e CSS que a página pode exigir.

Para que o Landerito Bot indexe o conteúdo da melhor maneira para a página, certifique-se de que tudo o que é necessário para um usuário renderizar a página está disponível para o Landerito Bot.

### Coleta
Para fins didáticos, realizou-se a coleta no dia 11 de Julho de 2021 de **páginas públicas**, obedecendo a politíca de exclusão de robôs - disponível no _robos.txt_ das páginas, por meio das seguintes sementes:
- https://jovemnerd.com.br/
- https://g1.globo.com/
- https://www.gov.br/
- https://www.folha.uol.com.br/
- https://www.nytimes.com/
- https://pt.stackoverflow.com/
- https://www.estadao.com.br/
- https://www.em.com.br/

Para mais detalhes veja [landeritoBot](https://github.com/jonathancsr/recuperacao-da-informacao/tree/main/exercises/coletor).

### Suporte ou Contato
Você teve problema com o projeto? Entre em contato com o [suporte](mailto:jonathancsrr@gmail.com) ou [suporte](mailto:raylanderfl@gmail.com) por e-mail.
