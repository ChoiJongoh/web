from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from board.forms import PostForm
from board.models import Post
from reply.forms import ReplyForm


@login_required(login_url='/user/login')
def create(request): # form 태그로 입력한 것을 우리에게 보내줌. 서버에 저장
    if request.method == "GET":
        postForm = PostForm()
        context = {'postForm': postForm}
        return render(request, "board/create.html", context)
    elif request.method == "POST":
        postForm = PostForm(request.POST)

        if postForm.is_valid():
            post = postForm.save(commit=False)
            post.writer = request.user
            post.save()
        return redirect('/board/read/'+str(post.id))


def list(request):
    posts = Post.objects.all().order_by('-id')
    context = {'posts': posts}
    return render(request, 'board/list.html', context)

def read(request, bid):
    post = Post.objects.prefetch_related('reply_set').get(id=bid)
    replyForm = ReplyForm()
    context = {'post': post, 'replyForm': replyForm }
    return render(request, 'board/read.html', context)

@login_required(login_url='/user/login')
def delete(request, bid):
    post = Post.objects.get(id=bid)
    if request.user != post.writer:
        return redirect('/board/read/'+str(bid))
    post.delete()
    return redirect('/board/list')

@login_required(login_url='/user/login')
def update(request, bid):
    post = Post.objects.get(id=bid)
    if request.user != post.writer:
        return redirect('/board/read/'+str(bid))

    if request.method=="GET":
        context = {'post': post}
        return render(request, "board/update.html", context)

    elif request.method=="POST":
        postForm = PostForm(request.POST, instance=post)
        if postForm.is_valid():
            post = postForm.save(commit=False)
            post.save()
        return redirect('/board/read/'+str(bid))

@login_required(login_url='/user/login') # 로그인 정보 있다면 추가
def like(request, bid):
    post = Post.objects.get(id=bid) # 게시글 번호를 담은 board 모델
    # post.like.add(request.user) # 로그인 한 사용자 정보
    user = request.user
    if post.like.filter(id=user.id).exists() : # get은 하나 filter는 여러 개 뽑아옴, 인덱스로 접근
        #filter의 id는 user 밑의 id를 자동으로 찾아준다.
        post.like.remove(user)
        return JsonResponse({'message': 'deleted', 'like_cnt':post.like.count()})
    else :
        post.like.add(user)
        return JsonResponse({'message': 'added', 'like_cnt':post.like.count()})