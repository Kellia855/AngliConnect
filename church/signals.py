from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Member, Role, MemberRole


@receiver(post_save, sender=Member)
def assign_default_member_role(sender, instance, created, **kwargs):
    """Assign default church member role when a new member is created."""
    if not created:
        return

    default_role = Role.objects.filter(name__iexact="Church Member").first()
    if not default_role:
        default_role = Role.objects.filter(name__iexact="Member").first()

    if not default_role:
        default_role = Role.objects.create(name="Church Member")

    MemberRole.objects.get_or_create(
        member=instance,
        role=default_role,
        start_date=timezone.localdate(),
    )
