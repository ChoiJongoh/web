from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from board.forms import PostForm
from board.models import Post, PostImage
from reply.forms import ReplyForm

from django.core.paginator import Paginator

@login_required(login_url='/user/login')
def create(request): # form 태그로 입력한 것을 우리에게 보내줌. 서버에 저장
    if request.method == "GET": #사용자 입력으로 올 때
        postForm = PostForm()
        context = {'postForm': postForm}
        return render(request, "board/create.html", context)
    elif request.method == "POST": # 로그인 상태, 서버에서 올 때
        postForm = PostForm(request.POST)

        if postForm.is_valid():
            post = postForm.save(commit=False)
            post.writer = request.user
            post.save()
            for image in request.FILES.getlist('image', None): # 그냥은 1:1일 때, for문은 1:다일 때
                postImage = PostImage()
                postImage.image = image
                postImage.post = post
                postImage.save()

        return redirect('/board/read/'+str(post.id))


def list(request): # 저장한 내용을 보여주는 것
    # 여러 개를 가져올 것인가 하나를 가져올 것인가
    posts = Post.objects.all().order_by('-id')
    context = {'posts': posts}
    return render(request, 'board/list.html', context)

def read(request, bid):
    post = Post.objects.prefetch_related('reply_set', 'postimage_set').get(id=bid)
    print(post)
    replyForm = ReplyForm() # 댓글 폼 생성

    postImage = PostImage()

    context = {'post': post, 'replyForm': replyForm, 'image_set': postImage } # 게시판 댓글 같이 전송
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
        postForm = PostForm(request.POST, instance=post) # 객체 생성
        # instance = instance화 : 클래스라는 빈 틀에 객체로 채운다.(변수 초기화 같은 것)
        if postForm.is_valid():
            post = postForm.save(commit=False)
            post.save()
        return redirect('/board/read/'+str(bid))


# 좋아요 함수
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


def search(request):
    posts = Post.objects.all().order_by('-id')
    q = request.POST.get('q', "")

    if q:
        post = posts.filter(title__icontains=q)
        return render(request, 'board/search.html', {'post': post, 'q': q})

    else:
        return render(request, 'board/search.html')

def index(request):
    page = request.GET.get('page', 1)  # 페이지 / GET방식으로 page를 파라미터로 가져올 때 사용, 파라미터 없이 들어올 때 dafault값을 1로 줌.

    # 조회
    post_list = Post.objects.order_by('-id')  # -로 역순

    # 페이징
    paginator = Paginator(post_list, 9)  # 한 페이지당 개수
    page_obj = paginator.get_page(page)

    context = {'post_list': page_obj}
    # return HttpResponse('Hi pybo') # Hi pybo를 response해라
    return render(request, 'board/list.html', context)