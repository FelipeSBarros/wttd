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