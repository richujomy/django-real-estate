from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PropertyForm
from .models import PropertyImage, Location, Property, PropertyInquiry, ChatMessage
from django.http import JsonResponse
from django.contrib import messages


@login_required
def sell_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_obj = form.save(commit=False)

            # Get selected district and area
            district = form.cleaned_data['district']
            area = form.cleaned_data['area']
            
            try:
                # Get the location object matching the district and area
                location = Location.objects.get(district=district, area=area)
                property_obj.location = location
                property_obj.user = request.user
                property_obj.save()
                
                # Save multiple images
                images = request.FILES.getlist('images')
                for image in images:
                    PropertyImage.objects.create(property=property_obj, image=image)

                return redirect('property_list')  # Redirect to property listing
            except Location.DoesNotExist:
                form.add_error(None, "The selected location does not exist.")
    else:
        form = PropertyForm()

    return render(request, 'properties/sell_property.html', {'form': form})

def property_list(request):
    properties = Property.objects.all()
    return render(request, 'properties/property_list.html', {'properties': properties})

# Function to fetch areas dynamically
def get_areas(request):
    district = request.GET.get('district')
    print(f"Received request for areas in district: {district}")  # Debug print
    
    if district:
        areas = list(Location.objects.filter(district=district).values_list('area', flat=True).distinct())
        print(f"Found {len(areas)} areas: {areas}")  # Debug print
        return JsonResponse({'areas': areas})
    
    print("No district provided")  # Debug print
    return JsonResponse({'areas': []})

def debug_locations(request):
    locations = Location.objects.all()
    location_data = [
        {"id": loc.id, "state": loc.state, "district": loc.district, "area": loc.area} 
        for loc in locations
    ]
    return JsonResponse({"locations": location_data})

# Add this to your views.py
def test_locations(request):
    # First, check if we have any locations
    locations = Location.objects.all()
    count = locations.count()
    
    # If no locations exist, create some test data
    if count == 0:
        # Create test data
        test_locations = [
            {'state': 'California', 'district': 'Los Angeles', 'area': 'Downtown'},
            {'state': 'California', 'district': 'Los Angeles', 'area': 'Hollywood'},
            {'state': 'California', 'district': 'San Francisco', 'area': 'Mission District'},
            {'state': 'California', 'district': 'San Francisco', 'area': 'Financial District'},
            {'state': 'New York', 'district': 'New York City', 'area': 'Manhattan'},
            {'state': 'New York', 'district': 'New York City', 'area': 'Brooklyn'},
        ]
        
        for loc in test_locations:
            Location.objects.create(**loc)
        
        created = len(test_locations)
        message = f"Created {created} test locations."
    else:
        # Show existing locations
        location_list = []
        for loc in locations:
            location_list.append(f"{loc.area}, {loc.district}, {loc.state}")
        
        message = f"Found {count} existing locations: {', '.join(location_list[:5])}..."
    
    # Return all districts and sample areas
    districts = Location.objects.values_list('district', flat=True).distinct()
    district_areas = {}
    for district in districts:
        areas = Location.objects.filter(district=district).values_list('area', flat=True)
        district_areas[district] = list(areas)
    
    return JsonResponse({
        'message': message,
        'districts': list(districts),
        'district_areas': district_areas
    })

def debug_get_areas(request):
    """A simple view to verify the URL routing is working correctly"""
    available_districts = list(Location.objects.values_list('district', flat=True).distinct())
    return JsonResponse({
        'message': 'The get-areas view is working correctly!',
        'available_districts': available_districts
    })


def property_list(request):
    properties = Property.objects.all()
    return render(request, 'properties/property_list.html', {'properties': properties})

def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    return render(request, 'properties/property_detail.html', {'property': property})


#create enqurey


@login_required
def create_inquiry(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id)
    
    # Check that users don't inquire about their own property
    if property_obj.user == request.user:
        messages.error(request, "You cannot inquire about your own property.")
        return redirect('property_detail', pk=property_id)
    
    if request.method == 'POST':
        message = request.POST.get('message')
        
        # Check if an active inquiry already exists
        existing_inquiry = PropertyInquiry.objects.filter(
            property=property_obj,
            sender=request.user,
            receiver=property_obj.user,
            is_active=True
        ).first()
        
        if existing_inquiry:
            # Add a new message to existing inquiry
            ChatMessage.objects.create(
                inquiry=existing_inquiry,
                sender=request.user,
                content=message
            )
            return redirect('chat_detail', inquiry_id=existing_inquiry.id)
        else:
            # Create new inquiry
            inquiry = PropertyInquiry.objects.create(
                property=property_obj,
                sender=request.user,
                receiver=property_obj.user,
                message=message
            )
            
            # Create initial chat message
            ChatMessage.objects.create(
                inquiry=inquiry,
                sender=request.user,
                content=message
            )
            
            messages.success(request, "Your inquiry has been sent to the property owner.")
            return redirect('chat_detail', inquiry_id=inquiry.id)
    
    return redirect('property_detail', pk=property_id)

@login_required
def chat_detail(request, inquiry_id):
    inquiry = get_object_or_404(PropertyInquiry, id=inquiry_id)
    
    # Security check - only sender and receiver can access the chat
    if request.user != inquiry.sender and request.user != inquiry.receiver:
        messages.error(request, "You don't have permission to access this conversation.")
        return redirect('property_list')
    
    # Get all messages for this inquiry
    chat_messages = ChatMessage.objects.filter(inquiry=inquiry).order_by('timestamp')
    
    return render(request, 'properties/chat_detail.html', {
        'inquiry': inquiry,
        'chat_messages': chat_messages,
        'property': inquiry.property
    })

@login_required
def send_message(request, inquiry_id):
    inquiry = get_object_or_404(PropertyInquiry, id=inquiry_id)
    
    # Security check - only sender and receiver can send messages
    if request.user != inquiry.sender and request.user != inquiry.receiver:
        messages.error(request, "You don't have permission to send messages in this conversation.")
        return redirect('property_list')
    
    if request.method == 'POST':
        content = request.POST.get('message')
        if content:
            ChatMessage.objects.create(
                inquiry=inquiry,
                sender=request.user,
                content=content
            )
    
    return redirect('chat_detail', inquiry_id=inquiry_id)

@login_required
def my_inquiries(request):
    # Get inquiries where the user is either sender or receiver
    sent_inquiries = PropertyInquiry.objects.filter(sender=request.user).order_by('-created_at')
    received_inquiries = PropertyInquiry.objects.filter(receiver=request.user).order_by('-created_at')
    
    return render(request, 'properties/my_inquiries.html', {
        'sent_inquiries': sent_inquiries,
        'received_inquiries': received_inquiries
    })