# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# 用户模型.
class User(AbstractUser):

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        
    def __str__(self):
        return self.username
    
    
class proUser(models.Model):
    name = models.CharField(max_length=30, verbose_name='用户名称')
    pasw = models.CharField(max_length=30, verbose_name='密码')
    class Meta:
        verbose_name = '普通用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
    
# tag（标签）
class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name='标签名称')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
    
# 分类
class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name='分类名称')
    index = models.IntegerField(default=999,verbose_name='分类的排序')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __str__(self):
        return self.name
    
# 文章模型
class Article(models.Model):
    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.CharField(max_length=50, verbose_name='文章描述')
    content = models.TextField(verbose_name='文章内容')
    click_count = models.IntegerField(default=0, verbose_name='点击次数')
    is_recommend = models.BooleanField(default=False, verbose_name='是否推荐')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    user = models.ForeignKey(User, verbose_name='用户',on_delete=models.CASCADE)
    category = models.ForeignKey(Category, blank=True, null=True, verbose_name='分类',on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, verbose_name='标签')

    # objects = ArticleManager()

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']

    def __str__(self):
        return self.title
    
# 评论模型
class Comment(models.Model):
    content = models.TextField(verbose_name='评论内容')
    username = models.CharField(max_length=30, blank=True, null=True, verbose_name='用户名')
    email = models.EmailField(max_length=50, blank=True, null=True, verbose_name='邮箱地址')
    url = models.URLField(max_length=100, blank=True, null=True, verbose_name='个人网页地址')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    user = models.ForeignKey(User, blank=True, null=True, verbose_name='用户',on_delete=models.CASCADE)
    article = models.ForeignKey(Article, blank=True, null=True, verbose_name='文章',on_delete=models.CASCADE)
    pid = models.ForeignKey('self', blank=True, null=True, verbose_name='父级评论',on_delete=models.CASCADE)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)
    
# 教程
class Course(models.Model):
    title = models.CharField(max_length=50, verbose_name='教程标题')
    click_count = models.IntegerField(default=0, verbose_name='点击次数')
    desc = models.CharField(max_length=100, blank=True,verbose_name='描述')
        
    class Meta:
        verbose_name = '教程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
    
# 教程目录内容
class CourseList(models.Model):
    catalog = models.CharField(max_length=50, verbose_name='目录标题')
    index = models.IntegerField(default=999,verbose_name='目录的排序')
    course_title = models.ForeignKey(Course, blank=True, null=True, verbose_name='教程标题',on_delete=models.CASCADE)
    content = models.TextField(verbose_name='目录内容')
    
    class Meta:
        verbose_name = '教程目录'
        verbose_name_plural = verbose_name
        ordering = ['index']
        

    def __str__(self):
        return self.catalog
 
    
        
# 教程视频
class CourseVideo(models.Model):
    title = models.CharField(max_length=50, verbose_name='教程标题')
    click_count = models.IntegerField(default=0, verbose_name='点击次数')
    desc = models.CharField(max_length=100, verbose_name='描述')
        
    class Meta:
        verbose_name = '教程视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    
# 教程视频目录内容
class CourseVideoList(models.Model):
    catalog = models.CharField(max_length=50, verbose_name='目录标题')
    index = models.IntegerField(default=999,verbose_name='目录的排序')
    courseVideo_title = models.ForeignKey(CourseVideo, blank=True, null=True, verbose_name='教程视频',on_delete=models.CASCADE)
    videoUrl = models.CharField(max_length=100, verbose_name='视频url')
    
    class Meta:
        verbose_name = '教程视频目录内容'
        verbose_name_plural = verbose_name
        ordering = ['index']

    def __str__(self):
        return self.catalog
    


