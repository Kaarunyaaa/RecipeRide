from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser, addrecipe, Comment, Notification,Follow,Saves,Rating
from .models import UserProfile
from django.contrib.auth.models import User
from .modules import recommend

import collections
from fuzzywuzzy import process

# Create your views here.
def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('/')

def login1(request):
    if request.method == 'POST':
        username = request.POST.get('uname') 
        password1 = request.POST.get('pwd') 
        user = authenticate(username=username, password=password1)
        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            messages.error(request, 'Invalid login credentials')
    return render(request, 'login.html')

def signup1(request):
    if request.method == 'POST':
        uname1 = request.POST.get('uname')
        pwd1 = request.POST.get('pwd')
        repwd1 = request.POST.get('repwd')
        
        if pwd1 != repwd1:
            messages.error(request, "Passwords do not match")
            return redirect('/signup')
        
        if CustomUser.objects.filter(username=uname1).exists():
            messages.error(request, 'Username is already taken')
            return redirect('/signup')
        
        if pwd1 and repwd1:
            user = CustomUser.objects.create_user(username=uname1, password=pwd1)
            user.save()
            messages.success(request, "Registration successful ")
            messages.success(request, "Login here ")
            return redirect('/login')
    return render(request, 'signup.html')

@login_required
def view(request,):
    a = addrecipe.objects.all()
    return render(request, 'view.html', {'data': a})

@login_required
def adddish(request):
    if request.method == 'POST': 
        dish_name = request.POST.get('dname')
        dish_img = request.FILES.get('dimg')
        dish_ingre = request.POST.get('dingre')
        dish_proc = request.POST.get('dproc')
        addrecipe.objects.create(user=request.user, name=dish_name, img=dish_img, ingredients=dish_ingre, procedure=dish_proc)
    a = addrecipe.objects.filter(user=request.user)
    return render(request, "add.html", {'data': a})

def recipe(request, recipe_id):
    recipe = get_object_or_404(addrecipe, id=recipe_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment = Comment.objects.create(recipe=recipe, user=request.user, content=content)
            Notification.objects.create(user=recipe.user, comment=comment)
            
    saveFlag=Saves.objects.filter(user=request.user,recipe=recipe).exists()
    
    user_rating=None
    if Rating.objects.filter(user=request.user,recipe=recipe).exists():
        user_rating=Rating.objects.get(user=request.user,recipe=recipe)
        
    avgRate=None
    if Rating.objects.filter(recipe=recipe).exists():
        rating=Rating.objects.filter(recipe=recipe)
        rate=0
        for i in rating:
            rate+=i.rating
        avgRate=round(rate/len(rating),2)
    
    comments = recipe.comments.all()
    num = [i * 0.5 for i in range(1,11)]
    context = {
        'img':recipe.img,
        'ingredients': recipe.ingredients,
        'procedure': recipe.procedure,
        'recipe': recipe,
        'comments': comments,
        'posted_by':recipe.user, 
        'saveFlag':saveFlag,
        'user_rating':user_rating,
        'defaultRange':num,
        'forIfCondition':[0.5, 1.5, 2.5, 3.5, 4.5],
        'avgRate':avgRate,
    }
    return render(request, 'recipe.html', context)


def user_recipe(request,id):
    print(id)
    user_data=CustomUser.objects.get(username=id)
    data=addrecipe.objects.filter(user=user_data.id)
    return render(request,'user_recipe.html',{'data':data,'data1':user_data})

@login_required
def edit(request, edit_id):
    a = get_object_or_404(addrecipe, id=edit_id)
    
    if request.method == 'POST':
        a.name = request.POST.get('dname', '').strip()
        a.ingredients = request.POST.get('dingre', '').strip()
        a.procedure = request.POST.get('dproc', '').strip()
        
        if 'dimg' in request.FILES:
            if a.img:
                a.img.delete(save=False)
            a.img = request.FILES['dimg']
        
        a.save()
        return redirect('/add')
    
    return render(request, 'edit.html', {'data': a})

@login_required
def delete(request, delete_id):
    del_obj = addrecipe.objects.get(id=delete_id)
    del_obj.img.delete()
    del_obj.delete()
    
    return redirect('/add')

@login_required
def notifications(request):
    # Fetch unread notifications for the logged-in user
    unread_notifications = Comment.objects.filter(user=request.user, read=False)
    # Mark notifications as read
    unread_notifications.update(read=True)

    context = {
        'notifications': unread_notifications
    }
    return render(request, 'notifications.html', context)

@login_required
def dashboard(request):
    # Check for notifications
    return redirect('notifications')

from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile
from django.contrib.auth.decorators import login_required

@login_required
def profile_edit_view(request,id):
    # Check if the user already has a profile
    recipe_of_user=CustomUser.objects.get(username=id)
    
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        # Get form data
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        description = request.POST.get('description')
        profile_pic = request.FILES.get('profile_pic')

        if profile:
            # If profile exists, update it
            profile.email = email
            profile.phone_number = phone_number
            profile.description = description
            if profile_pic:
                profile.profile_pic = profile_pic
            profile.save()
        else:
            # Create a new profile if it doesn't exist
            UserProfile.objects.create(
                user=request.user,
                email=email,
                phone_number=phone_number,
                description=description,
                profile_pic=profile_pic
            )

        #return redirect('profile_view')  # Redirect after saving

    context = {
        'profile': profile,
        
    }
    return render(request, 'profile_edit.html', context)

def profile_view(request,id):
    # Check if the user already has a profile
    user=User.objects.get(username=id)
    recipe=addrecipe.objects.filter(user=user)
    
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = None
    
    following=Follow.objects.filter(follower=request.user.id)
    following=list(following.values_list('followed',flat=True))

    context = {
        'profile': profile,
        'data':user,
        'dish':recipe,
        'following':following,
    }
    return render(request, 'profile.html', context)
@login_required
def follow_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user != request.user:
        following=Follow.objects.filter(follower=request.user.id)
        #print(following)
        #print(list(following.values_list('followed',flat=True)))
        #print(following.exists())
        if following.exists() and ( user_id in list(following.values_list('followed',flat=True))):
            #print("inside if")
            Follow.objects.filter(follower=request.user,followed=user).delete()   #kaaru   #harish
        else:
            Follow.objects.create(follower=request.user,followed=user)
    return redirect('profile_view',id=user)

def save(request,id):
    recipe=addrecipe.objects.get(id=id)
    if Saves.objects.filter(user=request.user,recipe=recipe).exists():
        Saves.objects.filter(user=request.user,recipe=recipe).delete()
        return redirect('/recipe/'+id+'/')
    else:
        Saves.objects.create(user=request.user,recipe=recipe)
        return redirect('/recipe/'+id+'/')
    
def view_saved(request):
    data=[]
    saved_data=Saves.objects.filter(user=request.user)
    print(saved_data)
    print(saved_data.exists())
    for x in saved_data:
        print(x)
        data.append(addrecipe.objects.get(id=x.recipe_id))
    return render(request,'view_saved.html',{'data':data})

def following(request):
    following_users = Follow.objects.filter(follower=request.user)
    followed_accounts = []
    for i in following_users:
        profilePic=None
        if UserProfile.objects.filter(user=i.followed).exists():
            profilePic=UserProfile.objects.get(user=i.followed).profile_pic
            
        t={
            'profilePic':profilePic,
            'userData':i.followed,
        }
        followed_accounts.append(t)
    context={
        'followed_accounts': followed_accounts,
    }
    return render(request, 'following.html',context)

@login_required
def rate(request,id,rate):
    recipe=addrecipe.objects.get(id=id)
    if Rating.objects.filter(user=request.user,recipe=recipe).exists():
        a=Rating.objects.get(user=request.user,recipe=recipe)
        if rate == '0':
            a.delete()
        else:
            a.rating=rate
            a.save()
    else:
        if rate!='0':
            Rating.objects.create(user=request.user,recipe=recipe,rating=rate)
    recommend.setZScoreParameters(request.user)
    return redirect(f'/recipe/{recipe.id}#stars')

def recommender(request):
    if not Rating.objects.filter(user=request.user).exists():
        return None
    allUserRatings=Rating.objects.filter(user=request.user)
    d=collections.defaultdict(int)
    u=set()
    for i in allUserRatings:
        othersRating = Rating.objects.filter(recipe = i.recipe)
        for j in othersRating:
            if j.user != request.user:
                if j.user not in u:
                    u.add(j.user)
                if abs(j.rating - i.rating) == 0.0:
                    d[j.user]+=5
                elif abs(j.rating - i.rating) == 0.5:
                    d[j.user]+=3.5
                elif abs(j.rating - i.rating) == 1.0:
                    d[j.user]+=2
                elif abs(j.rating - i.rating) == 1.5:
                    d[j.user]+=0.5
                elif abs(j.rating - i.rating) == 2.0:
                    d[j.user]+=0
                elif abs(j.rating - i.rating) == 2.5:
                    d[j.user]-=0.5
                elif abs(j.rating - i.rating) == 3.0:
                    d[j.user]-=2.0
                elif abs(j.rating - i.rating) == 3.5:
                    d[j.user]-=3.5
                elif abs(j.rating - i.rating) >= 4.0:
                    d[j.user]-=5.0
    l=[]
    for i in u:
        l.append({'u':i,'score':d[i],})
    recommend.recommendedPosts(request.user)
    return render(request,'temp.html',{'userScore':d, 'l':l,})

def recommendationPage(request):
    recommendedposts=recommend.recommendedPosts(request.user)
    popular=recommend.popular()
    topRated=recommend.topRated()
    allPost=addrecipe.objects.all()
    
    context={
        'recommendedPosts' : recommendedposts,
        'popular':popular,
        'topRated':topRated,
        'allPost':allPost[0:4],
    }
    return render(request,'recommendationPage.html',context)
    
def search_recipes(request):
    query = request.GET.get('query', '')
    if query:
        # Get all recipe names
        recipes = addrecipe.objects.all()
        recipe_names = [recipe.name for recipe in recipes]
        
        # Find best matches
        matches = process.extract(query, recipe_names, limit=5)
        print(matches)
        results=[]
        for name,score in matches:
            if score>60:
                try:
                    t=addrecipe.objects.get(name=name)
                    results.append(t)
                except:
                    for i in addrecipe.objects.filter(name=name):
                        results.append(i)
    else:
        results = []
    return render(request, 'search_results.html', {'results': results, 'query': query})
                
    








