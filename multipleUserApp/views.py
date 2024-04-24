from typing import Any
from django.contrib import messages
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password

from multipleUserApp.models import User,Student, Teacher, STUDENTCSV, StudentProfile,TeacherProfile

from django.contrib.auth.views import LoginView,LogoutView
from django.views.generic import CreateView, View, ListView,TemplateView
from django.urls import reverse_lazy

from django.contrib.auth.mixins  import PermissionRequiredMixin
from django.http import HttpResponseForbidden, JsonResponse, HttpResponseBadRequest

from .form import StudentSignUpForm, TeacherSignUpForm 
import csv
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.contrib.auth.hashers import make_password
# from django.contrib.auth.hashers import make_password

from django.core.paginator import Paginator

def logout_view(request):
    logout(request)
    return redirect('multipleUserApp:index')


class CustomLoginView(LoginView):
    template_name = 'multipleUserApp/login.html'
    success_url = reverse_lazy('multipleUserApp:index')

    def get_success_url(self):
        user = self.request.user
        if user.role == 'STUDENT':
            return reverse_lazy('Student:student_dashboard')
        
        else:
            return reverse_lazy('multipleUserApp:admin_home')

def index(request):
    users = User.objects.all()
    context = {users:users}
    return render(request, 'multipleUserApp/index.html', context)



class StudentList(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'multipleUserApp/list.html'
    context_object_name= 'page_obj1'
    paginate_by = 10
    permission_required = 'multipleUserApp.view_student'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        queryset1 = Student.objects.filter(role='STUDENT')
        # print(queryset1)

        role_search = self.request.GET.get('role-search') or ''
        search_area = self.request.GET.get('search-area') or ''

        if search_area:
            queryset1 = queryset1.filter(first_name__icontains=search_area) or queryset1.filter(last_name__icontains=search_area)
        if  role_search:
            queryset1 = queryset1.filter(role=role_search)
        if queryset1.exists():
            paginator1 = Paginator(queryset1, self.paginate_by)
            page_number1 = self.request.GET.get('page1')
            page_obj1 = paginator1.get_page(page_number1)
        else:
            page_obj1 = None    
            
        context['page_obj1'] = page_obj1
        context['role'] = "Student List"

        return context
    
    def dispatch(self, request, *args, **kwargs):
   
        if not request.user.has_perm(self.permission_required):
            return HttpResponseForbidden("You do not have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)


class TeacherList(LoginRequiredMixin, ListView):
    model = Teacher
    template_name = 'multipleUserApp/list.html'
    context_object_name= 'page_obj1'
    paginate_by = 10
    permission_required = 'multipleUserApp.view_teacher'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        queryset1 = Teacher.objects.filter(role='TEACHER')
        # print(queryset1)

        role_search = self.request.GET.get('role-search') or ''
        search_area = self.request.GET.get('search-area') or ''

        if search_area:
            queryset1 = queryset1.filter(first_name__icontains=search_area) | queryset1.filter(last_name__icontains=search_area)
        if  role_search:
            queryset1 = queryset1.filter(role=role_search)
        if queryset1.exists():
            paginator1 = Paginator(queryset1, self.paginate_by)
            page_number1 = self.request.GET.get('page1')
            page_obj1 = paginator1.get_page(page_number1)
        else:
            page_obj1 = None    
            
        context['page_obj1'] = page_obj1
        context['role'] = "Teacher List"
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm(self.permission_required):
            return HttpResponseForbidden("You do not have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)
#   ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class  StudentCreateView(LoginRequiredMixin, CreateView):
    model=Student
    form_class = StudentSignUpForm
    template_name='multipleUserApp/signup_form.html'
    # template_name='multipleUserApp/admin_home.html'
    success_url = reverse_lazy('multipleUserApp:admin_home')
    permission_required  = 'multipleUserApp.add_student'
    # context_object_name = 'info'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)   
        context['information']="Add a new student"
        return context
    
    # def handle_no_permission(self):
        # Customize the response when the user doesn't have the required permission
        # return HttpResponseForbidden("You do not have permission to access this page.")

    def dispatch(self, request, *args, **kwargs):
        # if not request.user.groups.filter(name = 'AdmInSuper').exists() | request.user.is_superuser:
        #     return HttpResponseForbidden("You do not have permission to access this page.")
        if not request.user.has_perm(self.permission_required):
            return HttpResponseForbidden("You do not have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)

class  TeacherCreateView(LoginRequiredMixin, CreateView):
    model=Teacher
    form_class = TeacherSignUpForm
    template_name='multipleUserApp/signup_form.html'
    success_url = reverse_lazy('multipleUserApp:admin_home')
    permission_required  = 'multipleUserApp.add_teacher'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)   
        context['information']="Add a new teacher"
        return context
        
    def dispatch(self, request, *args, **kwargs):
        # if not request.user.groups.filter(name = 'AdmInSuper').exists() | request.user.is_superuser:
        #     return HttpResponseForbidden("You do not have permission to access this page.")
        if not request.user.has_perm(self.permission_required):
            return HttpResponseForbidden("You do not have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)
#================================================================================================
class StudentUploadTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'multipleUserApp/from_file.html'
    # permission_required = 'multipleUserApp.upload_csv' 
    permission_required = 'multipleUserApp.add_studentcsv' 
    success_url = reverse_lazy('multipleUserApp:admin_home')

    def dispatch(self, request, *args, **kwargs):
        # Check if the user has the required permission
        if not request.user.has_perm(self.permission_required):
            return HttpResponseForbidden("You do not have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)

@login_required
# @user_passes_test(lambda u: u.is_staff)
def csv_load_view(request):
    if not request.method == 'POST':
        return HttpResponseBadRequest("Only POST requests are allowed.")

    # if not request.user.is_superuser:
        # return JsonResponse({"success": False, "message": f"You are not authorized to access this page."})
    
    if not request.user.groups.filter(name = 'AdmInSuper').exists() | request.user.is_superuser:
        return JsonResponse({"success": False, "message": f"You are not authorized to access this page."})
    
    CSV_file = request.FILES.get('file')
    if not CSV_file:
        return HttpResponseBadRequest("No file was provided.")

    CSV_file_name = CSV_file.name

    # Read the content of the file directly from memory
    content = CSV_file.read().decode('utf-8').splitlines()

    # Create a CSV reader from the file content
    reader = csv.reader(content)
    header = next(reader, None)  # Skip header

    if header is None or len(header) != 4:
        return JsonResponse({"success": False, "message": f"Invalid CSV format: The CSV file must have a header row with role fields."})

    user_data = []
    for row_num, row in enumerate(reader, start=2):  # Start counting rows from 2 (header is row 1)
        if len(row) != 4:
            return JsonResponse({"success": False, "message": f"Invalid data in row {row_num}: Each row must contain four fields."})
        
        first_name, last_name, password, role = row

        if len(password.strip()) < 6:
            return JsonResponse({"success": False, "message": f"Invalid data in row {row_num}: Password must be at least 6 characters long."})
        
        user_data.append({
            'first_name' : first_name,
            'last_name' : last_name,
            'username' : first_name,
            'password': make_password(password),
            'role': role,
            # 'userRole':role
        })

    # Bulk create users
    for data in user_data:
        role = data.pop('role')
        
        if role == "2":
            data['role']= 'STUDENT'
            Student.objects.get_or_create(**data)
        elif role == "1":
            data['role'] = 'TEACHER'
            Teacher.objects.get_or_create(**data)

        # if role == '2':
        #     student, created = Student.objects.get_or_create(**data)
        #     if created:
        #         StudentProfile.objects.create(user=student, student_id=student.username)
        # elif role == '1':
        #     teacher, created = Teacher.objects.get_or_create(**data)
        #     if created:
        #         TeacherProfile.objects.create(user=teacher, teacher_id=teacher.username)
        
    # If all rows are valid, save the CSV file to the database
    obj, created = STUDENTCSV.objects.get_or_create(file_name=CSV_file_name)
    if created:
        obj.CSV_file = CSV_file
        obj.save()
        return JsonResponse({"success": True, "message": "CSV file saved successfully."})
    else:
        return JsonResponse({"success": False, "message": "CSV file already exists."})


def delete_users(request):
    if request.method == 'POST':
        selected_user_ids = request.POST.getlist('selected_users')

        if not request.user.groups.filter(name = 'AdmInSuper').exists() | request.user.is_superuser:
            messages.error(request,"You are not authorized for this action." )
            redirect_url = request.META.get('HTTP_REFERER', '/')
            return redirect(redirect_url)
        
        if selected_user_ids:
            User.objects.filter(id__in=selected_user_ids).delete()
            messages.success(request, "Users have been deleted successfully")
            redirect_url = request.META.get('HTTP_REFERER', '/')
            return redirect(redirect_url)
        else:
            messages.warning(request, "No users were selected for deletion")
            redirect_url = request.META.get('HTTP_REFERER', '/')
            return redirect(redirect_url)
        
        redirect_url = request.META.get('HTTP_REFERER', '/')
        return redirect(redirect_url)


class AdminHomeView(LoginRequiredMixin, ListView ):
    model = Student
    model2 = Teacher
    model1 = User
    template_name = 'multipleUserApp/admin_home.html'
    # paginate_by = 3
    context_object_name = 'page_obj1'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser and request.user.role != "TEACHER":
            return HttpResponseForbidden("You do not have permission to access this page.")
        
        return super().dispatch(request, *args, **kwargs)


def graph_data(request):
    total_students =  User.objects.filter(role= 'STUDENT').count()
    total_teachers = Teacher.objects.filter(role= 'TEACHER').count()
    # total_admins = Admin.objects.filter(role= 'ADMIN').count()
    
    labels = ["Students", "Teachers"]
    data = {
        'labels':labels,
        'datasets':[
        {
            'label': 'Total Count',
            'data': [total_students, total_teachers],
        }
        ]
    }

    return JsonResponse(data, safe=False)

    