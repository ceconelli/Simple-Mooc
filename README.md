# **Django**
## Definições
DJANGO - ARQUITETURA MVT(MODEL,VIEW,TEMPLATE)
VIEW: CONTROLLER -> recebe um **Request** e retorna um **Response**.
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
## Views
O arquivo `views.py` é formado por funções que são endereçadas no arquivo `urls.py`. As funções da View ''mandam'' renderizar um **HTML** (normalmente localizado na pasta `templates` - não é preciso definir o path,como mostrado abaixo) 
Criar funções que retornam um HttpResponse como:
```python
def home(request):
	return render(request,'home.html')
```
## URL's
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






