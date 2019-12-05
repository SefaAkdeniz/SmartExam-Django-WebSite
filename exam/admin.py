from django.contrib import admin
from . import models

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text','trueAnswer','category')
    list_display_links = ('text','trueAnswer','category')
    list_filter = ('category','trueAnswer')
    list_per_page = 10

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)
    list_per_page = 10

class Student_LogAdmin(admin.ModelAdmin):
    list_display = ('question','user','date','answer')
    list_display_links = ('question','user','date','answer')
    list_filter = ('question','user','date','answer')
    list_per_page = 10

# Register your models here.
admin.site.register(models.Category,CategoryAdmin)
admin.site.register(models.Question,QuestionAdmin)
admin.site.register(models.Student_Log,Student_LogAdmin)