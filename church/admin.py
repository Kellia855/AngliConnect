from django.contrib import admin
from .models import Diocese, Parish, Member, Role, MemberRole


@admin.register(Diocese)
class DioceseAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Parish)
class ParishAdmin(admin.ModelAdmin):
    list_display = ['name', 'diocese']
    list_filter = ['diocese']
    search_fields = ['name', 'diocese__name']
    ordering = ['diocese__name', 'name']


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'parish', 'get_diocese']
    list_filter = ['parish__diocese', 'parish']
    search_fields = ['first_name', 'last_name', 'phone', 'parish__name']
    ordering = ['last_name', 'first_name']
    
    def get_diocese(self, obj):
        return obj.parish.diocese.name
    get_diocese.short_description = 'Diocese'
    get_diocese.admin_order_field = 'parish__diocese__name'


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(MemberRole)
class MemberRoleAdmin(admin.ModelAdmin):
    list_display = ['member', 'role', 'start_date', 'end_date']
    list_filter = ['role', 'start_date']
    search_fields = ['member__first_name', 'member__last_name', 'role__name']
    date_hierarchy = 'start_date'
