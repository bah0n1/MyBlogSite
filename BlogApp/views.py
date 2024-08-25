from django.shortcuts import render
import re
import random
from django.shortcuts import redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from .models import UserAgentIP,Post,Tag,Categories,Author,UserOtp
from django.core import serializers
from .forms import PostForm,AuthorForm,LoginForm,RegisterForm,UserOtpForm
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from BlogProject.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

def indexs(request):

    return render(request,"pagedetails.html")



def index(request):
    posts=Post.objects.all()
    popularpost_view=posts[0].viewed
    popularpost=posts[0]
    for post in posts:
        if popularpost_view<=post.viewed:
            popularpost=post
    recent_posts = Post.objects.order_by('-last_updated')
    trending_post=[]
    for post in recent_posts[4:]:
        if post.titel ==popularpost.titel:
            pass
        else:
            trending_post.append(post)
    temp=trending_post[0]
    for i in range(len(trending_post)):
        for j in range(i+1,len(trending_post)):
            if trending_post[i].viewed<=trending_post[j].viewed:
                temp=trending_post[i]
                trending_post[i]=trending_post[j]
                trending_post[j]=temp
    #editor choice 
    number=random.randint(0,len(posts)-1)
    editor_Choice_post=posts[number]
    authors=Author.objects.all()[:3]
    categories=Categories.objects.all()
    tags=Tag.objects.all()
    # print(popularpost)
    return render(request,"index.html",{'recent_posts':recent_posts[:4],'authors':authors,"tags":tags,"categories":categories,"popularpost":popularpost,"trending_post":trending_post[0:3],'editor_Choice_post':editor_Choice_post})
    
    # movie=request.COOKIES.get("movie")
    # cc=f"{request.META['HTTP_USER_AGENT']} and other one is \n {request.user_agent.browser}"
    # cookie=request.COOKIES.get("movie")
    # print(cookie)
    # if "google" in request.META['HTTP_USER_AGENT'].lower() or request.user_agent.is_bot or not(cookie):
    #     return render(request,"index.html",{'bot':True})
    # else:
    #     return render(request,"index.html")

def postByCategorie(request,categorie):
    print(categorie)
    posts = Post.objects.filter(categories__name=categorie)
    categories=Categories.objects.all()
    tags=Tag.objects.all()
    authors=[]
    for post in posts:
        if post.author not in authors:
            authors.append(post.author)
    print(len(authors))
    print(posts)
    recent_posts = Post.objects.order_by('-last_updated')[:3]
    return render(request, "search-result.html", {"posts": posts,"recent_posts":recent_posts,"authors":authors,"tags":tags,"categories":categories,"categorie":categorie})
    # except:
    #     return render(request, "404.html")

def movie(request):
    response=HttpResponse("cookie set successful")
    response.set_cookie("movie",True)
    return response


def aboutus(request):
    return render(request,"about-us.html")

def contactus(request):
    return render(request,"contact-us.html")

def authors(request):
    authors=Author.objects.all()
    print(authors)
    return render(request,"authors.html",{"authors":authors})

def authorsdetails(request,authorsdetails):
    try:
        categorie=[]
        author=Author.objects.get(url=authorsdetails)
        post=Post.objects.filter(author=author)
        count=post.count()
        for pt in post:
            print(pt.categories)
            if pt.categories not in categorie:
                categorie.append(pt.categories)
        return render(request,"author-details.html",{"author":author,"posts":post,'categorie':categorie,'count':count})
    except:
        return render(request, "404.html")



def authorsdetails_catagories(request,authorsdetails,catagories):
    categorie=[]
    author=Author.objects.get(name=authorsdetails)
    post=Post.objects.filter(author=author,categories__name=catagories)
    posts=Post.objects.filter(author=author)
    count=posts.count()
    for pt in posts:
        
        if str(pt.categories) not in categorie:
            categorie.append(str(pt.categories))
    catis=str(catagories)
    # print(type(catis),type(cat))
    for cat in categorie:
        if cat == catis:
            print("true")
            print(type(catis),type(str(cat)))
        else:

            print("false",cat,catis)
            print(type(catis),type(cat))
        
    return render(request,"author-details.html",{"author":author,"posts":post,'categorie':categorie,"catis": str(catis),'count':count})
    try:
        author=Author.objects.get(name=authorsdetails)
        post=Post.objects.filter(author=author)
        return render(request,"author-details.html",{"author":author,"post":posts})
    except:
        return render(request, "404.html")






def privacypolicy(request):
    return render(request,"privacy-policy.html")

def postdetails(request,tag,posturl):
    #debug
    # post = Post.objects.get(url=posturl)
    # print(posturl)
    # return render(request, "post-details.html", {"post": post})
    # post = Post.objects.get(url=posturl,tags__name=tag)
    # update_time=post.last_updated
    # post.viewed+=1
    # post.save()
    # print("i here")
    # relativeposts=Post.objects.filter(categories=post.categories).order_by('-viewed')
    # print("i here")
    # return render(request, "post-details.html", {"post": post,"relativeposts":relativeposts})
    try:
        post = Post.objects.get(url=posturl,tags__name=tag)
        post.increment_view_count()
        relativeposts=Post.objects.filter(categories=post.categories).order_by('-viewed')[:3]
        return render(request, "post-details.html", {"post": post,"relativeposts":relativeposts})
    except:
        return render(request, "404.html")

def tagResult(request, tag):
    tags=Tag.objects.all()
    posts = Post.objects.filter(tags__name=tag)
    recent_posts = Post.objects.order_by('-last_updated')[:3]
    categories=Categories.objects.all()
    authors=[]
    for post in posts:
        if post.author not in authors:
            authors.append(post.author)
    
    return render(request, "search-result.html",{"tag":tag,"posts":posts,"tags":tags,"recent_posts":recent_posts,"categories":categories,"authors":authors})

def search(request):
    if request.method == "POST":
        tags = Tag.objects.all()
        src_req = request.POST["search"]
        recent_posts = Post.objects.order_by('-last_updated')[:3]
        categories = Categories.objects.all()
        posts = []
        authors = []
        try:
            posts = Post.objects.filter(titel__icontains=src_req)
            # posts_all = Post.objects.all()
            # posts=[]
            # for post in posts_all:
            #     if  src_req.upper() in post.titel.upper():
            #         posts.append(post)

            for post in posts:
                if post.author not in authors:
                    authors.append(post.author)
        except Post.DoesNotExist:
            posts = []
        return render(request, "search-result.html", {
            "src_req": src_req,
            "posts": posts,
            "tags": tags,
            "recent_posts": recent_posts,
            "categories": categories,
            "authors": authors
        })
    else:
        # src_req = request.POST["search"]
        tags = Tag.objects.all()
        recent_posts = Post.objects.order_by('-last_updated')[:3]
        categories = Categories.objects.all()
        return render(request, "search-result.html", {
            "src_req": src_req,
            "tags": tags,
            "recent_posts": recent_posts,
            "categories": categories
        })

def autocomplete(request):
    if 'term' in request.GET:
        qs = Post.objects.filter(titel__istartswith=request.GET['term'])
        titel = []
        for tl in qs:
            titel.append(tl.titel)
         
    return JsonResponse(titel,safe=False)

def loadmore(request):
    if request.method == "POST":
        try:
            total_post = Post.objects.all().count()
            if 'recent_posts' in request.POST:
                offset = int(request.POST.get('offset', 0))
                limit = 4  # Adjust as needed
                posts = Post.objects.order_by('-last_updated')[offset:offset+limit]
                html = render_to_string('article.html', {'posts': posts})

                return JsonResponse({
                    'html': html,
                    'total_post': total_post,
                })
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)



def post_create(request):
    if request.user.is_authenticated and user_can_publish(request.user):
        cato=Categories.objects.all()
        tago=Tag.objects.all()
        if request.method == 'POST':
            print(request.POST)
            form = PostForm(request.POST, request.FILES)
            data=request.POST
            print(data['url'])
            if form.is_valid() and customeValidationForm(url=data['url'],titel=data['titel'],meta_description=data['meta_description'],tag=request.POST.getlist('tags'),catagoris=request.POST.getlist('categories')):
                try:
                    cat=Categories.objects.get(pk=int(data["categories"]))
                    aut=Author.objects.get(user=request.user)
                    post=Post(url=data['url'],titel=data['titel'],meta_description=data['meta_description'],categories=cat,image=request.FILES.get('image'),author=aut,viewed=0,description=data['description'])#here i am
                    post.save()
                    post.tags.set(Tag.objects.filter(pk__in=request.POST.getlist('tags')))
                    print("i am here4")
                    return HttpResponseRedirect("/")
                except:
                    is_url=False
                    try:
                        is_url=Post.objects.get(url=data['url'])
                    except:
                        signal="Some problem Guru Refresh your page!"
                    if is_url:
                        signal="The URL is already in use."
                    fm=request.POST
                    messages.warning(request,signal)
                    return render(request, 'post_form.html', {'form': form,'fm':fm,'cato':cato,'tago':tago,'selected_tags': request.POST.getlist('tags')})
            else:
                fm=request.POST  
                return render(request, 'post_form.html', {'form': form,'fm':fm,'cato':cato,'tago':tago,'selected_tags': request.POST.getlist('tags')})
        else:
            form = PostForm()
            cato=Categories.objects.all()
            tago=Tag.objects.all()
        return render(request, 'post_form.html', {'form': form,'cato':cato,'tago':tago})
    else:
        return HttpResponseRedirect("/")


def customeValidationForm(url,titel=None,meta_description=None,tag=None,catagoris=None,image=None):
    # url validation
    if url is not None and len(url)<=30:
        print("iam here2")
        url_pattern = re.compile(r'^[a-zA-Z0-9-_]+$')
        if url_pattern.match(url):
            print("iam here3")
            print(url)
            url= True
    else:
        url= False
    # titel validation
    if titel is not  None and (len(titel)<=60 and len(titel)>=10):
        titel=True
    else:
        titel=False
    # meta_description validation 
    if meta_description is not  None and (len(meta_description)<=160 and len(meta_description)>=120):
        meta_description=True
    else:
        meta_description=False
    
    # tags validation
    print(tag)
    if len(tag)>0 and len(tag)<=4:
        try:
            for tg in tag:
                t=Tag.objects.get(pk=int(tg))
            tag=True
        except:
            tag=False
    else:
        tag=False
    # catagoris validation
    print(catagoris)
    print(len(catagoris))
    if len(catagoris)==1:
        try:
            for cat in catagoris:
                ct=Categories.objects.get(pk=int(cat))
            catagoris=True
        except:
            catagoris=False
    else:
        catagoris=False

    
    if url and titel and meta_description and tag and catagoris:
        return True
    else:
        return False
             
# request for makeauthor    

def makeAuthor(request):
    if request.user.is_authenticated and not check_user_have_author_account(request.user):
        print(check_user_have_author_account(request.user))
        if request.method =="POST":
            form=AuthorForm(request.POST, request.FILES)
            if form.is_valid():
                author = form.save(commit=False)
                author.user = request.user  # Set the user if you have a user field in your Author model
                name=author.name
                name_url=name.replace(" ", "-")
                try:
                    auth=Author.objects.get(url=name_url)
                    author.url=name_url+str(request.user.id)
                except:
                    author.url=name_url
                
                author.can_publish = False  # Set the can_publish field if applicable
                author.save()
                return render(request,'author-make.html',{"form":form})
            else:
                form=AuthorForm(request.POST)
                return render(request,'author-make.html',{"form":form})
        form=AuthorForm()
        return render(request,'author-make.html',{"form":form})
    else:
        if request.user.is_authenticated:
            messages.warning(request,"You already have an account!!")
            return redirect('authorsdetails',Author.objects.get(user=request.user).url)
        else:
            return redirect('/')

def login_as_user(request):
    if not request.user.is_authenticated:
        if request.method =="POST":
            form=LoginForm(request.POST)
            if form.is_valid():
                user_email=form.cleaned_data['email']
                user_password=form.cleaned_data['password']
                try:
                    user_mail=User.objects.get(email=user_email)
                    print('i am here')
                    print(user_mail)
                    user=authenticate(username=user_mail.username,password=user_password)
                    print(user)
                    if user:
                        login(request,user)
                        return redirect('/')
                    else:
                        if user_mail.is_active == False:
                            send_user_otp(user_mail.email)
                            return redirect('userotp',user_mail.email)
                        messages.warning(request,'The email and password are incorrect! If you forget your password, you can ')
                        return redirect('login')
                except:
                    messages.warning(request,'The email and password are incorrect! If you forget your password, you can ')
                    return redirect('login')
            else:
                form=LoginForm(request.POST)
                return render(request,'login.html',{'form':form})

        else:
            form=LoginForm()
            return render(request,'login.html',{'form':form})
    else:
        return redirect('logout')


def register_as_user(request):
    if request.method =="POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            form.save()
            send_user_otp(email=email)
            return redirect('userotp',email=email)
    form=RegisterForm()
    return render(request,'register.html',{'form':form})


def user_otp_verify(request, email):
    user = User.objects.get(email=email)  # Retrieve the user object at the start
    if request.method == "POST":
        form = UserOtpForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            if send_user_otp(email=email, otp=otp):
                login(request, user)
                return redirect('/')  # Redirect to home page after successful login
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
        else:
            messages.error(request, 'Please enter a valid OTP.')

    # If it's a GET request or the OTP was incorrect, re-render the form
    form = UserOtpForm()
    return render(request, 'userotp.html', {'form': form,'email':email})

def logout_as_user(request):
    logout(request)
    return redirect("login")


# check user can publush or not
def user_can_publish(user):
    if not user.is_authenticated:
        return False
    try:
        author = Author.objects.get(user=user)
        return author.can_publish
    except Author.DoesNotExist:
        return False

#check user have author accoount
def check_user_have_author_account(user):
    try:
        author = Author.objects.get(user=user)
        print(author)
        return True
    except Author.DoesNotExist:
        return False

def send_user_otp(email,otp=None):
    if otp:
       print("iam here")
       userotp=UserOtp.objects.filter(user=User.objects.get(email=email)).last().otp
       print(otp)
       print(userotp)

       if int(otp) == int(userotp):
            user=User.objects.get(email=email)
            user.is_active=True
            user.save()
            return True
       else:
            return False

        
    otp=random.randint(100000, 999999)
    user=User.objects.get(email=email).first_name
    mess = f"Hello {user.capitalize()},\nYour OTP is {otp}\nThanks!"
    userotp=UserOtp(otp=otp,user=User.objects.get(email=email))
    userotp.save()
    send_mail(
                "Welcome to GuruiKnow - Verify Your Email",
                        mess,
                        EMAIL_HOST_USER,
                        [email],
                        fail_silently = False
                        )
    #email send
    # email=email
    # send otp in email.

   