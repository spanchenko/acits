from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
#from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import *


class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 
        'phone', 'birthday', 'age', 'language', 'status', 'created_at', 'updated_at', 'is_staff', 'is_active',)
    list_filter = ('username', 'email', 'first_name', 'last_name', 
        'phone', 'birthday', 'age', 'language', 'status', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'first_name', 'last_name', 'status', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)


admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Flat)
admin.site.register(FlatAttribute)
admin.site.register(FlatAttributesValue)
admin.site.register(Build)
admin.site.register(FlatRoom)
admin.site.register(RentOrder)