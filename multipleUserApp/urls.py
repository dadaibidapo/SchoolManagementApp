from django.urls import path
from . import views
from .views import CustomLoginView,StudentCreateView,TeacherCreateView,StudentUploadTemplateView,AdminHomeView,StudentList,TeacherList

app_name = 'multipleUserApp'

urlpatterns = [
    path('', views.index, name='index'),
    
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    
    
    # path('teacher/', views.teacher_home, name='teacher_home'),
    path('custom-admin/', AdminHomeView.as_view(), name='admin_home'),

    path('delete-users/', views.delete_users, name='delete_users'),



    path('student_list/', StudentList.as_view(), name='student_list'),
    path('teacher_list/', TeacherList.as_view(), name='teacher_list'),
    # path('admin_list/', AdminList.as_view(), name='admin_list'),
    
    path('from_file', StudentUploadTemplateView.as_view(), name='from_file'),
    path('upload/', views.csv_load_view, name='upload'),

    path('graph-data', views.graph_data, name="graph_data"), 

    # path('user_register/', UserListView.as_view(), name='user_register'),
    path('student_register/', StudentCreateView.as_view(), name='student_register'),
    path('teacher_register/', TeacherCreateView.as_view(), name='teacher_register'),
    # path('admin_register/', AdminCreateView.as_view(), name='admin_register'),
    # path('it_staff_register/', IT_StaffCreateView.as_view(), name='it_staff_register'),



]