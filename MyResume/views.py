from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def aboutme_view(request):
    
    return render(request, 'about.html')


def skills_view(request):

    skills = {
        'python':90,
        'sql':100,
        'Django':80,
        'Html':90,
        'React':20,
        'Css':50,
        'Js':50,
        'Jquery':100,
        'Bootstrap':60
    }
    context ={'skills':skills}
    return render(request, 'skills.html' , context)




def qualification(request):
    
    qualified = {
        "SSC":{"S.NO":1, "STUDY":"SCC","BOARD":"MUMBAI","MARKS":90},
        "HSC":{"S.NO":2, "STUDY":"HSC","BOARD":"MUMBAI","MARKS":80},
        "BSC-IT":{"S.NO":3, "STUDY":"SCC","BOARD":"MUMBAI","MARKS":8.7},
                
        }
    
    context = {"qualified":qualified}
    return render (request, 'qualification.html',context)


def project(request):
    proj = {
        "Project -1":"student management System",
        "Project -2":"bank management system Project",
        
    }
    context ={"proj": proj}
    return render(request, 'project.html', context)

def experience(request):
    exp = {
        "Python":"1 Year ",
        "MySql":"1 Year",
        "HTML":"1 Year",
        "CSS":"1 Year",
        "JAVA":"0 MONTH",
        "C#":"0 MONTH",
        "JavaScript":"1 Year",
        "JQuery":"1 Year"

    }
    context ={"exp":exp}
    return render( request, 'experience.html', context)


def contact(request):
    
    if request.method =="POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        p = request.POST.get('purpose')

        # print(name)
        # print(email)
        # print(p)
        context = {"name":name}
        return render(request, 'thanks.html', context)

    
    

    return render(request, 'contact.html' )