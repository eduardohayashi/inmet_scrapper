# inmet_scrapper

Scrapper de dados de estações automáticas do INMET - Instituto Nacional de Meteorologia
http://www.inmet.gov.br/portal/index.php?r=estacoes/estacoesAutomaticas

## Requisitos de instalação
- python 3.4
- requests 2.14.*
- beautifulsoup4 4.6.*
- python-dateutil 2.6.*
- pymongo 3.6.*
- dnspython 1.14.*
- mongodb 3.6 (local ou remoto)

## Instalação 

```
git clone https://github.com/eduardohayashi/inmet_scrapper.git
cd inmet_scrapper
pip3 install -r requirements.txt
```
Se estiver utilizando o Anaconda, ative um ambiente com Python3.4+ ou crie um novo, antes de usar o pip


## Configuração
Faça uma cópia do arquivo **inmet_scrapper/settings.default.py** com o nome **settings.py** e insira lá as suas configurações do MongoDB. Pode ser uma instalação local ou remota.


## Exemplo de Utilização 
```python3 service.py -c A001```

Esse comando vai trazer os dados da estação **A001** do INMET, que é a estação localizada em Brasília/DF.
Na página http://www.inmet.gov.br/portal/index.php?r=estacoes/estacoesAutomaticas você pode identificar a localização e o código de todas as estações, e assim fazer a coleta apenas da(s) estação(ões) desejada(s)

Assim, para pegar os dados da estação de Cuiabá/MG, deverá rodar desse modo:
```python3 service.py -c A901```

Eu adicionei um arquivo de referencia - [estacoes_inmet.txt](https://github.com/eduardohayashi/inmet_scrapper/blob/master/estacoes_inmet.txt) - que pode ser usado pra consultar os códigos e as localidades.

## Observações
No momento, o sistema traz apenas os dados de ontem e hoje, assim para uma coleta eficiente bastará rodar uma vez por dia para cada estação.
No INMET os dados ficam disponíveis por até um ano, então numa próxima atualização colocarei uma opção para coleta de datas personalizadas.

