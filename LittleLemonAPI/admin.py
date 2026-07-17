from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# 1. Unregister the default User configuration
admin.site.unregister(User)

# 2. Create a custom configuration class
class CustomUserAdmin(UserAdmin):
    # Add a custom method to display the groups as a comma-separated string
    list_display = ('username', 'display_groups', 'email', 'first_name', 'last_name', 'is_staff')

    def display_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    
    # Give the column a clean title in the admin interface
    display_groups.short_description = 'Groups'

# 3. Register the User model with our custom configuration
admin.site.register(User, CustomUserAdmin)