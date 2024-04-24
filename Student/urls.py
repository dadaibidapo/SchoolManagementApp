from django.urls import path
from . import views 
from .views import DasboardView
# from .views import 

app_name = 'Student'

urlpatterns = [
    path('', DasboardView.as_view(), name='student_dashboard'),
    
    # path('login/', CustomLoginView.as_view(), name='login'),
    # path('logout/', views.logout_view, name='logout'),
    

]