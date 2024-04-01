from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
def delete_selected_users(modeladmin, request, queryset):
    for user in queryset:
        user.delete()

delete_selected_users.short_description = "Delete selected users"  # Sets the display name for the action

# Register the custom action for the User model
admin.site.add_action(delete_selected_users)

# Register the User model with the admin interface
admin.site.unregister(User)  # Unregister the User model first if it's already registered by default
admin.site.register(User)