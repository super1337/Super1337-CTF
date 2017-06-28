from django.shortcuts import render

def challenge(request):
    return render(request,'mega_challenge/challenge.html',{})
