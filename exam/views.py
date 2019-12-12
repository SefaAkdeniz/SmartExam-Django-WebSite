from django.shortcuts import render,redirect
from exam.models import Student_Log,Question
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from django.utils import formats
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@login_required(login_url="login")
@csrf_exempt
def index(request):
    if request.method == 'POST':
        print(dict(request.POST)["cevaplar[]"])
        return redirect("index.html")
    else:
        if Student_Log.objects.filter(user=request.user).exists()==0:
            messages.add_message(request,messages.SUCCESS,'ilk sinav')
            queryCategory = Question.objects.values('category').distinct()
            categorys=[]
            for each in queryCategory:
                categorys.append(each["category"])
            question=[]
            idList=[]
            count=0
            for each in categorys:
                question.append(Question.objects.filter(category=each).first())
                idList.append(Question.objects.filter(category=each).first().id)
                count=count+1
                if count==20:
                    break
            for each in range(1,21-count):
                while(1):
                    queryQuestion=Question.objects.order_by('?').first()
                    if queryQuestion.id in idList:
                        continue
                    else:
                        question.append(queryQuestion)
                        idList.append(queryQuestion.id)
                        break
            imageList=""
            textList =""
            trueAnswerList=""
            falseAnswer1List=""
            falseAnswer2List=""
            falseAnswer3List="" 
            for each in range(0,20):
                imageList = imageList + "," + (str(question[each].image))
                textList = textList + "," + (str(question[each].text))
                trueAnswerList = trueAnswerList + "," + (str(question[each].trueAnswer))
                falseAnswer1List = falseAnswer1List + "," + (str(question[each].falseAnswer1))
                falseAnswer2List = falseAnswer2List + "," + (str(question[each].falseAnswer2))
                falseAnswer3List = falseAnswer3List + "," + (str(question[each].falseAnswer3))
            
            return render(request,'exam.html',{"id":idList,"image":imageList,"text":textList,"trueAnswer":trueAnswerList,"falseAnswer1":falseAnswer1List,"falseAnswer2":falseAnswer2List,"falseAnswer3":falseAnswer3List})
        if Student_Log.objects.filter(user=request.user,date__year=timezone.now().year,date__month=timezone.now().month,date__day=timezone.now().day).exists()==0:
            messages.add_message(request,messages.SUCCESS,'normal sinav')
            return render(request,'exam.html')           
        else:
            messages.add_message(request,messages.SUCCESS,'bugun sinav oldun')
            return redirect('index')
            
            
