from django.core.management.base import BaseCommand
from django.utils import timezone

from church.models import Member, Role, MemberRole


class Command(BaseCommand):
    help = "Assign default church member role to members who have no roles"

    def handle(self, *args, **options):
        default_role = Role.objects.filter(name__iexact="Church Member").first()
        if not default_role:
            default_role = Role.objects.filter(name__iexact="Member").first()

        if not default_role:
            default_role = Role.objects.create(name="Church Member")
            self.stdout.write(self.style.WARNING('Created missing role: "Church Member"'))

        members_without_roles = Member.objects.filter(role_assignments__isnull=True).distinct()

        count = 0
        for member in members_without_roles:
            MemberRole.objects.get_or_create(
                member=member,
                role=default_role,
                start_date=timezone.localdate(),
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f"Assigned default role to {count} member(s)."))
