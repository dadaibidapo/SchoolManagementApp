from django.contrib.auth.forms import UserCreationForm
from django import forms
from multipleUserApp.models import Student, User, Teacher
# from django.db import transaction

class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = Student
        fields = ['first_name', 'last_name', 'password1', 'password2']  # Include necessary fields
   
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.username = self.cleaned_data.get('first_name')
        user.role='STUDENT'  # Set username from the form
        if commit:
            user.save()
        return user

class TeacherSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    class Meta(UserCreationForm.Meta):
        model = Teacher
        fields = ['first_name', 'last_name', 'password1', 'password2']  # Include necessary fields
   
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.username = self.cleaned_data.get('first_name') 
        user.role = 'TEACHER' # Set username from the form
        if commit:
            user.save()
        return user

# from django.contrib.auth.forms import UserCreationForm
# from django import forms
# from multipleUserApp.models import Student, Teacher

# class StudentSignUpForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = Student
#         fields = ['first_name', 'last_name', 'password1', 'password2']  # Include necessary fields

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.first_name = self.cleaned_data.get('first_name')
#         user.last_name = self.cleaned_data.get('last_name')
#         if commit:
#             user.save()
#         return user

# class TeacherSignUpForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = Teacher
#         fields = ['first_name', 'last_name', 'password1', 'password2']  # Include necessary fields

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.first_name = self.cleaned_data.get('first_name')
#         user.last_name = self.cleaned_data.get('last_name')
#         if commit:
#             user.save()
#         return user
