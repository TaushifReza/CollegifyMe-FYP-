from django.contrib import admin

from post.models import Post, PostComment, PostLike, PostMedia


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "post_content", "post_date")
    ordering = ("-post_date",)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


@admin.register(PostMedia)
class PostMediaAdmin(admin.ModelAdmin):
    list_display = ("post",)
    ordering = ("-post",)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "like_date_time")
    ordering = ("-like_date_time",)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "comment_date_time")
    ordering = ("-comment_date_time",)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
