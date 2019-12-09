from django.db import models
import os
# Create your models here.

def get_image_path(instance, filename):
    return 'static/img/'+filename

class Category(models.Model):
    category = models.CharField(max_length=50,verbose_name='Kategori', unique=True)

    def __str__(self):
        return self.category
    
    class Meta:
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategori'

class Question(models.Model):
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True,verbose_name='Fotograf')
    text = models.TextField(verbose_name='Soru', unique=True)
    trueAnswer = models.CharField(max_length=50,verbose_name='Dogru Cevap')
    falseAnswer1 = models.CharField(max_length=50,verbose_name='Yanlis Cevap 1')
    falseAnswer2 = models.CharField(max_length=50,verbose_name='Yanlis Cevap 2')
    falseAnswer3 = models.CharField(max_length=50,verbose_name='Yanlis Cevap 3')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,verbose_name='Kategori')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Soru'
        verbose_name_plural = 'Soru'

class Student_Log(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,verbose_name='Soru')
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE,verbose_name='Ogrenci')
    date = models.DateTimeField(blank=True, null=True,verbose_name='Tarih')
    answer = models.BooleanField(verbose_name='Dogru')


    class Meta:
        verbose_name = 'Ogrenci Kayitlari'
        verbose_name_plural = 'Ogrenci Kayitlari'

