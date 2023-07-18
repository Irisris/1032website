from django.db import models
from django.contrib.auth.models import User
import datetime
from django.conf import settings

class Article(models.Model):
    article_choices = (
        ('E', '科普'),
        ('F', '小说'),
        ('G', '漫画/图像'),
        ('O', '其他'),
    )
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=1, choices=article_choices, default='O')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    pub_date = models.DateTimeField(default=datetime.datetime.now, null=True)
    summary = models.TextField(default='')
    image = models.ImageField(upload_to='articles/images/', blank=True, null=True)

class UserProfile(models.Model):
    gender_choices = (
        ('M', '男'),
        ('F', '女'),
        ('N', '不愿透露'),
        ('O', '其他'),
    )
    nature_choices = (
        ('Z', '主'),
        ('B', '贝'),
        ('W', '双'),
        ('N', '不愿透露'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=1, choices=gender_choices, default='N')
    nature = models.CharField(max_length=1, choices=nature_choices, default='N')
    avatar = models.ImageField(upload_to='avatars/')
    favourite_article = models.ManyToManyField(Article, related_name='favorited_by')
    like_article = models.ManyToManyField(Article, related_name='liked_by')
    dislike_article = models.ManyToManyField(Article, related_name='disliked_by')
    report_article = models.ManyToManyField(Article, related_name='reported_by')

class Image(models.Model):
    article = models.ForeignKey(Article, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='articles/images/')
    is_deleted = models.BooleanField(default=False)

class Chapter(models.Model):
    article = models.ForeignKey(Article, related_name='chapters', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()
    order = models.IntegerField(default=0)  # 用于表示章节的顺序
    images = models.ManyToManyField(Image, blank=True)

    class Meta:
        ordering = ['order']

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

# '''没用
class Graphics(models.Model):
    article_choices = (
        ('E', 'educational article'),
        ('F', 'Fiction'),
        ('G', 'Graphics'),
        ('O', 'Other'),
    )
    title = models.CharField(max_length=200)
    graphic_file = models.ImageField(upload_to='graphic_file/')
    type = models.CharField(max_length=1, choices=article_choices, default='O')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    pub_date = models.DateTimeField(default=datetime.datetime.now, null=True)
# '''