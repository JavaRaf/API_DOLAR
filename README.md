# Currency Image and Facebook Post

Este projeto busca a cotação do dólar em relação ao real brasileiro (USD/BRL) usando o site Wise.com, cria uma imagem com a cotação e a data, e faz um post dessa imagem em uma página do Facebook. Ele também registra as informações da cotação em arquivos de log.

## Funcionalidade

1. **Obter cotação do dólar**: O código busca os dados mais recentes sobre a cotação USD/BRL através do site Wise.com usando web scraping.
2. **Criar uma imagem**: A cotação é exibida em uma imagem personalizada usando ImageMagick, incluindo:
   - Valor da cotação
   - Data e hora (fuso horário Brasil)
   - Fonte da cotação
3. **Postar no Facebook**: A imagem gerada é postada automaticamente no Facebook usando a Graph API.
4. **Sistema de Logs**: 
   - Logs de aplicação com rotação (até 5 arquivos de 1MB)
   - Registro de cotações no diretório de histórico
   - Registro de URLs dos posts do Facebook

## Pré-requisitos

- Python 3.x
- ImageMagick instalado no sistema
- Conta de desenvolvedor no Facebook com acesso à Graph API

