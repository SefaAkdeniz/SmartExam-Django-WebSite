from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages

# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            messages.add_message(request,messages.SUCCESS,'Oturum açıldı.')
            return redirect('index')
        else:
            messages.add_message(request,messages.ERROR,'Hesap bulunamadı.')
            return redirect('login')
    else:
        return render(request,'login.html')

def register(request): 
    if request.method == 'POST':       
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        repassword = request.POST['repassword']
        if password==repassword:
            if User.objects.filter(username=username).exists():
                messages.add_message(request,messages.WARNING,'Bu kullanıcı adı daha önce kullanılmıştır.')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,first_name=first_name,last_name=last_name,password=password)
                user.save()
                messages.add_message(request,messages.SUCCESS,'Hesap başarıyla oluşturuldu.')
                return redirect('login')
        else:
            messages.add_message(request,messages.ERROR,'Parlolar eşleşmiyor.')
            return redirect('register')
    else:
        return render(request,'register.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.add_message(request,messages.SUCCESS,'Oturumunuz kapatıldı.')
        return redirect('index')
