from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile,User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request,'student/home.html')

def dashboard(request):
    return render(request,'student/dashboard.html')

def addachievement(request):
    return render(request,'student/addachievement.html')

def profile(request):
    return render(request,'student/profile.html')

def loginuser(request):
    if request.method=='GET':
        return render(request,'student/home.html')
    else:
        a=request.POST.get('username')
        b=request.POST.get('password')
        user=authenticate(request,username=a,password=b)
        if user is None:
            messages.error(request, 'Invalid username or password!')
            return redirect('home') 
        else:
            login(request,user)
            messages.success(request, f'Welcome {a}!')
            return (redirect('home'))
        
def signupuser(request):
    if request.method=='GET':
        return render(request,'student/home.html')
    else:
        a=request.POST.get('username')
        b=request.POST.get('password1')
        c=request.POST.get('password2')
        if(b==c):
            if(User.objects.filter(username=a).exists()):
                messages.error(request, 'User Already Exist!')
                return redirect('home') 
            else:
                user=User.objects.create_user(username=a,password=b)
                user.save()
                UserProfile.objects.create(user=user)
                login(request,user)
                messages.success(request, 'Signup Successful!')
                return (redirect('home'))
        else:
            messages.error(request, 'Password Mismatched!')
            return redirect('home') 
        

def logoutuser(request):
    if request.method=='GET':
        logout(request)
        return(redirect('home'))
    
@login_required
def profile(request):
    return render(request, 'student/profile.html')

@login_required
def edit_profile(request):
    profile = request.user.userprofile
    if request.method == "POST":
        # Update only if a value is provided
        bio = request.POST.get('bio', '').strip()
        location = request.POST.get('location', '').strip()
        linkedin = request.POST.get('linkedin_url', '').strip()
        github = request.POST.get('github_url', '').strip()
        website = request.POST.get('personal_website', '').strip()

        if bio != "":
            profile.bio = bio
        if location != "":
            profile.location = location
        if linkedin != "":
            profile.linkedin_url = linkedin
        if github != "":
            profile.github_url = github
        if website != "":
            profile.personal_website = website

        if 'profile_image' in request.FILES:
            profile.profile_image = request.FILES['profile_image']

        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')

    return render(request, 'student/editprofile.html', {'profile': profile})

