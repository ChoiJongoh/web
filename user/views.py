from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.contrib import auth

def logout(request):
    auth_logout(request)
    return redirect('/board/list')

def login(request):
    if request.method=="GET": # 로그인 페이지 요청
        loginForm = AuthenticationForm()
        context = {'loginForm':loginForm}
        return render(request, 'user/login.html', context)
    elif request.method=="POST": # 로그인 된 경우
        loginForm = AuthenticationForm(request, request.POST)
        if loginForm.is_valid():
            auth_login(request, loginForm.get_user())
            # request에는 사용자의 정보가 들어있다.
            # request 안에 POST가 들어있다.
            # 로그인 성공, 실패 비교 코드가 포함되어있다.
        return redirect('/board/list')
# Create your views here.
def signup(request):
    if request.method=="GET":
        signupForm = UserCreationForm()
        context = {'signupForm':signupForm}
        return render(request, 'user/signup.html', context)

    elif request.method=="POST":
        signupForm = UserCreationForm(request.POST)
        if signupForm.is_valid():
            user = signupForm.save(commit=False)

            user.is_active = False # 유저 비활성화

            user.save()

            current_site = get_current_site(request)

            message = render_to_string('account/activation_email.html',                         {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
                'token': account_activation_token.make_token(user),
            })

            mail_subject = "회원가입 계정 활성화 인증 메일"
            user_email = request.POST["email"]
            email = EmailMessage(mail_subject, message, to=[user_email])
            email.send()

        return redirect('/board/list')


# 계정 활성화 함수(토큰을 통해 인증)
def activate(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExsit):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        auth.login(request, user)
        return redirect("/board/list")

    return HttpResponse('비정상적인 접근입니다.')