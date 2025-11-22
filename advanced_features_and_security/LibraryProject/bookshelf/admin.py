from django.contrib import admin
from .models import Book
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.utils.translation import gettext_lazy as _
# Register your models here.


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('author', 'publication_year')
    search_fields = ('title', 'author')

admin.site.register(Book, BookAdmin)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Add the extra fields to admin forms and list display
    fieldsets = UserAdmin.fieldsets + (
        (_('Extra info'), {'fields': ('date_of_birth', 'profile_photo')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (_('Extra info'), {'fields': ('date_of_birth', 'profile_photo')}),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_of_birth')