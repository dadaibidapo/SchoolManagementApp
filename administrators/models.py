from django.db import models
# from django.contrib.auth import get_user_model
from multipleUserApp.models import Teacher  # Update the import path according to your project structure


# User = get_user_model()

class Class(models.Model):
    class_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    class_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, related_name='classes_taught', blank=True, null=True)

    def __str__(self):
        return self.class_name

class Department(models.Model):
    department_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.department_name

class Subject(models.Model):
    subject_name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    # Department =  models.ForeignKey(Department, on_delete=models.CASCADE, null=False)
    departments = models.ManyToManyField(Department, blank=True)

    def __str__(self):
        return self.subject_name


class TeacherSubject(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['teacher', 'subject', 'class_assigned']