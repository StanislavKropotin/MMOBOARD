from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Article(models.Model):
    TYPE = (
        ('Tank', 'Танк'),
        ('Heal', 'Хилер'),
        ('DD', 'ДД'),
        ('Byer', 'Торговец'),
        ('Gildmaster', 'Гилдмастер'),
        ('Kvestiver', 'Квестивер'),
        ('Blacksmith', 'Кузнец'),
        ('Tanner', 'Кожевник'),
        ('Potion', 'Зельевар'),
        ('Spellmaster', 'Мастер заклинаний'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=128, choices=TYPE, default='Tank')
    image = models.ImageField(upload_to='uploads/', blank=True, null=False)

    def __str__(self):
        return f'{self.title}{self.text[:50000]}{self.author}{self.category}'

    def get_absolute_url(self):
        return reverse('article', kwargs={'pk': self.pk})


class UserResponse(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    dateCreation = models.DateTimeField(auto_now_add=True)



