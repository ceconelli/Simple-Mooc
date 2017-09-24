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
<a href="{% url 'nome_do_namespace:nome_da_url' %}">link</a>
```
* Dessa forma, pesquisa-se primeiro qual app tem o namespace igual a `nome_do_namespace`. Caso entrado o app, procura-se nas urls desse app qual tem o `name` igual a `nome_da_url`.
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
```
python manage.py makemigrations # Cria um migration file
python manage.py migrate # Aplica a migração ao banco de dados
```

#### **Image Field**
```python
image = models.ImageField(upload_to = 'path',verbose_name='nome') #upload_to -> local onde as imagens do usuario serao colocadas
```
* É preciso installar o pillow para que o django reconheça se o arquivo é mesmo uma imagem (pip install pillow)

#### **Custom Model manager**
É possível criar uma classe dentro do próprio model, de forma a customizar o que aparecerá no `admin` do site:
```python
#Dentro do seu model

#O nome que aparecerá no admin será o atributo name
	def __str__(self):
		return self.name
#ordena o db pelo atributo name,e muda o nome do model
	class Meta:
		verbose_name = 'Curso'
		verbose_name_plural = 'Cursos'
		ordering = ['name']
```
É possível fazer mais customizações.

---

### **Consultas ao banco de dados**
Caso voce tenha um modelo no seu banco de dados, é possível fazer queries:
```python

	aux = Nome_do_seu_modelo.objects.all() #isso retorna todos os objetos do tipo Nome_do_seu_modelo
	aux = Nome_do_seu_modelo.objects.filter(atributo_do_seu_modelo = 'algum_especifico')
	aux = Nome_do_seu_modelo.objects.filter(atributo_do_seu_modelo = 'algum_especifico').filter(outro_atributo = 'algum_especifico')
```
## **ADMIN**
Na seção `admin` é possível gerenciar o banco de dados

* Depois de criar algum model, é preciso adicioná-lo ao `admin.py` do app :
```python
from .models import seu_model
	# Register your models here.
	admin.site.register(seu_model)
```
* Para acessar o admin, é preciso cadastrar um `superuser` antes:
```
python manage.py create superuser 
``` 
#### **Configurar o admin**
É possível criar uma classe que herda de admin.ModelAdmin, que contem atributos que alterarão a exibiçao no admin. Ex:

```python	
# Em admin.py
	class CourseAdmin(admin.ModelAdmin):
		list_display = ['name','slug','start_date','created_at']
		search_fields = ['name','slug']
		prepopulated_fields = {'slug':('name',)}
```
* `list_display` fará com que somente os campos especificados apareçam no admin.
* `search_fields` fará com que apareça uma aba de pequisa que pesquisará nos campos especificados.
* `prepopulated_fields` fará com que o campo slug seja preenchido automaticamente com o nome (retirando espaços e acentos)
* Um `modelAdmin` está associado a um model, logo é preciso registrá-lo junto com seu Model: 
```python
# Em admin.py
	admin.site.register(Seu_model,Seu_modelAdmin)
```

# **Renderizando uma página com dados do db**
Para mostrar imagens presentes no banco de dados em um template, é preciso carregá-las da seguinte maneira:
```HTML
<img src="{{ course.image.url }}">
```
No entanto, para que essas imagens estejam presentes no banco de dados, é preciso indicar o caminho onde elas serão armazenadas. Para isso, é preciso criar duas variáveis em `settings.py`:
```python
MEDIA_ROOT = os.path.join(BASE_DIR,'nome_do_projeto','media')
MEDIA_URL = '/media/'
```
Após definir os paths, é preciso adicioná-lo à `urls.py` do projeto, da seguinte maneira:
```python
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
```
Dessa maneira, será criada a seguinte estrutura de diretórios:

* diretório_do_projeto
  * nome_do_projeto
     * media

O upload de imagens será feito em `media`, dentro do diretório passado como parâmetro no model.Ex:

```python
image = models.ImageField(upload_to='courses/images',verbose_name='Imagem')
```
Portanto, as imagens serão armazenadas em:

* diretório_do_projeto
  * nome_do_projeto
     * media
         * courses
             * images

# **Carregando arquivos estáticos para um template**

Deve-se criar uma pasta `static` dentro do app, então, para referenciá-lo no template, é preciso colocar {% load static %} no inicio do template.

No `scr` ou `href`, fazer :
```html
<img src="{% static 'img/nome_da_imagem' %}">
<link rel="stylesheet" type="text/css" href="{% static 'css/nome_do_arquivo.css' %}">
```




