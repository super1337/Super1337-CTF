from django.shortcuts import render

from .models import SimpleQuestion, MultipleChoiceQuestion


def index(request):
    return render(request,'jeopardyctf/index.html',{})

def upload(request):
    return render(request,'jeopardyctf/upload.html',{})
