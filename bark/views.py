from django.shortcuts import render

def index(request):
    return render(request,'index.html')
def sidebar(request):
    return render(request,'sidebar.css')
