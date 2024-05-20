# CURRENCY EXCHANGE
Bem vindo à documentação do Currency Exchange. Sistema *fictício* de conversão de valores monetários da Data Stone.

## REQUISITOS
- Git instalado e atualizado
- Docker instalado e atualizado
- Possuir Python3.12.3 instalado e atualizado 
- Preferencialmente Sistema Linux Ubuntu 22.04 ou 24.04

## INSTALAÇÃO

### Rodando a aplicação local sem o Docker

1. Adquirir o código fonte via repositório git branch *main*.
2. Criar um *virtual environament*.
3. Instalação de dependências do projeto.
4. Configurar a aplicação Django.
5. Rodar a aplicação.

```
# clone repository
git clone https://github.com/AndreMyszko/ds_convert_cash.git
cd ds_convert_cash

# create a virtual environament named as *venv* and *activate* it 
python -m venv venv
. venv/bin/activate

# install required packages
pip install -q -r requirements.txt

# make the migrations
python manage.py show migrations
python manage.py makemigrations
python manage.py migrate

# create a superuser for /admin login
python manage.py createsuperuser

# run the application
python manage.py runserver

# para encerrar a aplicação apenas use o atalho: "*CTRL+C*"
```

### Rodando a aplicação com Docker
```
# O certo é não utilizar o camando *sudo*, mas sim alterar o *chmod* do Docker em */var/run/docker.sock*.

# build do container
sudo docker build -t ds_convert_cash .

# run do container
sudo docker run -d --name ds_convert_cash -p 8000:8000 ds_convert_cash:latest

# OPTIONAL: you also can access the container terminal than create a superuser
sudo docker exec -it <your-container-id> bash
python manage.py createsuperuser
exit

# parar o container
sudo docker stop ds_convert_cash

# remover o container
sudo docker rm ds_convert_cash
```

### checar se a imagem está na lista de containers do docker
```
sudo docker ps ds_convert_cash
```
O *outpu* deve ser algo como isso:
```
CONTAINER ID   IMAGE                    COMMAND                  CREATED          STATUS         PORTS      NAMES
2d4da929ce42   ds_convert_cash:latest   "python manage.py ru…"   11 seconds ago   Up 7 seconds   8000/tcp   ds_convert_cash
```

## UTILIZAÇÃO 
A utilização da API é simples e conta apenas com dois ENDPOINTS: 

"*/*": retorna os valores atuais para todas as moedas - USD, BRL, EUR, BTC e ETH.  
"*/exchange*": retorna a conversão de uma moeda para outra a partir da quantia desejada.

### ENDPOINT PARA CONSULTA DOS VALORES DE CADA MOEDA 
Retornar o valor atual de cada moeda em relação ao USD.

#### Exemplo URL request:
```
# [GET]
http://127.0.0.1:8000/
```
#### Exemplo de JSON response:
```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "currency": {
        "USD": "1.00000000",
        "BRL": "5.12957200",
        "EUR": "0.91971600",
        "BTC": "0.00001501",
        "ETH": "0.00032440"
    }
}
```

### ENDPOINT PARA CONVERSÃO DE VALORES
Retorna o valor convertido de uma moeda para outra.

#### Tipos de moedas aceitas:
- USD
- BRL
- EUR
- BTC
- ETH

#### Estrutura da URL:
```
# [GET]
http://127.0.0.1:8000/exchange/?from={YOUR_CURRENCY}&to={YOUR_CURRENCY}&amount={YOUR_AMOUNT}
```

#### Recebe como parâmetros: 
 - A moeda de origem "*from*".
 - A moeada a ser convertida "*to*"
 - O valor a ser convertido "*amount*"

#### Retorna um dicionário JSON com estes atributos:
 - A moeda de origem "*from*".
 - O valor a ser convertido "*amount*"
 - A moeada a ser convertida "*to*"
 - O valor total convertido "*exchange*"

#### Exemplo de URL request:
```
# [GET]
http://127.0.0.1:8000/exchange/?from=BTC&to=EUR&amount=15.4895
```

#### Exemplo de JSON response:
```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "exchange": {
        "from": "BTC",
        "amount": " 15.48950000",
        "to": "EUR",
        "exchange": "952905.75130435"
    }
}
```

## UTILIZAÇÃO DE TESTES DA APLICAÇÃO
1. Compatível com *pytest*.
2. Certifique-se de que seu ambiente está configurado para testes e que os testes estejam direcionados para o app *core*.
```
# exemplo de settings.json
{
  "python.testing.pytestArgs": ["core"],
  "python.testing.unittestEnabled": false,
  "python.testing.pytestEnabled": true
}
```

3. Para executar os testes pré configurados pela aplicação utilize o gerenciamento padrão.
```
python manage.py test
```


## APIs EXTERNAS UTILIZADAS

Endpoint fornecido pela API de moedas comuns - USD, BRL, EUR:
```
https://open.er-api.com/v6/latest/USD
```

Endpoint fornecido pela API de crypto moedas - BTC, ETH:
```
https://api.coingecko.com/api/v3/simple/price
```

## TÉCNOLOGIAS
pyenv, python, venv, django, restframewrok, requests, api, restful, sqlite, json, docker, pytest.