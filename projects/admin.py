# projects/admin.py
from django.contrib import admin
from .models import Project, Education, Certificate, Contact, Resume

admin.site.register(Project)
admin.site.register(Education)
admin.site.register(Certificate)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email','message_snippet', 'sent_at') # Shows columns in the list
    readonly_fields = ('name', 'email', 'message', 'sent_at') # Prevents you from editing user messages accidentally
    search_fields = ('name', 'email') # Adds a search bar
    ordering = ('-sent_at',) # Newest messages first

    # This function creates the preview column
    def message_snippet(self, obj):
        if len(obj.message) > 50:
            return obj.message[:50] + "..."
        return obj.message

    message_snippet.short_description = 'Message'

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'uploaded_at')