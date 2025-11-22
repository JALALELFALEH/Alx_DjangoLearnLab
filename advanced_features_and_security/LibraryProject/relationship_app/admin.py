from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import CustomUser, Author, Book, Library, Librarian, UserProfile 

# --- Custom Admin Class Definition ---
class CustomUserAdmin(UserAdmin):
    # This controls which fields appear in the change/edit form (when you click on a user)
    fieldsets = (
        (None, {'fields': ('email', 'password')}), # Use email instead of username
        ('Personal info', {'fields': ('first_name', 'last_name', 'date_of_birth', 'profile_photo')}), # <-- Added your custom fields
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # This controls which fields appear in the user list view
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'date_of_birth') # <-- Added date_of_birth

    # Override the search fields and filters if necessary (Inherited from UserAdmin)
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

# Register the custom model using the custom admin class
admin.site.register(CustomUser, CustomUserAdmin) 

# Register other models
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Library)
admin.site.register(Librarian)
admin.site.register(UserProfile)