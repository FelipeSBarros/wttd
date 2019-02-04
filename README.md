# Welcome To The Django

Repositório com tarefas e anotações extraídas do curso [Welcome to the Django](Welcometothedjango.com)  

```commandline
sudo apt-get install tree # para ver pastas e subpastas como arvore
```  

## M1A25  

Passos:  

1. Cria-se projeto Django (Eventex);  
1. Cria-se uma Django app (core);  
1. Adiciona app `core` ao settings (`eventex.core`);  
1. Configuramos uma rota para a raiz do site;  
1. Associamos a rota a uma view home dentro da app `core`;  
1. Criamso a index.html;    

### Organização  

```python
# Criando diretório para receber o projeto Django  

mkdir wttd  

# entrando na pasta  
cd wttd  

# criando ambiente virtual (venv)  
python3 -m venv .wttd  # cria diretorio oculto para separar arquivos e codigos do venv separados do projeto DjAngo

# para ativar venv:
source .wttd/bin/activate

# instalando django
pip install django
```
### Criando projeto Django  

```python
django-admin startproject eventex . #eventex e o nome do projeto; o ponto indica que projeto deve ser criado no diretorio raiz;  
# Caso ponto não seja indicato, uma pasta com o nome do projeto será criada apra armaneza-lo...
```  
  
O projeto criado é um pacote de python, uma vez que possui o dunder init (`__init___`)

O **manage.py** é o endpoint do Djngo. Vamos utilizá-lo para ativar todos os recursos do Django.  
  
Para pode acessar o manage.py a partir de outras pastas, podemos criar um *alias*:
```commandline
alias manage='python $VIRTUAL_ENV/../manage.py'
```
Esse *alias* pode ser adicionado ao `~/.bashhrc` ou `~/.profile`;  

#### Rodando o servidor do Django  

```commandline
manage runserver
```  

### Criando  uma Django app  

app é uma biblioteca python que segue conversões do Django.

```commandline
manage startapp core #core e o nome dado a app
```
Nossa app criada deve estar dentro da pasta do projeto Django (eventex, neste caso), que estará dentro do diretório de trabalho (wttd, neste caso).  
Nota mental: Por isso, mais à frente vamos inserir em `settings.py` o `eventex.core` em `INSTALLED_APPS`  
  
* Manage.py está alinhado ao eventx (é irmão);
* Dentro do *core* estará o *models*, *tests* e *views*;  

### Adicionando app ao settings  

No `settings.py` que está na pasta do projeto (eventex, neste caso), vamos adicionar `eventex.core` na lista de `INSTALLED_APPS`  
 **Não deixar de colocar mais uma virgula após a string nova**;  
 
### Adicionando uma rota  

O `urls.py` é a raiz de todas as rotas da nossa aplicação....  
Há duas formas de trabalhar com rotas:
`pasths` ou `expressões regulares`;  
Em `urlpatterns` vamos adicionar `path('', eventex.core.views.home)` # string vazia indicando a raiz do site;
Além disso, precisaremos garantir que `urls.py` está carregando a nossa app *core*:
`import eventex.core.views`  

### Criando view:  

Em core, abrimos `views.py` e inserimos uma função que receberá o request, a processará e retornará  
> Toda view do Django é um objeto chamado (função, classe, instancia). Sempre recebe como primeiro prâmetro uma instancia de  HTTP REQUQEST, e sempre retorna uma instancia de HTTP RESPONSE.  

O DJango possui um **render** que irá processar o request com um template (index.html) retornando uma instancia do http response....  

```python
def home(reques):
    return render(request, 'index.html')
```  

### Criando template a ser renderizado  

Em `core` criamos novo diretório chamado *templates* e dentro criamos *index.html*;  
Editamos a HTML para exibir o que desejamos e vemos rodar o servidor para ver o resultado.  

## M1A26  

### Adicionando arte do designer  

Em `core`, adicionar uma nova pasta `static` onde colocaremso os arquivos estaticos: `css, fonts, img, js`  
E o arquivo `index.html` vai para o `template`, substituir o `index.html` criando antes;  

Todos os arquivos estaticos tiveram erro (404) pq os caminhos relativos do designer não bate já que estamos usando o Django para isso e usando pastas diferentes:
```commandline
"GET /img/sponsor-silver-04.png HTTP/1.1" 404 2115
```

#### Template tag:  

Adicionamos no início do index.hmtl:
{% load static %}  

E alteramos todos os path relativos que deram erro (ex.: `img/favicon.ico`), ficando: 
<link rel="shortcut icon" href=" { % statuc% 'img/favicon.ico' % } ">  

**O que está entre chaves é o template do Django. o memso será processado pelo template e retornado**;  
Sugestão: aspas dupla (") para HTML e aspas simples (') para Django teplate;  


Para fazer alteração de tudo usando o find/replace usando expressões regulares:  

`(src|href)="((img|css|js).*?)"`
Replace: `$1="{% static '$2' %} "`  

## M1A27  

### Deploy no Heroku  

Instalando `heroku toolbelt`:  
`sudo snap install --classic heroku`

##### login

`heroku login`

## M1A28  

Algumas configurações necessárias antes do deploy pois temos um projeto com várias instancias. Precisamos separar do codigo os elementos que são das instancias e não do projeto.  

**Não deixar SECRET_KEY dentro do codigo fonte!!!!**  

### Python-decouple  

[python-decouple](https://pypi.org/project/python-decouple/)  
#### Instalação:  

`pip install python-decouple`    

Em `setting.py`:  
`from decouple import config`  

substituir `SECRET_KEY = ASASAQW` por `SECRET_KEY = config('SECRET_KEY')`.  
Sendo que o primeiro será adicionado a um arquivo `.env` na raiz do nosso projeto (**Removendo aspas e espaços**).  

Mesma coisa com `DEBUG`:
Settings: `DEBUG = config('DEBUG', default=False, cast=bool`  
.env: `DEBUG=True`  

### Base de dados  
Usar sqlite3 em desenvolvimento mas não em produção (usar PostgreSQL)

### Python dj-database  

[dj-database](https://pypi.org/project/dj-database-url/)

#### Instalação:  
`pip install dj-database-url`  

Capacidade de parsear e identificar dicionario de configuração do Django  

#### Configuração
Criar uma url default:
```python
default_dburl = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
DATABASES = {
    'default': config('DATABASE_URL', default_dburl, cast=dburl),
    }
```

### Allowed Hosts  

Heroku necesita saber se vai escutar tudo. Para isso:  
`ALLOWED_HOSTS = [*]`

### Configurando static files  

Para onde serão copiados todos os arquivos estaticos que no momento estão no core>static  
Como se trata de arquivos estatucos, não faz sentido passar por todo o processo sempre. Podemos separar em outro servidor, se for o caso.  
em `settings`: 
```python
STATICS_URL: '/static'
STATICS_ROOT: os.path.join(BASE_DIR, 'staticfiles') #   
 
```

### dj-static  

> Para servir os arquivos estaticos antes de chegar a requisição ao Django;  


[dj-static](https://pypi.org/project/dj-static/)
  
Agora vamos ao `wsgi.py` e alteramos para:  
```python
import os
from dj_static import Cling
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventex.settings')

application = Cling(get_wsgi_application())
```  
### Registrando dependencias do projeto  

No terminal:  
`pip freeze > requirements.txt`
```commandline
dj-database-url==0.5.0
dj-static==0.0.6
Django==2.1.5
pkg-resources==0.0.0
python-decouple==3.1
pytz==2018.9
static3==0.7.0
```

**Porém `heroku` tem algumas outras dependencias.**
Devemos incluir:  
`gunicorn=19.8.1`
`psycopg2=2.7.4`

### Criando arquivo para heroku iniciar o programa  

Criar `Procfile`na raiz do projeto (wttd); **Com P MAIUSCULO e sem extenção**;  
  
Adicionar:
`web: gunicorn eventex.wsgi --log-file -`

## Sobre repositório GIT  
Adicionar apenas arquivos fonte. Não adicionar arquivos gerados a partir de processamento...

`.idea` é relacionado ao projeto pycharm.
Remover o sqlite3 caso ele não vá ser usado (como é o nosso caso);  

### Heroku:  

`heroku apps:create eventex-felipesbarros`  
Para confirmar  
`git remote -v`  
Para confirmar criação app:  
`heroku open`   

### Configurar variáveis de ambiente produção/projeto  
Para saber as variáveis:
`cat .env`  

Usando aspas simples!  
`heroku config:set SECRET_KEY = 'COPIAR O Que ESTA EM .env'`  

`heroku config:set DEBUG=True`  

#### Enviando ao Heroku:  

`git push heroku master --force`  