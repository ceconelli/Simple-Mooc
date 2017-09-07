# **Django**
## Definições
DJANGO - ARQUITETURA MVT(MODEL,VIEW,TEMPLATE)<br>
VIEW: CONTROLLER -> recebe um **Request** e retorna um **Response**<br>
TEMPLATE: VIEW

---
## Inicialização
```
virtualenv -p python3 nome_do_ambiente 
pip install django==versao
django-admin.py startproject nomedoprojeto
```
## Dependências
Quando se clona um projeto em andamento, pode ser que ele esteja usando algumas dependências, que usualmente estão listada em um arquivo `requirements.txt`
```
pip freeze (mostra dependencias instaladas,pacotes)
pip freeze > requirements.txt (cria um arquivo com todas as dependencias que devem ser instaladas)
pip install -r requirements.txt (instala as dependências listadas)
```
---
# **Arquitetura MVT**
## **Views**
O arquivo `views.py` é formado por funções que são endereçadas no arquivo `urls.py`. As funções da View ''mandam'' renderizar um **HTML** (normalmente localizado na pasta `templates` - não é preciso definir o path,como mostrado abaixo) 
Criar funções que retornam um HttpResponse como:
```python
def home(request):
	return render(request,'home.html')
```
## **URL's**
Mapeia uma URL(Request) a uma função da `view.py`. **É importante refatorar o código das urls**, da seguinte maneira:
* Criar um arquivo `urls.py` em cada aplicativo do projeto
* No arquivo `urls.py` principal (do projeto):
```python
url(r'^',include('nome_do_aplicativo.urls'))
```
* No arquivo `urls.py`de `nome_do_aplicativo`:
```python
url(r'^$',views.nomedafuncao)
```
* Dessa forma, ocorre um "redirecionamento" de uma url para outra.

#### É importante colocar nome nas urls, da seguinte maneira:
```python
url(r'^$',views.nomedafuncao,name=nome_da_url)
```
Dessa forma, você pode acessar as url's a partir de um template
##### **OBS:**
Quando se usa o `include('nome_do_aplicativo.urls')`, é bom usar o **namespace**, para que não haja conflito de nomes.

* Caso exitam duas urls com o mesmo nome, porem são de apps diferentes: 
```HTML
href="{% url 'nome_do_namespace:nome_da_url %}
```
#### **URLPATTERN**: 
```python
urlpatterns = patterns('',
    url(r'^$', 'simplemooc.core.views.home',name='home'),
    url(r'^contato/$', 'simplemooc.core.views.contact',name='contact'),
)
```
As primeiras aspas simples `''` podem ser usadas para definir um path para todos os templates a serem renderizados.No exemplo acima ficaria:

```python
urlpatterns = patterns('simplemooc.core.views',
    url(r'^$', 'home', name='home'),
    url(r'^contato/$', 'contact', name='contact'),
)
```
## **TEMPLATES**
Criar uma pasta `templates` no diretório de cada app. Para cada app criado, adicionar seu nome a variável`INSTALLED_APPS` no arquivo `settings.py`

* Criar um arquivo **html** que será renderizado
*  fazer com que a funçao da view retorne uma renderizaçao do html criado:
```python
	def function(request):
		return render(request,'seuhtml.html')
```

* É possível passar parâmetros para a renderização do template,criando um dicionário `context` com as informações:

```python
# Dentro de views.py
	def function(request):
		name = 'Gustavo'
		value = 10
		context = {'name':name,'valor':value}
		return render(request,'seuhtml.html',context)
```

Para acessar os dados (context) no template, é preciso colocar duas chaves: {{ nome_da_variavel }}. É possível acessar atributos e indices(caso for string por exemplo) de uma variável, colocando um ponto e o nome do atributo: {{ nome_da_variavel.atributo }}
-> atributo pode ser um numero (indice): {{ nome_da_variavel.0 }}
-> Tags,filtros
-> Carregar arquivos estaticos para um template (css,javascript...)
-> Herança de templates ({% block content %})

## **MODELS**
---
Ao criar um model, cria-se uma tabela no banco de dados. Ex:

```python
class Treasure(models.Model):
	name = models.CharField(max_length = 100)
	value = models.DecimalField(max_digits = 10,decimal_places = 2)
	material = models.CharField(max_length = 100)
	location = models.CharField(max_length = 100)
	img_url = models.CharField(max_length = 100)
```
É importante notar que um model deve herdar da classe `models.Model`

* Após isso, para que uma função da`view` tenha acesso ao banco de dados, é preciso importá-lo em `views.py`. Dessa forma, será possível que os templates que a view 'chama' renderizem páginas com os dados do banco de dados:
```python
# em views.py
from django.shortcuts import render
from .models import Treasure

def index(request):
	#Treasure.objects.all() retorna todas as instancias de objetos Treasure (model),ou seja, todos os Treasures armazenados no db
	treasures = Treasure.objects.all()
	#{'treasures':treasures} é o context
	return render(request,'index.html',{'treasures':treasures})
	
```

* Após a criação do model, é preciso fazer a migração, o que cria um arquivo na pasta Migrations:
```python
	python manage.py makemigrations # Cria um migration file
	python manage.py migrate # Aplica a migração ao banco de dados
```

#### **Image Field**
```python
image = models.ImageField(upload_to = 'path',verbose_name='nome') #upload_to -> local onde as imagens do usuario serao colocadas
```
* É preciso installar o pillow para que o django reconheça se o arquivo é mesmo uma imagem (pip install pillow)

#### **Custom Model manager**








