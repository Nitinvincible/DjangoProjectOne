from django.template.loader import get_template
from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    data = {
        "Title": "Nitin Home Page",
        "Welcome_Message": "Welcome to Nitin's Django Application",
        "clist": ["Python", "Django", "JavaScript", "HTML", "CSS"],
        "studentDetails": [
            {"id": 1, "name": "Alice", "age": 22, "city": "Los Angeles"},
            {"id": 2, "name": "Bob", "age": 24, "city": "Chicago"},
            {"id": 3, "name": "Nitin", "age": 25, "city": "New York"}
        ],
        "numbers": [multiple * 10 for multiple in range(1, 11)]
    }
    return render(request, "index.html", data)
    #try:
        #template = get_template("index.html")
        #return HttpResponse(template.render({}, request))
    #except Exception as e:
    #    return HttpResponse(f"Template error: {e}")

def aboutUs(request):
    return HttpResponse("Welcome to Nitins About Us Page")

def blogs(request):
    return HttpResponse("Welcome to Nitins Blogs Page")

def courses(request):
    return HttpResponse("Welcome to Nitins Courses Page")

def course_detail(request, courseId):
    return HttpResponse(f"Details of Course ID: {courseId}")