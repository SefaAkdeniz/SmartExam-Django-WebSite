from django.shortcuts import render,redirect
from models import Student_Log
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages


# Create your views here.

@login_required(login_url="user:login")
def index(request):
    if request.method == 'POST':
        pass
    else:
        count = Student_Log.objects.filter(user=request.user).count()
        if count == 0:
            return render(request,'exam.html')