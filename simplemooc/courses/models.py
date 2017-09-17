from django.db import models

# Create your models here.


class CourseManager(models.Model):
	def search(self,query):
		return self.get_queryset().filter(
			models.Q(name__icontains=query) |
			models.Q(description__icontains=query)
		)

class Course(models.Model):
	name = models.CharField('Nome',max_length=100)
	slug = models.SlugField('Atalho') #Campo de URL
	description = models.TextField('Descrição',blank=True) #blank=True -> Campo nao é obrigatorio
	about = models.TextField('Sobre o curso',blank=True)
	start_date = models.DateField('Data de Inicio',null=True,blank=True)
	image = models.ImageField(upload_to='courses/images',verbose_name='Imagem',blank=True,null=True)
	created_at = models.DateTimeField('Criado em',auto_now_add=True) #campo data hora, a hora que for criado sera colocada no db
	uploaded_at = models.DateTimeField('Atualizado em',auto_now=True) #a data sera atualizada toda vez que ocorrer uma mudança salva

	objects = CourseManager() #acrescenta o metodo search ao objects

	# Esse metodo serve para que o nome do objeto apareça no db(admin)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Curso'
		verbose_name_plural = 'Cursos'
		ordering = ['name']
#null=True -> caso seja feita uma consulta no db, ele ira retornar Null se o campo nao for preenchido