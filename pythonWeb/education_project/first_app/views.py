# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.conf import settings
from .models import Article, Tag, CourseVideo, CourseVideoList, Course, CourseList,User,Comment,proUser,Category

from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger

# Create your views here.


#logger = logging.getLogger('first_app.views')

def global_setting(request):
    # 站点基本信息
    SITE_URL = settings.SITE_URL
    SITE_NAME = settings.SITE_NAME
    SITE_DESC = settings.SITE_DESC
    # 文章归档数据
    #archive_list = Article.objects.distinct_date()
    #BASE_DIR = settings.BASE_DIR
    return locals()


def index(request):
    courseVideo_title_id1 = CourseVideo.objects.get(title='python基础')
    title_id1 = courseVideo_title_id1.id
    python_Video_list = CourseVideoList.objects.filter(courseVideo_title_id=title_id1)[0:5]

    courseVideo_title_id2 = CourseVideo.objects.get(title='爬虫')
    title_id2 = courseVideo_title_id2.id
    crawl_Video_list = CourseVideoList.objects.filter(courseVideo_title_id=title_id2)
    
    courseVideo_title_id3 = CourseVideo.objects.get(title='Django')
    title_id3 = courseVideo_title_id3.id
    Django_Video_list = CourseVideoList.objects.filter(courseVideo_title_id=title_id3)
    
    courseVideo_title_id4 = CourseVideo.objects.get(title='Tornado')
    title_id4 = courseVideo_title_id4.id
    Tornado_Video_list = CourseVideoList.objects.filter(courseVideo_title_id=title_id4)
    
    courseVideo_title_id5 = CourseVideo.objects.get(title='C#')
    title_id5 = courseVideo_title_id5.id
    C_Video_list = CourseVideoList.objects.filter(courseVideo_title_id=title_id5)[0:5]
    
    
    courseVideo_title_id6 = CourseVideo.objects.get(title='Mybatis')
    title_id6 = courseVideo_title_id6.id
    M_Video_list = CourseVideoList.objects.filter(courseVideo_title_id=title_id6)[0:5]
    username = request.session.get('username' , 'admin')
    print('index'+ username)
    return render(request, 'index.html', locals())


def remen(request):
    try:
        strCom = '站长推荐'
        tagName = request.GET.get('tagName', None)
        if tagName:
            tagName = str(tagName)
            tagg = Tag.objects.get(name=tagName)

            print(tagg)
            article_list = Article.objects.filter(tag=tagg)
            tag_list = Tag.objects.all()
            print(tagName)
            
        else:
            # 最新文章数据
            article_list = Article.objects.all()
            tag_list = Tag.objects.all()
            #print(article_list)
        article_list_recommend = Article.objects.filter(is_recommend=1)[0:6]
        article_list = getPage(request, article_list)
    except Exception as e:
        #logger.error(e) 
        print(e)
    return render(request, 'remen.html', locals())

    
def userLead(request):
    try:
        try:
            username = request.GET.get('username', '')
            tagName = request.GET.get('tagName', None)
        except Exception as ee:
            print(ee)
        print(username)
        user_list = User.objects.all().order_by('id')
        tag_list = Tag.objects.all()
        strCom = '用户排行榜'
        if username == '':
            username = 'admin'
            article_list = Article.objects.all()
        else:
            userr = User.objects.filter(username=username)[0]
            article_list = Article.objects.filter(user=userr)
            for i in article_list:
                print(i.title)
        if tagName:
            tagName = str(tagName)
            tagg = Tag.objects.get(name=tagName)

            print(tagg)
            article_list = Article.objects.filter(tag=tagg)
            tag_list = Tag.objects.all()
            print(tagName)
        article_list = getPage(request, article_list)
    except Exception as e:
        #logger.error(e) 
        print(e)
    return render(request, 'userLead.html', locals())

# 分页代码
def getPage(request, article_list):
    paginator = Paginator(article_list, 6)
    try:
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        article_list = paginator.page(1)
    return article_list

# 文章详情
def article(request):
    try:
        id = request.GET.get('id', None)
        #commentName = request.POST.get("commentName","")
        commentName = request.session.get('username' , 'admin')
        
        print('评论名'+commentName)
        commentId = request.POST.get('commentId','')
        print(commentId)
        commentTextarea = request.POST.get('commentTextarea', '')
        print(commentTextarea)
        print(request.path)
        tagName = request.GET.get('tagName', None)
        tag_list = Tag.objects.all()
        try:
            # 获取文章信息
            article = Article.objects.get(pk=id)
            article.click_count += 1
            article.save()
            commentList = Comment.objects.filter(article=article)
            if commentName!='' and commentTextarea!='':
                comment = Comment.objects.create(username=commentName,content=commentTextarea,article=article)
                comment.save()
                
        except Article.DoesNotExist:
            return render(request, 'failure.html', {'reason': '没有找到对应的文章'})
        
        
    except Exception as e:
        print(e)
    return render(request, 'article.html', locals())


def course(request):
    try:
        id = request.GET.get('id', None)
        contentId = request.GET.get('v', None) 
        print('id是'+ id)
        print('v是'+ contentId)
        try:
            course = Course.objects.get(pk=id)
            
            
            course.click_count = course.click_count  + 1
 
            course.save()
            courseList = CourseList.objects.filter(course_title=id)
            
            content = CourseList.objects.filter(course_title=id).filter(index=contentId)
            contentCatalog = content[0].catalog

            contentContent = content[0].content
            courseID = id
        except Exception:
            return render(request, 'failure.html', {'reason': '没有找到对应的教程list'})
    except Exception as e:
        print(e)
    
    return render(request, 'course.html', locals())

def courseVideo(request):
    try:
        idd = request.GET.get('id', None) 
        
        vvideo = request.GET.get('v', None) 
        try:
            thisVideo = CourseVideoList.objects.filter(courseVideo_title=idd).filter(index=vvideo)
            courseVideoTitle = CourseVideo.objects.get(pk=idd)
            courseVideoList = CourseVideoList.objects.filter(courseVideo_title=idd)
            print(courseVideoTitle.title)
            print(thisVideo[0].videoUrl)
            video = str(thisVideo[0].videoUrl)
        except CourseVideoList.DoesNotExist:
            return render(request, 'failure.html', {'reason': '没有找到对应的视频'})
    except Exception as e:
        print(e)
    return render(request, 'courseVideo.html', locals())

def my(request):
    
    
    return render(request, 'my.html')

def author(request):
    
    return render(request, 'author.html')


def comment(request):
    
    print('comment')
    
def login(request):
    try:

        name = request.POST.get("username","")
        print('名'+name)
 
        pasw = request.POST.get('password', '')
        print(pasw)

        try:
            user = proUser.objects.filter(name=name,pasw=pasw)
            if user:
                print('登陆成功')
                request.session['username'] = name
                courseVideo_title_id1 = CourseVideo.objects.get(title='python基础')
                title_id1 = courseVideo_title_id1.id
                python_Video_list = CourseVideoList.objects.filter(courseVideo_title_id=title_id1)[0:5]
        
                courseVideo_title_id2 = CourseVideo.objects.get(title='爬虫')
                title_id2 = courseVideo_title_id2.id
                crawl_Video_list = CourseVideoList.objects.filter(courseVideo_title_id=title_id2)
            
                courseVideo_title_id3 = CourseVideo.objects.get(title='Django')
                title_id3 = courseVideo_title_id3.id
                Django_Video_list = CourseVideoList.objects.filter(courseVideo_title_id=title_id3)
                    
                courseVideo_title_id4 = CourseVideo.objects.get(title='Tornado')
                title_id4 = courseVideo_title_id4.id
                Tornado_Video_list = CourseVideoList.objects.filter(courseVideo_title_id=title_id4)
                
                courseVideo_title_id5 = CourseVideo.objects.get(title='C#')
                title_id5 = courseVideo_title_id5.id
                C_Video_list = CourseVideoList.objects.filter(courseVideo_title_id=title_id5)[0:5]
                
                
                courseVideo_title_id6 = CourseVideo.objects.get(title='Mybatis')
                title_id6 = courseVideo_title_id6.id
                M_Video_list = CourseVideoList.objects.filter(courseVideo_title_id=title_id6)[0:5]
               
                username = request.session.get('username' , 'admin')
                print('index'+ username)
                return render(request, 'index.html', locals())
            else:
                print('falie')
        except Article.DoesNotExist:
            return render(request, 'failure.html', {'reason': '没有找到对应的文章'})
        
        
    except Exception as e:
        print(e)
    return render(request, 'login.html',locals())
    

def articleAdd(request):
    
    username = request.session.get('username' , 'admin')
    try:
        
        title = request.POST.get('title', '')
        desc = request.POST.get('desc', '')
        content = request.POST.get('content', '')
        strcategory = request.POST.get('category', '')
        strtag = request.POST.get('tag', '')
        if title != '':
            print(title)
            print(desc)
            print(content)
            print(strcategory)
            print(strtag)
            strcategory = int(strcategory)
            strtag = int(strtag)
            user = User.objects.filter(username=username)[0]
            category = Category.objects.filter(pk=strcategory)[0]
            tag = Tag.objects.filter(pk=strtag)[0]
            
            article = Article.objects.create(title=title, desc=desc, content=content,category=category,user=user)
            article.tag.set(tag)
            article.save()
            istrue = '添加成功'
        else:
            print('title为空')
            
    except Exception as e:
        print(e)
    return render(request, 'articleAdd.html',locals())