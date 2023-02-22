from django.contrib import admin

from applications.post.models import Post, PostImage


class ImageAdmin(admin.TabularInline):
    model = PostImage
    fields = ('image',)
    max_num = 4

class PostAdmin(admin.ModelAdmin):
    inlines = (ImageAdmin,)

    list_display = ('title','owner')

    def post_count(self, obj):
        return obj.likes.filter(is_like=True).count()



admin.site.register(Post, PostAdmin)
admin.site.register(PostImage)