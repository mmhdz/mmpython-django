from django.contrib import admin
from .models import *



class CommentInline(admin.TabularInline):
    model = Comment
    extra = 3


class UserInline(admin.StackedInline):
    model = User
    extra = 4


class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Main info", {"fields": ["username", "password"]}),
        ("Registration date", {"fields": ["created_at"]})
    ]

    inlines = [CommentInline]
    list_filter = ["created_at"]
    search_fields = ["username"]


admin.site.register(User, UserAdmin)
admin.site.register(BlogPost)


class CommentAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Text", {"fields": ["text"]}),
        ("Post", {"fields": ["post"]}),
        ("User", {"fields": ["user"]})
    ]


admin.site.register(Comment, CommentAdmin)
admin.site.register(Hashtag)


