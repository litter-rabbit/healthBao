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
            student = Student.objects.create(name=sheet1.row_values(i)[0], id_card=int(sheet1.row_values(i)[1]), user=request.user,status=status)
            student.save()
        return HttpResponseRedirect(reverse('app:include'))
    return JsonResponse({'status': 1})


def logout(request):
    auth.logout(request)
    return render(request, 'app/login.html')


def include(request):
    students = Student.objects.filter(user=request.user).all()
    paginator = Paginator(students, 15)
    pag_objs = paginator.get_page(request.GET.get('page'))
    context = {}
    context['page_obj'] = pag_objs
    print('page_obj',students)
    return render(request, 'app/include.html', context=context)


def detail(request):
    return render(request, 'app/detail.html')
