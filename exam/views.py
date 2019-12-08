from django.shortcuts import render,redirect
from exam.models import Student_Log,Question
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from django.utils import formats


# Create your views here.

@login_required(login_url="login")
def index(request):
    if request.method == 'POST':
        pass
    else:
        if Student_Log.objects.filter(user=request.user).exists()==0:
            messages.add_message(request,messages.SUCCESS,'ilk sinav')
            sorular=
            return render(request,'exam.html')
        if Student_Log.objects.filter(user=request.user,date__year=timezone.now().year,date__month=timezone.now().month,date__day=timezone.now().day).exists()==0:
            messages.add_message(request,messages.SUCCESS,'normal sinav')
            return render(request,'exam.html')           
        else:
            messages.add_message(request,messages.SUCCESS,'bugun sinav oldun')
            return redirect('index')
            
            
