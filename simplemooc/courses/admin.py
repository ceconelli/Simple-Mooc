from django.contrib import admin
from .models import *
# Register your models here.
#Customize o model do admin aq

class CourseAdmin(admin.ModelAdmin):
	list_display = ['name','slug','start_date','created_at']
	search_fields = ['name','slug']

admin.site.register(Course,CourseAdmin)