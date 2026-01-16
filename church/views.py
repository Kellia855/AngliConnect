from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Q
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from .models import Parish, Member, Role, MemberRole, Diocese
from .forms import MemberForm, RoleForm, MemberRoleForm


def index(request):
    return render(request, 'church/index.html')


def dashboard(request):
    """Analytics dashboard with church statistics"""
    # Overall statistics
    total_members = Member.objects.count()
    total_dioceses = Diocese.objects.count()
    total_parishes = Parish.objects.count()
    total_roles = Role.objects.count()
    
    # Members by diocese
    diocese_stats = Diocese.objects.annotate(
        member_count=Count('parishes__members'),
        parish_count=Count('parishes')
    ).order_by('-member_count')
    
    # Members by parish
    parish_stats = Parish.objects.annotate(
        member_count=Count('members')
    ).select_related('diocese').order_by('-member_count')[:10]
    
    # Active role assignments (no end_date)
    role_stats = Role.objects.annotate(
        assignment_count=Count('assignments', filter=Q(assignments__end_date__isnull=True))
    ).order_by('-assignment_count')
    
    # Recent role assignments
    recent_assignments = MemberRole.objects.select_related(
        'member', 'role'
    ).order_by('-start_date')[:10]
    
    context = {
        'total_members': total_members,
        'total_dioceses': total_dioceses,
        'total_parishes': total_parishes,
        'total_roles': total_roles,
        'diocese_stats': diocese_stats,
        'parish_stats': parish_stats,
        'role_stats': role_stats,
        'recent_assignments': recent_assignments,
    }
    
    return render(request, 'church/dashboard.html', context)


def export_dashboard_excel(request):
    """Export dashboard statistics to Excel"""
    # Create workbook
    wb = Workbook()
    
    # Overall Statistics Sheet
    ws_overview = wb.active
    ws_overview.title = "Overview"
    
    # Header styling
    header_fill = PatternFill(start_color="2C5F8D", end_color="2C5F8D", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)
    
    # Overview statistics
    ws_overview['A1'] = "Church Management System - Overview"
    ws_overview['A1'].font = Font(bold=True, size=14)
    ws_overview.merge_cells('A1:B1')
    
    ws_overview['A3'] = "Metric"
    ws_overview['B3'] = "Count"
    ws_overview['A3'].fill = header_fill
    ws_overview['B3'].fill = header_fill
    ws_overview['A3'].font = header_font
    ws_overview['B3'].font = header_font
    
    overview_data = [
        ["Total Members", Member.objects.count()],
        ["Total Dioceses", Diocese.objects.count()],
        ["Total Parishes", Parish.objects.count()],
        ["Total Roles", Role.objects.count()],
    ]
    
    for idx, (metric, value) in enumerate(overview_data, start=4):
        ws_overview[f'A{idx}'] = metric
        ws_overview[f'B{idx}'] = value
    
    # Diocese Statistics Sheet
    ws_diocese = wb.create_sheet("Diocese Statistics")
    ws_diocese['A1'] = "Diocese"
    ws_diocese['B1'] = "Members"
    ws_diocese['C1'] = "Parishes"
    
    for cell in ['A1', 'B1', 'C1']:
        ws_diocese[cell].fill = header_fill
        ws_diocese[cell].font = header_font
    
    diocese_stats = Diocese.objects.annotate(
        member_count=Count('parishes__members'),
        parish_count=Count('parishes')
    ).order_by('-member_count')
    
    for idx, diocese in enumerate(diocese_stats, start=2):
        ws_diocese[f'A{idx}'] = diocese.name
        ws_diocese[f'B{idx}'] = diocese.member_count
        ws_diocese[f'C{idx}'] = diocese.parish_count
    
    # Parish Statistics Sheet
    ws_parish = wb.create_sheet("Parish Statistics")
    ws_parish['A1'] = "Parish"
    ws_parish['B1'] = "Diocese"
    ws_parish['C1'] = "Members"
    
    for cell in ['A1', 'B1', 'C1']:
        ws_parish[cell].fill = header_fill
        ws_parish[cell].font = header_font
    
    parish_stats = Parish.objects.annotate(
        member_count=Count('members')
    ).select_related('diocese').order_by('-member_count')
    
    for idx, parish in enumerate(parish_stats, start=2):
        ws_parish[f'A{idx}'] = parish.name
        ws_parish[f'B{idx}'] = parish.diocese.name
        ws_parish[f'C{idx}'] = parish.member_count
    
    # Member List Sheet
    ws_members = wb.create_sheet("All Members")
    ws_members['A1'] = "First Name"
    ws_members['B1'] = "Last Name"
    ws_members['C1'] = "Phone"
    ws_members['D1'] = "Parish"
    ws_members['E1'] = "Diocese"
    
    for cell in ['A1', 'B1', 'C1', 'D1', 'E1']:
        ws_members[cell].fill = header_fill
        ws_members[cell].font = header_font
    
    members = Member.objects.select_related('parish__diocese').all()
    
    for idx, member in enumerate(members, start=2):
        ws_members[f'A{idx}'] = member.first_name
        ws_members[f'B{idx}'] = member.last_name
        ws_members[f'C{idx}'] = member.phone
        ws_members[f'D{idx}'] = member.parish.name
        ws_members[f'E{idx}'] = member.parish.diocese.name
    
    # Auto-adjust column widths
    for ws in [ws_overview, ws_diocese, ws_parish, ws_members]:
        for column_cells in ws.columns:
            max_length = 0
            column_letter = None
            for cell in column_cells:
                # Skip merged cells
                if hasattr(cell, 'column_letter'):
                    column_letter = cell.column_letter
                    try:
                        if cell.value and len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
            if column_letter:
                adjusted_width = min(max_length + 2, 50)
                ws.column_dimensions[column_letter].width = adjusted_width
    
    # Create response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=church_management_report.xlsx'
    
    wb.save(response)
    return response


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
