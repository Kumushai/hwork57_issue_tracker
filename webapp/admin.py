from django.contrib import admin


from webapp.models import Todo, Status, Type

admin.site.register(Status)
admin.site.register(Type)


class TodoAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'status', 'type']
    list_display_links = ['id', 'content']
    list_filter = ['created_at']
    search_fields = ['content', 'status', 'type']
    fields = ['content', 'status', 'details', 'type']


admin.site.register(Todo, TodoAdmin)

