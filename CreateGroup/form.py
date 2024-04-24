from django import forms
from django.contrib.auth.models import Group, Permission
from multipleUserApp.models import User,Student, Teacher


class GroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.all(), required= False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Group
        fields = ['name', 'permissions']

# class RemoveUserFromGroupForm(forms.Form):
#     user = forms.ModelChoiceField(queryset=Teacher.objects.filter(role= 'TEACHER'), required=True)
#     groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=True)

class AddUserToGroupForm(forms.Form):
    users = forms.ModelMultipleChoiceField(queryset=Teacher.objects.filter(role='TEACHER'), widget=forms.CheckboxSelectMultiple)

# class RemoveUserFromGroupForm(forms.Form):
#     users = forms.ModelMultipleChoiceField(queryset=Teacher.objects.filter(role='TEACHER'), widget=forms.CheckboxSelectMultiple)

class RemoveUserFromGroupForm(forms.Form):
    users = forms.ModelMultipleChoiceField(queryset=Teacher.objects.filter(role='TEACHER'), widget=forms.CheckboxSelectMultiple)

    def __init__(self, group, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['users'].queryset = group.user_set.all()