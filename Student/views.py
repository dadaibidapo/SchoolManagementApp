from django.shortcuts import render
from django.views.generic import CreateView, View, ListView,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from multipleUserApp.models import User,Student, Teacher,STUDENTCSV
from django.http import HttpResponseForbidden, JsonResponse, HttpResponseBadRequest


class DasboardView(LoginRequiredMixin, ListView):
    model= Student
    template_name = 'Student/dashboard.html'

    def dispatch(self, request, *args, **kwargs):
   
        if not request.user.role == 'STUDENT':
            return HttpResponseForbidden("You do not have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)