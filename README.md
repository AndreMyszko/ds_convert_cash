# CURRENCY EXCHANGE
Bem vindo à documentação do Currency Exchange. Sistema *fictício* de conversão de valores monetários da Data Stone.

## REQUISITOS
- Git instalado e atualizado
- Docker intalado e atualizado
- Possuir Python3.12.X
- Sistema Linux 22.04 ou 24.04

## INSTALAÇÃO


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
pyenv, python, venv, django, restframewrok, requests, api, restful, sqlite, json.