from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Diocese, Parish, Member, Role, MemberRole, Baptism, Confirmation, Marriage


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


class MemberRoleInline(admin.TabularInline):
    model = MemberRole
    extra = 1  # Number of empty forms to display
    fields = ['role', 'start_date', 'end_date']
    # Show role as dropdown instead of autocomplete


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'parish', 'get_diocese', 'member_since', 'has_account']
    list_filter = ['parish__diocese', 'parish', 'created_at']
    search_fields = ['first_name', 'last_name', 'phone', 'parish__name']
    ordering = ['last_name', 'first_name']
    actions = ['create_user_accounts']
    inlines = [MemberRoleInline]
    
    def get_diocese(self, obj):
        return obj.parish.diocese.name
    get_diocese.short_description = 'Diocese'
    get_diocese.admin_order_field = 'parish__diocese__name'
    
    def member_since(self, obj):
        return obj.created_at.strftime('%b %d, %Y')
    member_since.short_description = 'Member Since'
    member_since.admin_order_field = 'created_at'
    
    def has_account(self, obj):
        return obj.user is not None
    has_account.boolean = True
    has_account.short_description = 'Has Login Account'
    
    @admin.action(description='Create user accounts for selected members')
    def create_user_accounts(self, request, queryset):
        """Create user accounts for members who don't have one"""
        created_count = 0
        already_have_count = 0
        
        for member in queryset:
            if member.user:
                already_have_count += 1
                continue
            
            # Generate username from name and ID
            base_username = f"{member.first_name.lower()}.{member.last_name.lower()}"
            username = base_username
            
            # Handle duplicate usernames
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            
            # Create user with default password
            default_password = 'church2026'
            user = User.objects.create_user(
                username=username,
                password=default_password,
                first_name=member.first_name,
                last_name=member.last_name
            )
            
            # Link to member
            member.user = user
            member.save()
            
            created_count += 1
        
        if created_count > 0:
            self.message_user(
                request,
                f'Successfully created {created_count} user account(s). Default password: church2026',
                messages.SUCCESS
            )
        if already_have_count > 0:
            self.message_user(
                request,
                f'{already_have_count} member(s) already have user accounts',
                messages.WARNING
            )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(MemberRole)
class MemberRoleAdmin(admin.ModelAdmin):
    list_display = ['member', 'role', 'start_date', 'end_date']
    list_filter = ['role', 'start_date']
    search_fields = ['member__first_name', 'member__last_name', 'role__name']
    date_hierarchy = 'start_date'


@admin.register(Baptism)
class BaptismAdmin(admin.ModelAdmin):
    list_display = ['member', 'baptism_date', 'parish', 'officiating_priest', 'certificate_number']
    list_filter = ['baptism_date', 'parish__diocese', 'parish']
    search_fields = ['member__first_name', 'member__last_name', 'certificate_number', 'officiating_priest']
    date_hierarchy = 'baptism_date'
    readonly_fields = ['certificate_number', 'created_at']
    
    fieldsets = (
        ('Member Information', {
            'fields': ('member', 'baptism_date', 'parish', 'officiating_priest')
        }),
        ('Godparents', {
            'fields': (
                ('godparent1_name', 'godparent1_gender'),
                ('godparent2_name', 'godparent2_gender'),
                ('godparent3_name', 'godparent3_gender'),
            ),
            'description': 'Anglican tradition: Boys have 2 male + 1 female godparents; Girls have 2 female + 1 male godparents'
        }),
        ('Certificate Details', {
            'fields': ('certificate_number', 'notes', 'created_at')
        }),
    )


@admin.register(Confirmation)
class ConfirmationAdmin(admin.ModelAdmin):
    list_display = ['member', 'confirmation_date', 'parish', 'confirming_bishop', 'certificate_number']
    list_filter = ['confirmation_date', 'parish__diocese', 'parish']
    search_fields = ['member__first_name', 'member__last_name', 'certificate_number', 'confirming_bishop']
    date_hierarchy = 'confirmation_date'
    readonly_fields = ['certificate_number', 'created_at']


@admin.register(Marriage)
class MarriageAdmin(admin.ModelAdmin):
    list_display = ['groom', 'bride', 'marriage_date', 'parish', 'officiating_priest', 'certificate_number']
    list_filter = ['marriage_date', 'parish__diocese', 'parish']
    search_fields = ['groom__first_name', 'groom__last_name', 'bride__first_name', 'bride__last_name', 'certificate_number']
    date_hierarchy = 'marriage_date'
    readonly_fields = ['certificate_number', 'created_at']
