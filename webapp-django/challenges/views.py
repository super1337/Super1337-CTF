from django.http import HttpResponse
from django.shortcuts import render

from .forms import FlagForm
from .models import Challenge


def download(req):
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=myfile.zip'
    return response


def textBased(request):
    challenges = Challenge.objects.all()
    return render(request, 'challenges/textBased.html', {'challenges': challenges})


def index(request):
    challenges = Challenge.objects.all()
    return render(request, 'challenges/index.html', {'challenges': challenges})


def challenge(request, name):
    chal = Challenge.objects.get(name=name)

    if request.method == 'POST':
        form = FlagForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['flag'] == chal.name:
                request.user.userprofile.solved_challenges = chal
    else:
        form = FlagForm()

    return render(request, 'challenges/challenge.html', {'challenge': chal, 'form': form})

    '''
    path=settings.MEDIA_ROOT
    file_list =os.listdir(path)
    return render(request,'challenges/index.html', {'files': file_list})
    



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
'''
