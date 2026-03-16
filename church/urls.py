from django.urls import path
from . import views

app_name = 'church'

urlpatterns = [
    path('', views.index, name='index'),
    path('portal/', views.member_portal, name='member_portal'),
    path('change-password/', views.change_password, name='change_password'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/export/', views.export_dashboard_excel, name='export_dashboard'),
    path('members/', views.MemberListView.as_view(), name='members'),
    path('members/export/excel/', views.export_members_excel, name='export_members_excel'),
    path('members/export/pdf/', views.export_members_pdf, name='export_members_pdf'),
    path('add-member/', views.MemberCreateView.as_view(), name='add_member'),
    path('edit-member/<int:pk>/', views.MemberUpdateView.as_view(), name='edit_member'),
    path('ajax/load-parishes/', views.load_parishes, name='ajax_load_parishes'),
    path('roles/', views.RoleListView.as_view(), name='roles'),
    path('add-role/', views.RoleCreateView.as_view(), name='add_role'),
    path('assign-role/<int:member_id>/', views.assign_role, name='assign_role'),
    path('member/<int:member_id>/roles/', views.member_roles, name='member_roles'),
    path('member/<int:member_id>/profile/', views.member_profile, name='member_profile'),
    path('sacraments/baptisms/', views.baptism_list, name='baptism_list'),
    path('sacraments/baptisms/add/', views.add_baptism, name='add_baptism'),
    path('sacraments/confirmations/', views.confirmation_list, name='confirmation_list'),
    path('sacraments/confirmations/add/', views.add_confirmation, name='add_confirmation'),
    path('sacraments/marriages/', views.marriage_list, name='marriage_list'),
    path('sacraments/marriages/add/', views.add_marriage, name='add_marriage'),
    path('certificates/baptism/<int:baptism_id>/', views.generate_baptism_certificate, name='generate_baptism_cert'),
    path('certificates/confirmation/<int:confirmation_id>/', views.generate_confirmation_certificate, name='generate_confirmation_cert'),
    path('certificates/marriage/<int:marriage_id>/', views.generate_marriage_certificate, name='generate_marriage_cert'),
    path('verify-certificate/', views.verify_certificate, name='verify_certificate'),
]
