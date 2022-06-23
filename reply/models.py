from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from board.models import Post


class Reply(models.Model):
    contents = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE) #board의 model 불러와서 담기
    writer = models.ForeignKey(User, on_delete=models.CASCADE) #user의 model 불러와서 담기
    # Django에서 만든 User, 회원가입된 user만 쓸 수 있다.