from django.contrib import admin
from .models import *

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):

    search_fields = ['title']
    
    list_display = ('title', 'desc', 'click_count',)
    list_display_links = ('title', 'desc', )
    # list_editable = ('click_count',)
    
    list_filter = ['title']
    
    list_max_show_all = 200
    list_per_page = 10

    fieldsets = (
        (None, {
            'fields': ('title', 'desc', 'content', 'user', 'category', 'tag', )
        }),
        ('高级设置', {
            'classes': ('collapse',),
            'fields': ('click_count', 'is_recommend',)
        }),
    )
    
    class Media:
        js = (
            '/static/js/kindeditor-4.1.10/kindeditor-min.js',
            '/static/js/kindeditor-4.1.10/lang/zh_CN.js',
            '/static/js/kindeditor-4.1.10/config.js',
        )
        
class CourseListAdmin(admin.ModelAdmin):

    search_fields = ['catalog']
    
    list_display = ('catalog', 'index', 'course_title',)
    #list_display_links = ('title', 'desc', )
    # list_editable = ('click_count',)
    
    list_filter = ['catalog']
    
    list_max_show_all = 200
    #list_per_page = 3


    
    class Media:
        js = (
            '/static/js/kindeditor-4.1.10/kindeditor-min.js',
            '/static/js/kindeditor-4.1.10/lang/zh_CN.js',
            '/static/js/kindeditor-4.1.10/config.js',
        )
        
    
class CourseVideoListAdmin(admin.ModelAdmin):

    search_fields = ['courseVideo_title']
    
    list_display = ('catalog', 'index', 'courseVideo_title',)
    #list_display_links = ('title', 'desc', )
    # list_editable = ('click_count',)
    
    list_filter = ['courseVideo_title']
    
    list_max_show_all = 200
    #list_per_page = 3


   

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(CourseList, CourseListAdmin)
admin.site.register(Course)
admin.site.register(CourseVideoList, CourseVideoListAdmin)
admin.site.register(CourseVideo)
admin.site.register(proUser)