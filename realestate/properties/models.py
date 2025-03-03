# models.py
from django.db import models
from accounts.models import User
from django.utils import timezone
from agents.models import Agent

class Location(models.Model):
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    area = models.CharField(max_length=100)

    class Meta:
        unique_together = ('state', 'district', 'area')

    def __str__(self):
        return f"{self.area}, {self.district}, {self.state}"
    


class Property(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='properties', null=True, blank=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    location = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=100)
    description = models.TextField()
    property_type = models.CharField(
        max_length=20,
        choices=[
            ('house', 'House'),
            ('apartment', 'Apartment'),
            ('land', 'Land'),
            ('commercial', 'Commercial')
        ]
    )
    type = models.CharField(
        max_length=20,
        choices=[
            ('sale', 'For Sale'),
            ('rent', 'For Rent'),
            ('lease', 'For Lease'),
        ]
    )
    price = models.DecimalField(max_digits=15, decimal_places=2)
    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    area_sqft = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=[
            ('available', 'Available'),
            ('sold', 'Sold'),
            ('pending', 'Pending')
        ],
        default='available'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


    
class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')

    def __str__(self):
        return f"Image for {self.property.title}"

# Add to your existing models.py
class PropertyInquiry(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='inquiries')
    sender = models.ForeignKey(User, related_name='sent_inquiries', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_inquiries', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Inquiry about {self.property.title} from {self.sender.username}"

class ChatMessage(models.Model):
    inquiry = models.ForeignKey(PropertyInquiry, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"