import datetime
from random import choice

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=150, verbose_name='Username', unique=True)
    avatar = models.FileField(upload_to='avatars/', verbose_name='Загрузите свой аватар')
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    email = models.EmailField(max_length=150, verbose_name='Email', unique=True)
    password = models.CharField(max_length=150, verbose_name='Пароль')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'avatar']

    def __str__(self):
        return self.username

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    lifetime = models.DurationField(default=datetime.timedelta(days=1))
    description = models.TextField(blank=True, verbose_name='Полное описание')
    image = models.ImageField(upload_to='question_image/', blank=True, null=True, verbose_name='Изображение')

    def is_active(self):
        return (self.pub_date + self.lifetime) > timezone.now()

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def percentage(self):
        total_votes = sum(choice.votes for choice in self.question.choice_set.all())
        if total_votes == 0:
            return 0
        return (self.votes / total_votes) * 100

    def __str__(self):
        return self.choice_text

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    votes_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question')
