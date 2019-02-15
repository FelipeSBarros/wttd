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
1. Criamos a index.html;    

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

O **manage.py** é o endpoint do Django. Vamos utilizá-lo para ativar todos os recursos do Django.  
  
Para poder acessar o manage.py a partir de outras pastas, podemos criar um *alias*:
```commandline
alias manage='python $VIRTUAL_ENV/../manage.py'
```
Esse *alias* pode ser adicionado ao `~/.bashhrc` ou `~/.profile`;  

#### Rodando o servidor do Django  

```commandline
manage runserver
```  

### Criando  uma Django app  

app é uma biblioteca python que segue conveções do Django.

```commandline
manage startapp core #core e o nome dado a app
```
Nossa app criada (*core*) deve estar dentro da pasta do projeto Django (*eventex*, neste caso), que estará dentro do diretório de trabalho (*wttd*, neste caso).  
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
  
1. Adicionamos ao *tamplate* a arte (pagina) do designer;  
1. Mudamos o caminho aos arquivos;    

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
  
1. Instalação do heroku
1. Login
  
### Deploy no Heroku  

Instalando `heroku toolbelt`:  
`sudo snap install --classic heroku`

##### login

`heroku login`

## M1A28  
  
1. Usamos o `python-decouple` para não deixar secret_key no codigo fonte do nosso projeto;  
1. Usamos o `dj-database` para quando estivermos em produção, usar o Postgre e não o SQLite;  
1. Habiitamos `static_files` com `dj-static`;  
1. Registramos e atutenticamos o projeto e enviamos ao *Heroku* por git;   
  
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
Dessa forma, sempre que for rodada a app, o decouple busca se o `DATABASE_URL` exite no `.env`. Não existindo ele usa o `default_dburl` (SQLite), usando o cast que irá retorná-lo como um dicionário de configuração do Django;  

### Allowed Hosts  

Heroku necesita saber se vai escutar tudo. Para isso:  
`ALLOWED_HOSTS = [*]`

### Configurando static files  

Para onde serão copiados todos os arquivos estaticos que no momento estão no core>static  
Como se trata de arquivos estatucos, não faz sentido passar por todo o processo sempre. Podemos separar em outro servidor, se for o caso.  
em `settings`:  
```python
STATIC_URL: '/static'
STATIC_ROOT: os.path.join(BASE_DIR, 'staticfiles') #   
 
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

## M2A01  

Sobre atualização de versões do Django:

Usar freeze para checar a versão;
Para upgrade:  
`pip install --upgrade django`  
**Atualizar o freeze!**
usar:
`manage check` Para identificar se há alguma modificação a ser feito devido ao *update*;  
`manage test` Para ver se precisa alterar algo de teste...  
commitar e enviar ao heroku;  

## M2A03  

Mandamos nosso site para produção, mas deixamos o `DEBUG = True`, o que é perigoso por expor algumas informações sensíveis;  
Para corrigir isso:
No ambiente virtual:
`heroku config:set DEBUG=False`  

Para mais informações:
`heroku config --help`

### **Explorando flag DEBUG**
Em settings, "setar" `ALLOWED_HOSTS = []`  
 
 Se DEBUG = False temos que definir o `ALLOWED_HOSTS` e também o `collect static`:  
 `python3 manage.py collectstatic`;
 
 A ideia geral é que em desenvolvimento, vamos permitir dois hosts: 127.0.0.1 e o localhost (e qualquer subsominio de localhost);
 `ALLOWED_HOSTS = ['127.0.0.1', '.localhost', '.herokuapp.com']`
 
 Como o `ALLOWED_HOST` é a configuração da instancia, temos que ir ao `.env`, para adicionar o `ALLOWED_HOST`:
`ALLOWED_HOSTS=127.0.0.1, .localhost, .herokuapp.com`  

Configurando o `DECOUPLE` também:
`ALLOWED_HOSTS = config('ALLOWED_HOSTS', default=[], cast=Csv())`
**E a linha criada anteriormente (ALLOWED_HOSTS) já poderá ser removida!**  
  
  **Não deixar de agregar *Csv* ao import**:
Ficando:
`from decouple import config, Csv`  

**Agora é configurar a var de ambiente e enviar ao Heroku**
`heroku config:set ALLOWED_HOSTS=.herokuapp.com`
Caso houvesse domínio customizados, seria o caso de adiciona-lo apos virgula.  

O heroku config fica assim:
```commandline
heroku config
=== eventex-felipesbarros Config Vars
ALLOWED_HOSTS: .herokuapp.com
DATABASE_URL:  postgres://qbkkdmugaqbukg:88e[...]h68f
DEBUG:         True
SECRET_KEY:    aaa
```
  
Agora e mandar as alterações ao Heroku pelo Git.

**Isso tudo foi feito para que possamos trabalhar em diferentes configurações de ambiente (desenvolvimento/produção) garantindo que`DEBUG`, `ALLOWED_HOSTS` serão bem carregados;
Diferença entre config de instancia e config de projeto:  

> Nos arquivos do projeto estão as configurações de instancia; No .env definimos as configurações de projeto, podendo assim, alternar entre produção e desenvolvimento sem ter que mudar a configuração das instancias, já que as mesmas passaram a ser configuradas pelo .env, usando de `decouple`;
> Projeto: codigo fonte (config das app); Já allowed_hosts, secret_key, email, etc são confirgurações de instancia; Com decouple permite que as configurações de instancias seja carregadas de acordo com as variáveis de ambiente;

## M2A04  

Arquivos estáticos X Media:  
Como o Django organiza e como não se enrolar;  
  
* Static: Arquivos estáticos que são parte do código fonte do seu projeto; Estão intrínsecamente vinculados ao código fonte;
    - css; javascripts; fontes; imagens fixas como logo;  
    - static entra no sistema quando se faz um deploy; Está conectado ao ciclo do sistema;  
* Media: Arquivos envidos ao sistem pelo usuário:
    - foto de perfil; planilhas; arquivos zip; qualquer anexo de upload;
    - entra no sistema quando o usuário faz upload; Tem que estar disponível idependente do *realease* do sistema.  
    
Quando estamos com `DEBUG=Flase` o Django não facilita a nossa vida. Ele não liga para os arquivos estáticos;

`manage collectstatic` faz com que o Django corra todo o sistema buscando os arquivos estáticos e os coloca em `proj/staticfiles`. Inclusive arquivos estáticos do Django admin;  
Django não garante a segurança do serviço dos arquivos estaticos; o dj-statics, sim.

Para provar como seria isso sem o dj-static, podemos desativa-lo no wsgi.py;  
Mesmo os dados estando na pasta staticfiles o Django não serve os arquivos, estando DEBUG=False e o dj-static (Cling) desabilitados (sem uso);  
O dj-static é necessário quando estivermos usando o Heroku;  

**Quando for deixar os staticsfiles em outro servidor/domínio diferente de onde está a aplicação Django, basta em static_URL e informar o link e porta apra os staticfiles.**  
Assim , pode-se ter uma aplicação divida em dois servidores:  
  
* Um servidor dedicado à aplicação (pagina dinâmica);
* Outro servidor dedicado aos arquivos estáticos;  

Exemplos do processo de serviço dos arquivos estáticos:  

![](./imgAnotacoes/staticfilesDiagrama.png)  

![](./imgAnotacoes/staticfilesHeroku.png)  

![](./imgAnotacoes/staticfileAmazon.png)  

Toda essa aula foi voltada para mostrar como o Django serve os arquivos estáticos, como o Heroku o processa e alternativas relacionadas a isso.  

## M2A05  

**TAFT: Test All The Fucking Time!**  

## M2A07  

**Todo erro diferente de assertionError é considerado ERRO no teste;**
**Quando temos assertionError, temos uma falha!**
**Resolver erro é mais prioritário que resolver falha**


**Katar**: Esculpir o código conforme a demanda do teste

**TDD não é fazer teste combinatório de tudo o que é possível e imaginável**; É criar código com confiança dos limites do código;

**O ideal é que as funções tenham apenas um `return`:. um ponto de saida.**

## M2A08  

**Um problema em se usar `assert` é que ele para onde houve erro. Não executa os demais testes;**  
A ideia é rodar todos os teste;  

Se assert é uma excessão podemos usar um try/except; Como teríamos que fazer isso a cada um dos testes, pode-se incluir isso em uma função:
```python
def assert_true(expr):
    try:
        assert expr
    except AssertError:
        print(expr)
```

### unittest  

classe desenvolvida para facilitar todo o processo de desenvolvimento de testes.

unittest.CaseTest: clase usadas
unittest.main(): executa os testes
Os testes passam a ser executados pelo test runner;
O interessante de usar o unittest é que além da facilidade, pode-se usar  terminal python, o comando:
`python -m unittest`
Que ele vai varrer os arquivos com extensão .py que tenham `unittest.main()` e os executa, tendo um relatório bem organizado de todos os *testes*, *falhas* e *erros*;  
  
#### O que o unittest faz?
  
* A partir do dir corrente, o testRunner, vai:
    * Procurar e carregar o módulo/package test*.py; (**Suites de teste**)  
    * Identifica cada cenário de teste; (**testCase**)  
    * Identificad cada teste nos cenários de teste; (**TestMethod**)  
    * Executa o *SetUp* (prepara o contexto do teste), *Teste*, e *tearDown* (limpa efeitos colaterais do teste) para cada teste;  

**Executando o teste no Django:**
`manage test`  
`manage test eventex.core` (só teste dentro do core)  
`manage test eventex.core.HomeTest` (apenas um cenário: HomeCore - clase TesteCase dentro do pacote)  
`manage test eventex.core.HomeTest.test_get` (apenas um método específico, o `test_get` dentro cenário HomTest)  

Há vários `asserts` do unittest. E o Django incrementa a lista  

![](./imgAnotacoes/assertUnittest.png)    
    
![](./imgAnotacoes/assertDjango.png)  

