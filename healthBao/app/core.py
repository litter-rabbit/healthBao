from .models import Student
from .utils import get_student_status
import datetime
from django.utils import timezone

def task(request=None):
    if request:
        students = Student.objects.filter(user=request.user).all()
    else:
        students = Student.objects.all()
    for student in students:
        status = get_student_status(student.id_card)
        if status in ['红色','绿色','未在健康宝注册','黄色']:
            student.status = status
            students.update_time = timezone.now()
            print('imte',timezone.now())
            student.save()











