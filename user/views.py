import hashlib
import random
import string
import traceback
import uuid

from django.core.mail import send_mail

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.contrib.auth import settings

from captcha.image import ImageCaptcha
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from user.models import TUser

# 登录
def login(request):
    username = request.COOKIES.get('username')
    if username:
        username = username.encode('latin-1').decode('utf-8')
        password = request.COOKIES.get('password')
        user = TUser.objects.filter(username=username, password=password)
        if user:
            request.session['is_logic'] = True
            return redirect('course:index')
    return render(request,'user/login.html')

# 登录逻辑
def login_logic(request):
    username = request.POST.get('username')
    password = request.POST.get('pwd')
    # salt = str(uuid.uuid4())
    # print(password+salt)
    try:
        result = TUser.objects.get(username=username)
        if result.is_active:
            b = result.salt
            sha = hashlib.md5()
            sha.update((password+b).encode())
            pwd = sha.hexdigest()
            print(pwd)
            rem = request.POST.get('remember')
            # res = TUser.objects.filter(username=username,password=pwd)
            if pwd == result.password:
                request.session['is_login'] = True
                resp = HttpResponse('yes')
                if rem:
                    username = username.encode('utf-8').decode('latin-1')
                    resp.set_cookie('username',username,max_age=3600*24*7)
                    resp.set_cookie('password',password,max_age=3600*24*7)
                else:
                    username = username.encode('utf-8').decode('latin-1')
                    resp.set_cookie('username', username)
                    resp.set_cookie('password', password)
                request.session['is_logic'] = True
                # return render(request,'course/index.html')
                return resp

            ser = Serializer(settings.SECRET_KEY, expires_in=120)
            # return render(request,'user/login.html')
            return HttpResponse('no')
        return HttpResponse('nooo')
    except:
        traceback.print_exc()
        return HttpResponse('no')



# 注册
def register(request):
    return render(request,'user/register.html')

# 注册逻辑
def register_logic(request):
    captcha = request.POST.get('captcha')
    print(captcha)
    if captcha.lower() == request.session.get('code').lower():
        try:
            username = request.POST.get('user_name')
            password = request.POST.get('cpwd')
            email = request.POST.get('email')
            res = TUser.objects.filter(username=username)
            if res:
                return HttpResponse("no")
            else:
                with transaction.atomic():
                    salt = str(uuid.uuid4())
                    print(password+salt)
                    sha = hashlib.md5()
                    sha.update((password+salt).encode())
                    pwd = sha.hexdigest()
                    print(pwd)
                    usersssss = TUser.objects.create(username=username,password=pwd,email=email,is_active=0,salt=salt)
                    if usersssss:
                        ser = Serializer(settings.SECRET_KEY, expires_in=120)
                        result = ser.dumps({'id': usersssss.id})
                        send_mail('邮件主题',f'用户{username} 请求激活帐号，链接为：http://127.0.0.1:8000/user/active/?token=' + result.decode('utf-8'),
                                  '212763079@qq.com', ['1848667242@qq.com'])
                        return HttpResponse("yes")
                    return HttpResponse("nooo")
        except:
            traceback.print_exc()
            return HttpResponse("no")
    else:
        return HttpResponse("noo")

def register_emali(request):
    username = request.POST.get('username')
    print(username)
    id=TUser.objects.get(username=username).id
    ser = Serializer(settings.SECRET_KEY, expires_in=120)
    result = ser.dumps({'id': id})
    send_mail('邮件主题', f'用户{username} 请求激活帐号，链接为：http://127.0.0.1:8000/user/active/?token=' + result.decode('utf-8'),
              '212763079@qq.com', ['1848667242@qq.com'])
    return HttpResponse('OK')


# 邮箱
def active(request):
    try:
        token = request.GET.get('token')
        ser = Serializer(settings.SECRET_KEY, expires_in=120)
        id = ser.loads(token).get('id')
        user = TUser.objects.get(pk=id)
        user.is_active = True
        user.save()
        return HttpResponse('成功')
    except:
        traceback.print_exc()
        return HttpResponse("失败")


# 判断用户名
def userss(request):
    username = request.POST.get('username')
    user = TUser.objects.filter(username=username)
    if user:
        print(1)
        return HttpResponse('用户名已存在')
    return HttpResponse('用户名合法')


# 验证码
def get_captcha(request):
    image = ImageCaptcha()
    code = random.sample(string.ascii_letters+string.digits,4)
    code = ''.join(code)
    request.session['code'] = code
    data = image.generate(code)
    return HttpResponse(data,'image/png')

def logout(request):
    return render(request,'user/logout.html')
