from django.db import models
from django.contrib.auth.models import User
import uuid


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
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='member')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    parish = models.ForeignKey(Parish, on_delete=models.CASCADE, related_name='members')
    photo = models.ImageField(upload_to='member_photos/', blank=True, null=True, help_text="Member profile photo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
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


class Baptism(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    member = models.OneToOneField(Member, on_delete=models.CASCADE, related_name='baptism')
    baptism_date = models.DateField()
    parish = models.ForeignKey(Parish, on_delete=models.CASCADE, related_name='baptisms')
    church_name = models.CharField(max_length=200, blank=True, help_text="Specific church building within the parish")
    officiating_priest = models.CharField(max_length=200)
    
    # Godparents
    godparent1_name = models.CharField(max_length=200)
    godparent1_gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    godparent2_name = models.CharField(max_length=200)
    godparent2_gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    godparent3_name = models.CharField(max_length=200)
    godparent3_gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    godparent4_name = models.CharField(max_length=200, blank=True)
    godparent4_gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    
    certificate_number = models.CharField(max_length=50, unique=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-baptism_date']
    
    def __str__(self):
        return f"{self.member.get_full_name()} - Baptized {self.baptism_date}"
    
    def save(self, *args, **kwargs):
        if not self.certificate_number:
            self.certificate_number = f"BPT-{self.baptism_date.year}-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)


class Confirmation(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE, related_name='confirmation')
    confirmation_date = models.DateField()
    parish = models.ForeignKey(Parish, on_delete=models.CASCADE, related_name='confirmations')
    church_name = models.CharField(max_length=200, blank=True, help_text="Specific church building within the parish")
    confirming_bishop = models.CharField(max_length=200)
    confirmation_verse = models.CharField(max_length=500, blank=True, help_text="Personal Bible verse")
    certificate_number = models.CharField(max_length=50, unique=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-confirmation_date']
    
    def __str__(self):
        return f"{self.member.get_full_name()} - Confirmed {self.confirmation_date}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        # Check if member is baptized
        if not hasattr(self.member, 'baptism'):
            raise ValidationError(f"{self.member.get_full_name()} must be baptized before confirmation.")
    
    def save(self, *args, **kwargs):
        if not self.certificate_number:
            self.certificate_number = f"CNF-{self.confirmation_date.year}-{uuid.uuid4().hex[:8].upper()}"
        self.full_clean()
        super().save(*args, **kwargs)


class Marriage(models.Model):
    groom = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='marriages_as_groom')
    bride = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='marriages_as_bride')
    marriage_date = models.DateField()
    parish = models.ForeignKey(Parish, on_delete=models.CASCADE, related_name='marriages')
    church_name = models.CharField(max_length=200, blank=True, help_text="Specific church building within the parish")
    officiating_priest = models.CharField(max_length=200)
    
    witness1_name = models.CharField(max_length=200)
    witness2_name = models.CharField(max_length=200)
    
    certificate_number = models.CharField(max_length=50, unique=True, blank=True)
    license_details = models.CharField(max_length=200, blank=True, help_text="Marriage license reference")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-marriage_date']
        verbose_name_plural = "Marriages"
    
    def __str__(self):
        return f"{self.groom.get_full_name()} & {self.bride.get_full_name()} - {self.marriage_date}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        # Check if both parties are baptized
        errors = []
        if not hasattr(self.groom, 'baptism'):
            errors.append(f"Groom ({self.groom.get_full_name()}) must be baptized before marriage.")
        if not hasattr(self.bride, 'baptism'):
            errors.append(f"Bride ({self.bride.get_full_name()}) must be baptized before marriage.")
        
        # Prevent marrying the same person
        if self.groom == self.bride:
            errors.append("Bride and groom cannot be the same person.")
        
        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        if not self.certificate_number:
            self.certificate_number = f"MAR-{self.marriage_date.year}-{uuid.uuid4().hex[:8].upper()}"
        self.full_clean()
        super().save(*args, **kwargs)
