from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.utils import timezone


# Create your models here.

class User(AbstractUser):

    timestamp = models.DateTimeField("timestamp", default=timezone.now)

    class Meta:
        managed = True
        verbose_name_plural = '用户管理'


class Student(models.Model):
    name = models.CharField(blank=True, null=True, max_length=255)
    status = models.CharField(blank=True, null=True, max_length=255)
    id_card = models.IntegerField(blank=True, null=True)
    update_time = models.DateTimeField("update_time", default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        managed = True
        verbose_name_plural = '学生管理'
