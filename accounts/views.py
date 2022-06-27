from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
import requests
from .forms import CustomUserChangeForm

# Create your views here.

@login_required(login_url='/user/login')
def user_update(request):
    if request.method=="GET":
        form = UserChangeForm(instance=request.user)
        context = {'form': form}
        return render(request, 'account/update.html', context)
    elif request.method=="POST":
        form = CustomUserChangeForm(request.POST, instance=request.usr)
        if form.is_valid():
            form.save()
            return redirect('/')

@login_required(login_url='/user/login')
def user_delete(request):
    if request.user.is_authenticated:
        request.user.delete()
        auth_logout(request)
    return redirect('/')


def password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        # 키워드인자명을 함께 써줘도 가능
        # form = PasswordChangeForm(user=request.user, data=request.POST)

        if form.is_valid():
            form.save()
            return redirect('/accounts/profile')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form': form}
    return render(request, 'account/password.html', context)

def profile(request) :

    return render(request, 'account/profile.html')


# 카카오 로그인
def kakaoLoginPage(request) :
    return render(request, 'user/login.html')


def getcode(request) :
    # 인가코드 받고
    code = request.GET.get('code')
    # 인가코드로 토큰 요청
    data = {'grant_type': 'authorization_code',
            'client_id': 'e919fc73bf3cc45ad11629761ff28028', # 카카오 REST API키 등록
            'redirect_uri' : 'http://127.0.0.1:8000/oauth/redirect',
            'code':code}
    headers = { 'Content-type' : 'application/x-www-form-urlencoded;charset=utf-8' }
    # 토큰을 받고
    res = requests.post('https://kauth.kakao.com/oauth/token', data=data, headers=headers)
    token_json = res.json()
    print(token_json)

    # 토큰으로 사용자 정보 요청
    access_token = token_json['access_token']

    headers = { 'Authorization': 'Bearer ' + access_token,
                'Content-type' : 'application/x-www-form-urlencoded;charset=utf-8'}

    res = requests.get('https://kapi.kakao.com/v2/user/me', headers=headers)
    profile_json = res.json()
    print(profile_json)

    kakaoid = profile_json['id']

    user = User.objects.filter(email=kakaoid).first() # 게시판 번호 가져옴
    if user is not None : #사용자 정보가 우리 DB에 있으면 로그인

        login(request, user, backend='django.contrib.auth.backends.ModelBackend') # login 함수로 전달
    else: # 없으면 가입

        user = User()  # 유저 저장하기
        user.email = kakaoid
        user.username = profile_json['properties']['nickname']
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend') # login 함수로 전달
    return redirect('/board/list')
