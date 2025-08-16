from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile,User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
import datetime

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
        return render(request,'student/loginuser.html')
    else:
        a=request.POST.get('username')
        b=request.POST.get('password')
        user=authenticate(request,username=a,password=b)
        if user is None:
            return render(request,'student/loginuser.html',{'error':'Invalid Credentials!'})
        else:
            login(request,user)
            return (redirect('home'))


def signupuser(request):
    if request.method=='GET':
        return render(request,'student/signupuser.html')
    else:
        a=request.POST.get('username')
        b=request.POST.get('password1')
        c=request.POST.get('password2')
        dob = request.POST.get('date_of_birth')
        e = request.POST.get('location')
        f = request.POST.get('bio')
        date_obj = datetime.datetime.strptime(dob, "%Y-%m-%d").date() if dob else None
        if(b==c):
            if(User.objects.filter(username=a).exists()):
                return render(request,'student/signupuser.html',{'error':'User Already Exists!'})
            else:
                user=User.objects.create_user(username=a,password=b)
                user.save()
                UserProfile.objects.create(user=user, location=e,bio=f, date_of_birth=date_obj)
                login(request,user)
                return (redirect('home'))
        else:
            return render(request,'student/signupuser.html',{'error':'Password Mismatched!'})

def logoutuser(request):
    if request.method=='GET':
        logout(request)
        return(redirect('home'))
    
@login_required
def my_profile(request):
    profile = request.user.userprofile
    return render(request, 'student/profile.html', {'profile_user': request.user, 'profile': profile})

@login_required
def profile_view(request, username=None):
    if username:
        user_obj = get_object_or_404(User, username=username)
    else:
        user_obj = request.user  

    profile = user_obj.userprofile  

    # Render the SAME template, it handles private vs public
    context = {
        'profile_user': user_obj,
        'profile': profile
    }
    return render(request, 'student/profile.html', context)

@login_required
def edit_profile(request):
    profile = request.user.userprofile
    if request.method == "POST":
        # Fetch values
        bio = request.POST.get('bio', '').strip()
        location = request.POST.get('location', '').strip()
        dob = request.POST.get('date_of_birth', '').strip()
        linkedin = request.POST.get('linkedin_url', '').strip()
        github = request.POST.get('github_url', '').strip()
        website = request.POST.get('personal_website', '').strip()
        profile.is_public = request.POST.get('is_public') == 'True'
        # Update only if a value is provided
        if bio:
            profile.bio = bio
        if location:
            profile.location = location
        if dob:  # Validate empty string
            profile.date_of_birth = dob
        if linkedin:
            profile.linkedin_url = linkedin
        if github:
            profile.github_url = github
        if website:
            profile.personal_website = website

        # Profile image
        if 'profile_image' in request.FILES:
            profile.profile_image = request.FILES['profile_image']

        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')

    return render(request, 'student/editprofile.html', {'profile': profile})


