from django.db import models
from django.conf import settings
from django.utils import timezone

class Agent(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    agency_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    location = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    profile_image = models.ImageField(upload_to='agents/profiles/', blank=True)
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.location}"

class AgentVerification(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='verifications')
    id_proof = models.FileField(upload_to='agents/verification/')
    business_license = models.FileField(upload_to='agents/verification/')
    additional_document = models.FileField(upload_to='agents/verification/', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    admin_notes = models.TextField(blank=True)
    
    def approve(self):
        self.status = 'approved'
        self.processed_at = timezone.now()
        self.save()
        
        # Update agent verification status
        agent = self.agent
        agent.is_verified = True
        agent.verification_date = timezone.now()
        agent.save()
    
    def reject(self):
        self.status = 'rejected'
        self.processed_at = timezone.now()
        self.save()