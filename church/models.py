from django.db import models


class Diocese(models.Model):
    name = models.CharField(max_length=200)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Parish(models.Model):
    name = models.CharField(max_length=200)
    diocese = models.ForeignKey(Diocese, on_delete=models.CASCADE, related_name='parishes')
    
    class Meta:
        verbose_name_plural = "Parishes"
        ordering = ['diocese__name', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.diocese.name})"


class Member(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    parish = models.ForeignKey(Parish, on_delete=models.CASCADE, related_name='members')
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Role(models.Model):
    name = models.CharField(max_length=200)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class MemberRole(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='role_assignments')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='assignments')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['-start_date']
        unique_together = ['member', 'role', 'start_date']
    
    def __str__(self):
        return f"{self.member.get_full_name()} - {self.role.name}"
