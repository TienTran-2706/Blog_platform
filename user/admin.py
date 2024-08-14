from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    # Define the fields to be displayed in the list view
    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser', 'is_email_confirmed')
    # Define the fields to be used for search
    search_fields = ('username', 'email')
    # Define the fields to be used for filtering
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'is_email_confirmed')
    # Define the fields to be editable inline
    readonly_fields = ('email_confirmation_token', 'email_confirmation_sent_at')

    # Define which fields should be displayed in the form view
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Profile', {
            'fields': ('profile_picture', 'bio')
        }),
    )

    # Define which fields should be editable in the admin interface
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', 'profile_picture', 'bio')
        }),
    )

    # Override the save model method to handle password hashing
    def save_model(self, request, obj, form, change):
        if not change:  # New object
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

admin.site.register(User, UserAdmin)
