from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from church.models import Member


class Command(BaseCommand):
    help = 'Create a user account for a church member'

    def add_arguments(self, parser):
        parser.add_argument('member_id', type=int, help='Member ID')
        parser.add_argument('username', type=str, help='Username for login')
        parser.add_argument('--password', type=str, default='changeme123', help='Password (default: changeme123)')

    def handle(self, *args, **options):
        member_id = options['member_id']
        username = options['username']
        password = options['password']
        
        try:
            member = Member.objects.get(id=member_id)
        except Member.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Member with ID {member_id} does not exist'))
            return
        
        # Check if member already has a user account
        if member.user:
            self.stdout.write(self.style.WARNING(f'Member {member.get_full_name()} already has a user account: {member.user.username}'))
            return
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f'Username "{username}" already exists'))
            return
        
        # Create user account
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=member.first_name,
            last_name=member.last_name,
            email=''  # You can add email field to Member model if needed
        )
        
        # Link user to member
        member.user = user
        member.save()
        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully created account for {member.get_full_name()}\n'
            f'Username: {username}\n'
            f'Password: {password}\n'
            f'⚠️  Member should change password after first login'
        ))
