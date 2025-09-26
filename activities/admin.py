from django.contrib import admin
from .models import User, Category, Activity
from django.contrib.auth.admin import UserAdmin

class AdminCustom(UserAdmin):
    list_display = ('bio', 'avatar')
    list_filter = ('username',)
    search_fields = ('username', 'bio')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'location_city', 'start_time', 'end_time', 'proposer', 'category')
    list_filter = ('category', 'location_city', 'start_time')
    search_fields = ('title', 'description', 'location_city', 'proposer__username')

admin.site.register(User, AdminCustom)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Activity, ActivityAdmin)
