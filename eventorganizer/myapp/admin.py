from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Department, Venue

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active','department')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'role')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role','department')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Department)
admin.site.register(Venue)
from .models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'organizer','date' ,'status')
    list_filter = ('status',)
    actions = ['approve_event', 'disapprove_event']

    def approve_event(self, request, queryset):
        queryset.update(status='approved')
    approve_event.short_description = "Approve selected events"

    def disapprove_event(self, request, queryset):
        queryset.update(status='disapproved')
    disapprove_event.short_description = "Disapprove selected events"

admin.site.register(Event, EventAdmin)