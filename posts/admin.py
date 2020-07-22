from django.contrib import admin

from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_name', 'course',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', )


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
        