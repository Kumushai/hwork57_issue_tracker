from django.contrib import admin


from webapp.models import Todo, Status, Type

admin.site.register(Status)
admin.site.register(Type)


class TodoAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'status', 'types']
    list_display_links = ['id', 'content']
    list_filter = ['created_at']
    search_fields = ['content', 'status', 'types']
    fields = ['content', 'status', 'details', 'types']


admin.site.register(Todo, TodoAdmin)

