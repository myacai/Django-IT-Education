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
    
class FirstAppWeixininfo(models.Model):
    title = models.CharField(max_length=100)
    date = models.CharField(max_length=50)
    from_name = models.CharField(max_length=50)
    read_num = models.CharField(max_length=20, blank=True, null=True)
    like_num = models.CharField(max_length=20, blank=True, null=True)
    articleurl = models.CharField(db_column='articleUrl', max_length=350, blank=True, null=True)  # Field name made lowercase.
    shijianchuo = models.CharField(max_length=50)
    digest = models.CharField(max_length=300, blank=True, null=True)
    updete_time = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'first_app_weixininfo'

class Jingdong(models.Model):
    productid = models.CharField(db_column='productId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    productname = models.CharField(db_column='productName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    shopname = models.CharField(db_column='shopName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    commentnums = models.CharField(db_column='commentNums', max_length=100, blank=True, null=True)  # Field name made lowercase.
    prices = models.CharField(max_length=20, blank=True, null=True)
    links = models.CharField(max_length=255, blank=True, null=True)
    imageUrl = models.CharField(max_length=255, blank=True, null=True)	

    class Meta:
        verbose_name = '京东信息'
        verbose_name_plural = verbose_name
        ordering = ['productname']

    def __str__(self):
        return self.productname

class Ouwang(models.Model):
    title = models.CharField(db_column='title', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ctt =  models.CharField(db_column='content', max_length=10000,  verbose_name='文章内容')   # Field name made lowercase.
    date = models.CharField(db_column='date', max_length=100, blank=True, null=True)  # Field name made lowercase.
    visitCount = models.CharField(db_column='visitCount', max_length=100, blank=True, null=True)  # Field name made lowercase.
    LinkUrl = models.CharField(db_column='LinkUrl', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        verbose_name = '瓯网信息'
        verbose_name_plural = verbose_name
        ordering = ['title']

    def __str__(self):
        return self.title
    
class DoupanTop(models.Model):
    no = models.CharField(db_column='no', max_length=100, blank=True, null=True)
    movie_name = models.CharField(db_column='movie_name', max_length=100, blank=True, null=True)
    director = models.CharField(db_column='director', max_length=1000, blank=True, null=True)
    writer = models.CharField(db_column='writer', max_length=100, blank=True, null=True)
    actor = models.CharField(db_column='actor', max_length=1000, blank=True, null=True)
    typee = models.CharField(db_column='typee', max_length=100, blank=True, null=True)
    region = models.CharField(db_column='region', max_length=1000, blank=True, null=True)
    language = models.CharField(db_column='language', max_length=100, blank=True, null=True)
    date = models.CharField(db_column='date', max_length=100, blank=True, null=True)
    length = models.CharField(db_column='length', max_length=100, blank=True, null=True)
    another_name = models.CharField(db_column='another_name', max_length=100, blank=True, null=True)
    introduction = models.CharField(db_column='introduction', max_length=100, blank=True, null=True)
    grade = models.CharField(db_column='grade', max_length=100, blank=True, null=True)
    comment_times = models.CharField(db_column='comment_times', max_length=100, blank=True, null=True)
    
    class Meta:
        verbose_name = '豆瓣'
        verbose_name_plural = verbose_name
        ordering = ['movie_name']

    def __str__(self):
        return self.movie_name