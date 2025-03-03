# properties/admin.py
from django.contrib import admin
from .models import Property, Location, PropertyImage

class PropertyImageInline(admin.TabularInline):  # Allows image uploads inside Property admin
    model = PropertyImage
    extra = 1  # Number of empty image slots

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'property_type', 'type', 'price', 'status', 'created_at')
    list_filter = ('property_type', 'type', 'status', 'location')
    search_fields = ('title', 'description', 'location__district')
    inlines = [PropertyImageInline]  # Attach images within the Property form
    prepopulated_fields = {'title': ('title',)}  # Auto-fill fields if required
    readonly_fields = ('created_at', 'updated_at')  # Make fields read-only

class LocationAdmin(admin.ModelAdmin):
    list_display = ('state', 'district', 'area')
    search_fields = ('state', 'district', 'area')

admin.site.register(Property, PropertyAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(PropertyImage)
