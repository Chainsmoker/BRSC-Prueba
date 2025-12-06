from django.contrib import admin
from .models import DailyActivity # , ActivityCategory


# @admin.register(ActivityCategory)
# class ActivityCategoryAdmin(admin.ModelAdmin):
#     list_display = ('name',)


@admin.register(DailyActivity)
class DailyActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'title', 'score')
    list_filter = ('date', 'score')
    search_fields = ('title', 'description', 'user__username', 'user__first_name')