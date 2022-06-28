from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from board.models import Post
from reply.forms import ReplyForm
from reply.models import Reply

# 좋아요 함수
@login_required(login_url='/user/login') # 로그인 정보 있다면 추가
def like(request, bid):
    reply = Reply.objects.get(id=bid) # 게시글 번호를 담은 board 모델
    # post.like.add(request.user) # 로그인 한 사용자 정보
    user = request.user
    if reply.like.filter(id=user.id).exists() : # get은 하나 filter는 여러 개 뽑아옴, 인덱스로 접근
        #filter의 id는 user 밑의 id를 자동으로 찾아준다.
        reply.like.remove(user)
        return JsonResponse({'message': 'deleted', 'like_cnt':reply.like.count()})
    else :
        reply.like.add(user)
        return JsonResponse({'message': 'added', 'like_cnt':reply.like.count()})

@login_required(login_url='/user/login')
def create(request, bid): #게시글 번호 받아오기
    if request.method == "POST": # POST 방식으로 받는다. HTML의 body로 전달
        replyForm = ReplyForm(request.POST)  # 사용자가 입력한 값 받아 DB 자동 전달
        # 댓글 객체 생성
        print(request.POST.get('contents'))

        if replyForm.is_valid():
            print('ok_valid')
            reply = replyForm.save(commit=False)  # bid는 변수에 바로 저장이 안 됨
            # 저장된 댓글 열기
            reply.writer = request.user  # 열린 데이터의 작성자에 유저 정보 담기

            post = Post()  # 객체를 만들어서 저장해주어야 함
            # 게시판 객체 생성
            post.id = bid  # 번호로 게시글 지정

            reply.post = post  # 댓글의 게시판 번호에 불러온 게시글 번호 담기
            reply.save()  # 댓글 저장

    return redirect("/board/read/" + str(bid))
    # 특정 게시판을 보여주는 views.py의 함수로 전달


# 댓글 수정 삭제 추가 계획

@login_required(login_url='/user/login')
def delete(request, bid):
    post = Post.objects.get(id=bid)
    reply = Reply.objects.get(id=bid)
    if request.user != reply.writer:
        return redirect('/board/read/'+str(bid))
    if request.method == "POST":
        reply.delete()
        return redirect('/board/read/' + str(bid))
    else:
        return redirect('/board/read'+str(bid))

@login_required(login_url='/user/login')
def update(request, bid):
    post = Post.objects.get(id=bid)
    reply = Reply.objects.get(id=bid)
    #print(reply)
    if request.user != reply.writer:
        return redirect('/board/read/'+str(bid))

    if request.method == "GET": # 댓글 수정 창으로
        replyForm = ReplyForm(instance=reply)
        return render(request, 'reply/create.html',)

    elif request.method == "POST":
        replyForm = ReplyForm(request.POST, instance=reply)
        if replyForm.is_valid():
            data_save = replyForm.save(commit=False)
            data_save.save()
        return redirect('/reply/read/' + str(data_save.id))