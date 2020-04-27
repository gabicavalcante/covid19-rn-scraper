# covid19-rn-scraper

![](https://github.com/gabicavalcante/covid19-rn-scraper/workflows/CI/badge.svg) 


Scraper criado para dar suporte ao projeto de visualização de dados do Covid19 (https://leobezerra.github.io/covid19/).
Os dados extraidos pelo scraper estão nos [boletins epidemiológicos](http://www.saude.rn.gov.br/Conteudo.asp?TRAN=ITEM&TARG=7549&ACT=&PAGE=0&PARM=&LBL=Boletins+Epidemiol%F3gicos) divulgados pela SESAP-RN. A criação e manutenção no scraper deve ser creditada a:

- [gabicavalcante](https://github.com/gabicavalcante): autoria
- [leobezerra](https://github.com/leobezerra): revisão e validação


## Informações sobre o parser

No momento, o parser desenvolvido raspa os casos suspeitos e confirmados apresentados na Tabela 1. Adicionalmente, o parser pode adicionar coordenadas geográficas ao CSV produzido.

- script: `rn-parser.py`
- dependências: `requirements.py`
- arquivo base de coordenadas: coordenadas-rn.csv