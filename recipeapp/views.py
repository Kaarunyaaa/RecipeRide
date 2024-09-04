from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser, addrecipe, Comment, Notification

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
            return redirect('/view')
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
def view(request):
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
    
    comments = recipe.comments.all()
    context = {
        'img':recipe.img,
        'ingredients': recipe.ingredients,
        'procedure': recipe.procedure,
        'recipe': recipe,
        'comments': comments
    }
    return render(request, 'recipe.html', context)

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
