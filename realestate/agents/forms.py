from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Agent, AgentVerification
from django.contrib.auth import get_user_model

User = get_user_model()  # Dynamically get the correct user model




class AgentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    agency_name = forms.CharField(max_length=100)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    experience_years = forms.IntegerField(min_value=0)
    location = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=20)
    profile_image = forms.ImageField(required=False)
    id_proof = forms.FileField()
    business_license = forms.FileField()
    additional_document = forms.FileField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            agent = Agent.objects.create(
                user=user,
                agency_name=self.cleaned_data['agency_name'],
                bio=self.cleaned_data['bio'],
                experience_years=self.cleaned_data['experience_years'],
                location=self.cleaned_data['location'],
                phone=self.cleaned_data['phone'],
                profile_image=self.cleaned_data.get('profile_image')
            )
            AgentVerification.objects.create(
                agent=agent,
                id_proof=self.cleaned_data['id_proof'],
                business_license=self.cleaned_data['business_license'],
                additional_document=self.cleaned_data.get('additional_document')
            )
        return user

class AgentLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class AgentVerificationForm(forms.ModelForm):
    class Meta:
        model = AgentVerification
        fields = ['status', 'admin_notes']
