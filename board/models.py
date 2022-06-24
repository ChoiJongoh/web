from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    contents = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.ManyToManyField(User, related_name='likes', blank=True)
    # blank기능 like를 입력하지 않아도 된다.

    #image = models.ImageField(upload_to='images/', blank=True, null=True)
    # 이미지 필트 이미지 업로드 추가
    # null은 DB에서 blank은 입력 양식에서 관련됨

class PostImage(models.Model):
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # 관계 맺기 = ForeignKey 속성으로