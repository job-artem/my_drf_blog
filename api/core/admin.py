from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'tag_list')
    pass

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())


admin.site.register(Post, PostAdmin)
