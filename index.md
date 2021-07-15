## Welcome to GitHub Pages

You can use the [editor on GitHub](https://github.com/jonathancsr/recuperacao-da-informacao/edit/gh-pages/index.md) to maintain and preview the content for your website in Markdown files.

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/jonathancsr/recuperacao-da-informacao/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.


---
title: Bifaro Bot
---
## Seja Bem-Vindo ao Bifaro Bot

Este projeto foi desenvolvido por [Beatriz Souza da Silva](https://github.com/bia-souza), [Fadoa Glauss Vieira](https://github.com/fadoaglauss) e [Robert Cristiam Faustino de Souza](https://github.com/hobbitx) como parte da discplina de _Tópicos Especiais em Computação e Algoritmos: Algorimos de Organização e Recuperação de Informação_ do Centro Federal de Educação Tecnológica de Minas Gerais (CEFET-MG). Seu objetivo é promover o estudo e aprendizado de um coletor de próposito geral para Web.

### Identificando o Bifaro Bot
O tráfego proveniente é identificado por seu agente de usuário: bifaroBot.

### Customizando as regras de _robots.txt_
Bifaro Bot respeita as diretivas padrão de _robots.txt_. Neste exemplo, o Bifaro Bot não coleta documentos em `private` ou `not-allowed` por meio do uso da biblioteca _RobotFileParser_: 
```
User-agent: bifaroBot
Allow: /                     # Allow everything
Disallow: /private/          # Disallow this directory
```
```
User-agent: *                # Any robot
Disallow: /not-allowed/      # Disallow this directory
```

#### Regras de Renderização e Robô
O Bifaro Bot pode processar o conteúdo de seu site em um navegador. Se resursos forem bloqueados por meio de _robots.txt_, o Bifaro Bot pode não ser capaz de processar o conteúdo corretamente. Isso inclui XHR, JS e CSS que a página pode exigir.

Para que o Bifaro Bot indexe o melhor conteúdo para a página, certifique-se de que tudo o que é necessário para um usuário renderizar a página está disponível para o Bifaro Bot. Como alternativa, certifique-se de que o site seja renderizado de forma limpa, mesmo se todos os recursos não estiverem disponíveis. 


### Coleta
Para fins didáticos, realizou-se a coleta no dia 15 de Outubro de 2020 de **páginas públicas**, obedecendo a politíca de exclusão de robôs - disponível em _robos.txt_ da página, por meio das seguintes sementes:
- http://cnn.com
- https://pt.wikipedia.org/wiki/House,_M.D.
- https://globoesporte.globo.com

Para mais detalhes veja [BifaroBot](https://github.com/fadoaglauss/InfoBifaroBot).

### Suporte ou Contato
Você teve problema com o projeto? Entre em contato com o [suporte](mailto:fadoa.glauss@gmail.com) por e-mail.
