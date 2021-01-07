from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.contrib import messages
from .models import Student
from django.http import JsonResponse
from django.core.paginator import Paginator
from .utils import  get_student_status
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from threading import Thread
from django.utils import timezone
import re
from .core import task
# Create your views here.
import xlrd


def index(request):


    return render(request, 'app/index.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email'].strip()
        password = request.POST['password'].strip()
        user = authenticate(request, username=email, password=password)
        if user:
            auth.login(request, user)
            print('登录成功')
            return HttpResponseRedirect(reverse('app:index'))
        else:
            # 返回错误信息
            messages.add_message(request, messages.ERROR, '用户名或密码错误')
            return render(request, 'app/login.html')
    return render(request, 'app/login.html')


def include_file(request):
    print('提交')
    if request.method == 'POST':
        files = request.FILES.get('file')
        print(files)
        print('提交')
        f = open(files.name, 'wb')
        for chunk in files.chunks():
            f.write(chunk)
        f.close()
        xlsx = xlrd.open_workbook(files.name)
        sheet1 = xlsx.sheets()[0]
        for i in range(1, sheet1.nrows):
            print(sheet1.row_values(i))
            status=get_student_status(int(sheet1.row_values(i)[1]))
            if status in ['红色', '绿色', '未在健康宝注册', '黄色']:
                student = Student.objects.filter(id_card=int(sheet1.row_values(i)[1])).all()
                if student:
                    student.status=status
                    student.update_time = timezone.now()
                    student.save()
                    print('已存在')
                else:
                    student = Student.objects.create(name=sheet1.row_values(i)[0], id_card=int(sheet1.row_values(i)[1]), user=request.user,status=status)
                    student.save()
            print('状态',status)
        return HttpResponseRedirect(reverse('app:include'))
    return JsonResponse({'status': 1})


def logout(request):
    auth.logout(request)
    return render(request, 'app/login.html')


def include(request):
    students = Student.objects.filter(user=request.user).all()
    paginator = Paginator(students, 50)
    pag_objs = paginator.get_page(request.GET.get('page'))
    context = {}
    context['page_obj'] = pag_objs
    print('page_obj',students)
    return render(request, 'app/include.html', context=context)


def detail(request):

    green_student_count = Student.objects.filter(status='绿色',user=request.user).count()
    red_student_count = Student.objects.filter(status='红色',user=request.user).count()
    all_count = Student.objects.filter(user=request.user).count()
    other_count = all_count-green_student_count-red_student_count
    context={}
    context['g'] = green_student_count
    context['r'] = red_student_count
    context['other'] = other_count

    return render(request, 'app/detail.html',context=context)

@csrf_exempt
def search(request):

    search_content = request.POST.get('search_data')

    re_res = re.match('\d+',search_content)
    if re_res:
        search_content=re_res.group()

    if re_res:
        students = Student.objects.filter(id_card=search_content,user=request.user).all()
    else:
        students = Student.objects.filter(name=search_content,user=request.user).all()
    students = serializers.serialize("json",students)
    print(students)
    return JsonResponse({'students':students})

@csrf_exempt
def update_status(request):

    # 更新状态函数
    t = Thread(target=task,args=(request,))
    t.start()
    students = Student.objects.filter(user=request.user).all()
    paginator = Paginator(students, 50)
    pag_objs = paginator.get_page(request.GET.get('page'))
    context = {}
    context['page_obj'] = pag_objs
    print('page_obj',students)
    return render(request, 'app/include.html', context=context)
    pass

