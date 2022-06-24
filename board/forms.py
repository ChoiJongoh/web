from django import forms
from board.models import Post
from board.models import PostImage
#model에서 가져오기

class PostForm(forms.ModelForm): # 게시글을 만드는 폼
    class Meta:
        model = Post
        fields = ('title', 'contents', ) # 모델의 속성 이름, 입력 받는 것
        exclude = ('writer', ) # 입력 받지 않는 것

class PostImageForm():
    class Meta:
        model = PostImage
        field = ('image', 'post',)