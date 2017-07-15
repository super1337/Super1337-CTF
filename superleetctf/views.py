from django.shortcuts import render


def index(request):
    return render(request, 'superleetctf/index.html')


def timer(request):
    return render(request, 'superleetctf/timer.html')
