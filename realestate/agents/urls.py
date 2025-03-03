from django.urls import path
from .views import agent_register, agent_login, agent_dashboard, admin_verify_agents, verify_agent
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', agent_register, name='agent_register'),
    path('login/', agent_login, name='agent_login'),
    path('logout/', LogoutView.as_view(next_page='agent_login'), name='agent_logout'),
    path('dashboard/', agent_dashboard, name='agent_dashboard'),
    path('admin/verify-agents/', admin_verify_agents, name='admin_verify_agents'),
     path('admin/verify-agent/<int:verification_id>/', verify_agent, name='verify_agent'),
]
