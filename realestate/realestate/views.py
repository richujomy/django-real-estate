from django.shortcuts import render
from properties.models import Property,Location  #
from django.db.models import Min, Max
from django.db.models import Q
from django.core.paginator import Paginator

def home(request):
    properties = Property.objects.all()
    featured_properties = Property.objects.all()[:4]
    
    # Get unique property types for dropdown
    property_types = Property._meta.get_field('property_type').choices
    
    districts = Location.objects.values_list('district', flat=True).distinct().order_by('district')
    
    
    # Get min and max prices from database for price range
    price_stats = Property.objects.aggregate(min_price=Min('price'), max_price=Max('price'))
    min_price = price_stats['min_price'] or 0
    max_price = price_stats['max_price'] or 1000000
    
    # Create price ranges dynamically
    step = (max_price - min_price) / 5  # Divide into 5 ranges
    price_ranges = []
    
    for i in range(5):
        lower = min_price + (i * step)
        upper = min_price + ((i + 1) * step)
        if i == 0:
            label = f"Under ₹{int(upper):,}"
        elif i == 4:
            label = f"Above ₹{int(lower):,}"
        else:
            label = f"₹{int(lower):,} - ₹{int(upper):,}"
        price_ranges.append((f"{int(lower)}-{int(upper)}", label))
    
    context = {
        'properties': properties, 
        'featured_properties': featured_properties,
        'property_types': property_types,
        'districts': districts,
        'price_ranges': price_ranges,
    }
    
    return render(request, 'home.html', context)


def filter_properties(request):
    """
    View for filtering properties based on user-selected criteria
    """
    properties = Property.objects.all().order_by('-created_at')
    
    # Apply filters if they exist in the request
    if request.method == 'GET':
        # Basic filters
        property_type = request.GET.get('property_type')
        property_purpose = request.GET.get('property_purpose')  # For Sale/Rent/Lease
        district = request.GET.get('district')
        bedrooms = request.GET.get('bedrooms')
        bathrooms = request.GET.get('bathrooms')
        
        # Price range filter
        price_range = request.GET.get('price_range')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        
        # Apply filters conditionally
        if property_type and property_type != 'all':
            properties = properties.filter(property_type=property_type)
            
        if property_purpose and property_purpose != 'all':
            properties = properties.filter(type=property_purpose)
            
        if district and district != 'all':
            properties = properties.filter(location__district=district)
            
        if bedrooms and bedrooms.isdigit():
            bedrooms = int(bedrooms)
            if bedrooms == 4:  # If "4+" is selected
                properties = properties.filter(bedrooms__gte=4)
            else:
                properties = properties.filter(bedrooms=bedrooms)
                
        if bathrooms and bathrooms.isdigit():
            bathrooms = int(bathrooms)
            if bathrooms == 4:  # If "4+" is selected
                properties = properties.filter(bathrooms__gte=4)
            else:
                properties = properties.filter(bathrooms=bathrooms)
        
        # Handle price filter
        if price_range and '-' in price_range:
            low, high = map(int, price_range.split('-'))
            properties = properties.filter(price__gte=low, price__lte=high)
        elif min_price and max_price:
            try:
                min_price = float(min_price)
                max_price = float(max_price)
                properties = properties.filter(price__gte=min_price, price__lte=max_price)
            except ValueError:
                pass  # Invalid price values, skip this filter
        
        # Handle keyword search if provided
        keyword = request.GET.get('keyword')
        if keyword:
            properties = properties.filter(
                Q(title__icontains=keyword) | 
                Q(description__icontains=keyword) |
                Q(location__area__icontains=keyword) |
                Q(location__district__icontains=keyword)
            )
    
    # Pagination
    paginator = Paginator(properties, 9)  # Show 9 properties per page
    page = request.GET.get('page')
    properties = paginator.get_page(page)
    
    # Get filter options for the form
    property_types = Property._meta.get_field('property_type').choices
    property_purposes = Property._meta.get_field('type').choices
    districts = Location.objects.values_list('district', flat=True).distinct().order_by('district')
    
    # Get min and max prices for price slider
    price_stats = Property.objects.aggregate(min_price=Min('price'), max_price=Max('price'))
    min_price = price_stats['min_price'] or 0
    max_price = price_stats['max_price'] or 1000000
    
    # Create price ranges dynamically
    step = (max_price - min_price) / 5
    price_ranges = []
    for i in range(5):
        lower = min_price + (i * step)
        upper = min_price + ((i + 1) * step)
        if i == 0:
            label = f"Under ₹{int(upper):,}"
        elif i == 4:
            label = f"Above ₹{int(lower):,}"
        else:
            label = f"₹{int(lower):,} - ₹{int(upper):,}"
        price_ranges.append((f"{int(lower)}-{int(upper)}", label))
    
    context = {
        'properties': properties,
        'property_types': property_types,
        'property_purposes': property_purposes,
        'districts': districts,
        'price_ranges': price_ranges,
        'filter_applied': request.GET.get('property_type') or request.GET.get('district') or request.GET.get('price_range'),
        'total_results': paginator.count,
        'min_price': int(min_price),
        'max_price': int(max_price),
        # Keep the selected filters for form persistence
        'selected_type': request.GET.get('property_type', ''),
        'selected_purpose': request.GET.get('property_purpose', ''),
        'selected_district': request.GET.get('district', ''),
        'selected_bedrooms': request.GET.get('bedrooms', ''),
        'selected_bathrooms': request.GET.get('bathrooms', ''),
        'selected_price_range': request.GET.get('price_range', ''),
        'keyword': request.GET.get('keyword', ''),
    }
    
    return render(request, 'property_filter.html', context)


def district_properties(request, district):
    """
    View to filter properties by a specific district
    """
    # Ensure the district is properly capitalized
    district = district.capitalize()
    
    # Filter properties for the specific district
    all_properties = Property.objects.filter(location__district=district).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(all_properties, 9)  # Show 9 properties per page
    page = request.GET.get('page')
    properties = paginator.get_page(page)
    
    # Get price stats from the original queryset, not the paginated one
    price_stats = all_properties.aggregate(min_price=Min('price'), max_price=Max('price'))
    min_price = price_stats['min_price'] or 0
    max_price = price_stats['max_price'] or 1000000
    
    # Get filter options for the form
    property_types = Property._meta.get_field('property_type').choices
    property_purposes = Property._meta.get_field('type').choices
    districts = Location.objects.values_list('district', flat=True).distinct().order_by('district')
    
    # Create price ranges dynamically
    step = (max_price - min_price) / 5
    price_ranges = []
    for i in range(5):
        lower = min_price + (i * step)
        upper = min_price + ((i + 1) * step)
        if i == 0:
            label = f"Under ₹{int(upper):,}"
        elif i == 4:
            label = f"Above ₹{int(lower):,}"
        else:
            label = f"₹{int(lower):,} - ₹{int(upper):,}"
        price_ranges.append((f"{int(lower)}-{int(upper)}", label))
    
    context = {
        'properties': properties,
        'district': district,
        'property_types': property_types,
        'property_purposes': property_purposes,
        'districts': districts,
        'price_ranges': price_ranges,
        'total_results': paginator.count,
        'min_price': int(min_price),
        'max_price': int(max_price),
    }
    
    return render(request, 'property_filter.html', context)

  