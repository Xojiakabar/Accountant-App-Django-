from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Client)
admin.site.register(Accountant)
# admin.site.register(Job)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['id','title','description','accountant','client','deadline']
    list_editable = ['accountant']
