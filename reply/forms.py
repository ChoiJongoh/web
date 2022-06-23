from django import forms

from reply.models import Reply


class ReplyForm(forms.ModelForm):
    class Meta :
        model = Reply  # models클래스 불러오기
        field = ('contents', )  # 받아온 models에서 양식으로 보여줄 것
        exclude = ('writer', 'post',)  # 사용자에게 보여주지 않을 것