from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'student/home.html')

def dashboard(request):
    return render(request,'student/dashboard.html')

def addachievement(request):
    return render(request,'student/addachievement.html')

def profile(request):
    return render(request,'student/profile.html')