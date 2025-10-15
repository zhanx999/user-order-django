from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField( max_length=50, blank=False)
    email = models.EmailField( max_length=254,blank=False)
    age = models.IntegerField(blank=False)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
    
    def __str__(self):
        return self.name


class Order(models.Model):
    title = models.CharField(blank=False, max_length=50)
    description = models.TextField()
    user= models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
    def __str__(self):
        return self.title

