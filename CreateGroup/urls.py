from django.urls import path
from .views import CreateGroupView,GroupListView,ViewGroupPermissionsView,AddUsersToGroupView,RemoveUsersFromGroupView

app_name = 'CreateGroup'

urlpatterns = [
    path('create_group/', CreateGroupView.as_view(), name='create_group'),

    path('list_group/', GroupListView.as_view(), name='list_group'),

    path('groups/<int:pk>/permissions/', ViewGroupPermissionsView.as_view(), name='view_group_permissions'),

    path('<int:group_id>/add_users/', AddUsersToGroupView.as_view(), name='add_users_to_group'),

    path('<int:group_id>/remove_users/', RemoveUsersFromGroupView.as_view(), name='remove_users_from_group'),
]