from django.urls import path
from . import views

app_name = 'church'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/export/', views.export_dashboard_excel, name='export_dashboard'),
    path('members/', views.MemberListView.as_view(), name='members'),
    path('add-member/', views.MemberCreateView.as_view(), name='add_member'),
    path('ajax/load-parishes/', views.load_parishes, name='ajax_load_parishes'),
    path('roles/', views.RoleListView.as_view(), name='roles'),
    path('add-role/', views.RoleCreateView.as_view(), name='add_role'),
    path('assign-role/<int:member_id>/', views.assign_role, name='assign_role'),
    path('member/<int:member_id>/roles/', views.member_roles, name='member_roles'),
]
