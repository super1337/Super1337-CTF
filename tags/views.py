from django.shortcuts import render

from .models import Tag


def tags(request):
    tags = Tag.objects.all()
    return render(request, 'tags/tags.html', {'tags': tags})
