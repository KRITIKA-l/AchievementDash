from django.contrib import admin
from .models import UserProfile,Opportunity,Skill,OpportunityApplication
# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    list_filter = ('skills',)
    
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'start_date', 'end_date', 'created_at', 'posted_by')
    search_fields = ('title', 'description', 'location')
    list_filter = ('start_date', 'end_date', 'skills_required')
    filter_horizontal = ('skills_required',)

@admin.register(OpportunityApplication)
class OpportunityApplicationAdmin(admin.ModelAdmin):
    list_display = ('opportunity', 'student', 'status', 'applied_at')
    search_fields = ('opportunity__title', 'student__username')
    list_filter = ('status',)