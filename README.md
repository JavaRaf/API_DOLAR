# Currency Image and Facebook Post

Este projeto busca a cotação do dólar em relação ao real brasileiro (USD/BRL) usando o web scraping, cria uma imagem com a cotação e a data, e faz um post dessa imagem em uma página do Facebook. Ele também registra as informações da cotação em arquivos de log.

## Funcionalidade

1. **Obter cotação do dólar**: O código busca os dados mais recentes sobre a cotação USD/BRL.

2. **Criar uma imagem**: A cotação é exibida em uma imagem personalizada usando ImageMagick, incluindo:
   - Valor da cotação
   - Data e hora são geradas automaticamente, com fuso horário Brasileiro
   - Fonte da cotação
3. **Postar no Facebook**: A imagem gerada é postada automaticamente no Facebook usando a Graph API.
4. **Sistema de Logs**: 
   - Logs de aplicação com rotação (até 5 arquivos de 1MB)
   - Registro de cotações no diretório de histórico
   - Registro de URLs dos posts do Facebook

## Pré-requisitos

- Python 3.x
- Conta de desenvolvedor no Facebook com acesso à Graph API

## Como Usar

1. Faça um fork do projeto ou use um template do GitHub.
2. Configure a variável de ambiente `FB_TOKEN` com seu token de acesso do Facebook:
   - A variável deve ser um token válido referente a uma página do Facebook.
3. O script roda em horários fixos, mas pode ser alterado no arquivo `.github/workflows/init.yaml`:
   
   ```bash
   on:
   schedule:
   - cron: '0 9 * * *'   # Executa às 6:00   Brasilia
   - cron: '0 15 * * *'  # Executa às 12:00  Brasilia
   - cron: '0 00 * * *'  # Executa às 21:00  Brasilia
   ```

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo [LICENSE.md](LICENSE.md) para mais detalhes.

