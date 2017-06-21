from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

from .models import Challenge


# from .forms import DocumentForm


def index(request):
    challenges = Challenge.objects.all()
    return render(request, 'challenges/index.html', {'challenges': challenges})

    '''
    path=settings.MEDIA_ROOT
    file_list =os.listdir(path)
    return render(request,'challenges/index.html', {'files': file_list})
    '''


def upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'challenges/upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'challenges/upload.html')

def upload2(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/jeopardy')
    else:
        form = DocumentForm()
    return render(request, 'challenges/upload2.html', {
        'form': form
    })
