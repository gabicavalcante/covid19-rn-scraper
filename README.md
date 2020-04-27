# covid19-rn-scraper

![](https://github.com/gabicavalcante/covid19-rn-scraper/workflows/CI/badge.svg) 


Scraper criado para dar suporte ao projeto de visualização de dados do Covid19 (https://leobezerra.github.io/covid19/).
Os dados extraidos pelo scraper estão nos [boletins epidemiológicos](http://www.saude.rn.gov.br/Conteudo.asp?TRAN=ITEM&TARG=7549&ACT=&PAGE=0&PARM=&LBL=Boletins+Epidemiol%F3gicos) divulgados pela SESAP-RN. A criação e manutenção no scraper deve ser creditada a:

- [gabicavalcante](https://github.com/gabicavalcante): autoria
- [leobezerra](https://github.com/leobezerra): revisão e validação


## Informações sobre o scraper

No momento, o scraper raspa os boletins do último mês e faz a coleta dos casos suspeitos, descartados e confirmados apresentados na Tabela 1.

- script: `corona_rn_spider.py`
- dependências: `requirements.py`
- dependências: `requirements-dev.py`
- arquivo base de coordenadas: `coordenadas-rn.csv`

## Rodar

Para rodar o scraper basta executar no terminal:
```
$ sh collect.sh
```

Como resultado as seguites pastas vão ser criadas/atualizadas:

- **download**: contém os pdfs baixados pelo crawler 
- **log**: contém o arquivo de log 
- **output**: contém o csv resultante do scraper 

## TODO:
  - [x] raspar links para os boletins
  - [x] raspar casos suspeitos, descartados e confirmados
  - [ ] adicionar coordenadas geográficas ao CSV produzido
  - [ ] adicionar obitos
  - [ ] pegar data dos boletins automaticamente 