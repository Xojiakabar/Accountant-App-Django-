from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.admin import settings


# Create your models here.


class Client(models.Model):
    JISMONIY_SHAXS = 'J'
    YURIDIK_SHAXS = 'Y'

    PERSON_TYPE = [
        (JISMONIY_SHAXS, 'Jismoniy Shaxs'),
        (YURIDIK_SHAXS, 'Yuridik Shaxs  '),
    ]
    person_type = models.CharField(max_length=1, choices=PERSON_TYPE, default=JISMONIY_SHAXS)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Accountant(models.Model):
    certificate = models.FileField(upload_to='accountant/files', null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.user.username


class Job(models.Model):
    NOT_STARTED = 'NS'
    ON_PROCESS = 'OP'
    FINISHED = 'FN'

    PROCESS_STATUS = [
        (NOT_STARTED, 'NOT STARTED'),
        (ON_PROCESS, 'ON PROCESS'),
        (FINISHED, 'FINISHED'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='client/jobs')
    deadline = models.DateField()
    accountant = models.ForeignKey(Accountant, on_delete=models.SET_NULL, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, )
    accepted_by_account = models.BooleanField(default=False)
    accepted_by_client = models.BooleanField(default=False)
    status = models.CharField(max_length=2, choices=PROCESS_STATUS, default=NOT_STARTED)
    finish = models.BooleanField(default=False)
    decline = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Comment(models.Model):

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='comments')
    description = models.TextField(validators=[MinLengthValidator(20, message="Comment kamida 20 ta belgidan iborat bo'lishi kerak.")])
