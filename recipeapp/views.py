from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser
from .models import addrecipe
from django.contrib.auth import logout

# Create your views here.
def home(request):
    return render(request,'home.html')

def logout_view(request):
    logout(request)
    return redirect('/')

def login1(request):
    if request.method == 'POST':
        username = request.POST.get('uname') #kaaru
        password1 = request.POST.get('pwd') #123
        user = authenticate(username=username, password=password1)
        if user is not None:
            login(request, user)
            return redirect('/view')
        else:
            messages.error(request, 'Invalid login credentials')
    return render(request,'login.html')

def signup1(request):
    if request.method == 'POST':
        uname1 = request.POST.get('uname')
        pwd1=request.POST.get('pwd')
        repwd1=request.POST.get('repwd')
        
        
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
    return render(request,'signup.html')

@login_required
def view(request):
    a=addrecipe.objects.all()
    return render(request,'view.html',{'data':a})
    

def adddish(request):
    if request.method=='POST': 
        dish_name=request.POST.get('dname')
        dish_img=request.FILES.get('dimg')
        dish_ingre=request.POST.get('dingre')
        dish_proc=request.POST.get('dproc')
        addrecipe.objects.create(user=request.user,name=dish_name,img=dish_img,ingredients=dish_ingre,procedure=dish_proc)
    a=addrecipe.objects.filter(user=request.user)
    return render(request,"add.html",{'data':a})


def recipe(request, recipe_id):
    recipe = get_object_or_404(addrecipe, id=recipe_id)
    context = {
        'img':recipe.img,
        'ingredients': recipe.ingredients,
        'procedure': recipe.procedure
    }
    return render(request, 'recipe.html', context)

def edit(request, edit_id):
    a = get_object_or_404(addrecipe, id=edit_id)  # Fetch the object with proper error handling
    
    if request.method == 'POST':
        a.name = request.POST.get('dname', '').strip()
        a.ingredients = request.POST.get('dingre', '').strip()
        a.procedure = request.POST.get('dproc', '').strip()
        
        # Handle image upload if provided
        if 'dimg' in request.FILES:
            if a.img:  # Delete the existing image if it exists
                a.img.delete(save=False)
            a.img = request.FILES['dimg']  # Assign the new image
        
        a.save()
        return redirect('/add')
    
    return render(request, 'edit.html', {'data': a})

def delete(request,delete_id):
    del_obj=addrecipe.objects.get(id=delete_id)
    print(del_obj.img)
    #line 60 and 61 is meant to delete the locn of the respective img or docs file. This will also delete the image from the original path
    del_obj.img.delete()    #'img' given here is from model
    
    #line 64 is meant to delete the entire data
    del_obj.delete()
    
    return redirect('/add')