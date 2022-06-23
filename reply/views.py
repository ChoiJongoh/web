from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from board.models import Post
from reply.forms import ReplyForm


@login_required(login_url='/user/login')
def create(request, bid): #게시글 번호 받아오기
    if request.method == "POST": # POST 방식으로 받는다. HTML의 body로 전달
        replyForm = ReplyForm(request.POST)  # 사용자가 입력한 값 받아 DB 자동 전달
        # 댓글 객체 생성
        print(request.POST.get('contents'))

        if replyForm.is_valid():
            print('aa')
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

def read(request, bid):
    #db_get = DB_model.objects.get(Q(id=bid)) # bid변수에 담긴 id를 Q에

    db_get = DB_model.objects.prefetch_related('reply_set').get(id=bid)

    db_form = DB_form()
    # form 객체 생성, form 불러오기
    context = {'db_get' : db_get, 'db_form' : db_form }

    return render(request, 'reply/read.html', context)

@login_required(login_url='/user/login')
def delete(request, bid):
    db_get = DB_model.objects.get(id=bid)
    db_get.delete()

    return redirect('/reply/list_print')

@login_required(login_url='/user/login')
def update(request, bid):
    db_get = DB_model.objects.get(id=bid)
    if request.method == "GET":
        db_form = DB_form(instance=db_get) # 객체 생성
        # instance = instance화 : 클래스라는 빈 틀에 객체로 채운다.(변수 초기화 같은 것)
        return render(request, 'reply/create.html')
    elif request.method == "POST":
        db_form = DB_form(request.POST, instance=db_get)
        if db_form.is_valid():
            data_save = db_form.save(commit=False)
            data_save()
        return redirect('/reply/read/' + str(data_save.id))