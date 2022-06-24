from django.contrib.sites import requests
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def kakaoLoginPage(request) :
    return render(request, 'login.html')


def getcode(request) :
    code = request.GET.get('code')
    data = {'grant_type': 'authorization_code',
            'client_id': 'e919fc73bf3cc45ad11629761ff28028', # 카카오 REST API키 등록
            'redirect_uri' : 'http://127.0.0.1:8000/oauth/redirect',
            'code':code}
    headers = { 'Content-type' : 'application/x-www-form-urlencoded;charset=utf-8' }
    res = requests.post('https://kauth.kakao.com/oauth/token', data=data, headers=headers)
    token_json = res.json()
    print(token_json)


    access_token = token_json['access_token']

    headers = { 'Authorization': 'Bearer ' + access_token,
                'Content-type' : 'application/x-www-form-urlencoded;charset=utf-8'}
    res = requests.get('https://kapi.kakao.com/v2/user/me', headers=headers)
    profile_json = res.json()
    print(profile_json)

    kakaoid = profile_json['id']
    from django.contrib.auth.models import User
    user = User.objects.filter(email=kakaoid).first() # 게시판 번호 가져옴
    if user is not None :
        from django.contrib.auth import login
        login(request, user, backend='django.contrib.auth.backends.ModelBackend') # login 함수로 전달
    else:
        user = User()  # 유저 저장하기
        user.email = kakaoid
        user.username = profile_json['properties']['nickname']
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend') # login 함수로 전달

    return HttpResponse(code)

def profile(request) :
    HttpResponse('profile.html')