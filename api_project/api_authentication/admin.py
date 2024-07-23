from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import UserCreationForm, UserChangeForm


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    
    list_display = ('username', 'first_name', 'last_name', 'patronymic', 
                    'email', 'phone_number', 'role', 'date_joined')
    list_filter = ('role', 'date_joined')
    search_fields = ('^username', '^last_name', '^first_name', 
                     '^email', '^phone_number')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'patronymic', 'email', 'phone_number')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'patronymic', 
                       'email', 'phone_number', 'role', 'password1', 'password2')}
        ),
    )
