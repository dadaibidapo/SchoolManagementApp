from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# from django.utils.crypto import get_random_string
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT =  'STUDENT', "Student"
        TEACHER = 'TEACHER', 'Teacher'

    base_role =Role.TEACHER

    role = models.CharField(max_length = 50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk: # new
            if self.role == self.Role.STUDENT:
                self.username = self.generate_student_id()
            elif self.role == self.Role.TEACHER:
                self.username = self.generate_teacher_id()
            # self.role = self.base_role
            super().save(*args,**kwargs)
    
    def generate_student_id(self):
        last_student = User.objects.filter(role=self.Role.STUDENT).order_by('-id').first()
        if last_student:
            last_id = int(last_student.username.split('-')[1])
            new_id = last_id + 1
        else:
            new_id = 1
        return f'STU-{new_id:04}'

    def generate_teacher_id(self):
        last_teacher = User.objects.filter(role=self.Role.TEACHER).order_by('-id').first()
        if last_teacher:
            last_id = int(last_teacher.username.split('-')[1])
            new_id = last_id + 1
        else:
            new_id = 1
        return f'TEA-{new_id:04}'

#############################################################################
        
class StudentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs).filter(role=User.Role.STUDENT)
        return results
       

class Student(User):
    base_role = User.Role.STUDENT

    student = StudentManager()

    class Meta:
        proxy=True 

    def welcome(self):
        return "Only for students"
    
##########################################################################
# generating student_id
class StudentProfile(models.Model):
    SEX_CHOICES =  [('M', 'Male'),('F', 'Female')]

    user = models.OneToOneField(User,  on_delete=models.CASCADE)
    first_name = models.CharField(max_length=32, blank=True)
    last_name = models.CharField(max_length=32, blank=True)
    student_id = models.CharField(max_length=20, primary_key=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES) 
    address = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

@receiver(post_save, sender=Student)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.role == User.Role.STUDENT:
        StudentProfile.objects.create(user=instance, student_id=instance.username, first_name=instance.first_name, last_name=instance.last_name)
############################################################################    
class TeacherManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs).filter(role=User.Role.TEACHER)
        return results
      
        
class Teacher(User):
    base_role = User.Role.TEACHER

    teacher = TeacherManager()

    class Meta:
        proxy=True 

    def welcome(self):
        return "Only for teacher"
    
############################################################################
class TeacherProfile(models.Model):
    SEX_CHOICES =  [('M', 'Male'),('F', 'Female')]

    user = models.OneToOneField(User,  on_delete=models.CASCADE)
    teacher_id = models.CharField(max_length=20, primary_key=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES) 
    address = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

@receiver(post_save, sender=Teacher)
def create_teacher_profile(sender, instance, created, **kwargs):
    if created and instance.role == User.Role.TEACHER:
        TeacherProfile.objects.create(user=instance, teacher_id=instance.username)
    
##########################################################################
class STUDENTCSV(models.Model):
    file_name = models.CharField(max_length=120, null=True)
    CSV_file = models.FileField(upload_to='student_csvs', null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.file_name)
  