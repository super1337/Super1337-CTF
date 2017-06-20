from django.shortcuts import render



def index(request):
    return render(request,'jeopardyctf/index.html',{})

def upload(request):
    return render(request,'jeopardyctf/upload.html',{})
