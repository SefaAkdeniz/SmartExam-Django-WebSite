from django.shortcuts import render,redirect
from exam.models import Student_Log,Question,Category
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from django.utils import formats
from django.views.decorators.csrf import csrf_exempt
from collections import Counter
from django.http import HttpResponse
from django.template import loader

# Create your views here.
falsePastQuestions=[]
truePastQuestions=[]
@login_required(login_url="login")
@csrf_exempt
def stat(request):
    if request.method == 'POST':   
        year,month,day=request.POST["date"].split("-")
        falsePastQuestions = Student_Log.objects.filter(user=request.user, answer=False,date__year=year,date__month=month,date__day=day)
        truePastQuestions = Student_Log.objects.filter(user=request.user, answer=True,date__year=year,date__month=month,date__day=day) 

        dateLog=[]
        PastQuestions = Student_Log.objects.filter(user=request.user,)
        for each in PastQuestions:
            dateLog.append(str(each.date)[0:10])
    
        output = []
        for x in dateLog:
            if x not in output:
                output.append(x)
        dateLog=output
        dateLog.remove(request.POST["date"])
        dateLog.insert(0,request.POST["date"])
    else:
        falsePastQuestions = Student_Log.objects.filter(user=request.user, answer=False)
        truePastQuestions = Student_Log.objects.filter(user=request.user, answer=True)

        dateLog=[]
        PastQuestions = Student_Log.objects.filter(user=request.user,)
        for each in PastQuestions:
            dateLog.append(str(each.date)[0:10])
    
        output = []
        for x in dateLog:
            if x not in output:
                output.append(x)
        dateLog=output

    falseCount=0
    trueCount=0

    dateArray = ""
    for date in dateLog:
        dateArray += "*-*" + date
       
    falseCategoryLog=[]
    for each in falsePastQuestions:
        falseCategoryLog.append(str(each.question.category))
        falseCount +=1

    falseCategoryLog=Counter(falseCategoryLog)
    falseCategoryLabel = ""
    categoryFalse=[]
    for key, value in falseCategoryLog.items():
        categoryFalse.append(value)
        falseCategoryLabel += "*-*" + key
       
    trueCategoryLog=[]
    for each in truePastQuestions:
        trueCategoryLog.append(str(each.question.category))
        trueCount += 1

    trueCategoryLog=Counter(trueCategoryLog)
    trueCategoryLabel = ""
    categoryTrue=[]
    for key, value in trueCategoryLog.items():
        categoryTrue.append(value)
        trueCategoryLabel += "*-*" + key

    result=str((trueCount/(falseCount+trueCount))*100)
    result=result.split(".")[0]
       
    return render(request,'stat.html',{"falseCategoryLabel":falseCategoryLabel,"categoryFalse":categoryFalse,"trueCategoryLabel":trueCategoryLabel,"categoryTrue":categoryTrue,"dateLog":dateArray,"result":result})

@login_required(login_url="login")
@csrf_exempt
def index(request):
    if request.method == 'POST':   
        print(request.POST["answers"][0:3:1])
        if request.POST["answers"][0:3:1]=="*-*":
            falseQuestion=request.POST["answers"][3::1]
            falseQuestion=list(falseQuestion.split(","))
            print(falseQuestion)
            trueQuestion=[]
        elif request.POST["answers"][-3:]=="*-*":
            falseQuestion=[]
            trueQuestion=request.POST["answers"][0:-3:1]
            print(trueQuestion)
            trueQuestion=list(trueQuestion.split(","))
        else:        
            trueQuestion,falseQuestion=request.POST["answers"].split("*-*")
            trueQuestion=list(trueQuestion.split(","))
            falseQuestion=list(falseQuestion.split(","))
    
        for each in trueQuestion:
            answered=Question.objects.filter(id=each).first()
            questionLog = Student_Log(user=request.user, question=answered, answer=True, date=timezone.now())
            questionLog.save()

        for each in falseQuestion:
            answered=Question.objects.filter(id=each).first()
            questionLog = Student_Log(user=request.user, question=answered, answer=False, date=timezone.now())
            questionLog.save()

        return redirect("index.html")
    else:
        if Student_Log.objects.filter(user=request.user).exists()==0:

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
        
        elif Student_Log.objects.filter(user=request.user,date__year=timezone.now().year,date__month=timezone.now().month,date__day=timezone.now().day).count()==0:

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
                if count==10:
                    break

            pastQuestions = Student_Log.objects.filter(user=request.user, answer=False)
            
            z=[]
            for each in pastQuestions:
                z.append(str(each.question.category))           
          
            z=Counter(z)  
            z=dict(z)
            inverse = [[value, key] for key, value in z.items()]
            
            for each in range(1,21-count):
                maxCategory=max(inverse)[1]
                idCategory=Category.objects.filter(category=maxCategory).first().id
                print(inverse)
                for each in inverse:                   
                    if each[1]==maxCategory:
                        each[0]=each[0]/2
                while(1):
                    queryQuestion=Question.objects.filter(category=idCategory).order_by('?').first()
                    if queryQuestion.id in idList:
                        continue
                    else:
                        question.append(queryQuestion)
                        idList.append(queryQuestion.id)
                        break
        else:
            messages.add_message(request,messages.SUCCESS,'Bugünki sınav hakkınız dolmuştur.')
            return redirect('index')

        questionIDList = ""
        imageList=""
        textList =""
        trueAnswerList=""
        falseAnswer1List=""
        falseAnswer2List=""
        falseAnswer3List="" 

        if str(question[0].image) == "":
            imageList = "NaN"
        else:
            imageList = str(question[0].image)

        textList = str(question[0].text)
        trueAnswerList = str(question[0].trueAnswer)
        falseAnswer1List = str(question[0].falseAnswer1)
        falseAnswer2List = str(question[0].falseAnswer2)
        falseAnswer3List = str(question[0].falseAnswer3)
        questionIDList = str(question[0].id)

        for each in range(1,20):
            if str(question[each].image) == "":
                imageList = imageList + "*-*" + "NaN"
            else:
                imageList = imageList + "*-*" + (str(question[each].image))

            textList = textList + "*-*" + (str(question[each].text))
            trueAnswerList = trueAnswerList + "*-*" + (str(question[each].trueAnswer))
            falseAnswer1List = falseAnswer1List + "*-*" + (str(question[each].falseAnswer1))
            falseAnswer2List = falseAnswer2List + "*-*" + (str(question[each].falseAnswer2))
            falseAnswer3List = falseAnswer3List + "*-*" + (str(question[each].falseAnswer3))
            questionIDList = questionIDList + "*-*" + (str(question[each].id))          
    
        return render(request,'exam.html',{"id":questionIDList,"image":imageList,"text":textList,"trueAnswer":trueAnswerList,"falseAnswer1":falseAnswer1List,"falseAnswer2":falseAnswer2List,"falseAnswer3":falseAnswer3List})
                 
        
            
            
