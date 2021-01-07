from .models import Student
from .utils import get_student_status



def task():
    students = Student.objects.all()
    for student in students:
        status = get_student_status(student.id_card)
        student.status = status
        student.save()











