from django.contrib import admin


from webapp.models import Todo, Status, Type, Project

admin.site.register(Status)
admin.site.register(Type)
admin.site.register(Project)


class TodoAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'status', 'display_types', 'project']
    list_display_links = ['id', 'content']
    list_filter = ['created_at']
    search_fields = ['content', 'status', 'types']
    fields = ['content', 'status', 'details', 'types', 'project']

    def display_types(self, obj):
        return ", ".join([todo_type.name for todo_type in obj.types.all()])

    display_types.short_description = 'Types'


admin.site.register(Todo, TodoAdmin)

