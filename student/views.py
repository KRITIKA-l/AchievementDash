from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile,User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile,Opportunity,OpportunityApplication,Skill
import datetime
from django.db.models import Q
from django.utils import timezone

# Create your views here.

def home(request):
    return render(request,'student/home.html')

@login_required
def dashboard(request):
    user_profile = request.user.userprofile
    applications = request.user.applications.all() 

    context = {
        'profile': user_profile,
        'applications': applications,
    }
    return render(request, 'student/dashboard.html', context)

@login_required
def addachievement(request):
    skills = Skill.objects.all()  

    if request.method == "POST":
        skill_id = request.POST.get('skill_id')
        other_skill_name = request.POST.get('other_skill', '').strip()

        if skill_id == "other" and other_skill_name:
            skill, created = Skill.objects.get_or_create(name=other_skill_name)
            request.user.userprofile.skills.add(skill)
            messages.success(request, f"New skill '{skill.name}' added successfully!")
        elif skill_id:
            skill = Skill.objects.get(id=skill_id)
            request.user.userprofile.skills.add(skill)
            messages.success(request, f"Skill '{skill.name}' added successfully!")
        else:
            messages.error(request, "Please select a skill or enter a new one.")

        return render(request, 'student/addachievement.html', {'skills': skills})
    return render(request, 'student/addachievement.html', {'skills': skills})

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
    user_obj = request.user
    profile = user_obj.userprofile
    is_owner = True 

    context = {
        'profile_user': user_obj,
        'profile': profile,
        'is_owner': is_owner,
    }
    return render(request, 'student/profile.html', context)

@login_required
def profile_view(request, username=None):
    if username:
        user_obj = get_object_or_404(User, username=username)
    else:
        user_obj = request.user  

    profile = user_obj.userprofile  
    is_owner = (request.user == user_obj)
    
    context = {
        'profile_user': user_obj,
        'profile': profile,
        'is_owner': is_owner,
    }
    return render(request, 'student/profile.html', context)

@login_required
def edit_profile(request):
    profile = request.user.userprofile
    if request.method == "POST":
        bio = request.POST.get('bio', '').strip()
        location = request.POST.get('location', '').strip()
        dob = request.POST.get('date_of_birth', '').strip()
        linkedin = request.POST.get('linkedin_url', '').strip()
        github = request.POST.get('github_url', '').strip()
        website = request.POST.get('personal_website', '').strip()
        profile.is_public = request.POST.get('is_public') == 'True'

        if bio:
            profile.bio = bio
        if location:
            profile.location = location
        if dob:  
            profile.date_of_birth = dob
        if linkedin:
            profile.linkedin_url = linkedin
        if github:
            profile.github_url = github
        if website:
            profile.personal_website = website

        if 'profile_image' in request.FILES:
            profile.profile_image = request.FILES['profile_image']

        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('my_profile')

    return render(request, 'student/editprofile.html', {'profile': profile})


@login_required
def opportunity_list(request):
    today = timezone.now().date()
    opportunities = Opportunity.objects.all()

    ongoing = opportunities.filter(start_date__lte=today, end_date__gte=today)
    upcoming = opportunities.filter(start_date__gt=today)
    closed = opportunities.filter(end_date__lt=today)

    return render(request, 'student/opplist.html', {
        'ongoing': ongoing,
        'upcoming': upcoming,
        'closed': closed,
    })

def opportunity_detail(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)

    already_applied = False
    if request.user.is_authenticated:
        already_applied = OpportunityApplication.objects.filter(
            opportunity=opportunity,
            student=request.user
        ).exists()

    return render(request, 'student/oppdetail.html', {
        'opportunity': opportunity,
        'already_applied': already_applied
    })

@login_required
def apply_for_opportunity(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)

    existing_application = OpportunityApplication.objects.filter(opportunity=opportunity, student=request.user).first()
    if existing_application:
        return redirect('opportunity_detail', pk=pk)

    if request.method == "POST":
        resume = request.FILES.get('resume')
        cover_letter = request.POST.get('cover_letter')

        OpportunityApplication.objects.create(
            opportunity=opportunity,
            student=request.user,
            resume=resume,
            cover_letter=cover_letter,
        )
        return redirect('opportunity_detail', pk=pk)

    return render(request, 'student/applyform.html', {'opportunity': opportunity})

@login_required
def search(request):
    query = request.POST.get('prod_search', '').strip()
    profiles = []
    opportunities = []

    if query:
        profiles = UserProfile.objects.filter(
            Q(user__username__icontains=query) |
            Q(location__icontains=query) |
            Q(skills__name__icontains=query)
        ).distinct()

        opportunities = Opportunity.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query) |
            Q(skills_required__name__icontains=query)
        ).distinct()

    context = {
        'query': query,
        'profiles': profiles,
        'opportunities': opportunities,
    }
    return render(request, 'student/search_result.html', context)