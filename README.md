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
CONTAINER ID   IMAGE                    COMMAND                  CREATED          STATUS          PORTS                                       NAMES
8a7d7beb874d   ds_convert_cash:latest   "python manage.py ru…"   11 minutes ago   Up 11 minutes   0.0.0.0:8000->8000/tcp, :::8000->8000/tcp   ds_convert_cash
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
2. Para executar os testes pré configurados pela aplicação utilize o gerenciamento padrão.
```
python manage.py test
```
Caso o camando falhe, certifique-se de que seu ambiente está configurado para testes e que os testes estão direcionados para o app *core*.
```
# exemplo de settings.json
{
  "python.testing.pytestArgs": ["core"],
  "python.testing.unittestEnabled": false,
  "python.testing.pytestEnabled": true
}
```

## POR QUE ESTAS ABORDAGENS FORAM UTILIZADAS?
- BANCO DE DADOS
Banco de dados 'db.sqlite3' por se tratar de um microsserviço sem persistência de dados, esta abordagem é mais do que suficiente para lidar com os dados gerados pelo django para seu gerenciamento para finalidade de uma POK.

- ARQUITETURA
A separação de responsabilidades entre os serviços e a camada de vizualização a fim de aplicar boas práticas, além de facilitar o crescimento da aplicação. A aplicação faz suas requisições dentro de laços try/excep, desta forma controlando restornos imprevistos, e que os usuário estejam sempre acompanhando os valores atuais provenientes das APIs externas, gerando mensagem de erro como retorn para as requisições que não tiveram exito com no caso de *Too many requests*.

- TESTE
Testes com cobertura simples das funcionalidades básicas do aplicativo, garantindo valores máximos e mínimos para as moedas. Foram criados ao todo 4 testes, dois para checagem dos serviçoes e dois para checagem das views.

- UTILIZAÇÃO
A api foi pensada para ser simples, poderiam haver mais tipos de moedas com o mínimo de esforço, mas fiquei mais atento para a estrutura da aplicação em si. Da forma com que ela se encontra é capaz de rodas diretamente apenas utilizando Python3.12.3 ou utilizando o Docker o que é ideal para ambientes clusterizados e sucetíveis a orquestração de infraestrutura.

- PRÓXIMAS ATUALIZAÇÕES POSSÍVEIS
1. Criação de um arquivo .YAML para automação de processos de *workflow* para o *git* e Gerenciamento de *pull requests* para a branch *main* utilizada para "produção". Isso possibilitaria o controle de versões das imagens docker da aplicação, a forma com que é feito o deploy dela entre outras funcionalidades interessantes.
2. Estudo de caso para utilização de ferramentas *cloud* como Google Cloud *Source Repository* e *Artifactory Manager* utilizadas para versionamento de código fonte e versionamento de imagens docker respectivamente. Poderia utilizar o Google *Secret Manager* para gerenciamento de chaves e passwords da aplicação em produção que rodaria em um *GKE - Google Kubernetes Engine*, desta forma podendo utilizar boas práticas, como por exemplo fornecer a aplicação em diversas regiões e possibilitar o *load balancing*. Poderiam ser utilizadas *contas de serviço* para gerenciamento automático e seguro da aplicação.
3. A aplicação está rodando perfeitamente em Ubuntu 24.04.

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
pyenv, python, venv, django, restframewrok, requests, api, restful, sqlite, json, docker, pytest, linux, ubuntu, bash, vscode, git, vscode.