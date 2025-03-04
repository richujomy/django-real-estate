from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import AgentRegistrationForm, AgentLoginForm, AgentVerificationForm
from .models import AgentVerification, Agent
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


def agent_register(request):
    if request.method == 'POST':
        form = AgentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('agent_dashboard')
    else:
        form = AgentRegistrationForm()
    return render(request, 'agents/register.html', {'form': form})

def agent_login(request):
    if request.method == 'POST':
        form = AgentLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('agent_dashboard')
    else:
        form = AgentLoginForm()
    return render(request, 'agents/login.html', {'form': form})

def agent_dashboard(request):
    is_verified = request.user.agent.is_verified
    return render(request, 'agents/dashboard.html',{'is_verified': is_verified})

@login_required
def approved_agents_list(request):
    approved_agents=Agent.objects.filter(is_verified=True)
    context = {'approved_agents':approved_agents}
    return render(request, 'agents/approved_agents_list.html',context)

@staff_member_required
def admin_verify_agents(request):
    verifications = AgentVerification.objects.filter(status='pending')
    return render(request, 'admin/verify_agents.html', {'verifications': verifications})

@staff_member_required
def verify_agent(request, verification_id):
    verification = get_object_or_404(AgentVerification, id=verification_id)

    if request.method == 'POST':
        form = AgentVerificationForm(request.POST, instance=verification)
        if form.is_valid():
            verification = form.save(commit=False)
            if verification.status == 'approved':
                verification.approve()  # Calls the approve() method in models.py
            elif verification.status == 'rejected':
                verification.reject()  # Calls the reject() method in models.py
            return redirect('admin_verify_agents')
    else:
        form = AgentVerificationForm(instance=verification)

    return render(request, 'admin/verify_agent_detail.html', {'form': form, 'verification': verification})