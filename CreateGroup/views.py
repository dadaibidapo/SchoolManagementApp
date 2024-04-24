from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import Group
from django.urls import reverse_lazy, reverse

from django.views.generic import CreateView, ListView,DetailView, FormView

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin

from multipleUserApp.models import User,Student, Teacher

from .form import GroupForm,AddUserToGroupForm, RemoveUserFromGroupForm

from django.http import HttpResponseForbidden, JsonResponse, HttpResponseBadRequest
from django.http import HttpResponse

# Create your views here.
class CreateGroupView(LoginRequiredMixin, UserPassesTestMixin,CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'CreateGroup/create_group.html'
    success_url = '/group/create_group/'
    permission_required = 'CreateGroup.add_group'

    def form_valid(self, form):
        group = form.save(commit=False)
        group.save()
        form.save_m2m()  # Save ManyToManyField for permissions
        messages.success(self.request, f"Group '{group.name}' created successfully.")
        return super().form_valid(form)
    
    # def test_func(self) -> bool | None:
    #     return self.request.user.is_superuser

    def test_func(self):
        # Define your custom access control logic here
        user1 = self.request.user.is_authenticated and self.request.user.groups.filter(name='AdmInSuper').exists()
        return user1 or self.request.user.is_superuser

    # def get_permission_required(self):
    #     return self.permission_required

    # def handle_no_permission(self):
    #     if self.request.user.has_perm(self.permission_required):
    #         return HttpResponseForbidden("You do not have permission to access this page.")
    #     return super().handle_no_permission()
    
class GroupListView(LoginRequiredMixin,UserPassesTestMixin, ListView):
    model = Group
    template_name = 'CreateGroup/group_list.html'
    context_object_name = 'groups'
    permission_required ='CreateGroup.view_group' #['CreateGroup.view_group','CreateGroup.add_group', 'CreateGroup.change_group', 'CreateGroup.delete_group']
    raise_exception = True  # This will raise a 403 Forbidden error if the user doesn't have permission
    
    def test_func(self):
        # Define your custom access control logic here
        user1 = self.request.user.is_authenticated and self.request.user.groups.filter(name='AdmInSuper').exists()
        return user1 or self.request.user.is_superuser
    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.has_perm(self.permission_required):
    #         return HttpResponseForbidden("You do not have permission to access this page.")
    #     return super().dispatch(request, *args, **kwargs)
    

class ViewGroupPermissionsView(LoginRequiredMixin, UserPassesTestMixin,DetailView):
    model = Group
    template_name = 'CreateGroup/view_group_permissions.html'
    context_object_name = 'group'
    permission_required = 'CreateGroup.veiw_permission'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = self.get_object()
        permissions = group.permissions.all()
        context['permissions'] = permissions
        return context
    def test_func(self):
        # Define your custom access control logic here
        user1 = self.request.user.is_authenticated and self.request.user.groups.filter(name='AdmInSuper').exists()
        return user1 or self.request.user.is_superuser
    # def handle_no_permission(self):
    #     return HttpResponseForbidden("You do not have permission to access this page.")

class AddUsersToGroupView(LoginRequiredMixin, UserPassesTestMixin,FormView):
    template_name = 'CreateGroup/add_users_to_group.html'
    form_class = AddUserToGroupForm
    success_url = '/group/list_group/'
    permission_required = 'CreateGroup.add_permission'

    def form_valid(self, form):
        group_id = self.kwargs['group_id']
        group = Group.objects.get(id=group_id)
        users = form.cleaned_data['users']
        group.user_set.add(*users)
        return HttpResponseRedirect(reverse('CreateGroup:list_group'))
    def test_func(self):
        # Define your custom access control logic here
        user1 = self.request.user.is_authenticated and self.request.user.groups.filter(name='AdmInSuper').exists()
        return user1 or self.request.user.is_superuser
    # def handle_no_permission(self):
    #     return HttpResponseForbidden("You do not have permission to access this page.")


class RemoveUsersFromGroupView(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = 'CreateGroup/remove_users_from_group.html'
    form_class = RemoveUserFromGroupForm
    success_url = '/group/list_group/'
    permission_required = 'CreateGroup.delete_permission'

    def get_group(self):
        return Group.objects.get(id=self.kwargs['group_id'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['group'] = self.get_group()
        return kwargs

    def form_valid(self, form):
        group = self.get_group()
        users = form.cleaned_data['users']
        group.user_set.remove(*users)
        return HttpResponseRedirect(reverse('CreateGroup:list_group'))
    
    def test_func(self):
        # Define your custom access control logic here
        user1 = self.request.user.is_authenticated and self.request.user.groups.filter(name='AdmInSuper').exists()
        return user1 or self.request.user.is_superuser
    # def handle_no_permission(self):
    #     return HttpResponseForbidden("You do not have permission to access this page.")