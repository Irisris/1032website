from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import *
from planet1032 import models
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator     #分页
from django.db import models
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse


# forms.py
class UserSignUpForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'gender', 'nature', 'avatar']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    username = forms.CharField(
        max_length=150, 
        help_text='仅限字母 数字 @/./+/-/_',  # 自定义帮助文本
        error_messages={
            'max_length': '',  # 自定义错误信息
        }
    )
    class Meta:
        model = User
        fields = ['username', 'password']

class UserSignInFrom(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class UploadArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'summary', 'type', 'images']

    article_choices = (
        ('E', '科普'),
        ('F', '小说'),
        ('G', '漫画/图像'),
        ('O', '其他'),
    )
    title = forms.CharField(max_length=200)
    body = forms.CharField(widget=forms.Textarea, required=False)
    summary = forms.CharField(widget=forms.Textarea, required=False)
    type = forms.ChoiceField(choices=article_choices)
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    
class ArticleForm(forms.ModelForm):
    new_images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    class Meta:
        model = Article
        fields = ['title', 'summary', 'body', 'type']

# chapter
class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['title', 'body', 'order', 'images']
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

# account update(username, pwd)
class UserEditForm(UserChangeForm):
    password = None  # remove the old password field
    new_password = forms.CharField(widget=forms.PasswordInput(), required=False)  # add a new password field

    username = forms.CharField(
        max_length=150, 
        help_text='必需  仅限字母 数字 @/./+/-/_',  # 自定义帮助文本
        error_messages={
            'max_length': '',  # 自定义错误信息
        }
    )

    class Meta:
        model = User
        fields = ['username', 'new_password']

    def save(self, commit=True):
        # if a new password has been provided, hash it
        if self.cleaned_data.get('new_password'):
            self.instance.set_password(self.cleaned_data.get('new_password'))
        return super().save(commit)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


# views.py
def home(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserSignUpForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            #user = user_form.save()
            #profile = profile_form.save(commit=False)
            
            #U_Form.save()
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password')
            # Create User object
            user = User.objects.create_user(username=username, password=password)
            user.save()
            
            # Create UserProfile object
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return HttpResponseRedirect('http://127.0.0.1:8000/signin')
    else:
        user_form = UserForm()
        profile_form = UserSignUpForm()
    return render(request,'signup.html',{'user_form': user_form, 'profile_form': profile_form})

def signin(request):
    if request.method == 'POST':
        U_Form = UserSignInFrom(request.POST)
        if U_Form.is_valid():
            username = U_Form.cleaned_data['username']
            password = U_Form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if not user.is_staff:
                    login(request, user)
                    return HttpResponseRedirect('http://127.0.0.1:8000/block_main')
                else:
                    return HttpResponseRedirect('http://127.0.0.1:8000/staff_main')
            else:
                return HttpResponse('Error Please check Name or Password')
    else:
        U_Form = UserSignInFrom()
    return render(request,'signin.html', {'Form': U_Form})

@login_required
def upload(request):
    if request.method == 'POST':
        A_Form = UploadArticleForm(request.POST, request.FILES)
        if A_Form.is_valid():
            articleupload = A_Form.save(commit=False)
            articleupload.user = request.user
            articleupload.pub_date = datetime.datetime.now()

            articleupload.save()

            for f in request.FILES.getlist('images'):
                Image.objects.create(image=f, article=articleupload)
            # return redirect('article_detail', id=article.id)
            return HttpResponseRedirect('http://127.0.0.1:8000/block_main')
    else:
        A_Form = UploadArticleForm()
    return render(request,'upload_articles.html',{'form':A_Form})

@login_required
def upload_chapter(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        form = ChapterForm(request.POST, request.FILES)
        if form.is_valid():
            new_chapter = form.save(commit=False)
            new_chapter.article = article
            new_chapter.save()

            for f in request.FILES.getlist('images'):
                Image.objects.create(image=f, chapter=new_chapter)
            # return redirect('article_detail', id=article.id)
            return HttpResponseRedirect(reverse('article_detail', args=[article.id]))
    else:
        form = ChapterForm()
    return render(request, 'upload_chapter.html', {'form': form, 'article': article})

'''
original - no chapter
@login_required
def upload(request):
    if request.method == 'POST':
        A_Form = UploadArticleForm(request.POST, request.FILES)
        if A_Form.is_valid():
            articleupload = A_Form.save(commit=False)
            articleupload.user = request.user
            articleupload.pub_date = datetime.datetime.now()

            articleupload.save()

            for f in request.FILES.getlist('images'):
                Image.objects.create(image=f, article=articleupload)
            # return redirect('article_detail', id=article.id)
            return HttpResponseRedirect('http://127.0.0.1:8000/block_main')
    else:
        A_Form = UploadArticleForm()
    return render(request,'upload_articles.html',{'form':A_Form})
'''

def signout(request):
    logout(request)
    return render(request,'signout.html')

def blockmain(request):
    currentuser=request.user
    if not currentuser.is_staff:
        return render(request, 'block_main.html')
    else:
        return render(request, 'staff_main.html')
    
@login_required
def homepage(request):
    return render(request, 'homepage.html')

# 科普文章列表 /edu_articles/
def article_list(request):
    articles_list = Article.objects.filter(type='E')
    paginator = Paginator(articles_list, 5)  # Show 5 articles per page
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    return render(request, 'edu_articles_list.html', {'articles': articles})

def article_detail(request, article_id, chapter_order=1):
    article = get_object_or_404(Article, pk=article_id)
    chapter = Chapter.objects.filter(article=article, order=chapter_order).first()
    comments = Comment.objects.filter(article=article)
    '''
    return render(request, 'article_detail.html', {
        'article': article, 
        'chapter': chapter, 
        'prev_order': prev_order, 
        'next_order': next_order,
        'comments': comments,
        'form': form,
    })
    '''
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
            # 处理Notification
            Notification.objects.create(user=article.user, comment=comment)
    else:
        form = CommentForm()
    if not chapter:
        messages.error(request, "This article has no chapters.")
        return render(request, 'article_detail_nochapter.html', {'article': article, 'comments': comments, 'form': form})
    prev_order = None
    next_order = None
    if chapter.order > 1:
        prev_order = chapter.order - 1
    if chapter.order < article.chapters.count():
        next_order = chapter.order + 1
    return render(request, 'article_detail.html', {'article': article, 'chapter': chapter, 'prev_order': prev_order, 'next_order': next_order})
    '''
    chapters = article.chapters.all()
    chapter_count = chapters.count()
    return render(request, 'article_detail.html', {'article': article, 'chapters': chapters})
    '''
# 翻页
def chapter_detail(request, article_id, order):
    chapter = get_object_or_404(Chapter, article_id=article_id, order=order)
    return render(request, 'chapter_detail.html', {'chapter': chapter})


def myuploads(request):
    articles_list = Article.objects.filter(user=request.user)
    paginator = Paginator(articles_list, 5)  # Show 5 articles per page
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    return render(request, 'myuploads.html', {'articles': articles})

@login_required
def editworks(request, article_id):
    # Get the existing article
    article = get_object_or_404(Article, pk=article_id)
    if request.method == 'POST':
        # Populate the form with data from the request
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            # delete marked images
            article.images.filter(is_deleted=True).delete()
            # new image
            for f in request.FILES.getlist('new_images'):
                Image.objects.create(image=f, article=form.instance)
            return HttpResponseRedirect('/myuploads/')
    else:
        # Populate the form with data from the existing article
        form = ArticleForm(instance=article)
    return render(request, 'editworks.html', {'form': form})

def deleteimage(request, image_id):
    image = get_object_or_404(Image, pk=image_id)
    image.is_deleted = True
    image.save()
    return HttpResponseRedirect(reverse('editworks', args=[image.article.id]))

@login_required
def editprofile(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('homepage/')
    else:
        form = UserSignUpForm(instance=request.user.userprofile)
    return render(request, 'editprofile.html', {'form': form})

@login_required
def accountUpdate(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('homepage/')
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'accountUpdate.html', {'form': form})

# 漫画文章列表 /graphics/
def graphics_list(request):
    articles_list = Article.objects.filter(type='G')
    paginator = Paginator(articles_list, 5)  # Show 5 articles per page
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    print("###########")
    return render(request, 'graphics.html', {'articles': articles})

def ff(request):
    articles_list = Article.objects.filter(type='F')
    paginator = Paginator(articles_list, 5)  # Show 5 articles per page
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    print("###########")
    return render(request, 'fiction.html', {'articles': articles})

# 小说文章列表 /fiction/
def fiction_list(request):
    print("###########")
    articles_list = Article.objects.filter(type='F')
    paginator = Paginator(articles_list, 5)  # Show 5 articles per page
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    return render(request, 'fiction.html', {'articles': articles})

# 显示用户的收藏 /myfavourites/
def favorites(request):
    usernow = request.user
    userprofile = UserProfile.objects.get(user=usernow)
    article_list  = userprofile.favourite_article.all()
    paginator = Paginator(article_list, 5)  # 创建一个分页对象，每页10篇文章

    page = request.GET.get('page')
    favorite_articles = paginator.get_page(page)  # 获取请求的页码的文章

    return render(request, 'myfavourites.html', {'favorite_articles': favorite_articles})

# 收藏动词
@login_required
def toggle_favorite(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    usernow = request.user
    userprofile = UserProfile.objects.get(user=usernow)
    if userprofile in article.favorited_by.all():
        # 取消收藏
        userprofile.favourite_article.remove(article)
        is_favorited = False
    else:
        # 添加收藏
        userprofile.favourite_article.add(article)
        is_favorited = True
    return JsonResponse({'is_favorited': is_favorited})

# 点赞动词
@login_required
def toggle_like(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    usernow = request.user
    userprofile = UserProfile.objects.get(user=usernow)
    if userprofile in article.liked_by.all():
        # 取消点赞
        userprofile.like_article.remove(article)
        is_liked = False
    else:
        # 添加点赞
        userprofile.like_article.add(article)
        is_liked = True
    return JsonResponse({'is_favorited': is_liked})

# 点踩动词
@login_required
def toggle_dislike(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    usernow = request.user
    userprofile = UserProfile.objects.get(user=usernow)
    if userprofile in article.disliked_by.all():
        # 取消点踩
        userprofile.dislike_article.remove(article)
        is_disliked = False
    else:
        # 添加点踩
        userprofile.dislike_article.add(article)
        is_disliked = True
    return JsonResponse({'is_disliked': is_disliked})

# 举报动词
@login_required
def toggle_report(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    usernow = request.user
    userprofile = UserProfile.objects.get(user=usernow)
    if userprofile in article.reported_by.all():
        # 取消点踩
        userprofile.report_article.remove(article)
        is_reported = False
    else:
        # 添加点踩
        userprofile.report_article.add(article)
        is_reported = True
    return JsonResponse({'is_reported': is_reported})

@login_required
def mymessages(request):
    notification_list = Notification.objects.filter(user=request.user).order_by('-timestamp')
    paginator = Paginator(notification_list, 5)
    page = request.GET.get('page')
    notifications = paginator.get_page(page)  # 获取请求的页码的文章
    return render(request, 'mymessages.html', {'notifications': notifications})

def edu(request):
    return render(request, 'education.html')

# need chapters
def fiction_list(request):
    return render(request, 'fiction.html')

def commercial(request):
    return render(request, 'commercial.html')



#### staffsan
def staff_main(request):
    return render(request, 'staff_main.html')

@login_required
def blacklist(request):
    return render(request, 'blacklist.html')