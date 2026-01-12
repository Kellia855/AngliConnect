from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from .models import Parish, Member, Role, MemberRole, Diocese
from .forms import MemberForm, RoleForm, MemberRoleForm


def index(request):
    return render(request, 'church/index.html')


def load_parishes(request):
    """AJAX view to load parishes based on selected diocese"""
    diocese_id = request.GET.get('diocese_id')
    parishes = Parish.objects.filter(diocese_id=diocese_id).order_by('name')
    return JsonResponse(list(parishes.values('id', 'name')), safe=False)


class MemberListView(ListView):
    model = Member
    template_name = 'church/members.html'
    context_object_name = 'members'
    
    def get_queryset(self):
        return Member.objects.select_related('parish', 'parish__diocese').all()


class MemberCreateView(CreateView):
    model = Member
    form_class = MemberForm
    template_name = 'church/add_member.html'
    success_url = reverse_lazy('church:members')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parishes'] = Parish.objects.all()
        return context


class RoleListView(ListView):
    model = Role
    template_name = 'church/roles.html'
    context_object_name = 'roles'


class RoleCreateView(CreateView):
    model = Role
    form_class = RoleForm
    template_name = 'church/add_role.html'
    success_url = reverse_lazy('church:roles')


def assign_role(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    
    if request.method == 'POST':
        form = MemberRoleForm(request.POST)
        if form.is_valid():
            member_role = form.save(commit=False)
            member_role.member = member
            member_role.save()
            return redirect('church:member_roles', member_id=member_id)
    else:
        form = MemberRoleForm()
    
    roles = Role.objects.all()
    return render(request, 'church/assign_role.html', {
        'member': member,
        'member_id': member_id,
        'roles': roles,
        'form': form
    })


def member_roles(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    roles = MemberRole.objects.filter(member=member).select_related('role')
    
    return render(request, 'church/member_roles.html', {
        'member': member,
        'member_id': member_id,
        'roles': roles
    })
