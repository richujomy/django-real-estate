# Let's check your current urls.py
from django.urls import path
from . import views
from .views import get_areas, test_locations, debug_get_areas
from .views import property_detail, property_list


urlpatterns = [
    path('sell-property', views.sell_property, name='sell_property'),
    path('property_list/', views.property_list, name='property_list'),
    path('get-areas/', get_areas, name='get_areas'),
    path('test-locations/', test_locations, name='test_locations'),
    path('debug-get-areas/', debug_get_areas, name='debug_get_areas'),
    path('properties/<int:pk>/', property_detail, name='property_detail'),
    path('property/<int:property_id>/inquire/',
         views.create_inquiry, name='create_inquiry'),
    path('chats/<int:inquiry_id>/', views.chat_detail, name='chat_detail'),
    path('chats/<int:inquiry_id>/send/',
         views.send_message, name='send_message'),
    path('my-inquiries/', views.my_inquiries, name='my_inquiries'),
]
# Note: If this is included in your project's main urls.py like this:
# path('properties/', include('properties.urls')),
# Then the actual URL would be /properties/get-areas/
