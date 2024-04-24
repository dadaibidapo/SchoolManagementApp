from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)
# admin.site.register(Admin)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
admin.site.register(STUDENTCSV)
# admin.site.register(LastGeneratedID)
