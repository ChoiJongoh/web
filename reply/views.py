from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from board.models import Post
from reply.forms import ReplyForm


@login_required(login_url='/user/login')
def create(request, bid):
    if request.method == "POST":
        replyForm = ReplyForm(request.POST)  # 댓글 객체 생성
        print(request.POST.get('contents'))

        if replyForm.is_valid():
            print('aa')
            reply = replyForm.save(commit=False)  # 저장된 댓글 열기
            reply.writer = request.user  # 열린 데이터의 작성자에 유저 정보 담기

            post = Post()  # 게시판 객체 생성
            post.id = bid  # 번호로 게시글 지정

            reply.post = post  # 댓글의 게시판 번호에 불러온 게시글 번호 담기
            reply.save()  # 댓글 저장

    return redirect("/board/read/" + str(bid))
    # 특정 게시판을 보여주는 views.py의 함수로 전달
